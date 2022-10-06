import numpy as np
import math
import copy
from ..utils.particle import particle

K = np.float_(np.multiply(np.float_(9.0), np.float_(10 ** -9)))


class manager(object):
    __name = str()
    __children = list()
    __static = list()
    __tick = np.float_()

    def __init__(self, name, tick: np.float_):
        self.__name = name
        self.__tick = tick

    @property
    def name(self):
        return self.__name

    @property
    def tick(self):
        return self.__tick

    @property
    def children(self):
        return self.__children

    @property
    def static(self):
        return self.__static

    def add_child(self, c: particle):
        child = copy.deepcopy(c)
        child.particle_manager = self
        if child.is_static:
            self.__static.append(child)
        else:
            self.__children.append(child)

    def add_children(self, children: list[particle]):
        for ch in children:
            c = copy.deepcopy(ch)
            c.particle_manager = self
            if c.is_static:
                self.__static.append(c)
            else:
                self.__children.append(c)
            c.particle_manager = self

    def update(self):
        for c in self.__children:
            force = np.zeros(3)
            for s in self.__static:
                vec = np.subtract(c.pos, s.pos) \
                    if c.charge * s.charge > 0 else np.subtract(s.pos, c.pos)
                vec_len_square = np.sum(np.square(vec))
                vec_len = np.sqrt(vec_len_square) if c.charge * s.charge > 0 \
                    else np.multiply(np.sqrt(vec_len_square), -1.0)

                # F = KQ1Q2/r^2
                F = np.divide(
                    np.multiply(np.multiply(c.charge, s.charge), K),
                    vec_len_square
                )

                deg_xz_y = math.asin(vec[1] / vec_len)  # 连线和 x-z 平面夹角
                projectile_y_xz = np.multiply(math.cos(deg_xz_y), vec_len)  # 投影长
                deg_projectile_x = math.asin(
                    vec[0] / projectile_y_xz if abs(vec[0] / projectile_y_xz) <= 1 else 1.0)  # 投影和 x 夹角

                fy = np.multiply(F, math.sin(deg_xz_y))
                fp = np.multiply(F, math.cos(deg_xz_y))
                fx = np.multiply(fp, math.sin(deg_projectile_x))
                fz = np.multiply(fp, math.cos(deg_projectile_x))

                force = np.add(force, np.array([fx, fy, fz], dtype=np.float_))

            for s in self.__children:
                if s is not c:
                    vec = np.subtract(c.pos, s.pos) \
                        if c.charge * s.charge > 0 else np.subtract(s.pos, c.pos)
                    vec_len_square = np.sum(np.square(vec))
                    vec_len = np.sqrt(vec_len_square) if c.charge * s.charge > 0 \
                        else np.multiply(np.sqrt(vec_len_square), -1.0)

                    # F = KQ1Q2/r^2
                    F = np.divide(
                        np.multiply(np.multiply(c.charge, s.charge), K),
                        vec_len_square
                    )

                    deg_xz_y = math.asin(vec[1] / vec_len)  # 连线和 x-z 平面夹角
                    projectile_y_xz = np.multiply(math.cos(deg_xz_y), vec_len)  # 投影长
                    deg_projectile_x = math.asin(
                        vec[0] / projectile_y_xz if abs(vec[0] / projectile_y_xz) <= 1 else 1.0)  # 投影和 x 夹角

                    fy = np.multiply(F, math.sin(deg_xz_y))
                    fp = np.multiply(F, math.cos(deg_xz_y))
                    fx = np.multiply(fp, math.sin(deg_projectile_x))
                    fz = np.multiply(fp, math.cos(deg_projectile_x))

                    force = np.add(force, np.array([fx, fy, fz], dtype=np.float_))
            c.f = force
            c.update(self.__tick)
