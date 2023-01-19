# -*- coding: utf-8 -*-
# inopoa_Attribute_Connector
import os
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import *
from PySide2.QtCore import *
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
import PySide2.QtWidgets as QtWidgets
import PySide2.QtGui as QtGui
import PySide2.QtCore as QtCore
import maya.cmds as cmds
import webbrowser
VERSION = 0.1
try:
    TOOLDIR = os.path.dirname(os.path.abspath(__file__))
except:
    TOOLDIR = r'Y:\tool\ND_Tools\DCC\AttributeConnectTool'


def undoable(func):
    def _undoable(*args):
        try:
            cmds.undoInfo(openChunk=True)
            return func(*args)
        finally:
            cmds.undoInfo(closeChunk=True)
    return _undoable


def connecting(src, dsts, flags):
    for dst in dsts:
        if flags[0] == True:
            try:
                cmds.connectAttr('{}.tx'.format(src), '{}.tx'.format(dst))
            except Exception as e:
                print(e)
        if flags[1] == True:
            try:
                cmds.connectAttr('{}.ty'.format(src), '{}.ty'.format(dst))
            except:
                pass
        if flags[2] == True:
            try:
                cmds.connectAttr('{}.tz'.format(src), '{}.tz'.format(dst))
            except:
                pass
        if flags[3] == True:
            try:
                cmds.connectAttr('{}.rx'.format(src), '{}.rx'.format(dst))
            except:
                pass
        if flags[4] == True:
            try:
                cmds.connectAttr('{}.ry'.format(src), '{}.ry'.format(dst))
            except:
                pass
        if flags[5] == True:
            try:
                cmds.connectAttr('{}.rz'.format(src), '{}.rz'.format(dst))
            except:
                pass
        if flags[6] == True:
            try:
                cmds.connectAttr('{}.sx'.format(src), '{}.sx'.format(dst))
            except:
                pass
        if flags[7] == True:
            try:
                cmds.connectAttr('{}.sy'.format(src), '{}.sy'.format(dst))
            except:
                pass
        if flags[8] == True:
            try:
                cmds.connectAttr('{}.sz'.format(src), '{}.sz'.format(dst))
            except:
                pass
        if flags[9] == True:
            try:
                cmds.connectAttr('{}.shear'.format(src), '{}.shear'.format(dst))
            except:
                pass


def break_connecting(src, dsts, flags):
    for dst in dsts:
        if flags[0] == True:
            try:
                cmds.disconnectAttr('{}.tx'.format(src), '{}.tx'.format(dst))
            except Exception as e:
                pass
        if flags[1] == True:
            try:
                cmds.disconnectAttr('{}.ty'.format(src), '{}.ty'.format(dst))
            except:
                pass
        if flags[2] == True:
            try:
                cmds.disconnectAttr('{}.tz'.format(src), '{}.tz'.format(dst))
            except:
                pass
        if flags[3] == True:
            try:
                cmds.disconnectAttr('{}.rx'.format(src), '{}.rx'.format(dst))
            except:
                pass
        if flags[4] == True:
            try:
                cmds.disconnectAttr('{}.ry'.format(src), '{}.ry'.format(dst))
            except:
                pass
        if flags[5] == True:
            try:
                cmds.disconnectAttr('{}.rz'.format(src), '{}.rz'.format(dst))
            except:
                pass
        if flags[6] == True:
            try:
                cmds.disconnectAttr('{}.sx'.format(src), '{}.sx'.format(dst))
            except:
                pass
        if flags[7] == True:
            try:
                cmds.disconnectAttr('{}.sy'.format(src), '{}.sy'.format(dst))
            except:
                pass
        if flags[8] == True:
            try:
                cmds.disconnectAttr('{}.sz'.format(src), '{}.sz'.format(dst))
            except:
                pass
        if flags[9] == True:
            try:
                cmds.disconnectAttr('{}.shear'.format(src),
                                    '{}.shear'.format(dst))
            except Exception as e:
                print(e)


def connect_inner_node(src, dsts, flags):
    for dst in dsts:
        if True in flags[0:2]:
            inter_node = cmds.createNode('plusMinusAverage')
            cmds.addAttr(inter_node, longName='src', dt='string')
            cmds.addAttr(inter_node, longName='dst', dt='string')
            cmds.setAttr('{}.src'.format(inter_node), src, type='string')
            cmds.setAttr('{}.dst'.format(inter_node), dst, type='string')
            dif_vec = get_diff(src, dst, 'translate')
            cmds.setAttr(
                inter_node+'.input3D[1]', dif_vec[0], dif_vec[1], dif_vec[2], type='double3')
            if flags[0] == True:
                cmds.connectAttr('{}.translateX'.format(src),
                                '{}.input3D[0].input3Dx'.format(inter_node), f=True)
                cmds.connectAttr('{}.output3Dx'.format(inter_node),
                                '{}.translateX'.format(dst), f=True)
            if flags[1] == True:
                cmds.connectAttr('{}.translateY'.format(src),
                                '{}.input3D[0].input3Dy'.format(inter_node), f=True)
                cmds.connectAttr('{}.output3Dy'.format(inter_node),
                                '{}.translateY'.format(dst), f=True)
            if flags[2] == True:
                cmds.connectAttr('{}.translateZ'.format(src),
                                '{}.input3D[0].input3Dz'.format(inter_node), f=True)
                cmds.connectAttr('{}.output3Dz'.format(inter_node),
                                '{}.translateZ'.format(dst), f=True)

        if True in flags[3:5]:
            inter_node = cmds.createNode('plusMinusAverage')
            cmds.addAttr(inter_node, longName='src', dt='string')
            cmds.addAttr(inter_node, longName='dst', dt='string')
            cmds.setAttr('{}.src'.format(inter_node), src, type='string')
            cmds.setAttr('{}.dst'.format(inter_node), dst, type='string')
            dif_vec = get_diff(src, dst, 'rotate')
            cmds.setAttr(
                inter_node+'.input3D[1]', dif_vec[0], dif_vec[1], dif_vec[2], type='double3')
            if flags[3] == True:
                cmds.connectAttr('{}.rotateX'.format(src),
                                '{}.input3D[0].input3Dx'.format(inter_node), f=True)
                cmds.connectAttr('{}.output3Dx'.format(inter_node),
                                '{}.rotateX'.format(dst), f=True)
            if flags[4] == True:
                cmds.connectAttr('{}.rotateY'.format(src),
                                '{}.input3D[0].input3Dy'.format(inter_node), f=True)
                cmds.connectAttr('{}.output3Dy'.format(inter_node),
                                '{}.rotateY'.format(dst), f=True)
            if flags[5] == True:
                cmds.connectAttr('{}.rotateZ'.format(src),
                                '{}.input3D[0].input3Dz'.format(inter_node), f=True)
                cmds.connectAttr('{}.output3Dz'.format(inter_node),
                                '{}.rotateZ'.format(dst), f=True)
        if True in flags[6:8]:
            inter_node = cmds.createNode('multiplyDivide')
            cmds.addAttr(inter_node, longName='src', dt='string')
            cmds.addAttr(inter_node, longName='dst', dt='string')
            cmds.setAttr('{}.src'.format(inter_node), src, type='string')
            cmds.setAttr('{}.dst'.format(inter_node), dst, type='string')
            dif_vec = get_diff(src, dst, 'scale')
            cmds.setAttr(inter_node+'.input2',
                        dif_vec[0], dif_vec[1], dif_vec[2], type='double3')
            if flags[6] == True:
                cmds.connectAttr('{}.scaleX'.format(src),
                                '{}.input1.input1X'.format(inter_node), f=True)
                cmds.connectAttr('{}.outputX'.format(inter_node),
                                '{}.scaleX'.format(dst), f=True)
            if flags[7] == True:
                cmds.connectAttr('{}.scaleY'.format(src),
                                '{}.input1.input1Y'.format(inter_node), f=True)
                cmds.connectAttr('{}.outputY'.format(inter_node),
                                '{}.scaleY'.format(dst), f=True)
            if flags[8] == True:
                cmds.connectAttr('{}.scaleZ'.format(src),
                                '{}.input1.input1Z'.format(inter_node), f=True)
                cmds.connectAttr('{}.outputZ'.format(inter_node),
                                '{}.scaleZ'.format(dst), f=True)


class AttributeConnectGUI(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(AttributeConnectGUI, self).__init__(parent)
        ui_name = 'act_gui.ui'
        self.ui_path = os.path.join(TOOLDIR, ui_name)
        self.ui = QUiLoader().load(self.ui_path)
        self.setCentralWidget(self.ui)
        self.setWindowTitle('Attribute Connect Tool')
        self.ui_connect()
        help_path = ('https://onedrive.live.com/redir?resid=58BD60C626427A2A%21105&authkey=%21AMSN23DVAc9fKa0&page=View&wd=target%28Setup.one%7C89c694e3-7806-4dff-9d60-92e84a7e167b%2FAttribute%20Connect%20Tool%7C28a18493-c134-41e6-81e0-91bd40ab0b04%2F%29&wdorigin=703')
        self.ui.actionHelp_open_webbrowser.triggered.connect(
            lambda: webbrowser.open(help_path))

    def ui_connect(self):
        self.ui.get_A_button.clicked.connect(self.get_A_button_clicked)
        self.ui.get_B_button.clicked.connect(self.get_B_button_clicked)
        self.ui.connect_button.clicked.connect(self.connect_button_clicked)
        self.ui.break_button.clicked.connect(self.break_button_clicked)

        self.ui.connect_all.stateChanged.connect(
            self.connect_all_checked)
        self.ui.connect_t_row.stateChanged.connect(
            self.connect_t_row_checked)
        self.ui.connect_r_row.stateChanged.connect(
            self.connect_r_row_checked)
        self.ui.connect_s_row.stateChanged.connect(
            self.connect_s_row_checked)
        self.ui.connect_x_column.stateChanged.connect(
            self.connect_x_column_checked)
        self.ui.connect_y_column.stateChanged.connect(
            self.connect_y_column_checked)
        self.ui.connect_z_column.stateChanged.connect(
            self.connect_z_column_checked)

        self.ui.break_all.stateChanged.connect(
            self.break_all_checked)
        self.ui.break_t_row.stateChanged.connect(
            self.break_t_row_checked)
        self.ui.break_r_row.stateChanged.connect(
            self.break_r_row_checked)
        self.ui.break_s_row.stateChanged.connect(
            self.break_s_row_checked)
        self.ui.break_x_column.stateChanged.connect(
            self.break_x_column_checked)
        self.ui.break_y_column.stateChanged.connect(
            self.break_y_column_checked)
        self.ui.break_z_column.stateChanged.connect(
            self.break_z_column_checked)

        self.ui.clear_A_button.clicked.connect(self.clear_A_button_clicked)
        self.ui.clear_B_button.clicked.connect(self.clear_B_button_clicked)

        self.ui.parent_const_button.clicked.connect(
            self.parent_const_button_clicked)

    def get_A_button_clicked(self):
        # self.ui.listA.clear()
        objs = cmds.ls(sl=True)
        for obj in objs:
            print(obj)
            self.ui.list_A.addItem(obj)

    def get_B_button_clicked(self):
        # self.ui.list_B.clear()
        objs = cmds.ls(sl=True)
        for obj in objs:
            self.ui.list_B.addItem(obj)

    def clear_A_button_clicked(self):
        # self.ui.list_A.clear()
        row = self.ui.list_A.currentRow()
        self.ui.list_A.takeItem(row)
        # for item in self.ui.list_A:
        #     self.listA.takeItem(self.listA.row(item))

    def clear_B_button_clicked(self):
        # self.ui.list_B.clear()
        row = self.ui.list_B.currentRow()
        self.ui.list_B.takeItem(row)
        # for item in self.ui.list_B:
        #     self.listB.takeItem(self.listB.row(item))

    @undoable
    def connect_button_clicked(self):
        flags = [
            self.ui.connect_tx.isChecked(),
            self.ui.connect_ty.isChecked(),
            self.ui.connect_tz.isChecked(),
            self.ui.connect_rx.isChecked(),
            self.ui.connect_ry.isChecked(),
            self.ui.connect_rz.isChecked(),
            self.ui.connect_sx.isChecked(),
            self.ui.connect_sy.isChecked(),
            self.ui.connect_sz.isChecked(),
            self.ui.connect_shear.isChecked(),
        ]
        # for i in range(self.ui.list_A.count()):
        try:
            # src_obj = self.ui.list_A.itemAt(i, 0).text()
            src_obj = self.ui.list_A.currentItem().text()
            dst_objs = []
            for obj in self.ui.list_B.selectedItems():
                dst_objs.append(obj.text())
            # dst_obj = self.ui.list_B.itemAt(i, 0).text()
            pre_relation = self.ui.connect_pre.isChecked()
            if pre_relation == False:
                connecting(src_obj, dst_objs, flags)
            else:
                connect_inner_node(src_obj, dst_objs, flags)
        except Exception as e:
            print(e)

    @undoable
    def break_button_clicked(self):
        flags = [
            self.ui.break_tx.isChecked(),
            self.ui.break_ty.isChecked(),
            self.ui.break_tz.isChecked(),
            self.ui.break_rx.isChecked(),
            self.ui.break_ry.isChecked(),
            self.ui.break_rz.isChecked(),
            self.ui.break_sx.isChecked(),
            self.ui.break_sy.isChecked(),
            self.ui.break_sz.isChecked(),
            self.ui.break_shear.isChecked(),
        ]
        for i in range(self.ui.list_A.count()):
            try:
                src_obj = self.ui.list_A.itemAt(i, 0).text()
                # dst_obj = self.ui.list_B.itemAt(i, 0).text()
                dst_objs = []
                for obj in self.ui.list_B.selectedItems():
                    dst_objs.append(obj.text())
                if self.ui.break_pre.isChecked() == False:
                    break_connecting(src_obj, dst_objs, flags)
                else:
                    break_matrix_parent_constraint(src_obj, dst_objs)
            except Exception as e:
                print(e)

    @undoable
    def parent_const_button_clicked(self):
        for i in range(self.ui.list_A.count()):
            try:
                src_obj = self.ui.list_A.itemAt(i, 0).text()
                dst_obj = self.ui.list_B.itemAt(i, 0).text()
                mo = self.ui.mo_check.isChecked()
                matrix_parent_constraint(
                    src_obj, dst_obj, mo)
                print(src_obj, dst_obj)
            except Exception as e:
                print(e)

    def connect_all_checked(self):
        if self.ui.connect_all.isChecked():
            flag = True
        else:
            flag = False
        self.ui.connect_tx.setChecked(flag)
        self.ui.connect_ty.setChecked(flag)
        self.ui.connect_tz.setChecked(flag)
        self.ui.connect_rx.setChecked(flag)
        self.ui.connect_ry.setChecked(flag)
        self.ui.connect_rz.setChecked(flag)
        self.ui.connect_sx.setChecked(flag)
        self.ui.connect_sy.setChecked(flag)
        self.ui.connect_sz.setChecked(flag)

        self.ui.connect_t_row.setChecked(flag)
        self.ui.connect_r_row.setChecked(flag)
        self.ui.connect_s_row.setChecked(flag)

        self.ui.connect_x_column.setChecked(flag)
        self.ui.connect_y_column.setChecked(flag)
        self.ui.connect_z_column.setChecked(flag)

    def connect_t_row_checked(self):
        if self.ui.connect_t_row.isChecked():
            flag = True
        else:
            flag = False
        self.ui.connect_tx.setChecked(flag)
        self.ui.connect_ty.setChecked(flag)
        self.ui.connect_tz.setChecked(flag)

    def connect_r_row_checked(self):
        if self.ui.connect_r_row.isChecked():
            flag = True
        else:
            flag = False
        self.ui.connect_rx.setChecked(flag)
        self.ui.connect_ry.setChecked(flag)
        self.ui.connect_rz.setChecked(flag)

    def connect_s_row_checked(self):
        if self.ui.connect_s_row.isChecked():
            flag = True
        else:
            flag = False
        self.ui.connect_sx.setChecked(flag)
        self.ui.connect_sy.setChecked(flag)
        self.ui.connect_sz.setChecked(flag)

    def connect_x_column_checked(self):
        if self.ui.connect_x_column.isChecked():
            flag = True
        else:
            flag = False
        self.ui.connect_tx.setChecked(flag)
        self.ui.connect_rx.setChecked(flag)
        self.ui.connect_sx.setChecked(flag)

    def connect_y_column_checked(self):
        if self.ui.connect_y_column.isChecked():
            flag = True
        else:
            flag = False
        self.ui.connect_ty.setChecked(flag)
        self.ui.connect_ry.setChecked(flag)
        self.ui.connect_sy.setChecked(flag)

    def connect_z_column_checked(self):
        if self.ui.connect_z_column.isChecked():
            flag = True
        else:
            flag = False
        self.ui.connect_tz.setChecked(flag)
        self.ui.connect_rz.setChecked(flag)
        self.ui.connect_sz.setChecked(flag)

    def break_all_checked(self):
        if self.ui.break_all.isChecked():
            flag = True
        else:
            flag = False
        self.ui.break_tx.setChecked(flag)
        self.ui.break_ty.setChecked(flag)
        self.ui.break_tz.setChecked(flag)
        self.ui.break_rx.setChecked(flag)
        self.ui.break_ry.setChecked(flag)
        self.ui.break_rz.setChecked(flag)
        self.ui.break_sx.setChecked(flag)
        self.ui.break_sy.setChecked(flag)
        self.ui.break_sz.setChecked(flag)

        self.ui.break_t_row.setChecked(flag)
        self.ui.break_r_row.setChecked(flag)
        self.ui.break_s_row.setChecked(flag)

        self.ui.break_x_column.setChecked(flag)
        self.ui.break_y_column.setChecked(flag)
        self.ui.break_z_column.setChecked(flag)

    def break_t_row_checked(self):
        if self.ui.break_t_row.isChecked():
            flag = True
        else:
            flag = False
        self.ui.break_tx.setChecked(flag)
        self.ui.break_ty.setChecked(flag)
        self.ui.break_tz.setChecked(flag)

    def break_r_row_checked(self):
        if self.ui.break_r_row.isChecked():
            flag = True
        else:
            flag = False
        self.ui.break_rx.setChecked(flag)
        self.ui.break_ry.setChecked(flag)
        self.ui.break_rz.setChecked(flag)

    def break_s_row_checked(self):
        if self.ui.break_s_row.isChecked():
            flag = True
        else:
            flag = False
        self.ui.break_sx.setChecked(flag)
        self.ui.break_sy.setChecked(flag)
        self.ui.break_sz.setChecked(flag)

    def break_x_column_checked(self):
        if self.ui.break_x_column.isChecked():
            flag = True
        else:
            flag = False
        self.ui.break_tx.setChecked(flag)
        self.ui.break_rx.setChecked(flag)
        self.ui.break_sx.setChecked(flag)

    def break_y_column_checked(self):
        if self.ui.break_y_column.isChecked():
            flag = True
        else:
            flag = False
        self.ui.break_ty.setChecked(flag)
        self.ui.break_ry.setChecked(flag)
        self.ui.break_sy.setChecked(flag)

    def break_z_column_checked(self):
        if self.ui.break_z_column.isChecked():
            flag = True
        else:
            flag = False
        self.ui.break_tz.setChecked(flag)
        self.ui.break_rz.setChecked(flag)
        self.ui.break_sz.setChecked(flag)


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


def matrix_parent_constraint(src, dsts, mo):
    for dst in dsts:
        # Constraint
        if not cmds.pluginInfo('matrixNodes', q=True, l=True):
            cmds.loadPlugin('matrixNodes')

        # create preserve(relative) matrix(; composeMatrix)
        if mo:
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

        if mo:
            cmds.connectAttr(compose_matrix+'.outputMatrix',
                            mult_matrix+'.matrixIn[0]')
        cmds.connectAttr(src+'.worldMatrix',
                        mult_matrix+'.matrixIn[1]')
        cmds.connectAttr(mult_matrix+'.matrixSum',
                        decompose_matrix+'.inputMatrix')
        try:
            cmds.connectAttr(decompose_matrix +
                            '.outputTranslate', dst+'.translate')
            cmds.connectAttr(decompose_matrix +
                            '.outputRotate',    dst+'.rotate')
            cmds.connectAttr(dst+'.parentInverseMatrix[0]',
                            mult_matrix+'.matrixIn[2]')
        except:
            pass


def search_mid_obj(src, dst):
    src_objs = cmds.listConnections(
        src, d=True)
    dst_objs = cmds.listConnections(
        dst, s=True)

    result_objs = set(src_objs) & set(dst_objs)
    return result_objs


def break_matrix_parent_constraint(src, dsts):
    for dst in dsts:
        pm_ave_list = cmds.ls(type='plusMinusAverage')
        for pm_ave in pm_ave_list:
            try:
                if cmds.getAttr('{}.src'.format(pm_ave)) == src:
                    if cmds.getAttr('{}.dst'.format(pm_ave)) == dst:
                        cmds.delete(pm_ave)
            except:
                pass
        mu_di_list = cmds.ls(type='multiplyDivide')
        for mu_di in mu_di_list:
            try:
                if cmds.getAttr('{}.src'.format(mu_di)) == src:
                    if cmds.getAttr('{}.dst'.format(mu_di)) == dst:
                        cmds.delete(mu_di)
            except:
                pass


def runs():
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    ui = AttributeConnectGUI()
    ui.show()


if __name__ == '__main__':
    runs()
