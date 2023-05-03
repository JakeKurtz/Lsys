import bpy
from bpy.types import NodeTree, Node, NodeSocket, PropertyGroup
from bpy.props import CollectionProperty, StringProperty, BoolProperty

import uuid

from ..LAxiom import LAxiom
from ..LRule import LRule
from ..LSystem import Lsystem

'''
def update_rule(self, context):
    node = context.active_node
    if node and hasattr(node, "_lsys"):
        if self.rule.strip():
            node.lsys.add_rule(self.name, LRule(self.rule))

def update_axiom(self, context):
    node = context.active_node
    if node and hasattr(node, "_lsys"):
        node.lsys.set_axiom(LAxiom(self.axiom))
'''

class LRulesProperty(PropertyGroup):
    rule: StringProperty(
        name="",
        description="",
        default = "")
    valid: BoolProperty()

class LTree(NodeTree):
    '''Description'''
    bl_idname = 'LTree'
    bl_label = "L-System Node Editor"
    bl_icon = 'NODETREE'

class LSocket(NodeSocket):
    '''Description'''
    bl_idname = 'LSocket'
    bl_label = "L-System Node Socket"

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)

class Lsys_OT_add_rule(bpy.types.Operator):
    bl_idname = "lsys.add_rule"
    bl_label = "Add Rule"

    def execute(self, context):
        node = context.active_node
        if node and hasattr(node, "rules"):
            #node.inputs.new('String', "")
            r = node.rules.add()
            #r.name = str(uuid.uuid4())

        return {'FINISHED'}

class Lsys_OT_del_rule(bpy.types.Operator):
    bl_idname = "lsys.del_rule"
    bl_label = "Delete Rule"

    index: bpy.props.IntProperty()

    def execute(self, context):
        node = context.active_node
        if node and hasattr(node, "rules"):
            rules = node.rules
            if 0 <= self.index < len(rules):
                #node.lsys.del_rule(rules[self.index].name)
                rules.remove(self.index)

        return {'FINISHED'}

class LNode(Node):
    '''A custom node'''
    bl_idname = 'LNode'
    bl_label = "L-System Node"

    #axiom: CollectionProperty(type=AxiomProperty)
    #rules: CollectionProperty(type=RuleProperty)
    axiom: StringProperty(
        name="",
        description="",
        default = ""
    )

    rules: CollectionProperty(type=LRulesProperty)

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'LTree'

    def init(self, context):
        self.inputs.new('LSocket', "J")
        self.inputs.new('LSocket', "K")
        self.inputs.new('LSocket', "M")

        self.outputs.new('LSocket', "L-System")

        '''
        self.lsys = Lsystem()
        self.lsys.set_axiom(LAxiom(self.axiom))

        r0 = self.rules.add()
        r0.name = str(uuid.uuid4())
        r0.rule = "F -> FF"
        self.lsys.add_rule(r0.name, LRule(r0.rule))

        r1 = self.rules.add()
        r1.name = str(uuid.uuid4())
        r1.rule = "X -> F[-X]F[-X]+X"
        self.lsys.add_rule(r1.name, LRule(r1.rule))
        '''

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.alert = (not self.axiom.valid)
        row.prop(self, "axiom", text="Axiom")

        layout.operator("lsys.add_rule")
        for i, rule in enumerate(self.rules):
            row = layout.row()
            if rule.rule == "":
                row.alert = False
            else:
                row.alert = (not rule.valid)

            row.prop(rule, "rule", text=f"Rule {i}")
            op = row.operator("lsys.del_rule", text="", icon='CANCEL')
            op.index = i

    '''
    def copy(self, node):
        print("Copying from node ", node)

    # Free function to clean up on removal.
    def free(self):
        print("Removing node ", self, ", Goodbye!")
        del self._lsys
    '''

class GroupOutputNode(Node):
    '''A custom node'''
    bl_idname = 'GroupOutputNode'
    bl_label = "Group Output"

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'LTree'

    def init(self, context):
        self.inputs.new('LSocket', "L-System")
