from abc import ABC, abstractmethod

class BasePackageManager(ABC):
    @abstractmethod
    def get_installed_packages(self):
        pass