import bpy
from bpy.types import NodeTree, Node, NodeSocket, PropertyGroup
from bpy.props import CollectionProperty, StringProperty, BoolProperty

class LNodeToMesh(Node):
    bl_idname = 'LNodeToMesh'
    bl_label = "To Mesh"

    my_items = (
        ('SKIN', "Skin", "Skin mesh"),
        ('TUBE', "Tube", "Tube Mesh"),
        ('WIRE', "Wire", "Wire Mesh")
    )

    my_enum_prop: bpy.props.EnumProperty(
        name="Type",
        description="Mesh Type",
        items=my_items,
        default='WIRE',
    )

    def init(self, context):
        self.inputs.new('LNodeSocketLsystem', "L-System")
        self.outputs.new('LNodeSocketMesh', "Mesh")

    def draw_buttons(self, context, layout):
        layout.prop(self, "my_enum_prop")