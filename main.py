import numpy as np

from emsim.utils import particle
from emsim.calculation import management
from emsim.rendering import pipeline

if __name__ == '__main__':
    obj1 = particle.particle('a', (np.float_(1.0), np.float_(1.0), np.float_(0.0)), np.float_(0.0001), np.float_(-4000),
                             np.array([0, -0.03, 0.0], dtype=np.float_), np.array([50, 0.0, 0.0], dtype=np.float_),
                             False)
    obj2 = particle.particle('b', (np.float_(0.0), np.float_(0.0), np.float_(1.0)), np.float_(0.0001), np.float_(4000),
                             np.array([0.0, 0.03, 0], dtype=np.float_), np.array([-50, 0.0, 0.0], dtype=np.float_),
                             False)
    obj3 = particle.particle('b', (np.float_(0.0), np.float_(0.0), np.float_(1.0)), np.float_(0.0001), np.float_(3000),
                             np.array([0.1, 0.1, 0.00], dtype=np.float_), np.array([-60, 0.0, 0.0], dtype=np.float_),
                             False)
    obj4 = particle.particle('b', (np.float_(0.0), np.float_(0.0), np.float_(1.0)), np.float_(0.0001), np.float_(-4000),
                             np.array([0, 0.02, 0], dtype=np.float_), np.array([0, 0.0, 0.0], dtype=np.float_),
                             True)

    manager = management.manager('m', np.float_(0.0000001))
    manager.add_child(obj1)
    manager.add_child(obj2)

    pipe = pipeline.rendering_pipeline(manager, max_frame=20000, sample=500)
    pipe.init_display()
