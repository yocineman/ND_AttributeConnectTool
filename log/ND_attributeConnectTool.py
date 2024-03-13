import maya.cmds as cmds
import maya.mel as mel


def undoable(func):
    def _undoable(*args):
        try:
            cmds.undoInfo(openChunk=True)
            return func(*args)
        finally:
            cmds.undoInfo(closeChunk=True)
    return _undoable


def get_diff(src, dst, attr='translate'):
    if attr is 'translate':
        src_val = cmds.getAttr(src+'.t')[0]
        dst_val = cmds.getAttr(dst+'.t')[0]
        return (dst_val[0]-src_val[0], dst_val[1]-src_val[1], dst_val[2]-src_val[2])
    elif attr is 'rotate':
        src_val = cmds.getAttr(src+'.r')[0]
        dst_val = cmds.getAttr(dst+'.r')[0]
        return (dst_val[0]-src_val[0], dst_val[1]-src_val[1], dst_val[2]-src_val[2])
    elif attr is 'scale':
        src_val = cmds.getAttr(src+'.s')[0]
        dst_val = cmds.getAttr(dst+'.s')[0]
        return (dst_val[0]/src_val[0], dst_val[1]/src_val[1], dst_val[2]/src_val[2])
    else:
        return None


def connect_with_inter_node(src_nodes, dst_nodes, attr, average_flag=False):
    dst_size = len(dst_nodes)
    for src in src_nodes:
        src_attr = src+'.'+attr
        dif_vec = get_diff(src, dst_nodes[0], attr)
        if attr == 'translate' or attr == 'rotate':
            inter_node = cmds.createNode('plusMinusAverage')
            if average_flag and dst_size != 1:
                average_node = cmds.createNode('multiplyDivide')
                for _axis in ['X', 'Y', 'Z']:
                    cmds.connectAttr(
                        src_attr+_axis, average_node+'.input1'+_axis, f=True)
                cmds.setAttr(average_node+'.operation', 2)		# Divide
                cmds.setAttr(average_node+'.input2', dst_size,
                             dst_size, dst_size, type='double3')
                cmds.connectAttr(average_node+'.outputX',
                                 inter_node+'.input3D[0].input3Dx', f=True)
                cmds.connectAttr(average_node+'.outputY',
                                 inter_node+'.input3D[0].input3Dy', f=True)
                cmds.connectAttr(average_node+'.outputZ',
                                 inter_node+'.input3D[0].input3Dz', f=True)
            else:
                cmds.connectAttr(src_attr+'X', inter_node +
                                 '.input3D[0].input3Dx', f=True)
                cmds.connectAttr(src_attr+'Y', inter_node +
                                 '.input3D[0].input3Dy', f=True)
                cmds.connectAttr(src_attr+'Z', inter_node +
                                 '.input3D[0].input3Dz', f=True)
            cmds.setAttr(
                inter_node+'.input3D[1]', dif_vec[0], dif_vec[1], dif_vec[2], type='double3')
            if attr == 'rotate' and dst_size > 1:
                dst_attr = dst_nodes[0]+'.'+attr
                cmds.connectAttr(inter_node+'.output3Dx', dst_attr+'X', f=True)
                cmds.connectAttr(inter_node+'.output3Dy', dst_attr+'Y', f=True)
                cmds.connectAttr(inter_node+'.output3Dz', dst_attr+'Z', f=True)
                unitConversionX = cmds.listConnections(
                    dst_attr+'X', s=True, d=False)[-1]
                unitConversionY = cmds.listConnections(
                    dst_attr+'Y', s=True, d=False)[-1]
                unitConversionZ = cmds.listConnections(
                    dst_attr+'Z', s=True, d=False)[-1]
                for dst in dst_nodes[1:]:
                    dst_attr = dst+'.'+attr
                    cmds.connectAttr(unitConversionX+'.output',
                                     dst_attr+'X', f=True)
                    cmds.connectAttr(unitConversionY+'.output',
                                     dst_attr+'Y', f=True)
                    cmds.connectAttr(unitConversionZ+'.output',
                                     dst_attr+'Z', f=True)
            else:
                for dst in dst_nodes:
                    dst_attr = dst+'.'+attr
                    cmds.connectAttr(inter_node+'.output3Dx',
                                     dst_attr+'X', f=True)
                    cmds.connectAttr(inter_node+'.output3Dy',
                                     dst_attr+'Y', f=True)
                    cmds.connectAttr(inter_node+'.output3Dz',
                                     dst_attr+'Z', f=True)
        else:
            inter_node = cmds.createNode('multiplyDivide')
            for _axis in ['X', 'Y', 'Z']:
                cmds.connectAttr(src_attr+_axis, inter_node +
                                 '.input1'+_axis, f=True)
            if average_flag and dst_size != 1:
                cmds.setAttr(
                    inter_node+'.input2', dif_vec[0]/dst_size, dif_vec[1]/dst_size, dif_vec[2]/dst_size, type='double3')
            else:
                cmds.setAttr(inter_node+'.input2',
                             dif_vec[0], dif_vec[1], dif_vec[2], type='double3')
            for dst in dst_nodes:
                for _axis in ['X', 'Y', 'Z']:
                    dst_attr = dst+'.'+attr
                    cmds.connectAttr(inter_node+'.output' +
                                     _axis, dst_attr+_axis, f=True)


def connect_directly(src, dst, attr_name):
    for _axis in ['X', 'Y', 'Z']:
        src_attr = src+'.'+attr_name+_axis
        dst_attr = dst+'.'+attr_name+_axis
        # if they were already connected
        if cmds.isConnected(src_attr, dst_attr):
            error_msg = src_attr+' and '+dst_attr+' were already connected.'
            mel.eval('warning "'+error_msg+'"')
            continue
        cmds.connectAttr(src_attr, dst_attr, f=True)

###
# main function
###


def connect_attr(src_nodes, dst_nodes, attr_name, need_inter_node=False, average_flag=False):
    if not need_inter_node:
        for src_node in src_nodes:
            for dst_node in dst_nodes:
                connect_directly(src_node, dst_node, attr_name)
    else:
        connect_with_inter_node(src_nodes, dst_nodes, attr_name, average_flag)


###
# parent matrix(by using Matrix)
###
def matrix_parent_constraint(src_nodes, dst_nodes, is_preserve):
    # check plugin
    if not cmds.pluginInfo('matrixNodes', q=True, l=True):
        cmds.loadPlugin('matrixNodes')

    for dst in dst_nodes:
        for src in src_nodes:
            # create preserve(relative) matrix(; composeMatrix)
            if is_preserve:
                t_dif_vec = get_diff(src, dst, 'translate')
                r_dif_vec = get_diff(src, dst, 'rotate')
                s_dif_vec = get_diff(src, dst, 'scale')
                compose_matrix = cmds.createNode('composeMatrix')
                cmds.setAttr(compose_matrix+'.inputTranslate',
                             t_dif_vec[0], t_dif_vec[1], t_dif_vec[2], type='double3')
                cmds.setAttr(compose_matrix+'.inputRotate',
                             r_dif_vec[0], r_dif_vec[1], r_dif_vec[2], type='double3')
                cmds.setAttr(compose_matrix+'.inputScale',
                             s_dif_vec[0], s_dif_vec[1], s_dif_vec[2], type='double3')

            mult_matrix = cmds.createNode('multMatrix')
            decompose_matrix = cmds.createNode('decomposeMatrix')

            if is_preserve:
                cmds.connectAttr(compose_matrix+'.outputMatrix',
                                 mult_matrix+'.matrixIn[0]')
            cmds.connectAttr(src+'.worldMatrix', mult_matrix+'.matrixIn[1]')
            cmds.connectAttr(mult_matrix+'.matrixSum',
                             decompose_matrix+'.inputMatrix')

            cmds.connectAttr(decompose_matrix +
                             '.outputTranslate', dst+'.translate')
            cmds.connectAttr(decompose_matrix +
                             '.outputRotate',    dst+'.rotate')
#			cmds.connectAttr(decompose_matrix+'.outputScale',     dst+'.scale')

            cmds.connectAttr(
                dst+'.parentInverseMatrix[0]', mult_matrix+'.matrixIn[2]')


###
# --- --- --- --- --- --- GUI --- --- --- --- --- ---
###
class AttributeConnectToolGUI(object):
    def __init__(self, windowName='AttributesConnectTool', width=400, height=200):
        self.wndW = width
        self.wndH = height
        self.wnd = windowName

        if cmds.window(self.wnd, q=True, exists=True):
            cmds.deleteUI(self.wnd)

        cmds.window(self.wnd, t=windowName, w=self.wndW,
                    h=self.wndH, menuBar=True)

        self.createUITemplate('attributeConnectToolTemplate')

        # main form
        self.mainForm = cmds.formLayout(p=self.wnd)
        # base frame --- --- ---
        self.baseframe = cmds.frameLayout(
            l='connection setting', p=self.mainForm, collapsable=True, width=300)

        # select src
        cmds.text(label='src node name', align='left')
        cmds.rowLayout(numberOfColumns=2)
        self.src_name_area = cmds.textField(h=20, w=260)
        cmds.button(l='set', c=self.set_src_name)
        cmds.setParent('..')

        # select target
        cmds.text(label='target node name', align='left')
        cmds.rowLayout(numberOfColumns=2)
        self.dst_name_area = cmds.textField(h=20, w=260)
        cmds.button(l='set', c=self.set_dst_name)
        cmds.setParent('..')

        # check box
        cmds.separator(style='in')
        cmds.text(label=' - Setting - ', align='left')
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(
            150, 80), columnAlign2=('center', 'center'))
        self.selectAttrCheckBox = cmds.checkBoxGrp(numberOfCheckBoxes=3, labelArray3=[
                                                   'translate', 'rotate', 'scale'], vertical=True)
        self.interCheckBox = cmds.checkBoxGrp(numberOfCheckBoxes=2, labelArray2=[
                                              'preserve relations', 'average'], vertical=True, changeCommand1=self.change_internal)
        cmds.checkBoxGrp(self.interCheckBox, e=True, enable2=False)
        cmds.setParent('..')

        cmds.button(l='create connections', c=self.apply_connections)

        # parentConstraint
        cmds.separator(style='in')
        cmds.text(label=' - parentConstraint(Matrix) - ', align='left')
        self.parentConstraintCheckBox = cmds.checkBoxGrp(
            numberOfCheckBoxes=1, label1='maintain offset')
        cmds.button(l='parentConstraint', c=self.apply_parentConstraint)

        cmds.formLayout(self.mainForm, e=True, ap=(
            self.baseframe, 'top', 0, 0))

        self.deleteUITemplate()

    @undoable
    def change_internal(self, opt):
        if cmds.checkBoxGrp(self.interCheckBox, q=True, value1=True):
            # enable average flag
            cmds.checkBoxGrp(self.interCheckBox, e=True, enable2=True)
        else:
            # disable average flag
            cmds.checkBoxGrp(self.interCheckBox, e=True, value2=False)
            cmds.checkBoxGrp(self.interCheckBox, e=True, enable2=False)

    @undoable
    def set_src_name(self, opt):
        sels = cmds.ls(sl=True)
        cmds.textField(self.src_name_area, e=True, text='')
        if len(sels) is not 0:
            cmds.textField(self.src_name_area, e=True, text=sels[0])

    @undoable
    def set_dst_name(self, opt):
        sels = cmds.ls(sl=True)
        cmds.textField(self.dst_name_area, e=True, text='')
        if len(sels) is not 0:
            tex = ''
            for sel in sels:
                tex += (sel+', ')
            tex = tex[:-2]
            cmds.textField(self.dst_name_area, e=True, text=tex)

    def get_from_textField(self, text_area):
        nodes_text = cmds.textField(text_area, q=True, text=True)
        nodes = nodes_text.split(',')
        return [n.strip() for n in nodes]

    @undoable
    def apply_connections(self, opt):
        src_node_name = self.get_from_textField(self.src_name_area)
        dst_node_name = self.get_from_textField(self.dst_name_area)
        inter_node_flag = cmds.checkBoxGrp(
            self.interCheckBox, q=True, value1=True)
        average_flag = cmds.checkBoxGrp(
            self.interCheckBox, q=True, value2=True)
        tranlate_flag = cmds.checkBoxGrp(
            self.selectAttrCheckBox, q=True, value1=True)
        rotate_flag = cmds.checkBoxGrp(
            self.selectAttrCheckBox, q=True, value2=True)
        scale_flag = cmds.checkBoxGrp(
            self.selectAttrCheckBox, q=True, value3=True)
        if tranlate_flag:
            connect_attr(src_node_name, dst_node_name,
                         'translate', inter_node_flag, average_flag)
        if rotate_flag:
            connect_attr(src_node_name, dst_node_name, 'rotate',
                         inter_node_flag, average_flag)
        if scale_flag:
            connect_attr(src_node_name, dst_node_name, 'scale',
                         inter_node_flag, average_flag)

    @undoable
    def apply_parentConstraint(self, opt):
        src_node_name = self.get_from_textField(self.src_name_area)
        dst_node_name = self.get_from_textField(self.dst_name_area)
        preserve_flag = cmds.checkBoxGrp(
            self.parentConstraintCheckBox, q=True, value1=True)
        _src_nodes = []
        _dst_nodes = []
        for n in src_node_name:
            if cmds.objExists(n):
                _src_nodes.append(n)
        for n in dst_node_name:
            if cmds.objExists(n):
                _dst_nodes.append(n)
        matrix_parent_constraint(_src_nodes, _dst_nodes, preserve_flag)

    def createUITemplate(self, template):
        self.currentTemplate = template
        if cmds.uiTemplate(self.currentTemplate, exists=True):
            cmds.deleteUI(self.currentTemplate, uiTemplate=True)
        cmds.uiTemplate(self.currentTemplate)
        cmds.frameLayout(dt=self.currentTemplate, labelAlign='bottom', borderStyle='etchedIn',
                         w=230, collapsable=True, marginWidth=5, marginHeight=5)
        cmds.setUITemplate(self.currentTemplate, pushTemplate=True)

    def deleteUITemplate(self):
        cmds.setUITemplate(popTemplate=True)
        if cmds.uiTemplate(self.currentTemplate, exists=True):
            cmds.deleteUI(self.currentTemplate, uiTemplate=True)
        self.currentTemplate = ''

    def showWindow(self):
        cmds.showWindow(self.wnd)


if __name__ == '__main__':
    # test case
    #	_src = 'pCube1'
    #	_dst = 'pCube2'
    #	connect_attr(_src, _dst, 'translate', True)
    #	connect_attr(_src, _dst, 'rotate', True)
    #	connect_attr(_src, _dst, 'scale', True)

    app = AttributeConnectToolGUI()
    app.showWindow()
