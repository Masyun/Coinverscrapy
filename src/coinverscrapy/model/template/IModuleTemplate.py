class IModuleTemplate:
    def initialize(self): pass
    def run(self): pass
    def finalize(self): pass

    def start(self):
        self.initialize()
        self.run()
        self.finalize()
