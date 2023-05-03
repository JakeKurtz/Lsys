bl_info = {
    "name": "Lsys",
    "description": "",
    "author": "Jake Kurtz",
    'license': 'GPL-3.0-only',
    "version": (1, 0, 0),
    "blender": (3, 5, 0),
    'location': '',
    "doc_url": "",
    "category": ""
}

import bpy
from multiprocessing import freeze_support
import uuid

from .LAxiom import LAxiom
from .LRule import LRule
from .LSystem import Lsystem
from .LTurtle import LTurtle
#from .nodes.LNodeTree import *

from .nodes import (
    RulePropertyGroup, VariablePropertyGroup, Lsys_OT_add_rule, Lsys_OT_del_rule, LNodeLsystem,
    LNodeOutput,
    LNodeToMesh
    )

from .sockets import (
    LNodeSocketLsystem,
    LNodeSocketNumber,
    LNodeSocketMesh
)

from .tree import LNodeTree

class Lsys_OT_test (bpy.types.Operator):
    bl_idname = "lsys.test_op"
    bl_label = "Lsys Test"

    def execute(self, context):
        
        lsys = Lsystem()

        lsys.set_axiom(LAxiom("FFFA"))
        lsys.add_rule(uuid.uuid4(), LRule("A= \"(0.6) [B] //// [B] //// [B]"))
        lsys.add_rule(uuid.uuid4(), LRule("B= &FFFA"))

        lsys.generate()

        frank = LTurtle()
        frank.run(lsys.command_list)

        mesh = bpy.data.meshes.new("Lsys Test Mesh")
        obj = bpy.data.objects.new(mesh.name, mesh)
        col = bpy.data.collections["Collection"]
        col.objects.link(obj)

        bpy.context.view_layer.objects.active = obj
        mesh.from_pydata(frank.verts, frank.edges, [])

        return {'FINISHED'}

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

# our own base class with an appropriate poll function,
# so the categories only show up in our own tree type

class MyNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'LTree'

# all categories in a list
node_categories = [
    # identifier, label, items list
    MyNodeCategory('Lsystem Nodes', "Some Nodes", items=[
        # our basic node
        NodeItem("LNodeLsystem"),
        NodeItem("LNodeOutput"),
        NodeItem("LNodeToMesh"),
    ]),
]

classes = (
    LNodeTree,
    Lsys_OT_test,
    LNodeSocketLsystem,
    LNodeSocketNumber,
    LNodeSocketMesh,
    RulePropertyGroup, VariablePropertyGroup, Lsys_OT_add_rule, Lsys_OT_del_rule, LNodeLsystem,
    LNodeOutput,
    LNodeToMesh
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    nodeitems_utils.register_node_categories('CUSTOM_NODES', node_categories)

def unregister():
    nodeitems_utils.unregister_node_categories('CUSTOM_NODES')

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()