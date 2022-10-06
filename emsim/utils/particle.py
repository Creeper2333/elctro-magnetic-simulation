import numpy as np


class particle(object):
    __name = str()
    __color = None
    __mass = np.float_()
    __charge = np.float_()
    __pos = np.zeros(3, dtype=np.float_)
    __v = np.zeros(3, dtype=np.float_)
    __a = np.zeros(3, dtype=np.float_)
    __f = np.zeros(3, dtype=np.float_)

    __is_static = bool()
    __parent = None
    __collider = None

    def __init__(self, name: str, color: tuple[np.float_, np.float_, np.float_], mass: np.float_, charge: np.float_,
                 pos: np.array, v: np.array, is_static: bool):
        self.__name = name
        self.__color = color
        self.__mass = mass if mass > 0 else np.float_(1.0)
        self.__charge = charge
        self.__pos = pos
        self.__v = v
        self.__is_static = is_static

    @property
    def name(self):
        return self.__name

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        self.__color = value

    @property
    def mass(self):
        return self.__mass

    @property
    def charge(self):
        return self.__charge

    @charge.setter
    def charge(self, value):
        self.__charge = value

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, value):
        self.__pos = value

    @property
    def v(self):
        return self.__pos

    @v.setter
    def v(self, value):
        self.__v = value

    @property
    def a(self):
        return self.__a

    @property
    def f(self):
        return self.__f

    @f.setter
    def f(self, value):
        self.__f = value

    @property
    def is_static(self):
        return self.__is_static

    @property
    def particle_manager(self):
        return self.__parent

    @particle_manager.setter
    def particle_manager(self, value):
        if self.__parent is None:
            self.__parent = value
        else:
            raise Exception("Object " + self.__name + " has already been binded to a parent!")

    def update(self, elapse_time: np.float_):
        self.__a = np.divide(self.__f, self.mass)
        self.__v = np.add(self.__v, np.multiply(self.__a, elapse_time))
        self.__pos = np.add(self.__pos, np.multiply(self.__v, elapse_time))

    def event_manager(self):
        pass
