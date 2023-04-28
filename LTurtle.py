###############################
#                    __       #
#         .,-;-;-,. /'_\      #
#       _/_/_/_|_\_\) /       #
#     '-<_><_><_><_>=/\       #
#       `/_/====/_/-'\_\      #
#        ""     ""    ""      #
###############################

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

    def execute_op(self, module):
        match module.symbol:
            # F(l,w,s,d)
            # Move forward (creating geometry) distance l of width w using s cross sections of d divisions each.
            case 'F':
                pass

            # H(l,w,s,d)
            # Move forward half the length (creating geometry) distance l of width w using s cross sections of d divisions each.
            case 'H':
                pass

            # G(l,w,s,d)
            # Move forward but don’t record a vertex distance l of width w using s cross sections of d divisions each.
            case 'G':
                pass
            
            # J(s,x,a,b,c), K(s,x,a,b,c), M(s,x,a,b,c) 
            # Copy geometry from leaf input J, K, or M at the turtle’s position after scaling and reorienting the geometry. 
            # The geometry is scaled by the s parameter (default Step Size) and stamped with the values a 
            # through c (default no stamping). Stamping occurs if the given parameter is present and the
            # relevant Leaf parameter is set. The x parameter is not used and should be set to 0.
            # Note that point vector attributes in the leaf inputs will be affected by the turtle movements. 
            case 'J':
                pass
            case 'K':
                pass
            case 'M':
                pass

            # T(g)
            # apply tropism vector (gravity). This angles the turtle towards the negative Y axis. 
            # The amount of change is governed by g. The default change is to use the Gravity parameter.
            case 'T':
                pass

            # f(l,w,s,d)
            # Move forward (no geometry created) distance l of width w using s cross sections of d divisions each.
            case 'f':
                pass

            # h(l,w,s,d)
            # Move forward a half length (no geometry created) distance l of width w using s cross sections of d divisions each.
            case 'h':
                pass
            
            # g(i)
            # Create a new primitive group to which subsequent geometry is added. The group name is the Group Prefix followed by the number i. 
            # The default if no parameter is given is to create a group with the current group number and then increment the current group number.
            case 'g':
                pass

            # a(attrib, v1, v2, v3)
            # This creates a point attribute of the name attrib. It is then set to the value v1, v2, v3 for the remainder of the points on this branch, 
            # or until another a command resets it. v2 and v3 are optional. If they are not present, an attribute of fewer floats will be created. The 
            # created attribute is always of float type and with zero defaults. For example, the rule a("Cd", 1, 0, 1) added to the start of the 
            # premise will make the L-system a nice pugnacious purple.
            case 'a':
                pass

            # +(a)
            # Turn right a degrees. Default Angle.
            case '+':
                pass

            # -(a)
            # Turn left a degrees (minus sign). Default Angle.
            case '-':
                pass

            # &(a)
            # Pitch down a degrees. Default Angle.
            case '&':
                pass

            # ^(a)
            # Pitch up a degrees. Default Angle.
            case '^':
                pass

            # \\(a)
            # Roll clockwise a degrees. Default Angle.
            case '\\':
                pass

            # /(a)
            # Roll counter-clockwise a degrees. Default Angle.
            case '/':
                pass

            # |
            # Turn 180 degrees
            case '|':
                pass

            # *
            # Roll 180 degrees
            case '*':
                pass

            # ~(a)
            # Pitch / Roll / Turn random amount up to a degrees. Default 180.
            case '~':
                pass

            # "(s)
            # Multiply current length by s. Default Step Size Scale.
            case '\"':
                pass

            # !(s)
            # Multiply current thickness by s. Default Thickness Scale.
            case '!':
                pass

            # ;(s)
            # Multiply current angle by s. Default Angle Scale.
            case ';':
                pass
            
            # _(s)
            # Divide current length (underscore) by s. Default Step Size Scale.
            case '_':
                pass
            
            # ?(s)
            # Divides current width by s. Default Thickness Scale.
            case '?':
                pass
            
            # @(s)
            # Divide current angle by s. Default Angle Scale.
            case '@':
                pass
            
            # '(u)
            # Increment color index U by u. Default UV Increment's first parameter.
            case '\'':
                pass
            
            # #(v)
            # Increment color index V by v. Default UV Increment's second parameter.
            case '#':
                pass
            
            # %
            # Cut off remainder of branch
            case '%':
                pass
            
            # $(x,y,z)
            # Rotates the turtle so the up vector is (0,1,0). Points the turtle in the direction of the point (x,y,z). Default behavior is only to orient 
            # and not to change the direction.
            case '$':
                pass
            
            # [
            # Push turtle state (start a branch)
            case '[':
                pass
            
            # ]
            # Pop turtle state (end a branch)
            case ']':
                pass
            
            # {
            # Start a polygon
            case '{':
                pass

            # }
            # End a polygon
            case '}':
                pass
            # .
            # Make a polygon vertex
            case '.':
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