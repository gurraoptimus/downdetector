<p align="center">
   <img src="https://github.com/gurraoptimus/downdetector/blob/main/assets/downdetector-logo.svg" alt="Down Detector Logo" width="600" height="600">
</p>

> A real-time website monitoring application with an animated terminal interface.

## 📚 Documentation

- [API Documentation](docs/API-Reference.md) - Detailed API reference and integration guide
- [Installation Guide](docs/INSTALLATION.md) - Complete setup instructions
- [Configuration Guide](docs/CONFIGURATION.md) - Advanced configuration options
- [Troubleshooting](docs/Troubleshooting.md) - Common issues and solutions
- [Contributing Guidelines](docs/CONTRIBUTING.md) - How to contribute to the project
- [Discussions](DISCUSSIONS.md) - Community discussions and feature requests
- [Wiki](https://github.com/gurraoptimus/downdetector/wiki) - Comprehensive documentation and guides

## ✨ Features

- 🌐 **Real-time Website Monitoring** - Monitor multiple websites simultaneously
- 🎨 **Animated Dashboard Interface** - Beautiful terminal UI with animations and colors
- 🔊 **Sound Notifications** - Audio alerts for status changes (Windows)
- ⚙️ **Configuration Management** - Easy setup via `.env` file
- 🔄 **Auto-Updates** - Automatic update checking from GitHub
- 🖥️ **Multi-platform Support** - Works on Windows, macOS, and Linux
- 📝 **Logging System** - Comprehensive logging with debug mode
- 🛠️ **System Management** - Reset, reboot, and configuration options

## 🚀 Installation

1. Clone or download the repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python downdetector.py
   ```

## ⚙️ Configuration

The application automatically creates a `.env` file with default settings on first run:

```env
# Website monitoring timeout in seconds
TIMEOUT=5

# File to store websites list
WEBSITES_FILE=websites.json

# Default monitoring interval in seconds
MONITOR_INTERVAL=5

# Animation speed (0.1 = fast, 0.5 = slow)
ANIMATION_SPEED=0.1

# Enable sound notifications (true/false)
ENABLE_SOUNDS=true

# Auto-check for updates on startup (true/false)
AUTO_UPDATE_CHECK=true

# Log file path
LOG_FILE=downdetector.log

# Enable debug mode (true/false)
DEBUG_MODE=false
```

## 📖 Usage

### Main Menu Options

| Option | Description |
|--------|-------------|
| **1** | Add Website - Add a new website to monitor |
| **2** | Remove Website - Remove websites from monitoring |
| **3** | View List - Display all configured websites |
| **4** | Check All - Perform one-time status check of all websites |
| **5** | Start Monitor - Begin continuous real-time monitoring |
| **6** | Settings - Configure application settings |
| **7** | System Updates - Check for and install updates |
| **8** | Reset System - Reset to default configuration |
| **9** | Reboot App - Restart the application |
| **0** | Exit App - Close the application |

### 📊 Monitoring Features

- **Live Dashboard** - Real-time status updates with animations
- **Status Indicators** - Visual indicators for online/offline status
- **Response Logging** - Detailed logs of all website checks
- **Customizable Intervals** - Set monitoring frequency
- **Sound Alerts** - Audio notifications for status changes

## 💻 System Requirements

- Python 3.6+
- Windows (for sound notifications), macOS, or Linux
- Internet connection for monitoring and updates

## 📦 Dependencies

The project includes a `requirements.txt` file for easy dependency management:

```txt
requests>=2.25.1
colorama>=0.4.4
python-dotenv>=0.19.0
```

| Package | Purpose |
|---------|---------|
| `requests` | HTTP requests for website checking |
| `colorama` | Cross-platform colored terminal text |
| `python-dotenv` | Environment variable management |
| `winsound` | Windows sound notifications (Windows only) |

## 🔄 Update System

The application includes an automatic update system that:
- ✅ Checks for updates from GitHub on startup
- ⬇️ Downloads and installs updates directly
- 💾 Creates backups before updating
- 🔍 Supports manual update checking

## 📋 Logging

Comprehensive logging system with:
- 🌐 Website check results with response times
- ⚠️ System events and errors
- 🔄 Update activities
- 📊 Configurable log levels (INFO/DEBUG)
- 📖 Log file viewer within the application

---

**Current Version:** `1.0`  
**Developer:** Gurraoptimus Development  
**License:** Open Source - Check repository for details