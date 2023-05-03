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
from math import radians

@dataclass
class TurtleState:
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

        self.state = TurtleState()

        self.state.pos = pos
        self.state.dir = dir
        self.state.angle = self.__default_angle
        self.state.step_size = self.__default_step_size
        self.state.thickness = self.__default_thickness

        self.update_orientation(Matrix())

    def set_default_state(self):
        pass

    def run(self, command_list):
        for command in command_list:
            self.execute(command)

    def execute(self, command):
        s = command.symbol
        p = command.parameters

        match s:
            # F(l,w,s,d)
            # Move forward (creating geometry) distance l of width w using s cross sections of d divisions each.
            case 'F':
                if len(p) > 0:
                    self.F(p[0])
                else:
                    self.F(self.__default_step_size)

            # H(l,w,s,d)
            # Move forward half the length (creating geometry) distance l of width w using s cross sections of d divisions each.
            case 'H':
                if len(p) > 0:
                    self.F(p[0] * 0.5)
                else:
                    self.F(self.__default_step_size * 0.5)

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
                if len(p) > 0:
                    self.f(p[0])
                else:
                    self.f(self.__default_step_size)

            # h(l,w,s,d)
            # Move forward a half length (no geometry created) distance l of width w using s cross sections of d divisions each.
            case 'h':
                if len(p) > 0:
                    self.f(p[0] * 0.5)
                else:
                    self.f(self.__default_step_size * 0.5)
            
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
                if len(p) > 0:
                    self.apply_yaw(p[0])
                else:
                    self.apply_yaw(self.state.angle)

            # -(a)
            # Turn left a degrees (minus sign). Default Angle.
            case '-':
                if len(p) > 0:
                    self.apply_yaw(-p[0])
                else:
                    self.apply_yaw(-self.state.angle)

            # &(a)
            # Pitch down a degrees. Default Angle.
            case '&':
                if len(p) > 0:
                    self.apply_pitch(p[0])
                else:
                    self.apply_pitch(self.state.angle)

            # ^(a)
            # Pitch up a degrees. Default Angle.
            case '^':
                if len(p) > 0:
                    self.apply_pitch(-p[0])
                else:
                    self.apply_pitch(-self.state.angle)

            # \\(a)
            # Roll clockwise a degrees. Default Angle.
            case '\\':
                if len(p) > 0:
                    self.apply_roll(p[0])
                else:
                    self.apply_roll(self.state.angle)

            # /(a)
            # Roll counter-clockwise a degrees. Default Angle.
            case '/':
                if len(p) > 0:
                    self.apply_roll(-p[0])
                else:
                    self.apply_roll(-self.state.angle)

            # |
            # Turn 180 degrees
            case '|':
                self.apply_yaw(180)

            # *
            # Roll 180 degrees
            case '*':
                self.apply_roll(180)

            # ~(a)
            # Pitch / Roll / Turn random amount up to a degrees. Default 180.
            case '~':
                pass

            # "(s)
            # Multiply current length by s. Default Step Size Scale.
            case '\"':
                if len(p) > 0:
                    self.state.step_size *= p[0]
                else:
                    self.state.step_size *= self.__default_step_size_scale

            # !(s)
            # Multiply current thickness by s. Default Thickness Scale.
            case '!':
                if len(p) > 0:
                    self.state.thickness *= p[0]
                else:
                    self.state.thickness *= self.__default_thickness_scale

            # ;(s)
            # Multiply current angle by s. Default Angle Scale.
            case ';':
                if len(p) > 0:
                    self.state.angle *= p[0]
                else:
                    self.state.angle *= self.__default_angle_scale
            
            # _(s)
            # Divide current length (underscore) by s. Default Step Size Scale.
            case '_':
                if len(p) > 0:
                    self.state.step_size /= p[0]
                else:
                    self.state.step_size /= self.__default_step_size_scale
            
            # ?(s)
            # Divides current width by s. Default Thickness Scale.
            case '?':
                pass
            
            # @(s)
            # Divide current angle by s. Default Angle Scale.
            case '@':
                if len(p) > 0:
                    self.state.angle /= p[0]
                else:
                    self.state.angle /= self.__default_angle_scale
            
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
                self.update_orientation(Matrix())
            
            # [
            # Push turtle state (start a branch)
            case '[':
                self.push_state()
            
            # ]
            # Pop turtle state (end a branch)
            case ']':
                self.pop_state()
            
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
    
    def F(self, l):

        if (len(self.verts) == 0):
            self.verts.append(self.state.pos)

        vertex_index = self.state.vertex_index

        # Translate turtle
        self.state.pos = (l * self.state.step_size) * self.state.dir + self.state.pos

        # Push new vertex position to the vertex list
        self.verts.append(self.state.pos)

        self.state.vertex_index = len(self.verts)-1

        # New Edge
        start = vertex_index
        end = self.state.vertex_index
        self.edges.append([start, end])

    def f(self, l):
        # Translate turtle
        self.state.pos = (l * self.state.step_size) * self.state.dir + self.state.pos

        self.verts.append(self.state.pos)
        self.state.vertex_index = len(self.verts)-1

    def apply_yaw(self, angle):
        self.apply_rotation(Matrix.Rotation(radians(angle), 4, self.state.up))
    
    def apply_pitch(self, angle):
        self.apply_rotation(Matrix.Rotation(radians(angle), 4, self.state.right))
    
    def apply_roll(self, angle):
        self.apply_rotation(Matrix.Rotation(radians(angle), 4, self.state.dir))

    def push_state(self):
        self.state_stack.append(self.state.copy())

    def pop_state(self):
        if len(self.state_stack) != 0:
            self.state = self.state_stack.pop()
        else:
            print("Turtle Error: tried to pop an empty stack! Ensure the brackets \'[\' and \']\' are balanced in the replacement string.")
        
    def apply_rotation(self, rot_mat):
        self.state.dir = Vector.normalized((rot_mat @ self.state.dir.to_4d()).to_3d())
        self.state.right =  Vector.normalized((rot_mat @ self.state.right.to_4d()).to_3d())
        self.state.up =  Vector.normalized((rot_mat @ self.state.up.to_4d()).to_3d())

    def update_orientation(self, rot_mat):
        self.state.dir = Vector.normalized(rot_mat @ self.state.dir.to_4d()).to_3d()
        self.state.right =  Vector.normalized(Vector.cross(self.state.dir, self.__world_up))
        self.state.up =  Vector.normalized(Vector.cross(self.state.right, self.state.dir))

    __world_up = Vector((0.0, 0.0, 1.0))

    __state = []
    __current_state = None

    __default_thickness = 0.1
    __default_thickness_scale = 0.5
    
    __default_step_size = 1.0
    __default_step_size_scale = 0.5

    __default_angle = 28.0
    __default_angle_scale = 1.0

    verts = []
    edges = []

    state_stack = []
    state = None

'''
lsys = Lsystem()

lsys.set_axiom(LAxiom("X"))
lsys.add_rule(LRule("X=F[-X][+X]"))

lsys.generate()

frank = LTurtle()
frank.run(lsys.command_list)
'''