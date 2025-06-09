import asyncio
import logging
from typing import Dict, Optional
import psutil
from datetime import datetime
from ..config.config_manager import ConfigManager

class VMService:
    def __init__(self):
        self.config = ConfigManager().config
        self.vm_name = self.config.vm.name
        self._state_translations = {
            'Running': 'Запущена',
            'Off': 'Выключена',
            'Starting': 'Запускается',
            'Stopping': 'Выключается',
            'Saved': 'Сохранена',
            'Paused': 'Приостановлена'
        }
        self._ensure_hyperv_module()

    def _ensure_hyperv_module(self):
        """Ensure Hyper-V module is available"""
        try:
            import subprocess
            result = subprocess.run(
                ["powershell", "-Command", "Import-Module Hyper-V"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            if result.returncode != 0:
                logging.error("Failed to import Hyper-V module. Make sure Hyper-V is installed and you have administrative privileges.")
                raise RuntimeError("Hyper-V module not available")
        except Exception as e:
            logging.error(f"Error checking Hyper-V module: {str(e)}")
            raise

    async def run_powershell(self, cmd: str) -> str:
        """Execute PowerShell command"""
        try:
            import subprocess
            result = subprocess.run(
                ["powershell", "-Command", f"Import-Module Hyper-V; {cmd}"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            if result.returncode != 0 and result.stderr:
                logging.error(f"PowerShell error: {result.stderr}")
                return result.stderr
            return result.stdout or result.stderr
        except Exception as e:
            logging.error(f"PowerShell execution error: {str(e)}")
            return str(e)

    def translate_state(self, state: str) -> str:
        """Translate VM state to Russian"""
        return self._state_translations.get(state, state)

    async def get_state(self) -> str:
        """Get current VM state"""
        ps_cmd = f"(Get-VM -Name '{self.vm_name}').State"
        result = (await self.run_powershell(ps_cmd)).strip()
        return self.translate_state(result)

    async def get_uptime(self) -> str:
        """Get VM uptime"""
        ps_cmd = f"Get-VM -Name '{self.vm_name}' | Select-Object Uptime | Format-Table -HideTableHeaders"
        uptime = await self.run_powershell(ps_cmd)
        return uptime.strip() if uptime and "Uptime" not in uptime else "Неизвестно"

    async def control(self, action: str) -> str:
        """Control VM state"""
        actions = {
            'start': f"Start-VM -Name '{self.vm_name}'",
            'stop': f"Stop-VM -Name '{self.vm_name}' -Force",
            'restart': f"Restart-VM -Name '{self.vm_name}' -Force"
        }
        if action not in actions:
            raise ValueError(f"Unsupported action: {action}")
        return await self.run_powershell(actions[action])

    async def get_system_stats(self) -> Dict[str, str]:
        """Get system statistics"""
        state = await self.get_state()
        uptime = await self.get_uptime()
        
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        memory_usage = f"{memory.percent}% ({memory.used // (1024*1024)} МБ из {memory.total // (1024*1024)} МБ)"
        
        return {
            "state": state,
            "uptime": uptime,
            "cpu_usage": f"{cpu_usage}%",
            "memory_usage": memory_usage,
            "current_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    async def get_logs(self, max_events: int = 10) -> Optional[str]:
        """Get VM event logs"""
        try:
            check_logs_cmd = (
                "Get-WinEvent -ListLog Microsoft-Windows-Hyper-V* -ErrorAction SilentlyContinue | "
                "Where-Object { $_.RecordCount -gt 0 } | Select-Object -ExpandProperty LogName"
            )
            available_logs = await self.run_powershell(check_logs_cmd)
            
            if not available_logs.strip():
                return "Логи Hyper-V недоступны или пусты"

            log_cmd = (
                f"Get-WinEvent -MaxEvents {max_events} "
                "-FilterHashtable @{LogName='System'; "
                "ProviderName='Microsoft-Windows-Hyper-V*'} "
                f"-ErrorAction SilentlyContinue | "
                f"Where-Object {{ $_.Message -like '*{self.vm_name}*' }} | "
                "Select-Object TimeCreated, LevelDisplayName, Message | "
                "Format-Table -Wrap"
            )
            logs = await self.run_powershell(log_cmd)
            
            if not logs.strip():
                return "Записи о событиях виртуальной машины не найдены"
                
            return logs
        except Exception as e:
            logging.error(f"Error getting logs: {str(e)}")
            return "Ошибка при получении логов: проверьте права доступа и наличие логов Hyper-V" 