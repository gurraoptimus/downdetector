# Development Guide

This guide provides comprehensive information for developers who want to contribute to or extend the Down Detector application.

## Table of Contents

- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Code Architecture](#code-architecture)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Coding Standards](#coding-standards)
- [Contributing Guidelines](#contributing-guidelines)
- [Building and Packaging](#building-and-packaging)
- [Debugging](#debugging)
- [Performance Considerations](#performance-considerations)

## Development Environment Setup

### Prerequisites

- Python 3.7 or higher
- Git for version control
- Text editor or IDE (VS Code, PyCharm, etc.)
- Terminal/Command Prompt access

### Setting Up the Development Environment

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/downdetector.git
   cd downdetector
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Development Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your development settings
   ```

5. **Verify Installation**
   ```bash
   python downdetector.py --version
   ```

### Development Dependencies

For development, you may want to install additional packages:

```bash
pip install pytest pytest-cov black flake8 mypy
```

## Project Structure

```
downdetector/
├── downdetector.py          # Main application file
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── .env.example            # Environment variable template
├── .gitignore             # Git ignore rules
├── README.md              # Project overview
├── LICENSE                # Project license
├── docs/                  # Documentation
│   ├── README.md          # Documentation index
│   ├── Getting-Started.md # Installation guide
│   ├── User-Guide.md      # User manual
│   ├── Configuration.md   # Configuration reference
│   ├── API-Reference.md   # API documentation
│   ├── Troubleshooting.md # Common issues
│   ├── Changelog.md       # Version history
│   └── Development.md     # This file
├── tests/                 # Test files
│   ├── __init__.py
│   ├── test_downdetector.py
│   └── test_utils.py
└── scripts/               # Utility scripts
    ├── build.py           # Build automation
    └── release.py         # Release management
```

## Code Architecture

### Main Components

The application is structured around the `DownDetectorApp` class with the following key components:

#### 1. Core Application (`DownDetectorApp`)
- **Purpose**: Main application controller
- **Responsibilities**: UI management, user input handling, application lifecycle
- **Key Methods**: `run()`, `main_menu()`, `display_menu()`

#### 2. Website Management
- **Methods**: `add_website()`, `remove_website()`, `check_website()`
- **Data Structure**: JSON-based website storage
- **Features**: URL validation, duplicate detection, batch operations

#### 3. Monitoring System
- **Methods**: `monitor_websites()`, `continuous_monitor()`
- **Features**: Real-time monitoring, configurable intervals, status tracking
- **Performance**: Concurrent checking, timeout handling

#### 4. Logging System
- **Methods**: `setup_logging()`, `log_website_check()`, `log_system_event()`
- **Features**: Multiple log levels, file rotation, structured logging
- **Storage**: File-based with configurable retention

#### 5. Update System
- **Methods**: `check_for_updates()`, `download_and_install_update()`
- **Features**: GitHub integration, automatic downloads, backup/restore
- **Security**: Checksum validation, safe installation

#### 6. Configuration Management
- **Methods**: `load_config()`, `save_config()`
- **Features**: Environment variables, JSON configuration, validation
- **Extensibility**: Plugin-ready configuration system

### Design Patterns Used

#### 1. Singleton Pattern
- Application instance management
- Configuration singleton
- Logger instance management

#### 2. Observer Pattern
- Status change notifications
- Event-driven monitoring updates
- Log event broadcasting

#### 3. Strategy Pattern
- Different monitoring strategies
- Configurable check methods
- Extensible notification systems

#### 4. Command Pattern
- Menu action handling
- Undo/redo operations for configuration
- Batch operation management

## Development Workflow

### Branch Management

1. **Main Branches**
   - `main`: Stable production code
   - `develop`: Integration branch for features
   - `release/*`: Release preparation branches
   - `hotfix/*`: Critical bug fixes

2. **Feature Development**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   # Make changes
   git add .
   git commit -m "feat: add new feature description"
   git push origin feature/your-feature-name
   # Create pull request
   ```

### Commit Message Convention

Follow the Conventional Commits specification:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions/modifications
- `chore:` Build process or auxiliary tool changes

### Code Review Process

1. Create feature branch from `develop`
2. Implement changes with tests
3. Update documentation if needed
4. Submit pull request with:
   - Clear description
   - Test coverage information
   - Breaking changes notice
   - Related issue links

## Testing

### Test Structure

```
tests/
├── unit/                  # Unit tests
│   ├── test_app.py
│   ├── test_monitoring.py
│   └── test_config.py
├── integration/           # Integration tests
│   ├── test_full_workflow.py
│   └── test_api_integration.py
└── fixtures/              # Test data
    ├── sample_websites.json
    └── mock_responses.py
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=downdetector

# Run specific test file
pytest tests/unit/test_app.py

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_website"
```

### Test Guidelines

1. **Unit Tests**
   - Test individual methods in isolation
   - Mock external dependencies
   - Aim for 90%+ code coverage
   - Use descriptive test names

2. **Integration Tests**
   - Test component interactions
   - Use real network calls sparingly
   - Test configuration loading
   - Verify file operations

3. **Test Data**
   - Use fixtures for consistent test data
   - Mock HTTP responses
   - Create realistic test scenarios
   - Clean up after tests

### Example Test

```python
import pytest
from unittest.mock import patch, MagicMock
from downdetector import DownDetectorApp

class TestDownDetectorApp:
    def setup_method(self):
        self.app = DownDetectorApp()
    
    def test_add_website_valid_url(self):
        """Test adding a valid website URL."""
        with patch('builtins.input', return_value='https://example.com'):
            self.app.add_website()
        
        assert len(self.app.websites) == 1
        assert self.app.websites[0]['url'] == 'https://example.com'
    
    @patch('requests.get')
    def test_check_website_success(self, mock_get):
        """Test successful website check."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.5
        mock_get.return_value = mock_response
        
        result = self.app.check_website('https://example.com')
        
        assert result['status'] == 'UP'
        assert result['response_time'] == 500
```

## Coding Standards

### Python Style Guide

Follow PEP 8 with these specific guidelines:

#### 1. Code Formatting
```python
# Use 4 spaces for indentation
# Maximum line length: 88 characters (Black default)
# Use double quotes for strings
# Add trailing commas in multi-line structures

class DownDetectorApp:
    """Main application class for Down Detector."""
    
    def __init__(self, config_file: str = "config.json") -> None:
        self.config_file = config_file
        self.websites: List[Dict[str, Any]] = []
        self.logger = self.setup_logging()
```

#### 2. Naming Conventions
- Classes: `PascalCase` (e.g., `DownDetectorApp`)
- Functions/Methods: `snake_case` (e.g., `check_website`)
- Constants: `UPPER_CASE` (e.g., `DEFAULT_TIMEOUT`)
- Private methods: `_snake_case` (e.g., `_validate_url`)

#### 3. Type Hints
```python
from typing import List, Dict, Any, Optional, Union

def check_website(self, url: str, timeout: int = 10) -> Dict[str, Any]:
    """Check website status and return results."""
    pass

def monitor_websites(
    self, 
    websites: List[str], 
    interval: Optional[int] = None
) -> None:
    """Monitor multiple websites continuously."""
    pass
```

#### 4. Documentation
```python
class DownDetectorApp:
    """
    Main application class for Down Detector.
    
    This class manages website monitoring, user interface,
    and application configuration.
    
    Attributes:
        websites (List[Dict]): List of monitored websites
        config (Dict): Application configuration
        logger (Logger): Application logger instance
    
    Example:
        >>> app = DownDetectorApp()
        >>> app.add_website("https://example.com")
        >>> app.run()
    """
    
    def check_website(self, url: str, timeout: int = 10) -> Dict[str, Any]:
        """
        Check the status of a website.
        
        Args:
            url: The URL to check
            timeout: Request timeout in seconds
            
        Returns:
            Dictionary containing status information:
            - status: "UP" or "DOWN"
            - response_time: Response time in milliseconds
            - status_code: HTTP status code
            - timestamp: Check timestamp
            
        Raises:
            ValueError: If URL is invalid
            requests.RequestException: If network error occurs
            
        Example:
            >>> result = app.check_website("https://example.com")
            >>> print(result["status"])
            UP
        """
        pass
```

### Code Quality Tools

#### 1. Black (Code Formatting)
```bash
# Format all Python files
black .

# Check what would be formatted
black --check .
```

#### 2. Flake8 (Linting)
```bash
# Run linting
flake8 downdetector.py

# Configuration in setup.cfg
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = venv/
```

#### 3. MyPy (Type Checking)
```bash
# Type check
mypy downdetector.py

# Configuration in mypy.ini
[mypy]
python_version = 3.7
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

## Contributing Guidelines

### How to Contribute

1. **Fork the Repository**
   - Click "Fork" on GitHub
   - Clone your fork locally
   - Add upstream remote

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature
   ```

3. **Make Changes**
   - Write code following style guidelines
   - Add tests for new functionality
   - Update documentation

4. **Test Your Changes**
   ```bash
   pytest
   black --check .
   flake8
   mypy downdetector.py
   ```

5. **Submit Pull Request**
   - Push to your fork
   - Create pull request to `develop` branch
   - Include detailed description

### Pull Request Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Updated documentation

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Commented complex code
- [ ] No new warnings
```

### Issue Reporting

When reporting issues:

1. **Use Issue Templates**
2. **Provide System Information**
   - Python version
   - Operating system
   - Application version

3. **Include Reproduction Steps**
4. **Add Error Messages/Logs**
5. **Suggest Solutions (if any)**

## Building and Packaging

### Local Build

```bash
# Install build dependencies
pip install build wheel

# Build package
python -m build

# Install locally
pip install dist/downdetector-*.whl
```

### Distribution

```bash
# Build for distribution
python setup.py sdist bdist_wheel

# Upload to PyPI (maintainers only)
twine upload dist/*
```

### Executable Creation

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --name downdetector downdetector.py

# Output in dist/ directory
```

## Debugging

### Debug Mode

Enable debug mode for detailed logging:

```python
# In .env file
DEBUG=true
LOG_LEVEL=DEBUG

# Or via command line
python downdetector.py --debug
```

### Common Debug Techniques

#### 1. Logging Debug Information
```python
import logging

logger = logging.getLogger(__name__)

def check_website(self, url: str) -> Dict[str, Any]:
    logger.debug(f"Checking website: {url}")
    
    try:
        response = requests.get(url, timeout=self.timeout)
        logger.debug(f"Response code: {response.status_code}")
        return {"status": "UP", "code": response.status_code}
    except Exception as e:
        logger.error(f"Error checking {url}: {e}")
        return {"status": "DOWN", "error": str(e)}
```

#### 2. Interactive Debugging
```python
# Add breakpoint for debugging
import pdb; pdb.set_trace()

# Or use built-in breakpoint (Python 3.7+)
breakpoint()
```

#### 3. Performance Profiling
```python
import cProfile
import pstats

def profile_monitoring():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Run monitoring code
    app.monitor_websites()
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
```

### Debug Configuration

```python
# debug_config.py
DEBUG_SETTINGS = {
    "verbose_logging": True,
    "mock_network_calls": False,
    "test_mode": True,
    "log_all_requests": True,
    "enable_profiling": False,
}
```

## Performance Considerations

### Optimization Guidelines

#### 1. Network Operations
- Use connection pooling for multiple requests
- Implement request timeouts
- Add retry logic with exponential backoff
- Cache DNS lookups when possible

#### 2. Memory Management
- Limit log file sizes with rotation
- Clean up old monitoring data
- Use generators for large datasets
- Profile memory usage regularly

#### 3. Concurrent Processing
```python
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

async def check_website_async(self, session, url: str) -> Dict[str, Any]:
    """Asynchronous website checking."""
    try:
        async with session.get(url, timeout=10) as response:
            return {
                "url": url,
                "status": "UP" if response.status == 200 else "DOWN",
                "status_code": response.status,
                "response_time": response.headers.get("response-time", 0)
            }
    except Exception as e:
        return {"url": url, "status": "DOWN", "error": str(e)}

async def monitor_websites_concurrent(self, urls: List[str]) -> List[Dict]:
    """Monitor multiple websites concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [self.check_website_async(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
```

#### 4. Configuration Caching
```python
import functools
import time

@functools.lru_cache(maxsize=128)
def get_cached_config(self, key: str, cache_timeout: int = 300):
    """Get configuration value with caching."""
    return self.config.get(key)

def invalidate_config_cache(self):
    """Invalidate configuration cache."""
    self.get_cached_config.cache_clear()
```

### Performance Monitoring

```python
import time
from functools import wraps

def measure_time(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        logger.debug(
            f"{func.__name__} executed in {end_time - start_time:.2f} seconds"
        )
        return result
    return wrapper

class PerformanceMonitor:
    """Monitor application performance metrics."""
    
    def __init__(self):
        self.metrics = {}
    
    def record_metric(self, name: str, value: float):
        """Record performance metric."""
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append({
            "value": value,
            "timestamp": time.time()
        })
    
    def get_average(self, name: str, last_n: int = 10) -> float:
        """Get average of last N measurements."""
        if name not in self.metrics:
            return 0.0
        
        recent = self.metrics[name][-last_n:]
        return sum(m["value"] for m in recent) / len(recent)
```

## Advanced Topics

### Plugin System

```python
class PluginManager:
    """Manage application plugins."""
    
    def __init__(self):
        self.plugins = {}
        self.hooks = {}
    
    def register_plugin(self, name: str, plugin_class):
        """Register a new plugin."""
        self.plugins[name] = plugin_class()
    
    def register_hook(self, event: str, callback):
        """Register callback for event."""
        if event not in self.hooks:
            self.hooks[event] = []
        self.hooks[event].append(callback)
    
    def trigger_hook(self, event: str, *args, **kwargs):
        """Trigger all callbacks for event."""
        if event in self.hooks:
            for callback in self.hooks[event]:
                callback(*args, **kwargs)
```

### Custom Notification Systems

```python
class NotificationManager:
    """Handle various notification methods."""
    
    def __init__(self):
        self.providers = {}
    
    def add_provider(self, name: str, provider):
        """Add notification provider."""
        self.providers[name] = provider
    
    def send_notification(self, message: str, providers: List[str] = None):
        """Send notification via specified providers."""
        target_providers = providers or list(self.providers.keys())
        
        for provider_name in target_providers:
            if provider_name in self.providers:
                try:
                    self.providers[provider_name].send(message)
                except Exception as e:
                    logger.error(f"Notification failed for {provider_name}: {e}")
```

### Configuration Extensions

```python
class ConfigManager:
    """Advanced configuration management."""
    
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config = {}
        self.watchers = []
    
    def watch_config(self, callback):
        """Watch for configuration changes."""
        self.watchers.append(callback)
    
    def reload_config(self):
        """Reload configuration from file."""
        try:
            with open(self.config_file, 'r') as f:
                new_config = json.load(f)
            
            if new_config != self.config:
                old_config = self.config.copy()
                self.config = new_config
                
                # Notify watchers
                for watcher in self.watchers:
                    watcher(old_config, new_config)
                    
        except Exception as e:
            logger.error(f"Failed to reload config: {e}")
```

This comprehensive development guide should help contributors understand the codebase, follow best practices, and contribute effectively to the Down Detector project. For additional questions or clarifications, please refer to the other documentation files or open an issue on GitHub.
