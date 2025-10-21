# User Guide - Down Detector

## 🌟 Main Menu Overview

Down Detector features a beautiful animated terminal interface with 10 main options:

```
┌─ Main Menu ──────────────────────────────────────────────┐
│                                                           │
│  █ 1 █ Add Website     █ 2 █ Remove Website  │
│                                                           │
│  █ 3 █ View List       █ 4 █ Check All       │
│                                                           │
│  █ 5 █ Start Monitor   █ 6 █ Settings        │
│                                                           │
│  █ 7 █ System Updates  █ 8 █ Reset System    │
│                                                           │
│  █ 9 █ Reboot App      █ 0 █ Exit App        │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

## 📝 Feature Guide

### 1️⃣ Add Website

**Purpose**: Add new websites to your monitoring list

**How to use**:
1. Select option 1 from main menu
2. Enter website URL in the form
3. URLs can be entered with or without protocol:
   - ✅ `google.com`
   - ✅ `https://github.com`
   - ✅ `http://example.com`

**Features**:
- Automatic protocol detection (adds https:// if missing)
- Duplicate detection and prevention
- Animated confirmation messages
- Automatic saving to JSON configuration

### 2️⃣ Remove Website

**Purpose**: Remove websites from monitoring

**Options**:
- **Single Removal**: Select specific website by number
- **Bulk Removal**: Remove all websites at once
- **Cancellation**: Exit without changes

**Safety Features**:
- Confirmation required for bulk operations
- Type "DELETE ALL" to confirm mass removal
- Individual website selection with numbered list

### 3️⃣ View List

**Purpose**: Display all monitored websites in a formatted table

**Information Shown**:
- Website number (for easy reference)
- Complete URL
- Total count of monitored sites
- Organized table format

### 4️⃣ Check All

**Purpose**: Perform one-time status check of all websites

**Features**:
- Real-time status checking with animations
- Response time measurement
- Status code reporting
- Sound notifications for each result
- Timestamped reports
- Color-coded results (Green=Online, Red=Offline)

### 5️⃣ Start Monitor

**Purpose**: Begin continuous real-time monitoring

**Configuration**:
- Custom interval setting (default from .env)
- Live dashboard with real-time updates
- Cycle counter for tracking rounds
- Press Ctrl+C to stop monitoring

**Live Dashboard Features**:
- Real-time status indicators
- Response time tracking
- Animated progress bars
- Countdown timer to next check
- Status summary header

### 6️⃣ Settings

**Purpose**: Configure application behavior

**Available Settings**:

#### Timeout Duration
- Default: 5 seconds
- Range: 1-60 seconds recommended
- Affects how long to wait for website response

#### Sound Effects
- Toggle audio notifications on/off
- Works with system audio
- Plays different sounds for online/offline status

#### Environment File Editing
- View current .env file location
- Manual editing instructions
- Reload settings without restart

#### Log File Management
- View log file contents (last 50 entries)
- Clear log files
- Open logs in notepad (Windows)
- Color-coded log levels

### 7️⃣ System Updates

**Purpose**: Manage application updates

**Features**:

#### Update Checking
- Manual update checks
- Automatic startup checks (configurable)
- GitHub API integration
- Version comparison

#### Update Installation
- Direct download from GitHub raw files
- Automatic backup creation
- One-click installation
- Auto-restart option

#### Update Management
- View current version info
- Toggle auto-update checking
- System information display
- Update history viewing

### 8️⃣ Reset System

**Purpose**: Return application to default state

**Reset Actions**:
- Clear all monitored websites
- Delete configuration files
- Reset timeout to defaults
- Preserve .env file settings

**Safety**:
- Confirmation required (type 'yes')
- Cannot be undone
- Animated reset process

### 9️⃣ Reboot App

**Purpose**: Restart the application completely

**Process**:
- Animated shutdown sequence
- Complete memory clearing
- Fresh startup sequence
- All settings preserved

### 0️⃣ Exit App

**Purpose**: Gracefully close the application

**Features**:
- Clean shutdown process
- Settings automatically saved
- Polite goodbye message

## 🎨 Interface Features

### Animations
- Loading spinners for all operations
- Progress bars for downloads and installs
- Bouncing text for important messages
- Typewriter effects for system messages

### Color Coding
- **Green**: Success, online status
- **Red**: Errors, offline status
- **Yellow**: Warnings, pending operations
- **Blue**: Information, system messages
- **Cyan**: Navigation and borders

### Sound System
- **Online Sound**: Success notification
- **Offline Sound**: Alert notification
- **Error Sound**: Problem notification
- **System Sound**: General notifications

## 📊 Monitoring Features

### Status Indicators
- ● **Green Circle**: Website is online (HTTP 200)
- ● **Red Circle**: Website is offline/error
- **Response Time**: Millisecond precision
- **Status Codes**: HTTP response codes displayed

### Logging System
- All checks logged with timestamps
- Response times recorded
- Error conditions tracked
- User actions logged
- System events recorded

### Performance Tracking
- Response time history
- Success/failure rates
- System resource usage
- Network performance metrics

## ⚙️ Advanced Features

### Environment Variables
All settings configurable via .env file:

```env
TIMEOUT=5                    # Request timeout in seconds
WEBSITES_FILE=websites.json  # Configuration file location
MONITOR_INTERVAL=5           # Default monitoring interval
ANIMATION_SPEED=0.1          # UI animation speed
ENABLE_SOUNDS=true           # Audio notifications
AUTO_UPDATE_CHECK=true       # Automatic update checking
LOG_FILE=downdetector.log    # Log file location
DEBUG_MODE=false             # Debug logging
```

### Keyboard Shortcuts
- **Ctrl+C**: Stop monitoring or exit application
- **Enter**: Confirm actions and continue
- **Number Keys**: Quick menu navigation

### Cross-Platform Support
- **Windows**: Full feature support with native sounds
- **macOS**: Complete compatibility with system integration
- **Linux**: Full functionality with audio support

## 🔧 Customization Tips

### Monitoring Optimization
- Set timeout based on network speed (3-10 seconds)
- Adjust interval for balance between responsiveness and system load
- Use shorter intervals (1-3s) for critical sites
- Use longer intervals (10-30s) for general monitoring

### Performance Tuning
- Disable sounds on slow systems
- Increase animation speed for faster UI
- Enable debug mode for troubleshooting
- Regular log file cleanup

### Workflow Recommendations
1. **Start Small**: Add 2-3 important websites first
2. **Test Settings**: Use "Check All" to verify configuration
3. **Monitor Gradually**: Start with longer intervals
4. **Review Logs**: Check logs periodically for issues
5. **Update Regularly**: Enable auto-updates for best experience

---

**Happy Monitoring!** 🚀 Your websites are in good hands with Down Detector.