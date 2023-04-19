import copy
from dataclasses import dataclass
from mathutils import Vector, Matrix

@dataclass
class TurtleVertex:
    dir = Vector((0, 0, 0))
    right = Vector((0, 0, 0))
    up = Vector((0, 0, 0))
    pos = Vector((0, 0, 0))
    step_size = 0.0
    thickness = 0.0
    angle = 0.0
    vertex_index = 0

    def copy(self):
        return copy.deepcopy(self)

class LTurtle:

    def __init__(self, pos = Vector((0, 0, 0)), dir = Vector((0, 1, 0))):
        pass

    def set_default_state(self):
        pass

    def build_curve(self):
        pass
    def execute_op(self, symbol, parameters):
        pass

    def F(self, len):
        pass
    def f(self, len):
        pass

    def apply_yaw(self, angle):
        pass
    def apply_pitch(self, angle):
        pass
    def apply_roll(self, angle):
        pass

    def push_state(self):
        pass
    def pop_state(self):
        pass

    __pos = None
    __dir = None

    __look_at = Matrix()
    __up = None
    __right = None
    __world_up = Vector((0.0, 0.0, 1.0))

    __state = []
    __current_state = None

    #std::string cmd_str = "";

    __thickness = 0.1
    __thickness_scale = 0.5
    
    __step_size = 1.0
    __step_size_scale = 0.5

    __angle = 28.0