from abc import abstractmethod


class ModuleTemplate:

    @abstractmethod
    def initialize(self): pass

    @abstractmethod
    def run(self): pass

    @abstractmethod
    def finalize(self): pass

    def start(self):
        self.initialize()
        self.run()
        self.finalize()
