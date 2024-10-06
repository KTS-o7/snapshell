import subprocess
from .base_package_manager import BasePackageManager

class DpkgPackageManager(BasePackageManager):
    def get_installed_packages(self):
        # Get the list of installed packages
        installed_packages = subprocess.check_output(['dpkg', '-l']).decode('utf-8').splitlines()
        package_names = [line.split()[1] for line in installed_packages[5:] if len(line.split()) >= 3]
        
        # Get detailed information for all packages in one call
        package_info = subprocess.check_output(['dpkg-query', '-W', '-f=${Package} ${Version} ${Description} ${Depends}\n'] + package_names).decode('utf-8').splitlines()
        
        packages = []
        for line in package_info:
            parts = line.split(' ', 3)
            if len(parts) >= 4:
                name, version, description, depends_on = parts[0], parts[1], parts[2], parts[3]
                packages.append({
                    'name': name,
                    'version': version,
                    'description': description,
                    'depends_on': depends_on.split(', ') if depends_on else []
                })
        
        return packages
