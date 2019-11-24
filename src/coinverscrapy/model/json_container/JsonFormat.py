from abc import ABC, abstractmethod


class JsonFormat(ABC):

    @abstractmethod
    def tojson(self): pass
