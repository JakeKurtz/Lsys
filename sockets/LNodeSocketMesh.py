import bpy
from bpy.types import NodeSocket

# Custom socket type
class LNodeSocketMesh(NodeSocket):
    bl_idname = 'LNodeSocketMesh'
    bl_label = "Custom Node Socket"

    object: bpy.props.PointerProperty(type=bpy.types.Mesh)

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "object", text=text)
    
    # Socket color
    def draw_color(self, context, node):
        return (0.4235, 0.8117, 0.9647, 1.0)