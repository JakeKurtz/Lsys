import bpy
from bpy.types import NodeTree, Node, NodeSocket, PropertyGroup
from bpy.props import CollectionProperty, StringProperty, BoolProperty, FloatProperty

class RulePropertyGroup(PropertyGroup):
    rule: StringProperty(
        name="",
        description="",
        default = "")
    valid: BoolProperty(default=False)

class VariablePropertyGroup(PropertyGroup):
    var: FloatProperty(
        name="",
        description="",
        default = 0.0)
    valid: BoolProperty(default=True)

class Lsys_OT_add_rule(bpy.types.Operator):
    bl_idname = "lsys.add_rule"
    bl_label = "Add Rule"

    node_name: bpy.props.StringProperty()

    def execute(self, context):
        node = context.active_node
        if node:
            node.select = False

        node_tree = context.space_data.node_tree
        node = node_tree.nodes[self.node_name]
        node.select = True
        node_tree.nodes.active = node

        if node and hasattr(node, "rules"):
            #node.inputs.new('LNodeSocketRule', f"Rule {len(node.inputs)}")
            #node.inputs.new('String', "")
            r = node.rules.add()
            v = node.vars.add()
            #r.name = str(uuid.uuid4())
            #self.inputs.new('LNodeSocketRule', f"Rule {len(self.inputs)}")

        return {'FINISHED'}

class Lsys_OT_del_rule(bpy.types.Operator):
    bl_idname = "lsys.del_rule"
    bl_label = "Delete Rule"

    node_name: bpy.props.StringProperty()
    index: bpy.props.IntProperty()

    def execute(self, context):
        node = context.active_node
        if node:
            node.select = False

        node_tree = context.space_data.node_tree
        node = node_tree.nodes[self.node_name]
        node.select = True
        node_tree.nodes.active = node

        if node and hasattr(node, "rules"):
            rules = node.rules
            if 0 <= self.index < len(rules):
                #node.lsys.del_rule(rules[self.index].name)
                rules.remove(self.index)
                node.vars.remove(self.index)

        return {'FINISHED'}

class LNodeLsystem(Node):
    bl_idname = 'LNodeLsystem'
    bl_label = "L-System Node"
    
    uuid: StringProperty(default="")

    rules: CollectionProperty(type=RulePropertyGroup)

    axiom: StringProperty(
        name="",
        description="",
        default = "")

    vars: CollectionProperty(type=VariablePropertyGroup)

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'LTree'

    def init(self, context):

        self.inputs.new('LNodeSocketMesh', "J")
        self.inputs.new('LNodeSocketMesh', "K")
        self.inputs.new('LNodeSocketMesh', "M")

        self.outputs.new('LNodeSocketLsystem', "L-System")

        self.uuid.set()

    def draw_buttons(self, context, layout):
        row = layout.row()
        #row.alert = (not self.axiom.valid)
        row.prop(self, "axiom", text="Axiom")

        layout.separator()
        add_op = layout.operator("lsys.add_rule", text="Add Rule", icon='ADD')
        add_op.node_name = self.name
        for i, rule in enumerate(self.rules):
            row = layout.row()
            
            row.alert = (not rule.valid)
            row.prop(rule, "rule", text=f"Rule {i}")

            del_op = row.operator("lsys.del_rule", text="", icon='CANCEL')
            del_op.node_name = self.name
            del_op.index = i

        layout.separator()

    def draw_buttons_ext(self, context, layout):
        for i, var in enumerate(self.vars):
            row = layout.row()
            #row.alert = (not rule.valid)
            row.prop(var, "var")


    '''
    def copy(self, node):
        print("Copying from node ", node)

    # Free function to clean up on removal.
    def free(self):
        print("Removing node ", self, ", Goodbye!")
        del self._lsys
    '''