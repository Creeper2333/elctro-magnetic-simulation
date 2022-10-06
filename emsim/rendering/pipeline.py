import numpy as np
import cv2
import imageio
import _thread
from copy import deepcopy

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from ..calculation.management import manager
from ..utils.particle import particle


class rendering_pipeline(object):
    __calculation_manager = None
    __tick = np.float_()
    __queue = []
    __max_queue_size = int()

    __elapse_time = np.float_()

    __win_w = 960
    __win_h = 540

    __frames = list()
    __max_frame = int()
    __current_frame = int()
    __sample = int()
    __generated = False

    __r = np.float_()

    def __init__(self, manager: manager, r=np.float_(0.1), max_frame=1000, sample=50):
        self.__calculation_manager = manager
        self.__tick = manager.tick
        self.__max_queue_size = int(1 / self.__tick) if self.__tick < 0.01 else 100
        self.__r = r
        self.__max_frame = max_frame
        self.__sample = sample

    def init_display(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
        glutInitWindowSize(self.__win_w, self.__win_h)
        glutCreateWindow("EM Simulation Display")
        self.reshape(self.__win_w, self.__win_h)
        glutReshapeFunc(self.reshape)
        glutDisplayFunc(self.update)
        glutIdleFunc(self.update)
        glutMainLoop()

    def reshape(self, w, h):
        R = self.__r
        if h <= 0: h = 1;
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if w <= h:
            gluOrtho2D(-R, R, -R * h / w, R * h / w)
        else:
            gluOrtho2D(-R * w / h, R * w / h, -R, R)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.__win_w = w
        self.__win_h = h

    def draw_particle(self, obj: particle):
        grid_color = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]

        glLineWidth(3)
        for i in range(3):
            origin = [0.0, 0.0, 0.0]
            tmp = [0.0, 0.0, 0.0]
            tmp[i] = 1
            origin[i] = -1
            glColor3f(*grid_color[i])
            glBegin(GL_LINES)
            glVertex3f(*origin)
            glVertex3f(*tmp)
            glEnd()

        glClearColor(1.0, 1.0, 1.0, 1.0)
        glColor3f(obj.color[0], obj.color[1], obj.color[2])
        glPointSize(3)
        glEnable(GL_POINT_SMOOTH)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBegin(GL_POINTS)
        glVertex3f(obj.pos[0], obj.pos[1], obj.pos[2])
        glVertex3f(obj.pos[0], obj.pos[1], obj.pos[2])
        glEnd()

    def cap_img(self):
        glReadBuffer(GL_FRONT)
        data = glReadPixels(0, 0, self.__win_w, self.__win_h, GL_RGB, GL_UNSIGNED_BYTE)
        out = np.zeros((self.__win_h * self.__win_w * 3), dtype=np.uint8)
        for i in range(0, len(data), 3):
            out[i] = data[i]
            out[i+1] = data[i+1]
            out[i+2] = data[i+2]
        out = np.reshape(out, (self.__win_h, self.__win_w, 3))
        out = cv2.flip(out, 0, out)
        out = cv2.putText(out, "time:  " + str(self.__elapse_time), (20, 20), cv2.FONT_ITALIC, 0.6, (255, 255, 255))
        out = cv2.putText(out, "frame: " + str(self.__current_frame), (20, 40), cv2.FONT_ITALIC, 0.6, (255, 255, 255))
        self.__frames.append(deepcopy(out))

    def update(self):
        self.__calculation_manager.update()
        for s in self.__calculation_manager.static:
            self.draw_particle(s)

        for c in self.__calculation_manager.children:
            self.draw_particle(c)

        self.__elapse_time += self.__tick

        if self.__current_frame <= self.__max_frame:
            if self.__current_frame % self.__sample == 0:
                self.cap_img()
        else:
            if not self.__generated:
                imageio.mimsave(self.__calculation_manager.name + ".gif", self.__frames, "GIF",
                                duration=self.__tick * self.__sample * 100)
                print('saved')
                self.__generated = True
        self.__current_frame += 1
        glutSwapBuffers()

