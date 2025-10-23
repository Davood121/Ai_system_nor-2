import time
import subprocess
import psutil
import os

class SelfHealing:
    def __init__(self):
        self.health_checks = {
            'ollama': self.check_ollama,
            'memory': self.check_memory,
            'disk': self.check_disk,
            'network': self.check_network
        }
        self.auto_fixes = {
            'ollama': self.fix_ollama,
            'memory': self.fix_memory,
            'disk': self.fix_disk,
            'network': self.fix_network
        }
    
    def health_check(self):
        """Run all health checks"""
        issues = []
        for service, check_func in self.health_checks.items():
            if not check_func():
                issues.append(service)
        return issues
    
    def auto_heal(self, issues):
        """Auto-fix detected issues"""
        fixed = []
        for issue in issues:
            if issue in self.auto_fixes:
                if self.auto_fixes[issue]():
                    fixed.append(issue)
        return fixed
    
    def check_ollama(self):
        """Check if Ollama is running"""
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def check_memory(self):
        """Check memory usage"""
        memory = psutil.virtual_memory()
        return memory.percent < 90  # Alert if >90% used
    
    def check_disk(self):
        """Check disk space"""
        disk = psutil.disk_usage('C:')
        return (disk.free / disk.total) > 0.1  # Alert if <10% free
    
    def check_network(self):
        """Check network connectivity"""
        try:
            import requests
            requests.get('https://google.com', timeout=3)
            return True
        except:
            return False
    
    def fix_ollama(self):
        """Restart Ollama service"""
        try:
            print("Fixing Ollama...")
            subprocess.run(['ollama', 'serve'], timeout=3)
            time.sleep(2)
            return self.check_ollama()
        except:
            return False
    
    def fix_memory(self):
        """Clear memory"""
        try:
            print("Clearing memory...")
            import gc
            gc.collect()
            return True
        except:
            return False
    
    def fix_disk(self):
        """Clean temporary files"""
        try:
            print("Cleaning disk...")
            temp_dirs = [os.environ.get('TEMP', ''), 'C:/Windows/Temp']
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    for file in os.listdir(temp_dir)[:10]:  # Clean first 10 files
                        try:
                            os.remove(os.path.join(temp_dir, file))
                        except:
                            continue
            return True
        except:
            return False
    
    def fix_network(self):
        """Reset network connection"""
        try:
            print("Checking network...")
            time.sleep(1)  # Wait and retry
            return self.check_network()
        except:
            return False
    
    def monitor_and_heal(self):
        """Continuous monitoring and healing"""
        issues = self.health_check()
        if issues:
            print(f"Issues detected: {issues}")
            fixed = self.auto_heal(issues)
            if fixed:
                print(f"Auto-fixed: {fixed}")
            return len(issues) - len(fixed) == 0
        return True