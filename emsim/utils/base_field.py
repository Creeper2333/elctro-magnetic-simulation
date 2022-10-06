import numpy as np

class field_type(object):
    NONE = 0
    MAGNETIC = 1
    ELECTRIC = 2

class base_field(object):
    __name = str()
    __type = field_type.NONE
    __strength = np.float_()
    __radius = np.float_()
    __direction = np.zeros(3, dtype=np.float_)

    def __init__(self, name: str, type: int, strength: np.float_, radius: np.float_, direction: np.array):
        self.__name = name
        self.__type = type
        self.__strength = strength
        self.__radius = radius if radius > 0 else np.float_(1.0)
        self.__direction = direction

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return self.__type

    @property
    def strength(self):
        return self.__strength

    @property
    def direction(self):
        return self.__direction
