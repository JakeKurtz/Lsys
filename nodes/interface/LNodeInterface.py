
class LNode:
    bl_width_min = 40
    bl_width_max = 5000

    @classmethod
    def poll(cls, nodeTree):
        return nodeTree.bl_idname == "lsys_LTree"

    def setup(self):
        pass

    # may be defined in nodes
    #def create(self):
    #    pass

    def edit(self):
        pass

    def duplicate(self, sourceNode):
        pass

    def delete(self):
        pass

    def save(self):
        pass

    def draw(self, layout):
        pass

    def drawLabel(self):
        return self.bl_label

    def drawControlSocket(self, layout, socket):
        layout.alignment = "LEFT" if socket.isInput else "RIGHT"
        layout.label(text = socket.name)

    # Don't override these functions
    ######################################

    def init(self, context):
        self.width_hidden = 100
        self.identifier = createIdentifier()
        self.setup()
        if self.isRefreshable:
            self.refresh()

    def update(self):
        '''Don't use this function at all!!'''
        pass

    def copy(self, sourceNode):
        self.identifier = createIdentifier()
        infoByNode[self.identifier] = infoByNode[sourceNode.identifier].clone()
        self.duplicate(sourceNode)

    def free(self):
        self.delete()
        self._clear()

    def draw_buttons(self, context, layout):
        if self.inInvalidNetwork: layout.label(text = "Invalid Network", icon = "ERROR")
        if self.nodeTree.editNodeLabels: layout.prop(self, "label", text = "")
        self.draw(layout)

    def draw_label(self):
        if nodeLabelMode == "MEASURE" and self.hide:
            return getMinExecutionTimeString(self)

        if self.dynamicLabelType == "NONE":
            return self.bl_label
        elif self.dynamicLabelType == "ALWAYS":
            return self.drawLabel()
        elif self.dynamicLabelType == "HIDDEN_ONLY" and self.hide:
            return self.drawLabel()

        return self.bl_label

