from abc import abstractmethod


class IModuleProxy:

    @abstractmethod
    def execute(self): pass
