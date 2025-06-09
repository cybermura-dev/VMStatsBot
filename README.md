# VMStatsBot

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies](#technologies)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Optimization](#optimization)
- [Contributing](#contributing)
- [License](#license)

## Overview

**VMStatsBot** is a Telegram bot for managing and monitoring Hyper-V virtual machines. The bot provides a convenient interface for controlling VM state, power management, and viewing system statistics through Telegram.

The application is built using a modular architecture to ensure high testability, maintainability, and scalability. It uses Windows PowerShell for Hyper-V interaction and python-telegram-bot for Telegram API integration.

### Target Audience
- System Administrators
- DevOps Engineers
- Hyper-V VM Managers

## Features

### Virtual Machine Management

- **State Monitoring**: View current VM state (running/stopped/etc.)
- **Power Management**: Start, stop, and restart VMs
- **Uptime Tracking**: Monitor VM uptime
- **System Statistics**: CPU and memory usage monitoring

### Notifications

- **State Changes**: Notifications when VM state changes
- **Critical Events**: Alerts for important system events
- **Resource Monitoring**: Notifications when resource usage exceeds thresholds

### Logging

- **Event Log**: View Hyper-V event logs
- **Action History**: Track all user actions
- **Length Limitation**: Automatic splitting of long messages

### Security

- **Authorization**: Access only for authorized users
- **Configuration**: Secure settings storage
- **Access Rights**: User permission management

## Technologies

### Development

- **Python**: Primary programming language
- **python-telegram-bot**: Telegram Bot API library
- **PowerShell**: Hyper-V interaction
- **psutil**: System resource monitoring

### Integrations

- **Hyper-V**: Virtual machine management
- **Telegram API**: User interaction interface
- **Windows Event Log**: System event retrieval

## Architecture

VMStatsBot is built on modular architecture principles:

1. **Handlers**: Telegram command and message handlers
2. **Services**: VM and system resource services
3. **Config**: Configuration management
4. **Keyboards**: Telegram custom keyboards

## Installation

### Prerequisites

- Windows 10/11 or Windows Server with Hyper-V
- Python 3.8+
- Administrator rights for Hyper-V operations
- Telegram bot token

### Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/takeshikodev/VMStatsBot.git
   cd VMStatsBot
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Settings:**
   - Fill in the required parameters:
     ```json
     {
       "telegram": {
         "token": "YOUR_BOT_TOKEN",
         "admin_ids": [
           123456789
         ]
       },
       "vm": {
         "name": "YOUR_VM_NAME",
         "address": "host:port",
            "password": "RDP_PASSWORD",
            "protocol": "RDP",
            "rdp_settings": {
                "username": "RDP_USERNAME",
                "screen_mode": 1,
                "desktop_width": 1920,
                "desktop_height": 1080,
                "session_bpp": 32
         }
       },
       "notifications": {
           "check_interval": 300
       }
     }
     ```

4. **Run the Bot:**
   ```bash
   python main.py
   ```

## Configuration

### Configuration Parameters

- **telegram.token**: Your Telegram bot token
- **telegram.admin_ids**: List of authorized users
- **vm.name**: Target virtual machine name
- **vm.monitoring**: Monitoring settings

### Monitoring

Configure monitoring parameters in `config.json`:
```json
"notifications": {
    "check_interval": 300         // Check interval in seconds
}
```

## Project Structure

```
vmstatsbot/
├── src/
│   ├── config/            # Configuration
│   │   └── config_manager.py  # Configuration management
│   ├── handlers/           # Command handlers
│   │   ├── base.py        # Base handler
│   │   ├── vm_control.py  # VM management
│   │   ├── settings.py    # Settings
│   │   └── action_log.py  # Logging
│   ├── services/          # Service classes
│   │   ├── vm_service.py  # VM service
│   │   └── monitor_service.py  # Monitoring
│   ├── keyboards/       # Telegram keyboards
│   └────── keyboards.py       # Keyboards
│   main.py           # Entry point
├── config.json           # Configuration
├── requirements.txt      # Dependencies
├── README.md            # Documentation
└── main.py           # Entry point
```

## Optimization

- VM state caching
- Efficient long message handling
- Asynchronous PowerShell command execution
- Optimized event log queries

## Contributing

If you want to contribute to the project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a Pull Request

Please ensure your code follows the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
