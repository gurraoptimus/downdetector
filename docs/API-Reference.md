# API Reference

## 📚 Technical Documentation

This document provides comprehensive technical documentation for the Down Detector application's internal APIs, methods, and data structures.

## 🏗️ Core Architecture

### Main Class: `DownDetectorApp`

The application is built around a single main class that handles all functionality:

```python
class DownDetectorApp:
    def __init__(self):
        # Core properties
        self.websites = []                    # List of monitored websites
        self.current_version = "1.0"          # Application version
        self.github_repo = "gurraoptimus/downdetector"  # GitHub repository
        
        # Configuration properties (from .env)
        self.timeout = int(os.getenv('TIMEOUT', '5'))
        self.websites_file = os.getenv('WEBSITES_FILE', 'websites.json')
        self.monitor_interval = int(os.getenv('MONITOR_INTERVAL', '5'))
        self.animation_speed = float(os.getenv('ANIMATION_SPEED', '0.1'))
        self.enable_sounds = os.getenv('ENABLE_SOUNDS', 'true').lower() == 'true'
        self.auto_update_check = os.getenv('AUTO_UPDATE_CHECK', 'true').lower() == 'true'
        self.log_file = os.getenv('LOG_FILE', 'downdetector.log')
        self.debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
        
        # Logging system
        self.logger = None  # Configured in setup_logging()
```

## 🔧 Core Methods

### Configuration and Setup

#### `setup_logging()`

Configures the logging system with file and console handlers.

**Purpose**: Initialize comprehensive logging system
**Parameters**: None
**Returns**: None
**Side Effects**: Creates log file, sets up logger handlers

```python
def setup_logging(self):
    """Setup logging configuration"""
    # Determines log level based on debug mode
    # Creates file and console handlers
    # Sets up formatters and filters
```

#### `create_env_file()`

Creates default `.env` configuration file if it doesn't exist.

**Purpose**: Initialize default configuration
**Parameters**: None
**Returns**: `bool` - Success status
**Side Effects**: Creates `.env` file with default values

#### `reload_env_settings()`

Reloads environment variables from `.env` file without restart.

**Purpose**: Apply configuration changes dynamically
**Parameters**: None
**Returns**: None
**Side Effects**: Updates instance variables with new values

### Website Management

#### `add_website()`

Interactive method to add new websites to monitoring list.

**Purpose**: Add website to monitoring
**Parameters**: None (interactive input)
**Returns**: None
**Side Effects**: Updates websites list, saves configuration
**User Interface**: Animated form with validation

#### `remove_website()`

Interactive method to remove websites from monitoring list.

**Purpose**: Remove websites from monitoring
**Parameters**: None (interactive input)  
**Returns**: None
**Side Effects**: Updates websites list, saves configuration
**Options**: Single removal or bulk removal

#### `view_websites()`

Display all monitored websites in formatted table.

**Purpose**: Show current monitoring list
**Parameters**: None
**Returns**: None
**Side Effects**: None (read-only display)

### Website Monitoring

#### `check_website(url)`

Core method to check individual website status.

**Purpose**: Test single website connectivity and response
**Parameters**: 
- `url` (str): Website URL to check
**Returns**: `tuple(bool, str)` - (is_online, status_info)
**Features**:
- Response time measurement
- HTTP status code capture
- Error handling and logging
- User-Agent header configuration

```python
def check_website(self, url):
    """Check if a single website is up or down"""
    start_time = time.time()
    try:
        headers = {'User-Agent': os.getenv('USER_AGENT', '...')}
        response = requests.get(url, timeout=self.timeout, headers=headers)
        response_time = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            self.log_website_check(url, True, response.status_code, response_time)
            return True, response.status_code
        else:
            self.log_website_check(url, False, response.status_code, response_time)
            return False, response.status_code
    except Exception as e:
        # Error handling and logging
        return False, str(e)
```

#### `check_all_websites()`

Check all configured websites once with animated dashboard.

**Purpose**: Perform one-time status check of all websites
**Parameters**: None
**Returns**: None
**Side Effects**: Displays results, plays sounds, logs activity

#### `monitor_websites()`

Start continuous monitoring with live dashboard.

**Purpose**: Real-time monitoring with configurable intervals
**Parameters**: None (interactive interval input)
**Returns**: None
**Side Effects**: Continuous monitoring loop until Ctrl+C
**Features**:
- Live status updates
- Configurable intervals
- Animated dashboard
- Cycle counting
- Keyboard interrupt handling

### Update System

#### `check_for_updates(silent=False)`

Check GitHub for application updates.

**Purpose**: Compare current version with latest GitHub release
**Parameters**:
- `silent` (bool): If True, suppress UI output
**Returns**: `tuple(bool, str, str, str)` - (has_update, version, notes, url)
**API Endpoints**: GitHub Releases API

```python
def check_for_updates(self, silent=False):
    """Check for application updates from GitHub"""
    try:
        headers = {
            'User-Agent': 'DownDetector-UpdateChecker/1.0',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.get(self.update_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            release_data = response.json()
            latest_version = release_data.get('tag_name', '').lstrip('v')
            # Version comparison logic
            return self.is_newer_version(latest_version, self.current_version)
    except Exception as e:
        # Error handling
        return False, "", "", ""
```

#### `download_and_install_update(version)`

Download and install update from GitHub raw files.

**Purpose**: Automated update installation
**Parameters**:
- `version` (str): Target version to install
**Returns**: None
**Side Effects**: 
- Downloads new application file
- Creates backup of current version
- Replaces current file
- Offers restart option

#### `is_newer_version(latest, current)`

Compare version numbers to determine if update needed.

**Purpose**: Semantic version comparison
**Parameters**:
- `latest` (str): Latest available version
- `current` (str): Current application version
**Returns**: `bool` - True if latest is newer
**Algorithm**: Semantic version parsing and comparison

### Logging System

#### `log_website_check(website, is_up, status, response_time=None)`

Log website monitoring results.

**Purpose**: Record website check results
**Parameters**:
- `website` (str): Website URL
- `is_up` (bool): Online status
- `status` (str/int): HTTP status or error message
- `response_time` (float, optional): Response time in milliseconds
**Returns**: None
**Log Format**: `CHECK | {website} | {status} | {response_time}ms`

#### `log_system_event(event_type, message)`

Log application system events.

**Purpose**: Record system-level activities
**Parameters**:
- `event_type` (str): Category of event
- `message` (str): Event description
**Returns**: None
**Log Format**: `SYSTEM | {event_type} | {message}`

#### `log_update_event(event, details="")`

Log update-related activities.

**Purpose**: Track update process steps
**Parameters**:
- `event` (str): Update event type
- `details` (str, optional): Additional information
**Returns**: None
**Log Format**: `UPDATE | {event} | {details}`

#### `log_error(error_type, message)`

Log error conditions.

**Purpose**: Record error events for debugging
**Parameters**:
- `error_type` (str): Error category
- `message` (str): Error description
**Returns**: None
**Log Format**: `ERROR | {error_type} | {message}`

### User Interface

#### `print_header()`

Display application header with branding.

**Purpose**: Consistent header across all screens
**Parameters**: None
**Returns**: None
**Features**: ASCII art, navigation bar, color coding

#### `print_menu()`

Display main menu with current status.

**Purpose**: Interactive main menu
**Parameters**: None
**Returns**: None
**Features**: Animated menu, status bar, option highlighting

#### Animation Methods

**`loading_animation(text="Loading", duration=2)`**
- Animated loading spinner with customizable text and duration

**`typewriter_effect(text, delay=None)`**
- Character-by-character text animation

**`progress_bar(duration=2, width=40)`**
- Animated progress bar for operations

**`bounce_text(text, color=Fore.CYAN)`**
- Bouncing text effect for important messages

**`pulsing_status(status, is_online)`**
- Pulsing status indicator with color coding

### File Operations

#### `load_websites()`

Load website configuration from JSON file.

**Purpose**: Initialize websites list from storage
**Parameters**: None
**Returns**: None
**Side Effects**: Populates self.websites from file
**Error Handling**: Creates empty list if file missing/corrupt

#### `save_websites()`

Save current website list to JSON file.

**Purpose**: Persist website configuration
**Parameters**: None
**Returns**: None
**Side Effects**: Writes websites.json file
**Format**: `{"websites": [...], "timeout": int}`

### System Operations

#### `reset_system()`

Reset application to default state.

**Purpose**: Clear all configuration and return to defaults
**Parameters**: None (interactive confirmation)
**Returns**: None
**Side Effects**: 
- Clears websites list
- Deletes configuration files
- Preserves .env settings

#### `reboot_system()`

Restart application with full shutdown sequence.

**Purpose**: Complete application restart
**Parameters**: None (interactive confirmation)
**Returns**: None
**Process**: Animated shutdown → Clear memory → Fresh startup

#### `run()`

Main application event loop.

**Purpose**: Primary execution loop and menu handling
**Parameters**: None
**Returns**: None
**Features**: 
- Menu navigation
- Error handling
- Graceful shutdown
- Sound feedback

## 📊 Data Structures

### Website Storage Format

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

### Log Entry Format

```
2025-10-21 10:30:15 | INFO     | CHECK | https://google.com | UP | 200 | 45.23ms
2025-10-21 10:30:16 | INFO     | SYSTEM | WEBSITE_ADDED | Added website: https://example.com
2025-10-21 10:30:20 | ERROR    | UPDATE_ERROR | Network timeout during update check
```

### Update Response Format

```json
{
  "tag_name": "v1.0",
  "body": "Release notes...",
  "html_url": "https://github.com/user/repo/releases/tag/v1.0",
  "published_at": "2025-10-21T10:00:00Z"
}
```

## 🔌 External Dependencies

### HTTP Requests
- **Library**: `requests >= 2.28.0`
- **Usage**: Website checking, GitHub API calls, update downloads
- **Configuration**: Custom User-Agent, timeout settings

### Terminal Colors
- **Library**: `colorama >= 0.4.4`
- **Usage**: Cross-platform colored output
- **Features**: ANSI color codes, background colors, text styles

### Environment Variables
- **Library**: `python-dotenv >= 0.19.0`
- **Usage**: Configuration management
- **Features**: .env file parsing, variable loading

### System Information
- **Library**: `psutil >= 5.9.0`
- **Usage**: System monitoring in info display
- **Features**: CPU, memory, disk usage statistics

## 🎯 Extension Points

### Custom Notification Systems

```python
def custom_notification_handler(website, status, response_time):
    """Example custom notification handler"""
    if not status:
        # Send email, Slack message, etc.
        send_alert(f"Website {website} is down!")
```

### Custom Website Validators

```python
def custom_website_checker(url):
    """Example custom website checking logic"""
    # Add custom validation, authentication, etc.
    return is_online, status_info
```

### Plugin Architecture Potential

```python
class PluginBase:
    def on_website_status_change(self, website, old_status, new_status):
        pass
    
    def on_monitoring_start(self, websites):
        pass
    
    def on_monitoring_stop(self, duration):
        pass
```

## ⚠️ Error Handling

### Exception Hierarchy

- **NetworkError**: Connection timeouts, DNS failures
- **ConfigurationError**: Invalid .env values, missing files
- **UpdateError**: GitHub API failures, download issues
- **FileSystemError**: Permission issues, disk space

### Graceful Degradation

- Missing dependencies fall back to basic functionality
- Network issues don't crash the application
- Invalid configurations use default values
- Logging failures don't interrupt operations

## 🔒 Security Considerations

### Network Security
- HTTPS preferred for all website checks
- Configurable User-Agent to avoid bot detection
- Request timeout limits to prevent hanging
- No sensitive data in logs

### File System Security
- Configuration files in application directory only
- No elevated privileges required
- Backup files created safely
- Log files with appropriate permissions

---

**API Documentation Complete** 🔧 Ready for development and integration!
