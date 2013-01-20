# -*- coding: utf-8 -*-

from PyQt4.QtGui import QMainWindow, QFileDialog
from PyQt4.QtGui import QTreeWidgetItem, QMessageBox
from PyQt4.QtCore import QStringList,QString
from PyQt4.QtCore import pyqtSignature
from PyQt4 import QtCore, QtGui
import os
from Ui_wmain import Ui_wMainClass
from GaInOS_SchedTbl import DlgScheduleTable
from GaInOS import *
from GaInOsGen import *
from  GaInOsSaveAndLoadXml import *
from GaInOsCfgCheck import *

#配置 默认文件路径及文件名称
#'%s/%s'%(ROOT_DIR,DFT_CFG_FILE)
if(os.name=='nt'):
    ROOT_DIR='F:/parai@foxmail.com/nt/GaInOS/osek_test'
else:
    ROOT_DIR='/home'
DFT_CFG_FILE='GaInOsCfg.xml'


class wMainClass(QMainWindow, Ui_wMainClass):
    """
    MaIn Window For GaInOS.
    """
    def __init__(self, parent = None):
        #成员变量初始化
        self.pxCurSelTreeItem=None;
        self.pxCurSelGaInOsObj=None;
        self.pxGaInOSTaskCfgList=[];
        self.xTaskNum=0;
        self.pxGaInOSCounterCfgList=[];
        self.xCounterNum=0;
        self.pxGaInOSAlarmCfgList=[];
        self.xAlarmNum=0;
        self.pxGaInOSResList=[];
        self.xResNum=0;
        self.pxGaInOSInResList=[];
        self.xInResNum=0;
        self.pxGaInOSScheduleTableList=[];
        self.xSchedTblNum=0;
        self.pxCurSelInResAddTreeItem=None;
        self.pxCurSelInResRemoveTreeItem=None;
        self.xGaInOSGeneralCfg=GaInOsGeneral();
        self.xCfgFile='';
        
        QMainWindow.__init__(self, parent);
        self.setupUi(self);
        self.setWindowTitle('GaInOS Studio(parai@foxmail.com)');
        #初始化菜单
        self.vDoMenuInit();
        #/*配置GaInOS中断最大优先级，及其初始值*/
        self.spbxMaxIpl.setRange(0,255);
        self.spbxMaxIpl.setValue(7);
        self.spbxMaxIpl.setRange(0, 15);
        #/*配置GaInOS任务最大优先级，及其初始值*/
        self.spbxMaxPrio.setRange(0,63);
        self.spbxMaxPrio.setValue(63);
        #/*配置GaInOS任务堆栈范围*/
        self.spbxTskStkSize.setRange(32,10240);

        #/*禁止GaInOS 任务配置相关控件，因为初始时没有任务*/
        #/*默认初始GaInOS任务类型为BCC1*/
        self.spbxTskMaxActivateCount.setDisabled(True);
        self.cmbxTskType.setDisabled(True);
        #/*默认初始GaInOS任务调度策略为FULL_PREEMPTIVE_SCHEDULE*/
        self.cbxTskPreemtable.setDisabled(True);
        self.btnDel.setDisabled(True);
        #禁止所有Tab页
        self.vDisableAllTab();
        #文件管理控件初始化
        self.leFileOpened.setDisabled(True);
        #禁止Schedule table 编辑模式
        self.pteSchedTblInfo.setReadOnly(True);
        #由于做到了自动化，控件禁止,有时间的话，把这些冗余的东西去掉
        self.cbxAlarm.setDisabled(True);
        self.cbxRes.setDisabled(True);
        self.cbxInRes.setDisabled(True);

    def vDoPrintInfoOfTaskCfg(self):
        for tsk in self.pxGaInOSTaskCfgList:
            tsk.printInfo();

    def vDoPrintInfoOfEventCfg(self, tsk):
        for event in tsk.xTaskEventList:
            event.printInfo();

    def vDoPrintInfoOfCounterCfg(self):
        for cnt in self.pxGaInOSCounterCfgList:
            cnt.printInfo();

    def vDoPrintInfoOfAlarmCfg(self):
        for alm in self.pxGaInOSAlarmCfgList:
            alm.printInfo();

    def vDoPrintInfoOfResCfg(self):
        for res in self.pxGaInOSResList:
            res.printInfo();

    def vDoPrintInfoOfInResCfg(self):
        for inRes in self.pxGaInOSInResList:
            inRes.printInfo();

    def vDoPrintInfoOfSchedTblCfg(self):
        for tbl in self.pxGaInOSScheduleTableList:
            tbl.printInfo();

    def listInseartTask(self, xTask):
        """Add a Task to list"""
        self.pxGaInOSTaskCfgList.append(xTask);

    def listMoveTaskToHead(self, xTask):
        """移动一个现有的Task到头部"""
        self.pxGaInOSTaskCfgList.remove(xTask);
        self.pxGaInOSTaskCfgList.insert(0, xTask);

    def listMoveTaskToTail(self, xTask):
        """移动一个现有的Task到尾部"""
        self.pxGaInOSTaskCfgList.remove(xTask);
        self.pxGaInOSTaskCfgList.append(xTask);

    def listInseartCounter(self, xCounter):
        """Add a Counter to list"""
        self.pxGaInOSCounterCfgList.append(xCounter);

    def listInseartAlarm(self, xAlarm):
        """Add a Alarm to list"""
        self.pxGaInOSAlarmCfgList.append(xAlarm);

    def listInseartResource(self, xRes):
        """Add a Resource to list"""
        self.pxGaInOSResList.append(xRes);

    def listInseartInResource(self, xInRes):
        """Add a Internal Resource to list"""
        self.pxGaInOSInResList.append(xInRes);
 
    def listInseartSchedTbl(self, xSchedTbl):
        """add a schedule table to list"""
        self.pxGaInOSScheduleTableList.append(xSchedTbl);

    def vDoDelEvent(self, parent, index):
        #QTreeWidgetItem* parent
        #int index;    the index of child item in parent
        tsk=self.vFindOutTask(parent.text(0));
        tsk.xTaskEventList.remove(self.pxCurSelGaInOsObj);
        #调试
        #self.vDoPrintInfoOfEventCfg(tsk);
    
    def vDoDelAndReSelectGaInOsObj(self, parent, index):
        """删除选中的GaInOS 对象"""
        #QTreeWidgetItem* parent
        #int index;    the index of child item in parent
        #根据父节点判断
        if(self.trGaInOsCfgList.indexOfTopLevelItem(parent)==0):
            #删除任务
            self.pxGaInOSTaskCfgList.remove(self.pxCurSelGaInOsObj);
            #打印信息，调试用
            #self.vDoPrintInfoOfTaskCfg();
        elif(self.trGaInOsCfgList.indexOfTopLevelItem(parent)==1):
            #删除资源
            self.pxGaInOSResList.remove(self.pxCurSelGaInOsObj);
            if(len(self.pxGaInOSResList)==0):
                self.cbxRes.setChecked(False);
            #打印信息，调试用
            #self.vDoPrintInfoOfResCfg();
        elif(self.trGaInOsCfgList.indexOfTopLevelItem(parent)==2):
            #删除内部资源
            self.pxGaInOSInResList.remove(self.pxCurSelGaInOsObj);
            #若果有任务被分配了改内部资源，取消分配
            for tsk in self.pxGaInOSTaskCfgList:
                if((tsk.xTaskWithInRes==True) and (tsk.xTaskInResName==self.pxCurSelGaInOsObj.xInResName)):
                    tsk.xTaskWithInRes=False;
                    tsk.xTaskInResName=None;
            if(len(self.pxGaInOSInResList)==0):
                self.cbxInRes.setChecked(False);
            #打印信息，调试用
            #self.vDoPrintInfoOfInResCfg();
        elif(self.trGaInOsCfgList.indexOfTopLevelItem(parent)==3):
            #删除计数器
            self.pxGaInOSCounterCfgList.remove(self.pxCurSelGaInOsObj);
            #打印信息，调试用
            #self.vDoPrintInfoOfCounterCfg();
        elif(self.trGaInOsCfgList.indexOfTopLevelItem(parent)==4):
            #删除报警器
            self.pxGaInOSAlarmCfgList.remove(self.pxCurSelGaInOsObj);
            if(len(self.pxGaInOSAlarmCfgList)==0):
                self.cbxAlarm.setChecked(False);
            #打印信息，调试用
            #self.vDoPrintInfoOfAlarmCfg();
        elif(self.trGaInOsCfgList.indexOfTopLevelItem(parent)==5):
            #删除调度表
            self.pxGaInOSScheduleTableList.remove(self.pxCurSelGaInOsObj);
            #self.vDoPrintInfoOfSchedTblCfg();
        elif(self.trGaInOsCfgList.indexOfTopLevelItem(parent.parent())==0):
            #删除事件
            self.vDoDelEvent(parent, index);

    def vEnableTab(self, xIndex):
        """使能xIndex指向的Tab页"""
        for i in  range(0, 7):
            if(i==xIndex):
                self.tblGaInOsCfg.setTabEnabled(i, True);
                self.tblGaInOsCfg.setCurrentIndex(i);
            else:
                self.tblGaInOsCfg.setTabEnabled(i, False);

    def vDisableAllTab(self):
        """进制所有的Tab页"""
        for i in  range(0, 7):
            self.tblGaInOsCfg.setTabEnabled(i, False);

    def vFindOutTask(self, xName):
        """从任务链表中找到任务，每个任务的名称唯一"""
        for tsk in self.pxGaInOSTaskCfgList:
            if(xName == tsk.xTaskName):
                return tsk;
        return None;

    def vFindOutCounter(self, xName):
        """从计数器链表中找到计数器，每个计数器的名称唯一"""
        for cnt in self.pxGaInOSCounterCfgList:
            if(xName == cnt.xCounterName):
                return cnt;
        return None;

    def vFindOutCounterID(self, xName):
        """从计数器链表中找到计数器ID，每个计数器的名称唯一"""
        id=0
        for cnt in self.pxGaInOSCounterCfgList:
            if(xName == cnt.xCounterName):
                return id;
            else:
                id+=1;
        #no found
        return 0xDEADBEEF; 

    def vFindOutAlarm(self, xName):
        """从报警器链表中找到报警器，每个报警器的名称唯一"""
        for alm in self.pxGaInOSAlarmCfgList:
            if(xName == alm.xAlarmName):
                return alm;
        return None;

    def vFindOutEvent(self, tsk, xEventName):
        """从任务的事件列表中找到事件"""
        for ent in tsk.xTaskEventList:
            if(ent.xEventName==xEventName):
                return ent;
        return None;

    def vFindOutRes(self, xResName):
        """找到资源"""
        for res in self.pxGaInOSResList:
            if(xResName==res.xResName):
                return res;
        return None;

    def vFindOutInRes(self, xInResName):
        """找到内部资源"""
        for inRes in self.pxGaInOSInResList:
            if(xInResName==inRes.xInResName):
                return inRes;
        return None;

    def vFindOutSchedTbl(self, xSchedTblName):
        """找到调度表"""
        for tbl in self.pxGaInOSScheduleTableList:
            if(xSchedTblName==tbl.xScheduleTableName):
                return tbl;
        return None;

    def vDoRefreshSpbxTskMaxActCnt(self, xOSConfCls, tsk):
        """刷新任务的最大激活次数控件"""
        if(xOSConfCls == 'BCC2'):
            self.spbxTskMaxActivateCount.setDisabled(False);
        elif(xOSConfCls=='ECC2' ):
            if(tsk.xTaskType=='BASIC_TASK'):
                self.spbxTskMaxActivateCount.setDisabled(False);
            else:
                tsk.xTaskMaxActivateCount=1;
                self.spbxTskMaxActivateCount.setDisabled(True);
        else:
            tsk.xTaskMaxActivateCount=1;
            self.spbxTskMaxActivateCount.setDisabled(True);
        self.spbxTskMaxActivateCount.setValue(tsk.xTaskMaxActivateCount);

    def vDoRefreshcmbxAlarmOwner(self):
        """刷新Alarm Tab的 Alarm Owner 控件"""
        self.cmbxAlarmOwner.clear();
        for cnt in self.pxGaInOSCounterCfgList:
            self.cmbxAlarmOwner.addItem(cnt.xCounterName);

    def vDoRefreshcmbxAlarmTask(self, condition):
        """刷新Alarm Tab的 Alarm Task 控件"""
        #该控件被复用，根据Alarm选择类型而定
        #condition ：if true，then add all of the tasks
        #if false, Only add the extended tasks
        alm=self.pxCurSelGaInOsObj;
        self.cmbxAlarmTask.clear();
        flag=False;
        index=0;
        for tsk in self.pxGaInOSTaskCfgList:
            #print(tsk.xTaskName);
            if(condition==True or tsk.xTaskType=='EXTEND_TASK'):
                self.cmbxAlarmTask.addItem(tsk.xTaskName);
                if(alm.xAlarmTask==tsk.xTaskName):
                    self.cmbxAlarmTask.setCurrentIndex(index);
                    flag=True;
                index+=1;
        if(flag==False):
            self.cmbxAlarmTask.setCurrentIndex(-1);

    def vDoRefreshcmbxAlarmEvent(self):
        """刷新Alarm Tab的 Alarm Event 控件"""
        alm=self.pxCurSelGaInOsObj;
        tsk=self.vFindOutTask(alm.xAlarmTask);
        self.cmbxAlarmEvent.clear();
        if(tsk!=None):
            flag=False;
            index=0;
            for ent in tsk.xTaskEventList:
                self.cmbxAlarmEvent.addItem(ent.xEventName);
                if(alm.xAlarmEvent==ent.xEventName):
                    self.cmbxAlarmEvent.setCurrentIndex(index);
                    flag=True;
                index+=1;
            if(flag==False):
                self.cmbxAlarmEvent.setCurrentIndex(-1);

    def vDoRefreshTaskTab(self, tsk):
        #tsk.prtintInfo();
        self.pxCurSelGaInOsObj=tsk;
        self.leTskName.setText(tsk.xTaskName);
        self.spbxTskStkSize.setValue(tsk.xTaskStackSize);
        if(tsk.xTaskType=='EXTEND_TASK'):
            self.cmbxTskType.setCurrentIndex(1);
        else:
            self.cmbxTskType.setCurrentIndex(0);
        self.spbxTskPrio.setValue(tsk.xTaskPriority);
        self.vDoRefreshSpbxTskMaxActCnt(self.xGaInOSGeneralCfg.xOSConfCls, tsk);
        self.cbxTskAutoStart.setChecked(tsk.xTaskAutoStart );
        self.cbxTskPreemtable.setChecked(tsk.xTaskPreemtable);

    def vDoRefreshCounterTab(self, cnt):
        #cnt.printInfo();
        self.pxCurSelGaInOsObj=cnt;
        self.leCntName.setText(cnt.xCounterName);
        self.spbxCntMaxAllowedValue.setValue(cnt.xCounterMaxAllowValue);
        self.spbxCntTickBase.setValue(cnt.xCounterTickPerBase);
        self.spbxCntMinCycle.setValue(cnt.xCounterMinCycle);

    def vDoRefreshAlarmTab(self, alm):
        self.pxCurSelGaInOsObj=alm;
        self.leAlarmName.setText(alm.xAlarmName);
        #刷新啊Alarm Owner 控件
        self.vDoRefreshcmbxAlarmOwner();
        id=self.vFindOutCounterID(alm.xAlarmOwner);
        if(id == 0xDEADBEEF):
            QMessageBox(QMessageBox.Information, 'GaInOS Info', 
                'The Counter %s assigned to Alarm %s has been deleted or name changed,roolback to %s.'%(
                    alm.xAlarmOwner, 
                    alm.xAlarmName, 
                    self.pxGaInOSCounterCfgList[0].xCounterName)).exec_();
            id=0;
            alm.xAlarmOwner=self.pxGaInOSCounterCfgList[0].xCounterName;
        self.cmbxAlarmOwner.setCurrentIndex(id);
        #刷新Alarm Type 控件
        if(alm.xAlarmType=='ALARM_CALLBACK'):
            id=0;
            self.leAlarmCbk.setText(alm.xAlarmCbk);
            self.leAlarmCbk.setDisabled(False);
            self.cmbxAlarmTask.setDisabled(True);
            self.cmbxAlarmEvent.setDisabled(True);
        if(alm.xAlarmType=='ALARM_TASK'):
            id=1;
            self.vDoRefreshcmbxAlarmTask(True);
            self.cmbxAlarmEvent.setDisabled(True);
            self.cmbxAlarmTask.setDisabled(False);
            self.leAlarmCbk.setDisabled(True);
            self.lblAlarmTask.setText('Alarm Activate Task:');
        if(alm.xAlarmType=='ALARM_EVENT'):
            id=2;
            self.vDoRefreshcmbxAlarmTask(False);
            self.vDoRefreshcmbxAlarmEvent();
            self.leAlarmCbk.setDisabled(True);
            self.cmbxAlarmTask.setDisabled(False);
            self.cmbxAlarmEvent.setDisabled(False);
            self.lblAlarmTask.setText('Alarm Event Task:');
        self.cmbxAlarmType.setCurrentIndex(id);

    def vDoRefreshEventTab(self, ent):
        self.pxCurSelGaInOsObj=ent;
        self.leEventName.setText(ent.xEventName);
        self.leEventMask.setText('%s'%(ent.xEventMask));

    def vDoRefreshResTab(self, res):
        self.pxCurSelGaInOsObj=res;
        self.leResName.setText(res.xResName);
        self.spbxResCeilPrio.setValue(res.xResCeilPriority);

    def vDoRefreshtrInResAssignedAndAvailableTask(self):
        self.trInResAssignedTask.clear();
        self.trInResAvailableTask.clear();
        for tsk in self.pxGaInOSTaskCfgList:
            name=QString('%s'%(tsk.xTaskName));
            if(tsk.xTaskWithInRes==False):
                pxTreeIlem=QTreeWidgetItem(self.trInResAvailableTask,QStringList(name));
                self.trInResAvailableTask.addTopLevelItem (pxTreeIlem);
            elif(tsk.xTaskInResName==self.pxCurSelGaInOsObj.xInResName):
                pxTreeIlem=QTreeWidgetItem(self.trInResAssignedTask,QStringList(name));
                self.trInResAssignedTask.addTopLevelItem (pxTreeIlem);

    def vDoRefreshInResTab(self, inRes):
        self.pxCurSelGaInOsObj=inRes;
        self.leInResName.setText(inRes.xInResName);
        self.spbxInResCeilPrio.setValue(inRes.xInResCeilPriority);
        self.vDoRefreshtrInResAssignedAndAvailableTask();
        #禁止相关控件
        self.btnInResAdd.setDisabled(True);
        self.btnInResRemove.setDisabled(True);

    def vDoRefreshSchedTblTab(self, tbl):
        """刷新调度表控制页，显示信息"""
        self.pxCurSelGaInOsObj=tbl;
        self.leSchedTblName.setText(tbl.xScheduleTableName);
        #self.pteSchedTblInfo.clear();
        self.pteSchedTblInfo.setPlainText(tbl.toString());

    def vDoRefreshTab(self, item):
        #QTreeWidgetItem* item
        #当前点击的为一个子节点，根据父节点判断
        if(self.trGaInOsCfgList.indexOfTopLevelItem(item.parent())==0):
            tsk=self.vFindOutTask(item.text(0));
            self.vDoRefreshTaskTab(tsk);
        elif(self.trGaInOsCfgList.indexOfTopLevelItem(item.parent())==1):
            res=self.vFindOutRes(item.text(0));
            self.vDoRefreshResTab(res);
        elif(self.trGaInOsCfgList.indexOfTopLevelItem(item.parent())==2):
            inRes=self.vFindOutInRes(item.text(0));
            self.vDoRefreshInResTab(inRes);
        elif(self.trGaInOsCfgList.indexOfTopLevelItem(item.parent())==3):
            cnt=self.vFindOutCounter(item.text(0));
            self.vDoRefreshCounterTab(cnt);
        elif(self.trGaInOsCfgList.indexOfTopLevelItem(item.parent())==4):
            alm=self.vFindOutAlarm(item.text(0));
            self.vDoRefreshAlarmTab(alm);
        elif(self.trGaInOsCfgList.indexOfTopLevelItem(item.parent())==5):
            tbl=self.vFindOutSchedTbl(item.text(0));
            self.vDoRefreshSchedTblTab(tbl);
        elif(self.trGaInOsCfgList.indexOfTopLevelItem(item)==-1):
            tsk=self.vFindOutTask(item.parent().text(0));
            ent=self.vFindOutEvent(tsk, item.text(0));
            self.vDoRefreshEventTab(ent);

    def vDoTabChange(self, item):
        #QTreeWidgetItem* item  
        #Current Task is Selected
        if(self.trGaInOsCfgList.topLevelItem(0).isSelected()):
            self.vDisableAllTab();
            self.btnDel.setDisabled(True);
        #Current Resource is Selected
        elif(self.trGaInOsCfgList.topLevelItem(1).isSelected()):
            self.vDisableAllTab();
            self.btnDel.setDisabled(True);
        #Current Internal Resource is Selected
        elif(self.trGaInOsCfgList.topLevelItem(2).isSelected()):
            self.vDisableAllTab();
            self.btnDel.setDisabled(True);
        #Current Counter is Selected
        elif(self.trGaInOsCfgList.topLevelItem(3).isSelected()):
            self.vDisableAllTab();
            self.btnDel.setDisabled(True);
        #Current ALarm is Selected
        elif(self.trGaInOsCfgList.topLevelItem(4).isSelected()):
            self.vDisableAllTab();
            self.btnDel.setDisabled(True);
        #Current Schedule Table is Selected
        elif(self.trGaInOsCfgList.topLevelItem(5).isSelected()):
            self.vDisableAllTab();
            self.btnDel.setDisabled(True);
        #当前点击的为一个子节点，根据父节点判断
        elif(self.trGaInOsCfgList.indexOfTopLevelItem(item.parent())==0):
            self.vEnableTab(0);
            self.btnDel.setDisabled(False);
        elif(self.trGaInOsCfgList.indexOfTopLevelItem(item.parent())==1):
            self.vEnableTab(1);
            self.btnDel.setDisabled(False);
        elif(self.trGaInOsCfgList.indexOfTopLevelItem(item.parent())==2):
            self.vEnableTab(2);
            self.btnDel.setDisabled(False);
        elif(self.trGaInOsCfgList.indexOfTopLevelItem(item.parent())==3):
            self.vEnableTab(3);
            self.btnDel.setDisabled(False);
        elif(self.trGaInOsCfgList.indexOfTopLevelItem(item.parent())==4):
            self.vEnableTab(4);
            self.btnDel.setDisabled(False);
        elif(self.trGaInOsCfgList.indexOfTopLevelItem(item.parent())==5):
            self.vEnableTab(5); 
            self.btnDel.setDisabled(False);
        else:
            self.vEnableTab(6);
            self.btnDel.setDisabled(False);

    def vAddTask(self):
        #/*添加一个任务节点，使用默认名称*/
        self.xTaskNum+=1;
        defaultTskName=QString('vTask%d'%(self.xTaskNum));
        pxTreeIlem=QTreeWidgetItem(self.pxCurSelTreeItem,QStringList(defaultTskName));
        self.pxCurSelTreeItem.addChild(pxTreeIlem);
        #/*新增一个任务对象*/
        xTask=GaInOsTask(defaultTskName,self.xTaskNum);
        #添加任务到链表中
        self.listInseartTask(xTask);
        #展开任务配置树
        self.pxCurSelTreeItem.setExpanded(True);

    def vDoAddEvent(self):
        tsk=self.pxCurSelGaInOsObj;
        if(len(tsk.xTaskEventList)<16):
            tsk.xTaskEventNum+=1;
            defaultEntName=QString('%sEvent%s'%(tsk.xTaskName, tsk.xTaskEventNum));
            pxTreeIlem=QTreeWidgetItem(self.pxCurSelTreeItem,QStringList(defaultEntName));
            self.pxCurSelTreeItem.addChild(pxTreeIlem);
            self.pxCurSelTreeItem.setExpanded(True);
            tsk.xTaskEventList.append(GaInOsEvent(defaultEntName, hex(1<<(tsk.xTaskEventNum-1))));

    def vAddRes(self):
        if(self.xGaInOSGeneralCfg.xOSUseRes==False):
            self.cbxRes.setChecked(True);
        #添加一个资源节点
        self.xResNum+=1;
        defaultCntName=QString('vRes%s'%(self.xResNum));
        pxTreeIlem=QTreeWidgetItem(self.pxCurSelTreeItem,QStringList(defaultCntName));
        self.pxCurSelTreeItem.addChild(pxTreeIlem);
        xRes=GaInOsResource(defaultCntName, self.xGaInOSGeneralCfg.xOSMaxPriority);
        #添加资源到链表中
        self.listInseartResource(xRes);
        #展开资源配置树
        self.pxCurSelTreeItem.setExpanded(True);
        #调试
        #self.vDoPrintInfoOfResCfg();

    def vAddInRes(self):
        if(self.xGaInOSGeneralCfg.xOSUseInRes==False):
            self.cbxInRes.setChecked(True);
        #添加一个资源节点
        self.xInResNum+=1;
        defaultCntName=QString('vInRes%s'%(self.xInResNum));
        pxTreeIlem=QTreeWidgetItem(self.pxCurSelTreeItem,QStringList(defaultCntName));
        self.pxCurSelTreeItem.addChild(pxTreeIlem);
        xInRes=GaInOsInResource(defaultCntName, self.xGaInOSGeneralCfg.xOSMaxPriority);
        #添加资源到链表中
        self.listInseartInResource(xInRes);
        #展开资源配置树
        self.pxCurSelTreeItem.setExpanded(True);
        #调试
        #self.vDoPrintInfoOfInResCfg();

    def vAddCounter(self):
        #添加一个计数器节点
        self.xCounterNum+=1;
        defaultCntName=QString('vCounter%s'%(self.xCounterNum));
        pxTreeIlem=QTreeWidgetItem(self.pxCurSelTreeItem,QStringList(defaultCntName));
        self.pxCurSelTreeItem.addChild(pxTreeIlem);
        #/*新增一个计数器对象*/
        xCounter=GaInOsCounter(defaultCntName);
        #添加计数器到链表中
        self.listInseartCounter(xCounter);
        #展开计数器配置树
        self.pxCurSelTreeItem.setExpanded(True);

    def vAddAlarm(self):
        if(len(self.pxGaInOSCounterCfgList)==0):
            QMessageBox(QMessageBox.Information, 'GaInOS Info', 
                'To use Alarm,At least One Counter must be added and configured!').exec_();
        else:
            if(self.xGaInOSGeneralCfg.xOSUseAlarm==False):
                self.cbxAlarm.setChecked(True);
            #添加一个定时器节点
            self.xAlarmNum+=1;
            defaultAlmName=QString('vAlarm%s'%(self.xAlarmNum));
            pxTreeIlem=QTreeWidgetItem(self.pxCurSelTreeItem,QStringList(defaultAlmName));
            self.pxCurSelTreeItem.addChild(pxTreeIlem);
            #/*新增一个定时器对象*/
            xAlarm=GaInOsAlarm(defaultAlmName, 
                    self.pxGaInOSCounterCfgList[0].xCounterName);
            #添加定时器到链表中
            self.listInseartAlarm(xAlarm);
            #展开定时器配置树
            self.pxCurSelTreeItem.setExpanded(True); 

    def vAddScheduleTable(self):
        if(len(self.pxGaInOSCounterCfgList)==0):
            QMessageBox(QMessageBox.Information, 'GaInOS Info', 
                'To use Schedule Table,At least One Counter must be added and configured!').exec_();
        else:
            #添加一个调度表节点
            self.xSchedTblNum+=1;
            defaultName=QString('vSchedTbl%s'%(self.xSchedTblNum));
            pxTreeIlem=QTreeWidgetItem(self.pxCurSelTreeItem,QStringList(defaultName));
            self.pxCurSelTreeItem.addChild(pxTreeIlem);
            #新增一个调度表对象
            xSchedTbl=GaInOsScheduleTable(defaultName);
            #添加调度表到链表中
            self.listInseartSchedTbl(xSchedTbl);
            #展开调度表配置树
            self.pxCurSelTreeItem.setExpanded(True);

    @pyqtSignature("QString")
    def on_leSchedTblName_textChanged(self, p0): 
        if(self.pxCurSelGaInOsObj!=None):
            self.pxCurSelGaInOsObj.xScheduleTableName=p0;
            self.pxCurSelTreeItem.setText(0, p0);

    @pyqtSignature("")
    def on_btnCfgSchedEp_clicked(self):
        """Detailly configure the expiry point for Schedule Table"""
        dlg = DlgScheduleTable(self);
        dlg.exec_();
        self.vDoRefreshSchedTblTab(self.pxCurSelGaInOsObj);
        
    @pyqtSignature("")
    def on_btnAdd_clicked(self):
        #Current Task is Selected
        if(self.trGaInOsCfgList.topLevelItem(0).isSelected()):
            self.vAddTask();
        #Current Resource is Selected
        elif(self.trGaInOsCfgList.topLevelItem(1).isSelected()):
            self.vAddRes();
        #Current Internal Resource is Selected
        elif(self.trGaInOsCfgList.topLevelItem(2).isSelected()):
            self.vAddInRes();
        #Current Counter is Selected
        elif(self.trGaInOsCfgList.topLevelItem(3).isSelected()):
            self.vAddCounter();
        #Current ALarm is Selected
        elif(self.trGaInOsCfgList.topLevelItem(4).isSelected()):
            self.vAddAlarm();
        #Current Schedule Table is Selected
        elif(self.trGaInOsCfgList.topLevelItem(5).isSelected()):
            self.vAddScheduleTable();
        #Current A Task Item is selected
        elif(self.pxCurSelTreeItem):
            if(self.trGaInOsCfgList.indexOfTopLevelItem(
                    self.pxCurSelTreeItem.parent())==0):
                if(self.xGaInOSGeneralCfg.xOSConfCls=='ECC1' or
                   self.xGaInOSGeneralCfg.xOSConfCls=='ECC2'):
                       tsk=self.vFindOutTask(self.pxCurSelTreeItem.text(0));
                       if(tsk.xTaskType=='EXTEND_TASK'):
                            self.vDoAddEvent();
    
    @pyqtSignature("")
    def on_btnDel_clicked(self):
        """删除所选中的GaInOS配置项"""
        parent=self.pxCurSelTreeItem.parent();
        index=parent.indexOfChild(self.pxCurSelTreeItem);
        parent.takeChild(index);
        #删除相应GaInOS对象
        self.vDoDelAndReSelectGaInOsObj(parent, index);
        #释放内存，重新赋值
        del self.pxCurSelTreeItem;
        if(index>0):
            parent.child(index-1).setSelected(True);
            self.pxCurSelTreeItem=parent.child(index-1);
            self.vDoRefreshTab(parent.child(index-1));            
        else:
            self.pxCurSelTreeItem=parent;
            self.vDisableAllTab();
            self.btnDel.setDisabled(True);

    def vDoGetBasePath(self, fullname):
        part=fullname.split('/');
        path='';
        for i in range(0, len(part)-1):
           path+=part[i]+'/';
        return path;

    @pyqtSignature("")
    def on_btnGen_clicked(self):
        """开始生成文件"""
        #首先保存配置文件(XML)
        if(self.xCfgFile==''):
            self.vDoSaveXmlCfgFile();
        else:
        #检查配置是否正确
            chk=GaInOsCfgCheck(self);
            print(chk.vCheckMessage);
            if(chk.vCheckResult==False):
                QMessageBox(QMessageBox.Information, 'GaInOS Info', 
                    '%s'%(chk.vCheckMessage)).exec_();
                return;
            else:
                QMessageBox(QMessageBox.Information, 'GaInOS Info', 
                    '^_^ No Error! ^_^\n%s'%(chk.vCheckMessage)).exec_();
        #开始生成配置文件
        if(self.xCfgFile!=''):
            if(os.name=='nt'):
                path=os.path.dirname(self.xCfgFile.toUtf8());
            else:
                path=self.vDoGetBasePath(self.xCfgFile.toUtf8());
            #print('path=%s'%(path))
            if(os.path.isfile('%s/CfgObj.h'%(path))):
                dlg=QMessageBox(QMessageBox.Question, 'GaInOS Warning', 
                        'Cfg C File Already Exist! Do Override Them Or Not?', 
                        QMessageBox.Yes|QMessageBox.No);
                if(dlg.exec_()==QMessageBox.No):
                    return;
            GaInOsGen(path, self);
            QMessageBox(QMessageBox.Information, 'GaInOS Info', 
                'Cfg Code Generated in %s !'%(path)).exec_();

    @pyqtSignature("")
    def on_btnFileSave_clicked(self):
        self.vDoSaveXmlCfgFile();
    
    @pyqtSignature("")
    def on_btnFileOpen_clicked(self):
        self.vDoOpenXmlCfgFile();

    @pyqtSignature("")
    def on_btnCheck_clicked(self):
        chk=GaInOsCfgCheck(self);
        print(chk.vCheckMessage);
        if(chk.vCheckResult==False):
            QMessageBox(QMessageBox.Information, 'GaInOS Info', 
                '%s'%(chk.vCheckMessage)).exec_();
        else:
            QMessageBox(QMessageBox.Information, 'GaInOS Info', 
                '^_^ No Error! ^_^\n%s'%(chk.vCheckMessage)).exec_();

    @pyqtSignature("QTreeWidgetItem*, int")
    def on_trGaInOsCfgList_itemClicked(self, item, column):
        #保存点击选中的Item指针
        self.pxCurSelTreeItem=item;
        #根据Item选择设置相应的配置页为活动页
        self.vDoTabChange(item);
        #根据Item刷新相应的控制页
        self.vDoRefreshTab(item);

#GaInOS General Configure
    @pyqtSignature("int")
    def on_spbxMaxIpl_valueChanged(self, p0):
        """修改GaInOS 中断最大优先级"""
        self.xGaInOSGeneralCfg.xOSMaxIpl=p0;
        if(self.xGaInOSGeneralCfg.xOSIsr2UseRes==True):
            self.spbxResCeilPrio.setRange(0, p0+self.xGaInOSGeneralCfg.xOSMaxIpl);

    @pyqtSignature("int")
    def on_spbxMaxPrio_valueChanged(self, p0):
        """修改GaInOS 任务最大优先级"""
        self.xGaInOSGeneralCfg.xOSMaxPriority=p0;
        self.spbxTskPrio.setRange(0,p0);
        if(self.xGaInOSGeneralCfg.xOSIsr2UseRes==True):
            self.spbxResCeilPrio.setRange(0, p0+self.xGaInOSGeneralCfg.xOSMaxIpl);
        else:
            self.spbxResCeilPrio.setRange(0, p0);
        self.spbxInResCeilPrio.setRange(0, p0);

    @pyqtSignature("QString")
    def on_cmbxStatus_currentIndexChanged(self, p0):
        """修改GaInOS 调试状态等级"""
        self.xGaInOSGeneralCfg.xOSStatusLevel=p0;

    def vDoDelAllEventTreeItemOfTask(self, tsk):
        """删除所有配置的任务事件并刷新界面"""
        xTree=self.trGaInOsCfgList.topLevelItem(0);
        for index in range(0, xTree.childCount()):
            xTaskTree=xTree.child(index);
            if(tsk.xTaskName==xTaskTree.text(0)):
                for index in range(0, xTaskTree.childCount()):
                    xTaskTree.takeChild(0);
                break;
        tsk.xTaskEventList=[];
        tsk.xTaskEventNum=0;

    def vDoRollbackAllTaskToBasic(self):
        """将所有任务改变为BASIC_TASK"""
        for tsk in self.pxGaInOSTaskCfgList:
            if(tsk.xTaskType=='EXTEND_TASK'):
                tsk.xTaskType='BASIC_TASK';
                if(len(tsk.xTaskEventList)>0):
                    self.vDoDelAllEventTreeItemOfTask(tsk);
            try:
                self.vDoRefreshTab(self.pxCurSelTreeItem);
            except:
                print 'Error in vDoRollbackAllTaskToBasic().'

    @pyqtSignature("QString")
    def on_cmbxCpuType_currentIndexChanged(self, p0):
        """修改GaInOS目标平台CPU类型"""
        self.xGaInOSGeneralCfg.xOSCpuType=p0;
        if(self.xGaInOSGeneralCfg.xOSCpuType=='MC9S12(X)'):
            self.spbxMaxIpl.setRange(0, 7);
        elif(self.xGaInOSGeneralCfg.xOSCpuType=='ARM920T'):
            self.spbxMaxIpl.setRange(0, 256);
        elif(self.xGaInOSGeneralCfg.xOSCpuType=='C166'):
            self.spbxMaxIpl.setRange(0, 15); 
        elif(self.xGaInOSGeneralCfg.xOSCpuType=='Tri-Core'):
            self.spbxMaxIpl.setRange(0, 15);
            QMessageBox(QMessageBox.Information, 'GaInOS Info', 
                '%s,%s,%s,%s,%s.\n%s'%(
                    'As Tri-Core\'s special CSA function',
                    'So a Basic Task named "vTaskIdle" should be configured in priority 0',
                    'only vTaskIdle in priority 0 and should be autostarted',  
                    'and vTaskIdle should never Terminate itself',
                    'but some idle work can be added in the Idle loop',  
                    'TASK(vTaskIdle)\n{\n    for(;;)\n    {\n        /* Add Some Idle Work Here. */\n    }\n}\n')).exec_();
        
    @pyqtSignature("QString")
    def on_cmbxOSConfCls_currentIndexChanged(self, p0):
        """修改GaInOS 最高任务类型"""
        #从高到低的转变提示，并抉择
        if(self.xGaInOSGeneralCfg.xOSConfCls=='ECC1' or
           self.xGaInOSGeneralCfg.xOSConfCls=='ECC2'):
               if(p0=='BCC1' or p0=='BCC2'):
                    dlg=QMessageBox(QMessageBox.Question, 'GaInOS Warning', 
                        'Do You Really Want To Rollback All Tasks To Basic Task!', 
                        QMessageBox.Yes|QMessageBox.No);
                    if(dlg.exec_()==QMessageBox.Yes):
                        self.vDoRollbackAllTaskToBasic();
                    else:
                        if(self.xGaInOSGeneralCfg.xOSConfCls=='ECC1'):
                            self.cmbxOSConfCls.setCurrentIndex(2);
                        else:
                            self.cmbxOSConfCls.setCurrentIndex(3);
                        return;
        #改变GaInOS最高任务类型
        self.xGaInOSGeneralCfg.xOSConfCls=p0;
        if(p0=='ECC1' or p0 == 'ECC2'):
            self.cmbxTskType.setDisabled(False);
            if(self.cmbxAlarmType.count()==2):
                self.cmbxAlarmType.addItem('ALARM_EVENT');
        elif(p0=='BCC1' or p0 == 'BCC2'):
            self.cmbxTskType.setDisabled(True);
            if(self.cmbxAlarmType.count()==3):
                self.cmbxAlarmType.removeItem(2);
        try:
            self.vDoRefreshSpbxTskMaxActCnt(p0, self.pxCurSelGaInOsObj);
        except:
            print "Error."

    @pyqtSignature("QString")
    def on_cmbxSchedPolicy_currentIndexChanged(self, p0):
        """修改GaInOS任务调度策略"""
        self.xGaInOSGeneralCfg.xOSSchedPolicy=p0;
        if(p0=='MIXED_PREEMPTIVE_SCHEDULE'):
            self.cbxTskPreemtable.setDisabled(False);
        else:
            self.cbxTskPreemtable.setDisabled(True);

    @pyqtSignature("bool")
    def on_cbxRes_toggled(self, checked):
        """修改GaInOS 是否使用普通资源"""
        self.xGaInOSGeneralCfg.xOSUseRes=checked;

    @pyqtSignature("bool")
    def on_cbxInRes_toggled(self, checked):
        """修改GaInOS 是否使用内部资源"""
        self.xGaInOSGeneralCfg.xOSUseInRes=checked;

    @pyqtSignature("bool")
    def on_cbxIsrUseRes_toggled(self, checked):
        """修改GaInOS 中断ISR2是否使用普通资源"""
        self.xGaInOSGeneralCfg.xOSIsr2UseRes=checked;
        if(checked==True):
            self.spbxResCeilPrio.setRange(0, 
                self.xGaInOSGeneralCfg.xOSMaxIpl+self.xGaInOSGeneralCfg.xOSMaxPriority);
        else:
            self.spbxResCeilPrio.setRange(0, self.xGaInOSGeneralCfg.xOSMaxPriority);

    @pyqtSignature("bool")
    def on_cbxAlarm_toggled(self, checked):
        """修改GaInOS 是否使用Alarm"""
        self.xGaInOSGeneralCfg.xOSUseAlarm=checked;

#GaInOS Task Configure
    @pyqtSignature("QString")
    def on_leTskName_textChanged(self, p0):
        """修改GaInOS 任务名称"""
        self.pxCurSelTreeItem.setText(0, p0);
        if(self.pxCurSelGaInOsObj!=None):
            self.pxCurSelGaInOsObj.xTaskName=p0;
   
    @pyqtSignature("int")
    def on_spbxTskPrio_valueChanged(self, p0):
        """修改GaInOS 任务的优先级"""
        if(self.pxCurSelGaInOsObj!=None):
            self.pxCurSelGaInOsObj.xTaskPriority=p0;

    @pyqtSignature("int")
    def on_spbxTskStkSize_valueChanged(self, p0):
        """修改GaInOS 任务堆栈大小"""
        if(self.pxCurSelGaInOsObj!=None):
            self.pxCurSelGaInOsObj.xTaskStackSize=p0;

    @pyqtSignature("QString")
    def on_cmbxTskType_currentIndexChanged(self, p0):
        """修改GaInOS 任务类型"""
        if(self.pxCurSelGaInOsObj!=None):
            if(self.pxCurSelGaInOsObj.xTaskType=='EXTEND_TASK' and
               p0=='BASIC_TASK'):
                dlg=QMessageBox(QMessageBox.Question, 'GaInOS Warning', 
                        'Do You Really Want To Change The Task To Basic Task?', 
                        QMessageBox.Yes|QMessageBox.No);
                if(dlg.exec_()==QMessageBox.Yes):
                    self.vDoDelAllEventTreeItemOfTask(self.pxCurSelGaInOsObj);
                else:
                    self.cmbxTskType.setCurrentIndex(1);
                    return;
        self.pxCurSelGaInOsObj.xTaskType=p0;
        self.vDoRefreshSpbxTskMaxActCnt(self.xGaInOSGeneralCfg.xOSConfCls, 
            self.pxCurSelGaInOsObj);

    @pyqtSignature("int")
    def on_spbxTskMaxActivateCount_valueChanged(self, p0):
        """修改GaInOS 任务的最大激活次数"""
        if(self.pxCurSelGaInOsObj!=None):
            self.pxCurSelGaInOsObj.xTaskMaxActivateCount=p0; 

    @pyqtSignature("bool")
    def on_cbxTskAutoStart_toggled(self, checked):
        """修改GaInOS 任务是否自启动"""
        if(self.pxCurSelGaInOsObj!=None):
            self.pxCurSelGaInOsObj.xTaskAutoStart =checked;

    @pyqtSignature("bool")
    def on_cbxTskPreemtable_toggled(self, checked):
        """修改GaInOS 任务是否可剥夺"""
        if(self.pxCurSelGaInOsObj!=None):
            self.pxCurSelGaInOsObj.xTaskPreemtable=checked;

#GaInOS Counter 配置
    @pyqtSignature("QString")
    def on_leCntName_textChanged(self, p0):
        """修改GaInOS 计数器名称"""
        self.pxCurSelTreeItem.setText(0, p0);
        if(self.pxCurSelGaInOsObj!=None):
            self.pxCurSelGaInOsObj.xCounterName=p0;

    @pyqtSignature("int")
    def on_spbxCntMaxAllowedValue_valueChanged(self, p0):
        """修改GaInOS计数器计数上限值"""
        if(self.pxCurSelGaInOsObj!=None):
            self.pxCurSelGaInOsObj.xCounterMaxAllowValue=p0;
    
    @pyqtSignature("int")
    def on_spbxCntTickBase_valueChanged(self, p0):
        """修改GaInOS 计数器计数基数"""
        if(self.pxCurSelGaInOsObj!=None):
            self.pxCurSelGaInOsObj.xCounterTickPerBase=p0;
    
    @pyqtSignature("int")
    def on_spbxCntMinCycle_valueChanged(self, p0):
        """修改GaInOS 计数器最小周期"""
        if(self.pxCurSelGaInOsObj!=None):
            self.pxCurSelGaInOsObj.xCounterMinCycle=p0;

#GaInOS Alarm 配置
    @pyqtSignature("QString")
    def on_leAlarmName_textChanged(self, p0):
        """配置GaInOS 报警器的名称"""
        self.pxCurSelTreeItem.setText(0, p0);
        if(self.pxCurSelGaInOsObj!=None):
            self.pxCurSelGaInOsObj.xAlarmName=p0;

    @pyqtSignature("QString")
    def on_cmbxAlarmOwner_currentIndexChanged(self, p0):
        """配置GaInOS 报警器的所有者"""
        if(self.pxCurSelGaInOsObj!=None):
            self.pxCurSelGaInOsObj.xAlarmOwner=p0;
    
    @pyqtSignature("QString")
    def on_cmbxAlarmType_currentIndexChanged(self, p0):
        """配置GaInOS 报警器的类型"""
        if(self.pxCurSelGaInOsObj!=None):
            self.pxCurSelGaInOsObj.xAlarmType=p0;
            self.vDoRefreshAlarmTab(self.pxCurSelGaInOsObj);
    
    @pyqtSignature("QString")
    def on_cmbxAlarmTask_activated(self, p0):
        """配置GaInOS 报警器的任务"""
        if(self.pxCurSelGaInOsObj!=None):
            self.pxCurSelGaInOsObj.xAlarmTask=p0;
            self.vDoRefreshAlarmTab(self.pxCurSelGaInOsObj);
    
    @pyqtSignature("QString")
    def on_cmbxAlarmEvent_currentIndexChanged(self, p0):
        """配置GaInOS 报警器的事件"""
        if(self.pxCurSelGaInOsObj!=None):
            self.pxCurSelGaInOsObj.xAlarmEvent=p0;

#GaInOS Resource 配置
    @pyqtSignature("QString")
    def on_leResName_textChanged(self, p0):
        """修改资源名称"""
        self.pxCurSelTreeItem.setText(0, p0);
        if(self.pxCurSelGaInOsObj!=None):
            self.pxCurSelGaInOsObj.xResName=p0;
    
    @pyqtSignature("int")
    def on_spbxResCeilPrio_valueChanged(self, p0):
        """修改资源的天花板优先级"""
        if(self.pxCurSelGaInOsObj!=None):
            self.pxCurSelGaInOsObj.xResCeilPriority=p0;

#GaInOS Internal Resource 配置
    @pyqtSignature("QString")
    def on_leInResName_textChanged(self, p0):
        """修改内部资源的名称"""
        self.pxCurSelTreeItem.setText(0, p0);
        if(self.pxCurSelGaInOsObj!=None):
            oldName=self.pxCurSelGaInOsObj.xInResName;
            count=self.trInResAssignedTask.topLevelItemCount();
            for index in range(0, count):
                tsk=self.vFindOutTask(self.trInResAssignedTask.topLevelItem(index).text(0));
                if(tsk.xTaskInResName==oldName):  
                    tsk.xTaskInResName=p0;
            self.pxCurSelGaInOsObj.xInResName=p0;
    
    @pyqtSignature("int")
    def on_spbxInResCeilPrio_valueChanged(self, p0):
        """配置内部资源的天花板优先级"""
        if(self.pxCurSelGaInOsObj!=None):
            self.pxCurSelGaInOsObj.xInResCeilPriority=p0;
    
    @pyqtSignature("QTreeWidgetItem*, int")
    def on_trInResAssignedTask_itemClicked(self, item, column):
        """选择一个已经分配内部资源的任务准备移除"""
        self.pxCurSelInResRemoveTreeItem=item;
        self.btnInResAdd.setDisabled(True);
        self.btnInResRemove.setDisabled(False);
    
    @pyqtSignature("QTreeWidgetItem*, int")
    def on_trInResAvailableTask_itemClicked(self, item, column):
        """选择一个可选的任务准备分配给内部资源"""
        self.pxCurSelInResAddTreeItem=item;
        self.btnInResAdd.setDisabled(False);
        self.btnInResRemove.setDisabled(True);
    
    @pyqtSignature("")
    def on_btnInResAdd_clicked(self):
        """为当前内部资源分配任务"""
        if(self.pxCurSelInResAddTreeItem!=None):
            tsk=self.vFindOutTask(self.pxCurSelInResAddTreeItem.text(0));
            tsk.xTaskWithInRes=True;
            tsk.xTaskInResName=self.pxCurSelGaInOsObj.xInResName;
            self.listMoveTaskToHead(tsk);
            index=self.trInResAvailableTask.indexOfTopLevelItem(self.pxCurSelInResAddTreeItem);
            self.trInResAvailableTask.takeTopLevelItem(index);
            name=QString('%s'%(tsk.xTaskName));
            pxTreeIlem=QTreeWidgetItem(self.trInResAssignedTask,QStringList(name));
            self.trInResAssignedTask.addTopLevelItem(pxTreeIlem);
            del self.pxCurSelInResAddTreeItem;
            self.pxCurSelInResAddTreeItem=self.trInResAvailableTask.topLevelItem(0);
            if(self.pxCurSelInResAddTreeItem==None):
                self.btnInResAdd.setDisabled(True);

    @pyqtSignature("")
    def on_btnInResRemove_clicked(self):
        """为当前内部资源移除已经分配的任务"""
        if(self.pxCurSelInResRemoveTreeItem!=None):
            tsk=self.vFindOutTask(self.pxCurSelInResRemoveTreeItem.text(0));
            tsk.xTaskWithInRes=False;
            tsk.xTaskInResName=None;
            self.listMoveTaskToTail(tsk);
            index=self.trInResAssignedTask.indexOfTopLevelItem(self.pxCurSelInResRemoveTreeItem);
            self.trInResAssignedTask.takeTopLevelItem(index);
            name=QString('%s'%(tsk.xTaskName));
            pxTreeIlem=QTreeWidgetItem(self.trInResAvailableTask,QStringList(name));
            self.trInResAvailableTask.addTopLevelItem(pxTreeIlem);
            del self.pxCurSelInResRemoveTreeItem;
            self.pxCurSelInResRemoveTreeItem=self.trInResAssignedTask.topLevelItem(0);
            if(self.pxCurSelInResRemoveTreeItem==None):
                self.btnInResRemove.setDisabled(True);

#GaInOS Event 的配置
    @pyqtSignature("QString")
    def on_leEventName_textChanged(self, p0):
        """修改事件名称"""
        self.pxCurSelTreeItem.setText(0, p0);
        if(self.pxCurSelGaInOsObj!=None):
            self.pxCurSelGaInOsObj.xEventName=p0;
   
    @pyqtSignature("QString")
    def on_leEventMask_textChanged(self, p0):
        """修改事件掩码"""
        if(self.pxCurSelGaInOsObj!=None):
            self.pxCurSelGaInOsObj.xEventMask=p0;

#GaInOS Studio Menu Action
    def vDoMenuInit(self):
        """关联快捷键"""
        self.actionOpen.setShortcut('Ctrl+O');
        self.actionSave.setShortcut('Ctrl+S');
        self.actionSave_As.setShortcut('Ctrl+Shift+S');
        self.actionNew.setShortcut('Ctrl+N');

    def vDoNewXmlCfgFile(self):
        """新建配置文件"""
        file=QFileDialog.getSaveFileName(self, 'New GaInOS Configure File.', 
            '%s/%s'%(ROOT_DIR,DFT_CFG_FILE), 'GaInOsCfgFile(*.xml)');
        if(file!=''):
            self.xCfgFile=file;
            self.leFileOpened.setText(file);
            GaInOsNewXml(self, file);
            QMessageBox(QMessageBox.Information, 'GaInOS Info', 
                'Create New Configure file <%s> Done!'%(file)).exec_();

    def vDoOpenXmlCfgFile(self):
        """加载配置文件"""
        file=QFileDialog.getOpenFileName(self, 'Open GaInOS Configure File.', 
                '%s/%s'%(ROOT_DIR,DFT_CFG_FILE), 'GaInOsCfgFile(*.xml)');
        if(file!=''):
            self.xCfgFile=file;
            self.leFileOpened.setText(file);
            GaInOsLoadXml(self, file);
            QMessageBox(QMessageBox.Information, 'GaInOS Info', 
                'Load Configure File <%s> Done!'%(file)).exec_();

    def vDoSaveXmlCfgFile(self):
        """保存配置文件"""
        chk=GaInOsCfgCheck(self);
        if(chk.vCheckResult==False):
            QMessageBox(QMessageBox.Information, 'GaInOS Info', 
                '%s'%(chk.vCheckMessage)).exec_();
            print(chk.vCheckMessage);
        else:
            if(self.xCfgFile==''):
                file=QFileDialog.getSaveFileName(self, 'Save GaInOS Configure File.', 
                    '%s/%s'%(ROOT_DIR,DFT_CFG_FILE), 'GaInOsCfgFile(*.xml)');
                self.xCfgFile=file;
            if(self.xCfgFile!=''):
                self.leFileOpened.setText(self.xCfgFile);
                GaInOsSaveXml(self, self.xCfgFile);
                QMessageBox(QMessageBox.Information, 'GaInOS Info', 
                    'Save Configure File <%s> Done!'%(self.xCfgFile)).exec_();

    def vDoSaveAsXmlCfgFile(self):
        """另存配置文件"""
        chk=GaInOsCfgCheck(self);
        if(chk.vCheckResult==False):
            QMessageBox(QMessageBox.Information, 'GaInOS Info', 
                '%s'%(chk.vCheckMessage)).exec_();
            print(chk.vCheckMessage);
        else:
            file=QFileDialog.getSaveFileName(self, 'Save GaInOS Configure File As ...', 
                '%s/%s'%(ROOT_DIR,DFT_CFG_FILE), 'GaInOsCfgFile(*.xml)');
            if(file!=''):
                self.xCfgFile=file;
                self.leFileOpened.setText(file);
                GaInOsSaveXml(self, file);
                QMessageBox(QMessageBox.Information, 'GaInOS Info', 
                    'Save As Configure File <%s> Done!'%(file)).exec_();

    @pyqtSignature("")
    def on_actionNew_triggered(self):
        """新建一个GaInOS配置文件"""
        self.vDoNewXmlCfgFile();
    
    @pyqtSignature("")
    def on_actionOpen_triggered(self):
        """加载配置文件"""
        self.vDoOpenXmlCfgFile();
    
    @pyqtSignature("")
    def on_actionSave_triggered(self):
        """保存配置文件"""
        self.vDoSaveXmlCfgFile();
    
    @pyqtSignature("")
    def on_actionSave_As_triggered(self):
        """另存配置文件"""
        self.vDoSaveAsXmlCfgFile();
    
    @pyqtSignature("")
    def on_actionQuit_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv);
    wMainWin = wMainClass();
    wMainWin.show()
    sys.exit(app.exec_())
