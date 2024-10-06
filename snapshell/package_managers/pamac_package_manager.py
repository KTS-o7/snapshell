import subprocess
from .base_package_manager import BasePackageManager

class PamacPackageManager(BasePackageManager):
    def get_installed_packages(self):
        # Get the list of installed packages
        installed_packages = subprocess.check_output(['pamac', 'list', '--installed']).decode('utf-8').splitlines()
        package_names = [line.split()[0] for line in installed_packages[1:]]  # Skip headers
        
        # Get detailed information for all packages in one call
        package_info = subprocess.check_output(['pamac', 'info'] + package_names).decode('utf-8').splitlines()
        
        packages = []
        current_package = {}
        for line in package_info:
            if line.startswith('Name'):
                if current_package:
                    packages.append(current_package)
                current_package = {'name': line.split(':', 1)[1].strip()}
            elif line.startswith('Version'):
                current_package['version'] = line.split(':', 1)[1].strip()
            elif line.startswith('Description'):
                current_package['description'] = line.split(':', 1)[1].strip()
            elif line.startswith('Depends On'):
                depends_on = line.split(':', 1)[1].strip()
                current_package['depends_on'] = depends_on.split() if depends_on != 'None' else []
        
        if current_package:
            packages.append(current_package)
        
        return packages