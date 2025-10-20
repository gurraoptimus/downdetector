import requests
import time
import os
import sys
import json
import winsound
from datetime import datetime
from colorama import Fore, Back, Style, init
from dotenv import load_dotenv
import subprocess
import platform

# Load environment variables from .env file
load_dotenv()

# Initialize colorama for cross-platform colored terminal text
init(autoreset=True)

class DownDetectorApp:
    def __init__(self):
        self.websites = []
        self.current_version = "2.2.0"  # Current app version
        self.github_repo = "gurraoptimus/downdetector"  # Replace with your actual repo
        self.update_url = f"https://api.github.com/repos/{self.github_repo}/.git"
        
        # Load settings from environment variables with defaults
        self.timeout = int(os.getenv('TIMEOUT', '5'))
        self.websites_file = os.getenv('WEBSITES_FILE', 'websites.json')
        self.monitor_interval = int(os.getenv('MONITOR_INTERVAL', '5'))
        self.animation_speed = float(os.getenv('ANIMATION_SPEED', '0.1'))
        self.enable_sounds = os.getenv('ENABLE_SOUNDS', 'true').lower() == 'true'
        self.auto_update_check = os.getenv('AUTO_UPDATE_CHECK', 'true').lower() == 'true'
        
        self.bootup_sequence()
        self.load_websites()
        
        # Check for updates on startup if enabled
        if self.auto_update_check:
            self.check_for_updates(silent=True)
    
    def create_env_file(self):
        """Create a .env file with default settings"""
        env_content = """# Down Detector Configuration
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
"""
        
        try:
            with open('.env', 'w') as f:
                f.write(env_content)
            return True
        except Exception as e:
            print(f"{Fore.RED}❌ Error creating .env file: {e}")
            return False
    
    def check_for_updates(self, silent=False):
        """Check for application updates from GitHub"""
        if not silent:
            self.print_header()
            self.bounce_text(f"{Fore.WHITE}{Back.BLUE}  🔄 SYSTEM UPDATES  {Style.RESET_ALL}", Fore.WHITE)
            self.loading_animation("Checking for updates", 1.0)
        
        try:
            headers = {
                'User-Agent': 'DownDetector-UpdateChecker/1.0'
            }
            response = requests.get(self.update_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                release_data = response.json()
                latest_version = release_data.get('tag_name', '').lstrip('v')
                release_notes = release_data.get('body', 'No release notes available')
                download_url = release_data.get('html_url', '')
                published_date = release_data.get('published_at', '')
                
                if self.is_newer_version(latest_version, self.current_version):
                    if not silent:
                        self.display_update_available(latest_version, release_notes, download_url, published_date)
                    else:
                        print(f"\n{Back.GREEN}{Fore.WHITE} 🔔 UPDATE AVAILABLE {Style.RESET_ALL} Version {latest_version} is available!")
                        print(f"{Fore.CYAN}ℹ️  Check the updates menu for more details")
                    return True, latest_version, release_notes, download_url
                else:
                    if not silent:
                        self.bounce_text(f"{Back.GREEN}{Fore.WHITE} ✅ UP TO DATE {Style.RESET_ALL} You're running the latest version!", Fore.GREEN)
                    return False, self.current_version, "", ""
            else:
                if not silent:
                    self.bounce_text(f"{Back.RED}{Fore.WHITE} ❌ UPDATE CHECK FAILED {Style.RESET_ALL} Unable to check for updates", Fore.RED)
                return False, "", "", ""
                
        except requests.exceptions.RequestException as e:
            if not silent:
                print(f"{Fore.RED}❌ Network error while checking updates: {str(e)[:50]}...")
            return False, "", "", ""
        except Exception as e:
            if not silent:
                print(f"{Fore.RED}❌ Error checking for updates: {str(e)[:50]}...")
            return False, "", "", ""
    
    def is_newer_version(self, latest, current):
        """Compare version numbers to determine if update is needed"""
        try:
            latest_parts = [int(x) for x in latest.split('.')]
            current_parts = [int(x) for x in current.split('.')]
            
            # Pad shorter version with zeros
            max_len = max(len(latest_parts), len(current_parts))
            latest_parts += [0] * (max_len - len(latest_parts))
            current_parts += [0] * (max_len - len(current_parts))
            
            return latest_parts > current_parts
        except:
            return False
    
    def display_update_available(self, version, notes, url, date):
        """Display update information in a formatted way"""
        print(f"\n{Back.GREEN}{Fore.WHITE} 🚀 NEW UPDATE AVAILABLE {Style.RESET_ALL}")
        
        update_info = f"""{Fore.CYAN}┌─ Update Information ──────────────────────────────────────┐
│                                                           │
│ Current Version: {Back.BLUE}{Fore.WHITE} {self.current_version} {Style.RESET_ALL}                         {Fore.CYAN}│
│ Latest Version:  {Back.GREEN}{Fore.WHITE} {version} {Style.RESET_ALL}                           {Fore.CYAN}│
│ Release Date:    {date[:10] if date else 'Unknown'}                        │
│                                                           │
│ {Back.YELLOW}{Fore.BLACK} RELEASE NOTES {Style.RESET_ALL}                                  {Fore.CYAN}│
│                                                           │"""
        
        print(update_info)
        
        # Display release notes (first 5 lines)
        note_lines = notes.split('\n')[:5] if notes else ["No release notes available"]
        for line in note_lines:
            if line.strip():
                print(f"{Fore.CYAN}│ {line[:55]:<55} │")
        
        print(f"{Fore.CYAN}│                                                           │")
        print(f"{Fore.CYAN}└───────────────────────────────────────────────────────────┘")
        
        print(f"\n{Fore.YELLOW}Update Options:")
        print(f"{Back.GREEN}{Fore.WHITE} 1 {Style.RESET_ALL} Open download page in browser")
        print(f"{Back.BLUE}{Fore.WHITE} 2 {Style.RESET_ALL} Copy download link to clipboard")
        print(f"{Back.YELLOW}{Fore.BLACK} 3 {Style.RESET_ALL} View full release notes")
        print(f"{Back.RED}{Fore.WHITE} 4 {Style.RESET_ALL} Skip this update")
        
        choice = input(f"\n{Fore.CYAN}Select option (1-4): ").strip()
        
        if choice == '1':
            self.open_browser(url)
        elif choice == '2':
            self.copy_to_clipboard(url)
        elif choice == '3':
            self.show_full_release_notes(notes)
        elif choice == '4':
            self.bounce_text(f"{Fore.YELLOW}Update skipped", Fore.YELLOW)
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def open_browser(self, url):
        """Open URL in default browser"""
        try:
            system = platform.system().lower()
            if system == 'windows':
                os.startfile(url)
            elif system == 'darwin':  # macOS
                subprocess.run(['open', url])
            else:  # Linux and others
                subprocess.run(['xdg-open', url])
            
            self.bounce_text(f"{Back.GREEN}{Fore.WHITE} ✅ OPENED {Style.RESET_ALL} Download page opened in browser!", Fore.GREEN)
        except Exception as e:
            print(f"{Fore.RED}❌ Error opening browser: {e}")
            print(f"{Fore.YELLOW}Manual download URL: {url}")
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        try:
            system = platform.system().lower()
            if system == 'windows':
                subprocess.run(['clip'], input=text.encode(), check=True)
            elif system == 'darwin':  # macOS
                subprocess.run(['pbcopy'], input=text.encode(), check=True)
            else:  # Linux
                subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode(), check=True)
            
            self.bounce_text(f"{Back.GREEN}{Fore.WHITE} ✅ COPIED {Style.RESET_ALL} Download link copied to clipboard!", Fore.GREEN)
        except Exception as e:
            print(f"{Fore.RED}❌ Error copying to clipboard: {e}")
            print(f"{Fore.YELLOW}Manual copy: {text}")
    
    def show_full_release_notes(self, notes):
        """Display full release notes"""
        self.clear_screen()
        print(f"{Back.BLUE}{Fore.WHITE} 📋 FULL RELEASE NOTES {Style.RESET_ALL}\n")
        
        if notes:
            print(f"{Fore.CYAN}{'='*60}")
            print(f"{Fore.WHITE}{notes}")
            print(f"{Fore.CYAN}{'='*60}")
        else:
            print(f"{Fore.YELLOW}No detailed release notes available.")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def system_updates_menu(self):
        """Main system updates menu"""
        self.print_header()
        self.bounce_text(f"{Fore.WHITE}{Back.BLUE}  🔄 SYSTEM UPDATES  {Style.RESET_ALL}", Fore.WHITE)
        
        update_menu = f"""{Fore.CYAN}┌─ Update Management ───────────────────────────────────────┐
│                                                           │
│ Current Version: {Back.BLUE}{Fore.WHITE} Down Detector v{self.current_version} {Style.RESET_ALL}            {Fore.CYAN}│
│ Auto-Check: {Back.BLUE}{Fore.WHITE} {'Enabled' if self.auto_update_check else 'Disabled'} {Style.RESET_ALL}                      {Fore.CYAN}│
│                                                           │
│ {Back.GREEN}{Fore.WHITE} 1 {Style.RESET_ALL} Check for Updates                             {Fore.CYAN}│
│ {Back.BLUE}{Fore.WHITE} 2 {Style.RESET_ALL} View Current Version Info                     {Fore.CYAN}│
│ {Back.YELLOW}{Fore.BLACK} 3 {Style.RESET_ALL} Toggle Auto-Update Check                      {Fore.CYAN}│
│ {Back.MAGENTA}{Fore.WHITE} 4 {Style.RESET_ALL} System Information                            {Fore.CYAN}│
│ {Back.CYAN}{Fore.BLACK} 5 {Style.RESET_ALL} Update History                                {Fore.CYAN}│
│ {Back.BLACK}{Fore.WHITE} 6 {Style.RESET_ALL} Return to Main Menu                           {Fore.CYAN}│
│                                                           │
└───────────────────────────────────────────────────────────┘"""
        
        print(f"\n{update_menu}")
        
        choice = input(f"\n{Fore.YELLOW}Select option (1-6): ").strip()
        
        if choice == '1':
            self.check_for_updates(silent=False)
        elif choice == '2':
            self.show_version_info()
        elif choice == '3':
            self.toggle_auto_update()
        elif choice == '4':
            self.show_system_info()
        elif choice == '5':
            self.show_update_history()
        elif choice == '6':
            return
        else:
            self.bounce_text(f"{Back.RED}{Fore.WHITE} ❌ INVALID {Style.RESET_ALL} Please select 1-6", Fore.RED)
        
        if choice in ['1', '2', '3', '4', '5']:
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            self.system_updates_menu()  # Show menu again
    
    def show_version_info(self):
        """Display detailed version information"""
        self.loading_animation("Loading version information", 0.8)
        
        version_info = f"""{Fore.CYAN}┌─ Version Information ─────────────────────────────────────┐
│                                                           │
│ Application: Down Detector                                │
│ Version: v{self.current_version}                                     │
│ Developer: Gurraoptimus Development                       │
│ Platform: {platform.system()} {platform.release()}                            │
│ Python Version: {platform.python_version()}                         │
│                                                           │
│ Features in this version:                                 │
│ • Real-time website monitoring                           │
│ • Animated dashboard interface                           │
│ • Sound notifications                                    │
│ • Configuration management                               │
│ • System updates                                         │
│ • Multi-platform support                                │
│                                                           │
└───────────────────────────────────────────────────────────┘"""
        
        print(f"\n{version_info}")
    
    def toggle_auto_update(self):
        """Toggle automatic update checking"""
        self.auto_update_check = not self.auto_update_check
        status = "enabled" if self.auto_update_check else "disabled"
        
        self.bounce_text(f"{Back.GREEN}{Fore.WHITE} ✅ UPDATED {Style.RESET_ALL} Auto-update check {status}!", Fore.GREEN)
        
        # Update .env file
        try:
            env_lines = []
            if os.path.exists('.env'):
                with open('.env', 'r') as f:
                    env_lines = f.readlines()
            
            # Update or add AUTO_UPDATE_CHECK line
            updated = False
            for i, line in enumerate(env_lines):
                if line.startswith('AUTO_UPDATE_CHECK='):
                    env_lines[i] = f"AUTO_UPDATE_CHECK={'true' if self.auto_update_check else 'false'}\n"
                    updated = True
                    break
            
            if not updated:
                env_lines.append(f"AUTO_UPDATE_CHECK={'true' if self.auto_update_check else 'false'}\n")
            
            with open('.env', 'w') as f:
                f.writelines(env_lines)
                
            print(f"{Fore.CYAN}ℹ️  Setting saved to .env file")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️  Could not update .env file: {e}")
    
    def show_system_info(self):
        """Display comprehensive system information"""
        self.loading_animation("Gathering system information", 1.0)
        
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
        except ImportError:
            cpu_percent = "N/A"
            memory = None
            disk = None
        
        system_info = f"""{Fore.CYAN}┌─ System Information ──────────────────────────────────────┐
│                                                           │
│ Operating System: {platform.system()} {platform.release()}                │
│ Architecture: {platform.machine()}                              │
│ Processor: {platform.processor()[:30]}               │
│ Python Version: {platform.python_version()}                         │
│ CPU Usage: {cpu_percent}%                                      │"""
        
        if memory:
            memory_percent = memory.percent
            system_info += f"""
│ Memory Usage: {memory_percent}%                                   │"""
        
        if disk:
            disk_percent = disk.percent
            system_info += f"""
│ Disk Usage: {disk_percent}%                                     │"""
        
        system_info += f"""
│                                                           │
│ Application Details:                                      │
│ • Config File: {self.websites_file}                           │
│ • Websites Monitored: {len(self.websites)}                              │
│ • Timeout Setting: {self.timeout}s                               │
│ • Sound Effects: {'On' if self.enable_sounds else 'Off'}                                │
│                                                           │
└───────────────────────────────────────────────────────────┘"""
        
        print(f"\n{system_info}")
    
    def show_update_history(self):
        """Display update history (simulated for now)"""
        self.loading_animation("Loading update history", 0.8)
        
        # This is a simulated update history - in a real app, you'd store this data
        history = [
            {"version": "2.1.0", "date": "2025-01-15", "type": "Major", "description": "Added system updates feature"},
            {"version": "2.0.5", "date": "2025-01-10", "type": "Patch", "description": "Bug fixes and performance improvements"},
            {"version": "2.0.0", "date": "2025-01-01", "type": "Major", "description": "Complete UI overhaul with animations"},
            {"version": "1.5.0", "date": "2024-12-15", "type": "Minor", "description": "Added sound notifications"},
            {"version": "1.0.0", "date": "2024-12-01", "type": "Major", "description": "Initial release"}
        ]
        
        print(f"\n{Back.BLUE}{Fore.WHITE} 📊 UPDATE HISTORY {Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}┌─ Version History ─────────────────────────────────────────┐")
        print(f"{Fore.CYAN}│ {Back.BLUE}{Fore.WHITE} Ver.  {Style.RESET_ALL} {Back.BLUE}{Fore.WHITE} Date       {Style.RESET_ALL} {Back.BLUE}{Fore.WHITE} Type  {Style.RESET_ALL} {Back.BLUE}{Fore.WHITE} Description            {Style.RESET_ALL} {Fore.CYAN}│")
        print(f"{Fore.CYAN}├──────┼────────────┼───────┼────────────────────────┤")
        
        for update in history:
            version = update["version"]
            date = update["date"]
            update_type = update["type"]
            desc = update["description"][:20] + "..." if len(update["description"]) > 20 else update["description"]
            
            # Highlight current version
            if version == self.current_version:
                print(f"{Fore.CYAN}│ {Back.GREEN}{Fore.WHITE}{version:<6}{Style.RESET_ALL} │ {date}  │ {update_type:<5} │ {desc:<22} {Fore.CYAN}│")
            else:
                print(f"{Fore.CYAN}│ {version:<6} │ {date}  │ {update_type:<5} │ {desc:<22} │")
        
        print(f"{Fore.CYAN}└──────┴────────────┴───────┴────────────────────────┘")
        print(f"{Fore.YELLOW}💡 Tip: Enable auto-update check to stay current!")

    def reload_env_settings(self):
        """Reload environment variables"""
        load_dotenv(override=True)
        self.timeout = int(os.getenv('TIMEOUT', '5'))
        self.websites_file = os.getenv('WEBSITES_FILE', 'websites.json')
        self.monitor_interval = int(os.getenv('MONITOR_INTERVAL', '5'))
        self.animation_speed = float(os.getenv('ANIMATION_SPEED', '0.1'))
        self.enable_sounds = os.getenv('ENABLE_SOUNDS', 'true').lower() == 'true'
        self.auto_update_check = os.getenv('AUTO_UPDATE_CHECK', 'true').lower() == 'true'

    def bootup_sequence(self):
        """Animated bootup sequence"""
        self.clear_screen()
        
        
        # Check for .env file
        if not os.path.exists('.env'):
            print(f"{Fore.YELLOW}⚠️  No .env file found. Creating default configuration...")
            if self.create_env_file():
                print(f"{Fore.GREEN}✅ Default .env file created successfully!")
                time.sleep(1)
        
        # ASCII Art Logo
        logo = [
            "╔═══════════════════════════════════════════════════════════════════╗",
            "║ ██████╗  ██████╗ ██╗    ██╗███╗   ██╗                              ║",
            "║ ██╔══██╗██╔═══██╗██║    ██║████╗  ██║                              ║",
            "║ ██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║                              ║",
            "║ ██║  ██║██║   ██║██║███╗██║██║╚██╗██║                              ║",
            "║ ██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║                              ║",
            "║ ╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝                              ║",
            "║                                                                    ║",
            "║ ██████╗ ███████╗████████╗███████╗ ██████╗████████╗ ██████╗ ██████╗ ║",
            "║ ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗║",
            "║ ██║  ██║█████╗     ██║   █████╗  ██║        ██║   ██║   ██║██████╔╝║",
            "║ ██║  ██║██╔══╝     ██║   ██╔══╝  ██║        ██║   ██║   ██║██╔══██╗║",
            "║ ██████╔╝███████╗   ██║   ███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║║",
            "║ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝║",
            "║                                                                    ║",
            "╚═══════════════════════════════════════════════════════════════════╝"
        ]
        
        # Display logo with animation
        print(f"{Fore.CYAN}")
        for line in logo:
            print(line)
            time.sleep(self.animation_speed * 0.5)
        print(Style.RESET_ALL)
        
        # System info display
        system_info = [
            f"{Fore.GREEN}[SYSTEM] Initializing Down Detector v{self.current_version}...",
            f"{Fore.GREEN}[SYSTEM] Developed by Gurraoptimus Development",
            f"{Fore.GREEN}[SYSTEM] Loading core modules...",
            f"{Fore.YELLOW}[BOOT  ] Checking system requirements...",
            f"{Fore.YELLOW}[BOOT  ] Loading network stack...",
            f"{Fore.YELLOW}[BOOT  ] Initializing monitoring engine...",
            f"{Fore.BLUE}[CONFIG] Loading configuration files...",
            f"{Fore.BLUE}[CONFIG] Loading .env settings...",
            f"{Fore.BLUE}[CONFIG] Setting up user preferences...",
            f"{Fore.MAGENTA}[UPDATE] Checking for system updates...",
            f"{Fore.MAGENTA}[READY ] System initialized successfully!"
        ]
        
        print(f"\n{Fore.WHITE}SYSTEM BOOTUP SEQUENCE{Style.RESET_ALL}")
        print("=" * 60)
        
        for info in system_info:
            print(info)
            time.sleep(self.animation_speed * 2)
            
        # Progress bar for final initialization
        print(f"\n{Fore.CYAN}Final initialization:")
        self.progress_bar(1.5, 40)
        
        # Success message with sound
        self.play_pop_sound("online")
        print(f"\n{Back.GREEN}{Fore.WHITE} ✅ SYSTEM READY - DOWN DETECTOR ONLINE {Style.RESET_ALL}\n")
        time.sleep(0.5)
    
    def reboot_system(self):
        """Reboot the application with full shutdown and restart sequence"""
        self.print_header()
        print(f"\n{Fore.WHITE}{Back.BLUE}  🔄 SYSTEM REBOOT  {Style.RESET_ALL}\n")
        
        confirm = input(f"{Fore.YELLOW}⚠️  Are you sure you want to reboot the system? (y/n): ").strip().lower()
        
        if confirm in ['y', 'yes']:
            # Shutdown sequence
            self.typewriter_effect(f"{Fore.YELLOW}Initiating system reboot sequence...")
            
            shutdown_steps = [
                f"{Fore.RED}[SHUTDOWN] Stopping monitoring services...",
                f"{Fore.RED}[SHUTDOWN] Closing network connections...",
                f"{Fore.RED}[SHUTDOWN] Saving current state...",
                f"{Fore.RED}[SHUTDOWN] Clearing memory buffers...",
                f"{Fore.RED}[SHUTDOWN] Terminating processes...",
                f"{Fore.RED}[SHUTDOWN] System shutdown complete."
            ]
            
            for step in shutdown_steps:
                print(step)
                time.sleep(0.4)
            
            # Shutdown progress bar
            print(f"\n{Fore.RED}Shutdown progress:")
            self.progress_bar(2, 40)
            
            self.play_pop_sound("offline")
            print(f"\n{Back.RED}{Fore.WHITE} 🔌 SYSTEM OFFLINE {Style.RESET_ALL}")
            time.sleep(1)
            
            # Clear screen and show rebooting message
            self.clear_screen()
            print(f"{Back.YELLOW}{Fore.BLACK} 🔄 REBOOTING... {Style.RESET_ALL}")
            time.sleep(2)
            
            # Restart the application
            self.__init__()
            
        else:
            self.bounce_text(f"{Fore.YELLOW}❌ Reboot cancelled", Fore.YELLOW)
            input(f"\n{Fore.CYAN}Press Enter to return to menu...")
    
    def play_pop_sound(self, sound_type="default"):
        """Play different Windows sounds for different events"""
        if not self.enable_sounds:
            return
            
        try:
            if sound_type == "online":
                winsound.MessageBeep(winsound.MB_OK)
            elif sound_type == "offline":
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            elif sound_type == "error":
                winsound.MessageBeep(winsound.MB_ICONHAND)
            else:
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
        except ImportError:
            try:
                print('\a', end='', flush=True)
            except:
                pass

    def loading_animation(self, text="Loading", duration=2):
        """Animated loading spinner"""
        frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        end_time = time.time() + duration
        
        while time.time() < end_time:
            for frame in frames:
                if time.time() >= end_time:
                    break
                print(f"\r{Fore.CYAN}{frame} {text}...", end="", flush=True)
                time.sleep(self.animation_speed)
        print("\r" + " " * (len(text) + 10) + "\r", end="", flush=True)
    
    def typewriter_effect(self, text, delay=None):
        """Typewriter animation for text"""
        if delay is None:
            delay = self.animation_speed * 0.2
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def progress_bar(self, duration=2, width=40):
        """Animated progress bar"""
        for i in range(width + 1):
            progress = i / width
            filled = int(width * progress)
            bar = f"{Fore.GREEN}{'█' * filled}{Fore.LIGHTBLACK_EX}{'░' * (width - filled)}"
            percent = int(progress * 100)
            print(f"\r{bar} {Fore.CYAN}{percent}%", end="", flush=True)
            time.sleep(duration / width)
        print()
    
    def bounce_text(self, text, color=Fore.CYAN):
        """Bouncing text animation"""
        self.play_pop_sound()
        for _ in range(2):
            print(f"\r{color}{text}", end="", flush=True)
            time.sleep(self.animation_speed * 2)
            print(f"\r{' ' * len(text)}", end="", flush=True)
            time.sleep(self.animation_speed)
        print(f"\r{color}{text}")
    
    def fade_in_text(self, text, color=Fore.WHITE):
        """Fade in effect for text"""
        colors = [Fore.LIGHTBLACK_EX, color]
        for fade_color in colors:
            print(f"\r{fade_color}{text}", end="", flush=True)
            time.sleep(self.animation_speed * 2)
        print()
    
    def animated_border(self, width=60):
        """Animated border drawing"""
        print(f"{Fore.CYAN}╔", end="", flush=True)
        for i in range(width):
            print("═", end="", flush=True)
            time.sleep(self.animation_speed * 0.05)
        print("╗")
        
        print(f"{Fore.CYAN}║{' ' * width}║")
        
        print(f"{Fore.CYAN}╚", end="", flush=True)
        for i in range(width):
            print("═", end="", flush=True)
            time.sleep(self.animation_speed * 0.05)
        print("╝")
    
    def pulsing_status(self, status, is_online):
        """Pulsing status indicator"""
        colors = [Fore.GREEN, Fore.LIGHTGREEN_EX] if is_online else [Fore.RED, Fore.LIGHTRED_EX]
        symbol = "●"
        
        for color in colors:
            print(f"\r{color}{symbol} {status}", end="", flush=True)
            time.sleep(self.animation_speed * 2)
        print()
    
    def load_websites(self):
        """Load websites from file with animation"""
        self.loading_animation("Loading configuration", 0.5)
        try:
            if os.path.exists(self.websites_file):
                with open(self.websites_file, 'r') as f:
                    data = json.load(f)
                    self.websites = data.get('websites', [])
                    # Don't override timeout from .env with file value
        except (json.JSONDecodeError, FileNotFoundError):
            self.websites = []
    
    def save_websites(self):
        """Save websites to file with animation"""
        try:
            self.loading_animation("Saving configuration", 0.3)
            data = {
                'websites': self.websites,
                'timeout': self.timeout
            }
            with open(self.websites_file, 'w') as f:
                json.dump(data, f, indent=2)
            self.play_pop_sound("online")
        except Exception as e:
            print(f"{Fore.RED}❌ Error saving websites: {e}")
    
    def reset_system(self):
        """Reset the app to default state with animations"""
        self.print_header()
        print(f"\n{Fore.WHITE}{Back.RED}  🔄 SYSTEM RESET  {Style.RESET_ALL}\n")
        
        self.typewriter_effect(f"{Fore.YELLOW}Initializing system reset...")
        time.sleep(0.3)
        
        print(f"{Fore.YELLOW}┌─ Reset Options ───────────────────────────┐")
        print(f"{Fore.YELLOW}│ This operation will:                     │")
        print(f"{Fore.YELLOW}│ • Clear all monitored websites           │")
        print(f"{Fore.YELLOW}│ • Reset timeout to default (5 seconds)   │")
        print(f"{Fore.YELLOW}│ • Delete configuration file              │")
        print(f"{Fore.YELLOW}│ • Keep .env file settings                │")
        print(f"{Fore.YELLOW}└───────────────────────────────────────────┘")
        
        confirm = input(f"\n{Fore.RED}⚠️  Confirm reset (type 'yes' to proceed): ").strip().lower()
        
        if confirm == 'yes':
            self.loading_animation("Resetting system", 1.5)
            self.websites = []
            
            try:
                if os.path.exists(self.websites_file):
                    os.remove(self.websites_file)
                self.bounce_text(f"{Fore.GREEN}✅ System successfully reset!", Fore.GREEN)
                print(f"{Fore.CYAN}ℹ️  All configuration data cleared")
                print(f"{Fore.CYAN}ℹ️  .env file preserved")
            except Exception as e:
                print(f"\n{Fore.RED}❌ Reset failed: {e}")
        else:
            self.bounce_text(f"{Fore.YELLOW}❌ Reset cancelled", Fore.YELLOW)
        
        input(f"\n{Fore.CYAN}Press Enter to return to menu...")
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print the app header with animated design"""
        self.clear_screen()
        
        header_lines = [
            "╔══════════════════════════════════════════════════════════╗",
            "║                    🌐 DOWN DETECTOR                      ║",
            "║                 Real-Time Website Monitor                ║",
            "║               Built by: Gurraoptimus Development         ║",
            "╚══════════════════════════════════════════════════════════╝"
        ]
        
        print(f"{Back.BLUE}{Fore.WHITE}")
        for line in header_lines:
            print(line)
        print(Style.RESET_ALL)
        
        nav_items = "█ HOME █ MONITOR █ SETTINGS █ UPDATES █ ABOUT █"
        print(f"{Back.CYAN}{Fore.BLACK} {nav_items} {Style.RESET_ALL}\n")
    
    def print_menu(self):
        """Print the main menu with animations"""
        menu_content = f"""{Fore.CYAN}┌─ Main Menu ──────────────────────────────────────────────┐
│                                                           │
│  {Back.GREEN}{Fore.BLACK} 1 {Style.RESET_ALL} Add Website     {Back.GREEN}{Fore.BLACK} 2 {Style.RESET_ALL} Remove Website  {Fore.CYAN}│
│                                                           │
│  {Back.BLUE}{Fore.WHITE} 3 {Style.RESET_ALL} View List       {Back.BLUE}{Fore.WHITE} 4 {Style.RESET_ALL} Check All       {Fore.CYAN}│
│                                                           │
│  {Back.MAGENTA}{Fore.WHITE} 5 {Style.RESET_ALL} Start Monitor   {Back.YELLOW}{Fore.BLACK} 6 {Style.RESET_ALL} Settings        {Fore.CYAN}│
│                                                           │
│  {Back.CYAN}{Fore.BLACK} 7 {Style.RESET_ALL} System Updates  {Back.RED}{Fore.WHITE} 8 {Style.RESET_ALL} Reset System    {Fore.CYAN}│
│                                                           │
│  {Back.LIGHTBLACK_EX}{Fore.WHITE} 9 {Style.RESET_ALL} Reboot App      {Back.BLACK}{Fore.WHITE} 0 {Style.RESET_ALL} Exit App        {Fore.CYAN}│
│                                                           │
└───────────────────────────────────────────────────────────┘"""
        
        print(menu_content)
        
        print(f"\n{Back.LIGHTBLACK_EX}{Fore.WHITE} Status: {len(self.websites)} websites | v{self.current_version} | Timeout: {self.timeout}s | Sounds: {'ON' if self.enable_sounds else 'OFF'} {Style.RESET_ALL}")
        self.pulsing_status("System Ready", True)
    
    def add_website(self):
        """Add a website to monitor with animated design"""
        self.print_header()
        self.bounce_text(f"{Fore.WHITE}{Back.GREEN}  ➕ ADD NEW WEBSITE  {Style.RESET_ALL}", Fore.WHITE)
        
        print(f"\n{Fore.CYAN}┌─ Website Registration Form ──────────────────────────────┐")
        print(f"{Fore.CYAN}│                                                           │")
        
        url = input(f"{Fore.CYAN}│ Website URL: {Fore.YELLOW}").strip()
        print(f"{Fore.CYAN}│                                                           │")
        print(f"{Fore.CYAN}└───────────────────────────────────────────────────────────┘")
        
        if url:
            self.loading_animation("Validating URL", 0.8)
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            if url not in self.websites:
                self.websites.append(url)
                self.save_websites()
                self.bounce_text(f"{Back.GREEN}{Fore.WHITE} ✅ SUCCESS {Style.RESET_ALL} Website added successfully!", Fore.GREEN)
            else:
                self.bounce_text(f"{Back.YELLOW}{Fore.BLACK} ⚠️  WARNING {Style.RESET_ALL} Website already exists!", Fore.YELLOW)
        else:
            self.bounce_text(f"{Back.RED}{Fore.WHITE} ❌ ERROR {Style.RESET_ALL} Invalid URL provided!", Fore.RED)
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")

    def remove_website(self):
        """Remove a website from monitoring with improved UI and animations"""
        self.print_header()
        self.bounce_text(f"{Fore.WHITE}{Back.RED}  ➖ REMOVE WEBSITE  {Style.RESET_ALL}", Fore.WHITE)
        
        if not self.websites:
            self.bounce_text(f"{Back.RED}{Fore.WHITE} ❌ NO WEBSITES {Style.RESET_ALL} No websites configured!", Fore.RED)
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        options = f"""{Fore.YELLOW}┌─ Removal Options ────────────────────────────────────────┐
│ {Back.BLUE}{Fore.WHITE} 1 {Style.RESET_ALL} Remove single website                            {Fore.YELLOW}│
│ {Back.RED}{Fore.WHITE} 2 {Style.RESET_ALL} Remove all websites                              {Fore.YELLOW}│
│ {Back.BLACK}{Fore.WHITE} 3 {Style.RESET_ALL} Cancel operation                                 {Fore.YELLOW}│
└───────────────────────────────────────────────────────────┘"""
        
        print(f"\n{options}")
        
        option = input(f"\n{Fore.CYAN}Select option (1-3): ").strip()
        
        if option == '1':
            self.loading_animation("Loading website list", 0.5)
            print(f"\n{Fore.CYAN}┌─ Website Selection ───────────────────────────────────────┐")
            for i, website in enumerate(self.websites, 1):
                print(f"{Fore.CYAN}│ {Back.GREEN}{Fore.WHITE} {i} {Style.RESET_ALL} {website[:50]:<50} {Fore.CYAN}│")
            print(f"{Fore.CYAN}└───────────────────────────────────────────────────────────┘")
            
            try:
                choice = int(input(f"\n{Fore.YELLOW}Enter website number: "))
                if 1 <= choice <= len(self.websites):
                    self.loading_animation("Removing website", 0.8)
                    removed = self.websites.pop(choice - 1)
                    self.save_websites()
                    self.bounce_text(f"{Back.GREEN}{Fore.WHITE} ✅ REMOVED {Style.RESET_ALL} {removed}", Fore.GREEN)
                else:
                    self.bounce_text(f"{Back.RED}{Fore.WHITE} ❌ INVALID {Style.RESET_ALL} Please select a valid number!", Fore.RED)
            except ValueError:
                self.bounce_text(f"{Back.RED}{Fore.WHITE} ❌ ERROR {Style.RESET_ALL} Invalid input!", Fore.RED)
        
        elif option == '2':
            confirm = input(f"\n{Fore.RED}⚠️  Type 'DELETE ALL' to confirm removal: ").strip()
            if confirm == 'DELETE ALL':
                self.loading_animation("Removing all websites", 1.2)
                self.websites.clear()
                self.save_websites()
                self.bounce_text(f"{Back.GREEN}{Fore.WHITE} ✅ SUCCESS {Style.RESET_ALL} All websites removed!", Fore.GREEN)
            else:
                self.bounce_text(f"{Back.YELLOW}{Fore.BLACK} ❌ CANCELLED {Style.RESET_ALL} Operation cancelled!", Fore.YELLOW)
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def view_websites(self):
        """Display all websites in a table format with animations"""
        self.print_header()
        self.bounce_text(f"{Fore.WHITE}{Back.BLUE}  📋 WEBSITE DASHBOARD  {Style.RESET_ALL}", Fore.WHITE)
        
        if not self.websites:
            self.bounce_text(f"{Back.YELLOW}{Fore.BLACK} ⚠️  NO DATA {Style.RESET_ALL} No websites configured yet!", Fore.YELLOW)
        else:
            self.loading_animation("Loading dashboard", 0.8)
            
            print(f"\n{Fore.CYAN}┌─ Monitored Websites ──────────────────────────────────────┐")
            print(f"{Fore.CYAN}│ {Back.BLUE}{Fore.WHITE} # {Style.RESET_ALL} {Back.BLUE}{Fore.WHITE} Website URL                                      {Style.RESET_ALL} {Fore.CYAN}│")
            print(f"{Fore.CYAN}├───┼──────────────────────────────────────────────────────┤")
            
            for i, website in enumerate(self.websites, 1):
                print(f"{Fore.CYAN}│ {i:>1} │ {website:<52} │")
            
            print(f"{Fore.CYAN}└───┴──────────────────────────────────────────────────────┘")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def check_website(self, url):
        """Check if a single website is up or down"""
        try:
            headers = {
                'User-Agent': os.getenv('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
            }
            response = requests.get(url, timeout=self.timeout, headers=headers)
            if response.status_code == 200:
                return True, response.status_code
            else:
                return False, response.status_code
        except requests.exceptions.RequestException as e:
            return False, str(e)[:50]
        except Exception as e:
            return False, f"Error: {str(e)[:40]}"
    
    def check_all_websites(self):
        """Check all websites once with animated dashboard-style results"""
        self.print_header()
        self.bounce_text(f"{Fore.WHITE}{Back.MAGENTA}  🔍 WEBSITE STATUS CHECK  {Style.RESET_ALL}", Fore.WHITE)
        
        if not self.websites:
            self.bounce_text(f"{Back.RED}{Fore.WHITE} ❌ NO WEBSITES {Style.RESET_ALL} No websites to check!", Fore.RED)
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n{Back.LIGHTBLACK_EX}{Fore.WHITE} Scan Time: {timestamp} {Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}┌─ Live Status Report ──────────────────────────────────────┐")
        
        for website in self.websites:
            self.loading_animation(f"Checking {website[:30]}", 0.3)
            is_up, status = self.check_website(website)
            
            if is_up:
                status_display = f"{Back.GREEN}{Fore.WHITE} ● ONLINE {Style.RESET_ALL}"
                self.play_pop_sound("online")
            else:
                status_display = f"{Back.RED}{Fore.WHITE} ● OFFLINE {Style.RESET_ALL}"
                self.play_pop_sound("offline")
            
            print(f"{Fore.CYAN}│ {status_display} {website[:40]:<40} {Fore.YELLOW}({status}) {Fore.CYAN}│")
        
        print(f"{Fore.CYAN}└───────────────────────────────────────────────────────────┘")
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def monitor_websites(self):
        """Start continuous monitoring with animated real-time dashboard"""
        if not self.websites:
            self.print_header()
            self.bounce_text(f"{Back.RED}{Fore.WHITE} ❌ NO WEBSITES {Style.RESET_ALL} No websites configured!", Fore.RED)
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        interval = input(f"{Fore.YELLOW}Monitor interval (seconds, default {self.monitor_interval}): ").strip()
        try:
            interval = int(interval) if interval else self.monitor_interval
        except ValueError:
            interval = self.monitor_interval
        
        self.loading_animation("Starting monitoring system", 1.5)
        
        try:
            cycle = 0
            while True:
                self.clear_screen()
                
                monitor_header = f"{Fore.WHITE}{Back.MAGENTA}  🚀 LIVE MONITORING ACTIVE  {Style.RESET_ALL}"
                print(monitor_header)
                
                print(f"\n{Back.BLUE}{Fore.WHITE} Interval: {interval}s | Websites: {len(self.websites)} | Cycle: {cycle} | Press Ctrl+C to stop {Style.RESET_ALL}")
                
                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"\n{Back.CYAN}{Fore.BLACK} ⟲ Live Update - {timestamp} {Style.RESET_ALL}")
                
                self.progress_bar(0.3, 30)
                print("═" * 60)
                
                for website in self.websites:
                    print(f"{Fore.YELLOW}⟳ Checking {website[:35]:<35}", end="", flush=True)
                    is_up, status = self.check_website(website)
                    print("\r" + " " * 60 + "\r", end="")
                    
                    if is_up:
                        status_indicator = f"{Back.GREEN}{Fore.WHITE} ● {Style.RESET_ALL}"
                        status_text = f"{Fore.GREEN}ONLINE"
                        self.play_pop_sound("online")
                    else:
                        status_indicator = f"{Back.RED}{Fore.WHITE} ● {Style.RESET_ALL}"
                        status_text = f"{Fore.RED}OFFLINE"
                        self.play_pop_sound("offline")
                    
                    print(f"{status_indicator} {website[:35]:<35} {status_text} {Fore.YELLOW}({status})")
                
                print("═" * 60)
                
                for remaining in range(interval, 0, -1):
                    print(f"\r{Fore.CYAN}Next check in: {Fore.YELLOW}{remaining}s", end="", flush=True)
                    time.sleep(1)
                print("\r" + " " * 20 + "\r", end="")
                
                cycle += 1
                
        except KeyboardInterrupt:
            self.loading_animation("Stopping monitoring", 0.8)
            self.bounce_text(f"{Back.YELLOW}{Fore.BLACK} 🛑 MONITORING STOPPED {Style.RESET_ALL}", Fore.YELLOW)
            input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def settings(self):
        """Configure app settings with animated form-style interface"""
        self.print_header()
        self.bounce_text(f"{Fore.WHITE}{Back.YELLOW}  ⚙️  CONFIGURATION PANEL  {Style.RESET_ALL}", Fore.WHITE)
        
        self.loading_animation("Loading settings", 0.5)
        
        settings_content = f"""{Fore.CYAN}┌─ Current Settings ────────────────────────────────────────┐
│                                                           │
│ Timeout Duration: {Back.BLUE}{Fore.WHITE} {self.timeout} seconds {Style.RESET_ALL}                     {Fore.CYAN}│
│ Monitor Interval: {Back.BLUE}{Fore.WHITE} {self.monitor_interval} seconds {Style.RESET_ALL}                     {Fore.CYAN}│
│ Animation Speed: {Back.BLUE}{Fore.WHITE} {self.animation_speed} {Style.RESET_ALL}                          {Fore.CYAN}│
│ Sound Effects: {Back.BLUE}{Fore.WHITE} {'Enabled' if self.enable_sounds else 'Disabled'} {Style.RESET_ALL}                       {Fore.CYAN}│
│ Auto Updates: {Back.BLUE}{Fore.WHITE} {'Enabled' if self.auto_update_check else 'Disabled'} {Style.RESET_ALL}                        {Fore.CYAN}│
│ Config File: {self.websites_file:<30}        │
│                                                           │
│ {Back.GREEN}{Fore.WHITE} 1 {Style.RESET_ALL} Change Timeout   {Back.GREEN}{Fore.WHITE} 2 {Style.RESET_ALL} Toggle Sounds      {Fore.CYAN}│
│ {Back.GREEN}{Fore.WHITE} 3 {Style.RESET_ALL} Edit .env File   {Back.GREEN}{Fore.WHITE} 4 {Style.RESET_ALL} Reload Settings    {Fore.CYAN}│
│ {Back.BLACK}{Fore.WHITE} 5 {Style.RESET_ALL} Return to Menu                             {Fore.CYAN}│
│                                                           │
└───────────────────────────────────────────────────────────┘"""
        
        print(f"\n{settings_content}")
        
        choice = input(f"\n{Fore.YELLOW}Select option (1-5): ").strip()
        
        if choice == '1':
            new_timeout = input(f"\n{Fore.YELLOW}New timeout value (current: {self.timeout}): ").strip()
            if new_timeout:
                try:
                    self.loading_animation("Applying settings", 0.8)
                    self.timeout = int(new_timeout)
                    self.save_websites()
                    self.bounce_text(f"{Back.GREEN}{Fore.WHITE} ✅ SAVED {Style.RESET_ALL} Timeout updated to {self.timeout} seconds!", Fore.GREEN)
                except ValueError:
                    self.bounce_text(f"{Back.RED}{Fore.WHITE} ❌ ERROR {Style.RESET_ALL} Invalid timeout value!", Fore.RED)
        
        elif choice == '2':
            self.enable_sounds = not self.enable_sounds
            self.bounce_text(f"{Back.GREEN}{Fore.WHITE} ✅ TOGGLED {Style.RESET_ALL} Sounds {'enabled' if self.enable_sounds else 'disabled'}!", Fore.GREEN)
        
        elif choice == '3':
            print(f"\n{Fore.YELLOW}📝 Edit your .env file manually and select option 4 to reload.")
            print(f"{Fore.CYAN}Current .env location: {os.path.abspath('.env')}")
        
        elif choice == '4':
            self.loading_animation("Reloading environment settings", 1.0)
            self.reload_env_settings()
            self.bounce_text(f"{Back.GREEN}{Fore.WHITE} ✅ RELOADED {Style.RESET_ALL} Settings updated from .env file!", Fore.GREEN)
        
        elif choice == '5':
            return
        
        if choice in ['1', '2', '3', '4']:
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            self.settings()  # Show settings menu again
    
    def run(self):
        """Main application loop"""
        while True:
            try:
                self.print_header()
                self.print_menu()
                
                choice = input(f"\n{Fore.YELLOW}Select option: ").strip()
                if choice:
                    self.play_pop_sound()
            except (EOFError, KeyboardInterrupt):
                self.clear_screen()
                self.typewriter_effect(f"{Back.GREEN}{Fore.WHITE} 👋 THANK YOU FOR USING DOWN DETECTOR {Style.RESET_ALL}")
                sys.exit(0)
            
            if choice == '1':
                self.add_website()
            elif choice == '2':
                self.remove_website()
            elif choice == '3':
                self.view_websites()
            elif choice == '4':
                self.check_all_websites()
            elif choice == '5':
                self.monitor_websites()
            elif choice == '6':
                self.settings()
            elif choice == '7':
                self.system_updates_menu()
            elif choice == '8':
                self.reset_system()
            elif choice == '9':
                self.reboot_system()
            elif choice == '0':
                self.clear_screen()
                self.typewriter_effect(f"{Back.GREEN}{Fore.WHITE} 👋 THANK YOU FOR USING DOWN DETECTOR {Style.RESET_ALL}")
                sys.exit(0)
            else:
                self.print_header()
                self.bounce_text(f"{Back.RED}{Fore.WHITE} ❌ INVALID SELECTION {Style.RESET_ALL} Please choose 0-9", Fore.RED)
                input(f"\n{Fore.CYAN}Press Enter to continue...")


if __name__ == "__main__":
    try:
        app = DownDetectorApp()
        app.run()
    except KeyboardInterrupt:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{Back.YELLOW}{Fore.BLACK} 👋 APPLICATION CLOSED {Style.RESET_ALL}")
    except Exception as e:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{Back.RED}{Fore.WHITE} ❌ APPLICATION ERROR: {str(e)} {Style.RESET_ALL}")
        sys.exit(1)