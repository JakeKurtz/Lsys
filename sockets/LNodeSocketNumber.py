import bpy
from bpy.types import NodeSocket

# Custom socket type
class LNodeSocketNumber(NodeSocket):
    bl_idname = 'LNodeSocketNumber'
    bl_label = "Custom Node Socket"

    value: bpy.props.FloatProperty(default=1.0)

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)