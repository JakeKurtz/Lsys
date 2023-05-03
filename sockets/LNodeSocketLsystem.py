import bpy
from bpy.types import NodeSocket

# Custom socket type
class LNodeSocketLsystem(NodeSocket):
    bl_idname = 'LNodeSocketLsystem'
    bl_label = "Custom Node Socket"

    #lsys: bpy.props.StringProperty(default="")

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        layout.label(text=text)

    # Socket color
    def draw_color(self, context, node):
        return (0.5960, 0.8078, 0.0, 1.0)