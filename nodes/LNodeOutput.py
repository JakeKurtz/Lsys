import bpy
from bpy.types import NodeTree, Node, NodeSocket, PropertyGroup
from bpy.props import CollectionProperty, StringProperty, BoolProperty

class LNodeOutput(Node):
    bl_idname = 'LNodeOutput'
    bl_label = "Output Node"

    def init(self, context):
        self.inputs.new('LNodeSocketMesh', "Mesh")