# Getting Started with Down Detector

## 📋 Prerequisites

Before installing Down Detector, ensure you have:

- **Python 3.7+** installed on your system
- **pip** package manager (usually comes with Python)
- **Internet connection** for monitoring websites and updates
- **Terminal/Command Prompt** access

## 🚀 Installation

### Method 1: Clone from GitHub (Recommended)

```bash
# Clone the repository
git clone https://github.com/gurraoptimus/downdetector.git

# Navigate to the directory
cd downdetector

# Install dependencies
pip install -r requirements.txt

# Run the application
python downdetector.py
```

### Method 2: Download ZIP

1. Download the latest release from GitHub
2. Extract the ZIP file to your desired location
3. Open terminal/command prompt in the extracted folder
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `python downdetector.py`

## ⚙️ Initial Setup

### 1. First Run

When you run Down Detector for the first time:

- A `.env` file will be automatically created with default settings
- The application will display an animated bootup sequence
- You'll see the main menu with 10 options

### 2. Environment Configuration

The application creates a `.env` file with these default settings:

```env
# Down Detector Configuration
TIMEOUT=5
WEBSITES_FILE=websites.json
MONITOR_INTERVAL=5
ANIMATION_SPEED=0.1
ENABLE_SOUNDS=true
AUTO_UPDATE_CHECK=true
USER_AGENT=Mozilla/5.0...
MAX_RETRIES=3
LOG_FILE=downdetector.log
DEBUG_MODE=false
```

### 3. Adding Your First Website

1. Select option **1** from the main menu
2. Enter a website URL (examples):
   - `google.com`
   - `https://github.com`
   - `http://example.com`
3. The application will automatically add `https://` if not provided
4. Confirm the website was added successfully

### 4. Testing the Monitor

1. Select option **4** to check all websites once
2. View the status report with response times
3. Listen for sound notifications (if enabled)

## 🎯 Quick Operations

### Check Single Website Status
- Menu Option 4: "Check All" - Tests all configured websites

### Start Continuous Monitoring
- Menu Option 5: "Start Monitor"
- Set custom interval (default: 5 seconds)
- Press `Ctrl+C` to stop monitoring

### View Configuration
- Menu Option 3: "View List" - See all monitored websites
- Menu Option 6: "Settings" - View/modify configuration

### System Updates
- Menu Option 7: "System Updates" - Check for new versions
- Auto-download and install updates available

## 🔧 Customization

### Timeout Settings
- Default: 5 seconds
- Modify in Menu → Settings → Change Timeout
- Or edit `.env` file: `TIMEOUT=10`

### Sound Notifications
- Toggle in Menu → Settings → Toggle Sounds
- Or edit `.env` file: `ENABLE_SOUNDS=false`

### Animation Speed
- Edit `.env` file: `ANIMATION_SPEED=0.2` (slower) or `0.05` (faster)

### Log Files
- View logs: Menu → Settings → View Log File
- Location: `downdetector.log` (configurable)
- Debug mode: Set `DEBUG_MODE=true` in `.env`

## ❗ Common First-Time Issues

### "Module not found" Error
```bash
# Install missing dependencies
pip install -r requirements.txt

# Or install individually
pip install requests colorama python-dotenv psutil
```

### Permission Errors (Updates)
- Run terminal as Administrator (Windows)
- Use `sudo` on macOS/Linux if needed
- Or manually download updates

### Sound Not Working
- Check system audio settings
- Set `ENABLE_SOUNDS=false` in `.env` to disable
- Install audio drivers if needed

### Websites Not Loading
- Check internet connection
- Verify firewall/antivirus settings
- Try different websites to test

## 🎉 Next Steps

Once you have Down Detector running:

1. **Add multiple websites** to monitor your entire infrastructure
2. **Customize settings** to match your monitoring needs
3. **Set up continuous monitoring** for real-time status updates
4. **Enable auto-updates** to stay current with new features
5. **Review logs** to track historical performance

## 📞 Getting Help

If you encounter issues:

1. Check the [Troubleshooting Guide](Troubleshooting.md)
2. Review the [User Guide](User-Guide.md) for detailed features
3. Check the log file for error details
4. Visit the GitHub repository for support

---

**Ready to monitor your websites? Let's get started!** 🚀