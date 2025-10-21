## 📋 Environment Variables

Down Detector uses a `.env` file for configuration. This file is automatically created on first run with default values.

### Configuration File Location
- **File**: `.env` (in the same directory as `downdetector.py`)
- **Format**: KEY=VALUE pairs
- **Encoding**: UTF-8

## ⚙️ Available Settings

### Core Monitoring Settings

#### `TIMEOUT`
- **Default**: `5`
- **Type**: Integer (seconds)
- **Range**: 1-60 recommended
- **Purpose**: Maximum time to wait for website response

```env
TIMEOUT=5          # 5 second timeout
TIMEOUT=10         # 10 second timeout for slower connections
```

#### `MONITOR_INTERVAL`
- **Default**: `5`
- **Type**: Integer (seconds)
- **Range**: 1-300 recommended
- **Purpose**: Default interval between monitoring cycles

```env
MONITOR_INTERVAL=5    # Check every 5 seconds
MONITOR_INTERVAL=30   # Check every 30 seconds
MONITOR_INTERVAL=1    # Check every second (intensive)
```

#### `WEBSITES_FILE`
- **Default**: `websites.json`
- **Type**: String (filename)
- **Purpose**: File to store monitored websites list

```env
WEBSITES_FILE=websites.json
WEBSITES_FILE=my_sites.json
WEBSITES_FILE=data/websites.json
```

### User Interface Settings

#### `ANIMATION_SPEED`
- **Default**: `0.1`
- **Type**: Float (seconds)
- **Range**: 0.01-1.0
- **Purpose**: Speed of UI animations and effects

```env
ANIMATION_SPEED=0.1    # Normal speed
ANIMATION_SPEED=0.05   # Faster animations
ANIMATION_SPEED=0.3    # Slower animations
ANIMATION_SPEED=0      # Disable animations
```

#### `ENABLE_SOUNDS`
- **Default**: `true`
- **Type**: Boolean
- **Values**: `true`, `false`
- **Purpose**: Enable/disable audio notifications

```env
ENABLE_SOUNDS=true     # Enable sounds
ENABLE_SOUNDS=false    # Disable sounds
```

### Update Management

#### `AUTO_UPDATE_CHECK`
- **Default**: `true`
- **Type**: Boolean
- **Values**: `true`, `false`
- **Purpose**: Check for updates on application startup

```env
AUTO_UPDATE_CHECK=true   # Check for updates
AUTO_UPDATE_CHECK=false  # Skip update checks
```

### Logging Configuration

#### `LOG_FILE`
- **Default**: `downdetector.log`
- **Type**: String (filename)
- **Purpose**: Location of log file

```env
LOG_FILE=downdetector.log
LOG_FILE=logs/monitoring.log
LOG_FILE=C:\Logs\downdetector.log
```

#### `DEBUG_MODE`
- **Default**: `false`
- **Type**: Boolean
- **Values**: `true`, `false`
- **Purpose**: Enable debug logging to console

```env
DEBUG_MODE=false    # Normal logging
DEBUG_MODE=true     # Debug logging enabled
```

### Network Settings

#### `USER_AGENT`
- **Default**: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...`
- **Type**: String
- **Purpose**: HTTP User-Agent header for requests

```env
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
USER_AGENT=DownDetector/1.0 Monitor
```

#### `MAX_RETRIES`
- **Default**: `3`
- **Type**: Integer
- **Range**: 0-10
- **Purpose**: Maximum retry attempts for failed requests

```env
MAX_RETRIES=3     # Retry 3 times
MAX_RETRIES=1     # Only retry once
MAX_RETRIES=0     # No retries
```

## 📝 Complete Example Configuration

```env
# Down Detector Configuration
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

# User Agent for HTTP requests
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36

# Maximum retries for failed requests
MAX_RETRIES=3

# Log file path (optional)
LOG_FILE=downdetector.log

# Enable debug mode (true/false)
DEBUG_MODE=false
```

## 🔧 Configuration Scenarios

### High-Performance Monitoring
```env
TIMEOUT=3
MONITOR_INTERVAL=1
ANIMATION_SPEED=0.05
ENABLE_SOUNDS=false
DEBUG_MODE=false
```

### Conservative/Slow Network
```env
TIMEOUT=15
MONITOR_INTERVAL=30
ANIMATION_SPEED=0.3
MAX_RETRIES=5
DEBUG_MODE=false
```

### Development/Debug Mode
```env
TIMEOUT=10
MONITOR_INTERVAL=10
ANIMATION_SPEED=0.2
ENABLE_SOUNDS=true
DEBUG_MODE=true
LOG_FILE=debug.log
```

### Silent Background Monitoring
```env
TIMEOUT=5
MONITOR_INTERVAL=60
ANIMATION_SPEED=0
ENABLE_SOUNDS=false
AUTO_UPDATE_CHECK=false
```

## 📁 File Structure

### Default Files Created
```
downdetector/
├── downdetector.py      # Main application
├── .env                 # Configuration file
├── websites.json        # Monitored websites
├── downdetector.log     # Log file
├── requirements.txt     # Dependencies
└── docs/               # Documentation
```

### Websites Configuration Format
The `websites.json` file stores your monitored websites:

```json
{
  "websites": [
    "https://google.com",
    "https://github.com",
    "https://stackoverflow.com"
  ],
  "timeout": 5
}
```

## 🔄 Applying Configuration Changes

### Method 1: In-App Reload
1. Modify `.env` file
2. Go to Settings menu (option 6)
3. Select "Reload Settings" (option 4)

### Method 2: Application Restart
1. Modify `.env` file
2. Exit application (option 0)
3. Restart application

### Method 3: Reboot Feature
1. Modify `.env` file
2. Use "Reboot App" (option 9)

## ⚠️ Configuration Notes

### File Permissions
- Ensure `.env` file is readable/writable
- Log file directory must exist and be writable
- Websites file needs write permissions for updates

### Validation
- Invalid values fall back to defaults
- Boolean values: only `true`/`false` accepted
- Numeric values: must be valid integers/floats
- File paths: relative to application directory

### Security Considerations
- `.env` file contains configuration only
- No sensitive data stored in plain text
- User-Agent can be customized for identification
- Log files may contain website URLs

---

**Configure once, monitor everywhere!** ⚙️