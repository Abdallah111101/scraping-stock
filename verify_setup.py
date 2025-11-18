#!/usr/bin/env python3
"""
Verification script to test the application setup locally
Run this before deployment to ensure everything is configured correctly
"""

import os
import sys
import json
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def check(condition, message):
    """Print check result"""
    status = f"{Colors.GREEN}✓{Colors.END}" if condition else f"{Colors.RED}✗{Colors.END}"
    print(f"{status} {message}")
    return condition

def main():
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}EGX Stock Scraper - Pre-Deployment Verification{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    all_passed = True
    
    # Check 1: Python Version
    print(f"{Colors.YELLOW}[1] Python Version{Colors.END}")
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    all_passed &= check(
        sys.version_info >= (3, 9),
        f"Python 3.9+ ({py_version})"
    )
    
    # Check 2: Required Files
    print(f"\n{Colors.YELLOW}[2] Required Files{Colors.END}")
    required_files = {
        'main.py': 'FastAPI application',
        'scraper.py': 'Selenium scraper',
        'Dockerfile': 'Docker container',
        'docker-compose.yml': 'Docker orchestration',
        'requirements.txt': 'Python dependencies',
        'README.md': 'Documentation',
    }
    
    for filename, description in required_files.items():
        exists = Path(filename).exists()
        all_passed &= check(exists, f"{filename} ({description})")
    
    # Check 3: Python Dependencies
    print(f"\n{Colors.YELLOW}[3] Python Dependencies{Colors.END}")
    required_packages = [
        'fastapi',
        'uvicorn',
        'selenium',
        'pandas',
        'openpyxl',
        'apscheduler',
    ]
    
    try:
        import pip
        installed_packages = {pkg.key for pkg in pip.get_installed_distributions()}
    except:
        # Fallback method
        import pkg_resources
        installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    
    for package in required_packages:
        installed = package.lower() in installed_packages
        all_passed &= check(installed, f"Package '{package}'")
    
    # Check 4: Directory Structure
    print(f"\n{Colors.YELLOW}[4] Directory Structure{Colors.END}")
    data_dir = Path('data')
    all_passed &= check(data_dir.exists(), "data/ directory exists")
    
    if data_dir.exists():
        all_passed &= check(
            os.access(data_dir, os.W_OK),
            "data/ directory is writable"
        )
    
    # Check 5: Configuration Files
    print(f"\n{Colors.YELLOW}[5] Configuration Files{Colors.END}")
    
    # Check docker-compose.yml syntax
    try:
        with open('docker-compose.yml', 'r') as f:
            import yaml
            yaml.safe_load(f)
        all_passed &= check(True, "docker-compose.yml is valid YAML")
    except Exception as e:
        all_passed &= check(False, f"docker-compose.yml: {str(e)}")
    
    # Check requirements.txt syntax
    try:
        with open('requirements.txt', 'r') as f:
            lines = f.readlines()
            # Check format: package==version
            valid_format = all(
                '==' in line or line.strip().startswith('#') or line.strip() == ''
                for line in lines
            )
        all_passed &= check(valid_format, "requirements.txt format is correct")
    except Exception as e:
        all_passed &= check(False, f"requirements.txt: {str(e)}")
    
    # Check 6: Environment Setup
    print(f"\n{Colors.YELLOW}[6] Environment Setup{Colors.END}")
    
    env_file = Path('.env.example')
    all_passed &= check(env_file.exists(), ".env.example exists")
    
    # Check 7: Docker & Docker Compose
    print(f"\n{Colors.YELLOW}[7] Docker Setup{Colors.End}")
    
    try:
        import subprocess
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        docker_installed = result.returncode == 0
        all_passed &= check(docker_installed, f"Docker installed: {result.stdout.strip()}")
    except:
        all_passed &= check(False, "Docker not found in PATH")
    
    try:
        result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
        compose_installed = result.returncode == 0
        all_passed &= check(compose_installed, f"Docker Compose installed: {result.stdout.strip()}")
    except:
        all_passed &= check(False, "Docker Compose not found in PATH")
    
    # Check 8: Port Availability
    print(f"\n{Colors.YELLOW}[8] Port Availability{Colors.END}")
    
    try:
        import socket
        
        def is_port_available(port):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            return result != 0
        
        ports = {
            8000: 'FastAPI app',
            4444: 'Selenium Hub',
        }
        
        for port, service in ports.items():
            available = is_port_available(port)
            all_passed &= check(available, f"Port {port} available ({service})")
    except Exception as e:
        print(f"{Colors.YELLOW}  Warning: Could not check port availability: {e}{Colors.END}")
    
    # Check 9: File Permissions
    print(f"\n{Colors.YELLOW}[9] File Permissions{Colors.END}")
    
    scripts = ['main.py', 'scraper.py']
    for script in scripts:
        if Path(script).exists():
            readable = os.access(script, os.R_OK)
            all_passed &= check(readable, f"{script} is readable")
    
    # Check 10: Git Configuration
    print(f"\n{Colors.YELLOW}[10] Git Configuration{Colors.END}")
    
    git_dir = Path('.git')
    all_passed &= check(git_dir.exists(), "Git repository initialized")
    
    gitignore_file = Path('.gitignore')
    all_passed &= check(gitignore_file.exists(), ".gitignore file exists")
    
    # Summary
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    
    if all_passed:
        print(f"{Colors.GREEN}{'='*60}{Colors.END}")
        print(f"{Colors.GREEN}✓ All checks passed!{Colors.END}")
        print(f"{Colors.GREEN}{'='*60}{Colors.END}")
        print(f"\n{Colors.BLUE}Next Steps:{Colors.END}")
        print(f"1. Test locally: {Colors.YELLOW}docker-compose up -d{Colors.END}")
        print(f"2. Access: {Colors.YELLOW}http://localhost:8000{Colors.END}")
        print(f"3. Check status: {Colors.YELLOW}docker-compose ps{Colors.END}")
        print(f"4. View logs: {Colors.YELLOW}docker-compose logs -f{Colors.END}")
        print(f"5. Deploy to Railway: Push code to GitHub and deploy\n")
        return 0
    else:
        print(f"{Colors.RED}{'='*60}{Colors.END}")
        print(f"{Colors.RED}✗ Some checks failed!{Colors.END}")
        print(f"{Colors.RED}{'='*60}{Colors.END}")
        print(f"\n{Colors.YELLOW}Please fix the issues above before deploying.{Colors.END}\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
