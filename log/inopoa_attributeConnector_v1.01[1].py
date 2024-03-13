# -*- coding: utf-8 -*-
# inopoa_Attribute_Connector
# https://inopoa.com

import pymel.core as pm

class Get_list:
    def __init__(self):
        self.sel_A = []
        self.sel_B = []

    def get_A(self):
        list_A.removeAll()
        self.sel_A = pm.ls(selection=True)
        list_A.append(self.sel_A)
        pm.select(clear=True)

    def get_B(self):
        list_B.removeAll()
        self.sel_B = pm.ls(selection=True)
        list_B.append(self.sel_B)
        pm.select(clear=True)

def connecting():
    t_value = boxTGrp.getValueArray3()
    r_value = boxRGrp.getValueArray3()
    s_value = boxSGrp.getValueArray3()
    shr_val = boxShrG.getValue()

    sel_a = len(cgl.sel_A)
    i = 0
    while i < sel_a:
        if t_value[0] == True:
            cgl.sel_A[i].tx >> cgl.sel_B[i].tx
        if t_value[1] == True:
            cgl.sel_A[i].ty >> cgl.sel_B[i].ty
        if t_value[2] == True:
            cgl.sel_A[i].tz >> cgl.sel_B[i].tz
        if r_value[0] == True:
            cgl.sel_A[i].rx >> cgl.sel_B[i].rx
        if r_value[1] == True:
            cgl.sel_A[i].ry >> cgl.sel_B[i].ry
        if r_value[2] == True:
            cgl.sel_A[i].rz >> cgl.sel_B[i].rz
        if s_value[0] == True:
            cgl.sel_A[i].sx >> cgl.sel_B[i].sx
        if s_value[1] == True:
            cgl.sel_A[i].sy >> cgl.sel_B[i].sy
        if s_value[2] == True:
            cgl.sel_A[i].sz >> cgl.sel_B[i].sz
        if shr_val == True:
            cgl.sel_A[i].shear >> cgl.sel_B[i].shear
        i = i + 1



def break_connecting():
    bsl = pm.ls(selection=True)
    bt_value = brkTGrp.getValueArray3()
    br_value = brkRGrp.getValueArray3()
    bs_value = brkSGrp.getValueArray3()
    bshr_val = brkShrG.getValue()
    sel_len = len(bsl)
    i = 0
    while i < sel_len:
        if bt_value[0] == True:
            bsl[i].tx.disconnect()
        if bt_value[1] == True:
            bsl[i].ty.disconnect()
        if bt_value[2] == True:
            bsl[i].tz.disconnect()
        if br_value[0] == True:
            bsl[i].rx.disconnect()
        if br_value[1] == True:
            bsl[i].ry.disconnect()
        if br_value[2] == True:
            bsl[i].rz.disconnect()
        if bs_value[0] == True:
            bsl[i].sx.disconnect()
        if bs_value[1] == True:
            bsl[i].sy.disconnect()
        if bs_value[2] == True:
            bsl[i].sz.disconnect()
        if bshr_val == True:
            bsl[i].shear.disconnect()
        i = i + 1

cgl = Get_list()


with pm.window(title='Inopoa_Attribute_Connector'):
    with pm.columnLayout(adjustableColumn = True):
        pm.text('controll ----> controlled')
        with pm.horizontalLayout():
            with pm.columnLayout(adjustableColumn = True):
                list_A = pm.textScrollList( numberOfRows=8, allowMultiSelection=True )
                pm.button( label = 'get A', command = pm.Callback( cgl.get_A ) )
            with pm.columnLayout(adjustableColumn = True):
                pm.text('\n\n\n')
                pm.text('------>')
            with pm.columnLayout(adjustableColumn = True ):
                list_B = pm.textScrollList( numberOfRows=8, allowMultiSelection=True )
                pm.button( label = 'get B', command = pm.Callback( cgl.get_B ) )
        pm.separator()
        with pm.columnLayout(adjustableColumn = True ):
            boxTGrp = pm.checkBoxGrp( numberOfCheckBoxes = 3, label = 'translate', labelArray3 = ['X', 'Y', 'Z'], value1 = True, value2 = True, value3 = True )
            boxRGrp = pm.checkBoxGrp( numberOfCheckBoxes = 3, label = 'rotate', labelArray3 = ['X', 'Y', 'Z'], value1 = True, value2 = True, value3 = True )
            boxSGrp = pm.checkBoxGrp( numberOfCheckBoxes = 3, label = 'scale', labelArray3 = ['X', 'Y', 'Z'], value1 = True, value2 = True, value3 = True )
            with pm.rowColumnLayout( parent = boxRGrp ):
                boxShrG = pm.checkBox( label = 'shear', value = True )
        with pm.autoLayout():
            pm.button( label = 'connect', command = pm.Callback( connecting ) )
            pm.separator()
        with pm.columnLayout(adjustableColumn = True):
            brkTGrp = pm.checkBoxGrp( numberOfCheckBoxes = 3, label = 'translate', labelArray3 = ['X', 'Y', 'Z'], value1 = True, value2 = True, value3 = True )
            brkRGrp = pm.checkBoxGrp( numberOfCheckBoxes = 3, label = 'rotate', labelArray3 = ['X', 'Y', 'Z'], value1 = True, value2 = True, value3 = True )
            brkSGrp = pm.checkBoxGrp( numberOfCheckBoxes = 3, label = 'scale', labelArray3 = ['X', 'Y', 'Z'], value1 = True, value2 = True, value3 = True )
            with pm.rowLayout( parent = brkRGrp ):
                brkShrG = pm.checkBox( label = 'shear', value = True )
        with pm.columnLayout(adjustableColumn = True):
            pm.button( label = 'break connection(selected items)', command = pm.Callback( break_connecting ) )

