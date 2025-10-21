# Troubleshooting Guide

## 🚨 Common Issues and Solutions

### Installation Problems

#### "Python not found" Error
**Problem**: `'python' is not recognized as an internal or external command`

**Solutions**:
1. **Install Python**: Download from [python.org](https://python.org)
2. **Add to PATH**: During installation, check "Add Python to PATH"
3. **Alternative command**: Try `python3` instead of `python`
4. **Verify installation**: Run `python --version`

#### "pip not found" Error
**Problem**: `'pip' is not recognized as an internal or external command`

**Solutions**:
1. **Reinstall Python**: Use "Add Python to PATH" option
2. **Manual pip installation**: Download get-pip.py and run it
3. **Alternative command**: Try `python -m pip` instead of `pip`
4. **Check installation**: Run `pip --version`

#### Module Import Errors
**Problem**: `ModuleNotFoundError: No module named 'requests'`

**Solutions**:
```bash
# Install missing dependencies
pip install -r requirements.txt

# Or install individually
pip install requests colorama python-dotenv psutil

# For Python 3 specifically
pip3 install -r requirements.txt
```

### Application Startup Issues

#### Permission Denied Errors
**Problem**: Cannot create files or access directories

**Solutions**:
- **Windows**: Run terminal as Administrator
- **macOS/Linux**: Use appropriate permissions or `sudo`
- **File permissions**: Ensure write access to application directory
- **Antivirus**: Add application folder to antivirus exceptions

#### ".env file not created" Error
**Problem**: Application cannot create configuration file

**Solutions**:
1. **Check directory permissions**: Ensure write access
2. **Manual creation**: Create `.env` file manually with default content
3. **Run as administrator**: Elevated permissions may be needed
4. **Disk space**: Ensure sufficient free space

#### Sound System Errors
**Problem**: Audio notifications not working

**Solutions**:
- **Windows**: Check system audio and drivers
- **macOS**: Verify System Preferences → Sound
- **Linux**: Install audio libraries (`sudo apt-get install python3-ossaudiodev`)
- **Disable sounds**: Set `ENABLE_SOUNDS=false` in .env file

### Website Monitoring Issues

#### "Connection timeout" Errors
**Problem**: Websites consistently timeout

**Solutions**:
1. **Increase timeout**: Set `TIMEOUT=10` or higher in .env
2. **Check internet**: Verify your internet connection
3. **DNS issues**: Try different DNS servers (8.8.8.8, 1.1.1.1)
4. **Firewall**: Check firewall/antivirus blocking connections
5. **Proxy settings**: Configure proxy if required

#### "SSL Certificate" Errors
**Problem**: SSL/TLS certificate verification failures

**Solutions**:
- **Update certificates**: Update your system's certificate store
- **Python certificates**: Reinstall Python with SSL support
- **Corporate networks**: May require proxy/certificate configuration
- **Temporary workaround**: Test with HTTP sites first

#### False Positive "Offline" Results
**Problem**: Sites show offline when they're actually online

**Common Causes & Solutions**:
1. **Rate limiting**: Websites blocking frequent requests
   - Increase `MONITOR_INTERVAL` to 30+ seconds
   - Change `USER_AGENT` in .env file

2. **Geolocation blocking**: Site blocking your region
   - Test from different location/VPN
   - Check site accessibility in browser

3. **Bot detection**: Anti-bot systems blocking requests
   - Modify `USER_AGENT` to standard browser string
   - Add delays between requests

### Update System Issues

#### Update Download Failures
**Problem**: Cannot download updates from GitHub

**Solutions**:
1. **Internet connection**: Verify stable internet access
2. **GitHub accessibility**: Check if GitHub.com is accessible
3. **Firewall settings**: Allow application internet access
4. **Manual update**: Download file manually from GitHub
5. **Proxy configuration**: Configure proxy settings if needed

#### Update Installation Failures
**Problem**: Downloaded update cannot be installed

**Solutions**:
- **File permissions**: Run as administrator/root
- **File in use**: Close other instances of the application
- **Antivirus interference**: Temporarily disable antivirus
- **Manual installation**: Replace file manually
- **Backup restoration**: Use created backup if installation fails

### Performance Issues

#### Slow Application Response
**Problem**: Application feels sluggish or unresponsive

**Solutions**:
1. **Reduce animation speed**: Set `ANIMATION_SPEED=0.05` or `0`
2. **Disable sounds**: Set `ENABLE_SOUNDS=false`
3. **Increase intervals**: Set higher `MONITOR_INTERVAL`
4. **System resources**: Close other applications
5. **Hardware**: Ensure adequate RAM and CPU

#### High Memory Usage
**Problem**: Application consuming too much memory

**Solutions**:
- **Restart application**: Use "Reboot App" option
- **Clear logs**: Use log file viewer to clear old logs
- **Reduce websites**: Monitor fewer sites simultaneously
- **Update application**: Newer versions may have optimizations

### Configuration Issues

#### Settings Not Saving
**Problem**: Configuration changes don't persist

**Solutions**:
1. **File permissions**: Ensure .env file is writable
2. **Reload settings**: Use Settings → Reload Settings
3. **File format**: Check .env file format (KEY=VALUE)
4. **Restart application**: Close and restart application
5. **Manual editing**: Edit .env file directly

#### Log File Problems
**Problem**: Cannot view or create log files

**Solutions**:
- **Directory permissions**: Ensure log directory is writable
- **File path**: Check `LOG_FILE` setting in .env
- **Disk space**: Verify sufficient disk space
- **File locks**: Close other applications using log file

### Network-Specific Issues

#### Corporate Firewalls
**Problem**: Application blocked by corporate network

**Solutions**:
1. **IT support**: Contact IT department for application approval
2. **Proxy configuration**: Configure HTTP/HTTPS proxy settings
3. **Port access**: Request access to HTTP (80) and HTTPS (443) ports
4. **VPN usage**: Use personal VPN if policy allows

#### DNS Resolution Issues
**Problem**: Domain names not resolving

**Solutions**:
- **DNS servers**: Use public DNS (8.8.8.8, 1.1.1.1)
- **Host file**: Check system hosts file for conflicts
- **Network adapter**: Reset network adapter settings
- **ISP issues**: Contact Internet Service Provider

### Emergency Recovery

#### Corrupted Configuration
**Problem**: Application won't start due to bad configuration

**Solutions**:
1. **Delete .env file**: Application will recreate with defaults
2. **Reset system**: Use menu option 8 if application loads
3. **Manual cleanup**: Delete websites.json and .env files
4. **Fresh installation**: Download and reinstall application

#### Complete Application Failure
**Problem**: Application crashes immediately on startup

**Solutions**:
1. **Check Python version**: Ensure Python 3.7+
2. **Reinstall dependencies**: `pip install -r requirements.txt --force-reinstall`
3. **Clear all files**: Delete .env, websites.json, *.log files
4. **Redownload application**: Get fresh copy from GitHub
5. **System reboot**: Restart computer and try again

## 🔍 Diagnostic Commands

### System Information
```bash
# Check Python version
python --version

# Check pip version
pip --version

# List installed packages
pip list

# Check application dependencies
pip show requests colorama python-dotenv psutil
```

### Network Testing
```bash
# Test internet connectivity
ping google.com

# Test DNS resolution
nslookup google.com

# Test specific website
curl -I https://example.com
```

### File Permissions (Linux/macOS)
```bash
# Check file permissions
ls -la .env websites.json *.log

# Fix permissions if needed
chmod 644 .env websites.json
chmod 755 .
```

## 📞 Getting Additional Help

### Before Seeking Help
1. **Check this guide**: Review all relevant sections
2. **Check logs**: Look at log file for detailed error messages
3. **Test with minimal setup**: Try with just one website
4. **Gather information**: Note your OS, Python version, error messages

### Support Channels
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check other wiki pages for detailed guides
- **Community**: Share experiences with other users

### Reporting Issues
When reporting problems, include:
1. **Operating System**: Windows/macOS/Linux version
2. **Python Version**: Output of `python --version`
3. **Error Messages**: Complete error text from console/logs
4. **Steps to Reproduce**: Exact steps that cause the problem
5. **Configuration**: Your .env file contents (remove sensitive data)

---

**Most issues are solvable!** 🛠️ Don't hesitate to seek help if needed.