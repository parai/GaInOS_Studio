# -*- coding: utf-8 -*-

"""
Module implementing ScheduleTable.
"""
from PyQt4.QtGui import QTreeWidgetItem, QMessageBox
from PyQt4.QtCore import QStringList,QString
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature
import os
from Ui_SchedTable import Ui_ScheduleTable

class DlgScheduleTable(QDialog, Ui_ScheduleTable):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self);
        self.parent=parent;
        self.pxSchedTbl=parent.pxCurSelGaInOsObj;
        self.setWindowTitle("Configure Schedule Table <%s>"%(self.pxSchedTbl.xScheduleTableName));
        self.vDisableAllTab();
        self.pxCurSelEp=None;
        self.pxCurSelEpSubIndex=-1;
        self.pxCurSelTreeItem=None;
        #根据table 刷新界面树，初始化
        index=0;
        for ep in self.pxSchedTbl.xSchedTblEpList:
            defaultName=QString('Expiry Point %s(%s)'%(index, ep[0]));
            pxTreeIlem=QTreeWidgetItem(self.trSchedTable,QStringList(defaultName));
            self.trSchedTable.addTopLevelItem(pxTreeIlem);
            index+=1;
            for epsub in ep[1]:
                defaultName=QString(epsub);
                pxTreeIlem2=QTreeWidgetItem(None,QStringList(defaultName));
                pxTreeIlem.addChild(pxTreeIlem2);
                pxTreeIlem.setExpanded(True);
        #刷新基本控件
        self.cbxSchedTblRepeatable.setChecked(self.pxSchedTbl.xSchedTblRepeatable);
        self.cbxSchedTblAutostartable.setChecked(self.pxSchedTbl.xSchedTblAutostartable);
        self.cmbxSchedTblAutoStartType.setCurrentIndex(self.vDoGetAutostartType());
        self.cmbxSchedTblSyncStrategy.setCurrentIndex(self.vDoGetSyncStrategy());
        self.spbxSchedTblAbsRel.setValue(self.pxSchedTbl.xSchedTblAbsRelValue);
        self.spbxSchedTblFinalDelay.setValue(self.pxSchedTbl.xSchedTblFinalDelay);
        self.spbxSchedTblMaxAdvance.setValue(self.pxSchedTbl.xSchedTblMaxAdvance);
        self.spbxSchedTblMaxRetard.setValue(self.pxSchedTbl.xSchedTblMaxRetard);
        self.spbxSchedTblPrecision.setValue(self.pxSchedTbl.xSchedTblExplicitPrecision);
        index=-1;
        i=0;
        for cnt in self.parent.pxGaInOSCounterCfgList:
            name=cnt.xCounterName;
            self.cmbxSchedTblDrivingCounter.addItem(name);
            if(self.pxSchedTbl.xSchedTblDrivingCounter==name):
                index=i;
            i+=1;
        #模拟一次点击刷新控件
        self.on_cbxSchedTblAutostartable_clicked(self.pxSchedTbl.xSchedTblAutostartable);
        #初始化控件
        self.btnAdd.setText("Add Expiry Point");
        self.btnAdd.setDisabled(False);
        self.btnInsert.setDisabled(True);
        self.btnDelete.setDisabled(True);

    def vDoGetAutostartType(self):
        type=self.pxSchedTbl.xSchedTblAutostartType;
        if(type=='ABSOLUTE'):
            return 0;
        elif(type=='RELATIVE'):
            return 1;
        elif(type=='SYNCHRON'):
            return 2;
        return -1;

    def vDoGetSyncStrategy(self):
        strategy=self.pxSchedTbl.xSchedTblSyncStrategy;
        if(strategy=='NONE'):
            return 0;
        elif(strategy=='EXPLICIT'):
            return 1;
        elif(strategy=='IMPLICIT'):
            return 2;
        return -1;

    @pyqtSignature("QString")
    def on_cmbxSetTskId_currentIndexChanged(self, p0):
        """修改SetEvent设置的任务"""
        if(self.pxCurSelEp!=None and self.pxCurSelEpSubIndex!=-1):
            str=self.pxCurSelEp[1][self.pxCurSelEpSubIndex];
            self.pxCurSelEp[1][self.pxCurSelEpSubIndex]='SetEvent(%s,)'%(p0);
            self.pxCurSelTreeItem.setText(0,'SetEvent(%s,)'%(p0));
            self.vDoRefreshCmbxEvent(p0, '')
    
    @pyqtSignature("QString")
    def on_cmbxSetEnt_currentIndexChanged(self, p0):
        """修改SetEvent设置的任务"""
        if(self.pxCurSelEp!=None and self.pxCurSelEpSubIndex!=-1):
            str=self.pxCurSelEp[1][self.pxCurSelEpSubIndex];
            grp=self.vDoGetTskEnt(str);
            self.pxCurSelEp[1][self.pxCurSelEpSubIndex]='SetEvent(%s,%s)'%(grp[0], p0);
            self.pxCurSelTreeItem.setText(0,'SetEvent(%s,%s)'%(grp[0], p0));
    
    @pyqtSignature("QString")
    def on_cmbxActTskId_currentIndexChanged(self, p0):
        """修改激活任务"""
        if(self.pxCurSelEp!=None and self.pxCurSelEpSubIndex!=-1):
            self.pxCurSelEp[1][self.pxCurSelEpSubIndex]='ActivateTask(%s)'%(p0);
            self.pxCurSelTreeItem.setText(0,'ActivateTask(%s)'%(p0));

    def vDoAddExpiryPoint(self):
        """添加一个Expiry Point"""
        length=len(self.pxSchedTbl.xSchedTblEpList);
        if(length==0):
            offset=10;
        else:
            offset=10+self.pxSchedTbl.xSchedTblEpList[length-1][0];
        defaultName=QString('Expiry Point %s(%s)'%(length,offset));
        pxTreeIlem=QTreeWidgetItem(self.trSchedTable,QStringList(defaultName));
        self.trSchedTable.addTopLevelItem(pxTreeIlem);
        self.pxSchedTbl.xSchedTblEpList.append([offset,[] ]);
        #print self.pxSchedTbl.xSchedTblEpList[length];

    def vDoInsertExpiryPoint(self):
        """插入一个Expiry Point"""
        if(self.pxCurSelTreeItem==None):
            return;
        index=self.trSchedTable.indexOfTopLevelItem(self.pxCurSelTreeItem.parent());
        if(index == -1):
            return;
        defaultName=QString('Expiry Point');
        pxTreeIlem=QTreeWidgetItem(None,QStringList(defaultName));
        self.trSchedTable.insertTopLevelItem(index, pxTreeIlem);
        offset=self.pxSchedTbl.xSchedTblEpList[index][0]-5;
        self.pxSchedTbl.xSchedTblEpList.insert(index, [offset,[] ]);
        self.vDoRefreshTreeTopItemName();

    def vDoAddActTsk(self):
        """为所选expiry point添加一个任务激活事件"""
        if(self.pxCurSelTreeItem==None):
            return;
        index=self.trSchedTable.indexOfTopLevelItem(self.pxCurSelTreeItem);
        if(index == -1):
            return;
        defaultName=QString('ActivateTask()');
        pxTreeIlem=QTreeWidgetItem(None,QStringList(defaultName));
        self.pxCurSelTreeItem.insertChild(0, pxTreeIlem);
        self.pxSchedTbl.xSchedTblEpList[index][1].insert(0,'ActivateTask()');
        self.pxCurSelTreeItem.setExpanded(True);
        #print self.pxSchedTbl.xSchedTblEpList[index];

    def vDoAddSetEnt(self):
        """为所选expiry point添加一个任务事件设置"""
        if(self.pxCurSelTreeItem==None):
            return;
        index=self.trSchedTable.indexOfTopLevelItem(self.pxCurSelTreeItem);
        if(index == -1):
            return;
        defaultName=QString('SetEvent(,)');
        pxTreeIlem=QTreeWidgetItem(self.pxCurSelTreeItem,QStringList(defaultName));
        self.pxCurSelTreeItem.addChild(pxTreeIlem);
        self.pxSchedTbl.xSchedTblEpList[index][1].append('SetEvent(,)');
        self.pxCurSelTreeItem.setExpanded(True);
        #print self.pxSchedTbl.xSchedTblEpList[index];

    @pyqtSignature("")
    def on_btnAdd_clicked(self):
        """添加一个节点"""
        if(self.btnAdd.text()=='Add Expiry Point'):
            self.vDoAddExpiryPoint();
        elif(self.btnAdd.text()=='Add ActivateTask'):
            self.vDoAddActTsk();

    @pyqtSignature("")
    def on_btnInsert_clicked(self):
        if(self.btnInsert.text()=='Add SetEvent'):
            self.vDoAddSetEnt();
        elif(self.btnInsert.text()=='Insert Expiry Point'):
            self.vDoInsertExpiryPoint();

    def vDoDeleteExpiryPoint(self):
        """删除当前Expiry Point"""
        if(self.pxCurSelTreeItem!=None):
            index=self.trSchedTable.indexOfTopLevelItem(self.pxCurSelTreeItem);
            if(index!=-1):
                self.trSchedTable.takeTopLevelItem(index);
                self.pxSchedTbl.xSchedTblEpList.remove(self.pxSchedTbl.xSchedTblEpList[index]);
                self.vDoRefreshTreeTopItemName();
                if(index>0):
                    item=self.trSchedTable.topLevelItem(index-1);
                else:
                    item=None;
                self.vDoFindNextItem(item);

    def vDoDeleteEpSub(self):
        """删除当前expiry point的选中的一个Action"""
        if(self.pxCurSelTreeItem!=None and self.pxCurSelEp!=None and self.pxCurSelEpSubIndex!=-1):
            index=self.trSchedTable.indexOfTopLevelItem(self.pxCurSelTreeItem);
            if(index==-1):
                parent=self.pxCurSelTreeItem.parent();
                index=parent.indexOfChild(self.pxCurSelTreeItem);
                parent.takeChild(index);
                self.pxCurSelEp[1].remove(self.pxCurSelEp[1][self.pxCurSelEpSubIndex]);
                if(index>0):
                    item=parent.child(index-1);
                else:
                    item=None;
                self.vDoFindNextItem(item);

    def vDoFindNextItem(self, item):
        #当删除一个对象时，尝试寻找下一个
        if(item!=None):
            #模拟一次Tree的点击效果，刷新
            self.on_trSchedTable_itemClicked(item, 0);
        else:
            #删除了所有，复为标志
            self.pxCurSelEp=None;
            self.pxCurSelEpSubIndex=-1;
            self.pxCurSelTreeItem=None; 
            #复位控件
            self.btnAdd.setText("Add Expiry Point");
            self.btnAdd.setDisabled(False);
            self.btnInsert.setDisabled(True);
            self.btnDelete.setDisabled(True);

    @pyqtSignature("")
    def on_btnDelete_clicked(self):
        if(self.btnDelete.text()=='Delete Expiry Point'):
            self.vDoDeleteExpiryPoint();
        elif(self.btnDelete.text()=='Delete Action'):
            self.vDoDeleteEpSub();
    
    def vDisableAllTab(self):
        """使能xIndex指向的Tab页"""
        for i in  range(0, 3):
            self.tblSchedTable.setTabEnabled(i, False);

    def vEnableTab(self, xIndex):
        """使能xIndex指向的Tab页"""
        for i in  range(0, 3):
            if(i==xIndex):
                self.tblSchedTable.setTabEnabled(i, True);
                self.tblSchedTable.setCurrentIndex(i);
            else:
                self.tblSchedTable.setTabEnabled(i, False);
   
    def vDoRefreshTreeTopItemName(self):
        """刷新expiry point名称，使其顺序"""
        for index in range(0, self.trSchedTable.topLevelItemCount()):
            item=self.trSchedTable.topLevelItem(index);
            item.setText(0, 'Expiry Point %s(%s)'%(index,
                    self.pxSchedTbl.xSchedTblEpList[index][0]));

    def vDoRefreshActivateTaskTab(self, xTaskId):
        self.cmbxActTskId.clear();
        for tsk in self.parent.pxGaInOSTaskCfgList:
            self.cmbxActTskId.addItem(tsk.xTaskName);
        if(xTaskId==''):
            self.cmbxActTskId.setCurrentIndex(-1);
            return;
        index=-1;
        for i in range(0, self.cmbxActTskId.count()):
            if(xTaskId==self.cmbxActTskId.itemText(i)):
                index=i;
                break;
        self.cmbxActTskId.setCurrentIndex(index);

    def vDoGetTskEnt(self, str):
        index=str.find(',');
        tsk=str[9:index];
        ent=str[index+1:-1];
        #print('%s,%s')%(tsk, ent);
        return (tsk, ent);

    def vDoRefreshCmbxEvent(self, xTaskId, xEvent):
        self.cmbxSetEnt.clear();
        flag=False;
        for tsk in self.parent.pxGaInOSTaskCfgList:
            if(tsk.xTaskType=='EXTEND_TASK' and tsk.xTaskName==xTaskId):
                flag=True;
                break;
        index=-1;
        i=-1;
        if(flag==True):
            for ent in tsk.xTaskEventList:
                self.cmbxSetEnt.addItem(ent.xEventName);
                i+=1;
                if(xEvent==ent.xEventName):
                    index=i;
        self.cmbxSetEnt.setCurrentIndex(index);

    def vDoRefreshSetEventTab(self, xTaskId, xEvent):
        self.cmbxSetTskId.clear();
        for tsk in self.parent.pxGaInOSTaskCfgList:
            if(tsk.xTaskType=='EXTEND_TASK'):
                self.cmbxSetTskId.addItem(tsk.xTaskName);
        if(xTaskId==''):
            self.cmbxSetTskId.setCurrentIndex(-1);
            return;
        index=-1;
        for i in range(0, self.cmbxSetTskId.count()):
            if(xTaskId==self.cmbxSetTskId.itemText(i)):
                index=i;
                break;
        self.cmbxSetTskId.setCurrentIndex(index);
        self.vDoRefreshCmbxEvent(xTaskId, xEvent);
    
    def vDoTabChangeAndRefresh(self, item):
        index = self.trSchedTable.indexOfTopLevelItem(item);
        if(index != -1):
            #点击的根节点，切换设置offset Tab页
            self.vEnableTab(2);
            self.pxCurSelEp=self.pxSchedTbl.xSchedTblEpList[index];
            self.pxCurSelEpSubIndex=-1;
            self.spbxSchedEpOffset.setValue(self.pxCurSelEp[0]);
            #刷新控件
            self.btnAdd.setText("Add ActivateTask");
            self.btnInsert.setText('Add SetEvent');
            self.btnDelete.setText('Delete Expiry Point');
            self.btnAdd.setDisabled(False);
            self.btnInsert.setDisabled(False);
            self.btnDelete.setDisabled(False);
        else:
            #点击的是子节点，根据节点信息切换相应Tab页
            text=item.text(0);
            index = self.trSchedTable.indexOfTopLevelItem(item.parent());
            self.pxCurSelEp=self.pxSchedTbl.xSchedTblEpList[index];
            self.pxCurSelEpSubIndex=item.parent().indexOfChild(item);
            if(text[0:12]=='ActivateTask'):
                self.vEnableTab(0);
                self.vDoRefreshActivateTaskTab(text[13:-1]);
            elif(text[0:8]=='SetEvent'):
                self.vEnableTab(1);
                grp=self.vDoGetTskEnt(str(text));
                self.vDoRefreshSetEventTab(grp[0], grp[1]);
            #刷新控件
            self.btnAdd.setText("Add Expiry Point");
            self.btnInsert.setText('Insert Expiry Point');
            self.btnDelete.setText('Delete Action');
            self.btnAdd.setDisabled(False);
            self.btnInsert.setDisabled(False);
            self.btnDelete.setDisabled(False);

    @pyqtSignature("QTreeWidgetItem*, int")
    def on_trSchedTable_itemClicked(self, item, column):
        """标记当前选择的项目"""
        #保存点击选中的Item指针
        self.pxCurSelTreeItem=item;
        #根据Item选择设置相应的配置页为活动页
        self.vDoTabChangeAndRefresh(item);
    
    @pyqtSignature("int")
    def on_spbxSchedEpOffset_valueChanged(self, p0):
        """刷新Ep的offset"""
        if(self.pxCurSelEp!=None):
            self.pxCurSelEp[0]=p0;
            self.pxCurSelTreeItem.setText(0, 'Expiry Point %s(%s)'%(
                self.trSchedTable.indexOfTopLevelItem(self.pxCurSelTreeItem), p0));

    @pyqtSignature("bool")
    def on_cbxSchedTblRepeatable_clicked(self, checked):
        """修改Schedule table是否自动重复"""
        self.pxSchedTbl.xSchedTblRepeatable=checked;
    
    @pyqtSignature("QString")
    def on_cmbxSchedTblDrivingCounter_currentIndexChanged(self, p0):
        """修改schedule table的驱动counter"""
        self.pxSchedTbl.xSchedTblDrivingCounter=p0;
    
    @pyqtSignature("bool")
    def on_cbxSchedTblAutostartable_clicked(self, checked):
        """修改schedule table是否自启动"""
        self.pxSchedTbl.xSchedTblAutostartable=checked;
        if(checked==True):
            self.cmbxSchedTblAutoStartType.setDisabled(False);
            if(self.pxSchedTbl.xSchedTblAutostartType!='SYNCHRON'):
                self.spbxSchedTblAbsRel.setDisabled(False);
            else:
                self.spbxSchedTblAbsRel.setDisabled(True);
        else:
            self.cmbxSchedTblAutoStartType.setDisabled(True);
            self.spbxSchedTblAbsRel.setDisabled(True);

    @pyqtSignature("QString")
    def on_cmbxSchedTblAutoStartType_currentIndexChanged(self, p0):
        """修改自启动类型"""
        self.pxSchedTbl.xSchedTblAutostartType=p0;
        if(p0=='ABSOLUTE'):
            self.lblSchedTblAbsRel.setText('Absolut Value:');
            self.spbxSchedTblAbsRel.setDisabled(False);
        elif(p0=='RELATIVE'):
            self.lblSchedTblAbsRel.setText('Relative Value:');
            self.spbxSchedTblAbsRel.setDisabled(False);
        else:
            self.spbxSchedTblAbsRel.setDisabled(True);

    @pyqtSignature("int")
    def on_spbxSchedTblAbsRel_valueChanged(self, p0):
        """修改 ABSOLUTE 和 RELATIVE类型是启动传入参数 value"""
        self.pxSchedTbl.xSchedTblAbsRelValue=p0;

    @pyqtSignature("int")
    def on_spbxSchedTblFinalDelay_valueChanged(self, p0):
        """修改final delay的值"""
        self.pxSchedTbl.xSchedTblFinalDelay=p0;

    @pyqtSignature("QString")
    def on_cmbxSchedTblSyncStrategy_currentIndexChanged(self, p0):
        """修改同步策略"""
        self.pxSchedTbl.xSchedTblSyncStrategy=p0;
        if(p0=='EXPLICIT'):
            self.spbxSchedTblMaxAdvance.setDisabled(False);
            self.spbxSchedTblMaxRetard.setDisabled(False);
            self.spbxSchedTblPrecision.setDisabled(False);
        else:
            self.spbxSchedTblMaxAdvance.setDisabled(True);
            self.spbxSchedTblMaxRetard.setDisabled(True);
            self.spbxSchedTblPrecision.setDisabled(True);
    
    @pyqtSignature("int")
    def on_spbxSchedTblMaxAdvance_valueChanged(self, p0):
        """修改最大允许前进值"""
        self.pxSchedTbl.xSchedTblMaxAdvance=p0;
    
    @pyqtSignature("int")
    def on_spbxSchedTblMaxRetard_valueChanged(self, p0):
        """修改最大允许后退值"""
        self.pxSchedTbl.xSchedTblMaxRetard=p0;
    
    @pyqtSignature("int")
    def on_spbxSchedTblPrecision_valueChanged(self, p0):
        """修改精度"""
        self.pxSchedTbl.xSchedTblExplicitPrecision=p0;
