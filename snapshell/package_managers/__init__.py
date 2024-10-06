import subprocess
from .base_package_manager import BasePackageManager
from .dpkg_package_manager import DpkgPackageManager
from .apt_package_manager import AptPackageManager
from .pacman_package_manager import PacmanPackageManager
from .pamac_package_manager import PamacPackageManager

def detect_package_manager():
    try:
        subprocess.check_output(['dpkg', '--version'])
        return DpkgPackageManager()
    except FileNotFoundError:
        pass

    try:
        subprocess.check_output(['apt', '--version'])
        return AptPackageManager()
    except FileNotFoundError:
        pass

    try:
        subprocess.check_output(['pacman', '--version'])
        return PacmanPackageManager()
    except FileNotFoundError:
        pass

    try:
        subprocess.check_output(['pamac', '--version'])
        return PamacPackageManager()
    except FileNotFoundError:
        pass

    raise Exception("No supported package manager found")