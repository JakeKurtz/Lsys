from bpy.types import NodeTree, Node, NodeSocket, PropertyGroup

class LNodeTree(NodeTree):
    bl_idname = 'LTree'
    bl_label = "L-System Node Editor"
    bl_icon = 'NODETREE'