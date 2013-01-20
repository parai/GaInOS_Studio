# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from PyQt4.QtGui import QTreeWidgetItem, QMessageBox
from PyQt4.QtCore import QStringList,QString
import sys
from GaInOS import *

def vIsTrue(str):
    if(str=='True'):
        return True;
    else:
        return False;

def vGetConfClsIndex(cls):
    if(cls=='BCC1'):
        return 0;
    elif(cls=='BCC2'):
        return 1;
    elif(cls=='ECC1'):
        return 2;
    elif(cls=='ECC2'):
        return 3;
    else:
        return -1;

def vGetCpuTypeIndex(type):
    if(type=='MC9S12(X)'):
        return 0;
    elif(type=='ARM920T'):
        return 1;
    elif(type=='C166'):
        return 2; 
    elif(type=='Tri-Core'):
        return 3; 
    else:
        return -1;

def vGetStatusIndex(status):
    if(status=='OS_STATUS_STANDARD'):
        return 0;
    elif(status=='OS_STATUS_EXTENED'):
        return 1;
    else:
        return -1;

def vGetSchedIndex(sched):
    if(sched=='FULL_PREEMPTIVE_SCHEDULE'):
        return 0;
    elif(sched=='MIXED_PREEMPTIVE_SCHEDULE'):
        return 1;
    elif(sched=='NONE_PREEMPTIVE_SCHEDULE'):
        return 2;
    else:
        return -1;

class GaInOsSaveXml():
    def __init__(self, parent, xmlFile):
        #保存传入的参数
        self.parent=parent;
        self.fp=open(xmlFile, 'w');
        self.fp.write('<?xml version="1.0" encoding="utf-8"?>\n<GaInOsCfg>\n');
        self.GaInOsSaveGeneralCfg();
        self.GaInOsSaveTaskCfg();
        self.GaInOsSaveResCfg();
        self.GaInOsSaveInResCfg();
        self.GaInOsSaveCounterCfg();
        self.GaInOsSaveAlarmCfg();
        self.GaInOsSaveSchedTblCfg();
        self.fp.write('</GaInOsCfg>\n');

    def GaInOsSaveGeneralCfg(self):
        self.fp.write('\t<GaInOsGeneralCfg>\n');
        self.fp.write('\t\t<GaInOsCpuType>%s</GaInOsCpuType>\n'%(self.parent.xGaInOSGeneralCfg.xOSCpuType));
        self.fp.write('\t\t<GaInOsMaxIpl>%s</GaInOsMaxIpl>\n'%(self.parent.xGaInOSGeneralCfg.xOSMaxIpl));
        self.fp.write('\t\t<GaInOsMaxPriority>%s</GaInOsMaxPriority>\n'%(self.parent.xGaInOSGeneralCfg.xOSMaxPriority));
        self.fp.write('\t\t<GaInOsConfCls>%s</GaInOsConfCls>\n'%(self.parent.xGaInOSGeneralCfg.xOSConfCls));
        self.fp.write('\t\t<GaInOsSchedPolicy>%s</GaInOsSchedPolicy>\n'%(self.parent.xGaInOSGeneralCfg.xOSSchedPolicy));
        self.fp.write('\t\t<GaInOsStatusLevel>%s</GaInOsStatusLevel>\n'%(self.parent.xGaInOSGeneralCfg.xOSStatusLevel));
        self.fp.write('\t\t<GaInOsUseAlarm>%s</GaInOsUseAlarm>\n'%(self.parent.xGaInOSGeneralCfg.xOSUseAlarm));
        self.fp.write('\t\t<GaInOsUseInRes>%s</GaInOsUseInRes>\n'%(self.parent.xGaInOSGeneralCfg.xOSUseInRes));
        self.fp.write('\t\t<GaInOsUseRes>%s</GaInOsUseRes>\n'%(self.parent.xGaInOSGeneralCfg.xOSUseRes));
        self.fp.write('\t\t<GaInOsIsr2UseRes>%s</GaInOsIsr2UseRes>\n'%(self.parent.xGaInOSGeneralCfg.xOSIsr2UseRes));
        self.fp.write('\t</GaInOsGeneralCfg>\n\n');

    def GaInOsSaveTaskCfg(self):
        self.fp.write('\t<GaInOsTaskCfg>\n');
        for tsk in self.parent.pxGaInOSTaskCfgList:
            self.fp.write('\t\t<GaInOsTask>\n');
            self.fp.write('\t\t\t<TaskName>%s</TaskName>\n'%(tsk.xTaskName));
            self.fp.write('\t\t\t<TaskType>%s</TaskType>\n'%(tsk.xTaskType));
            self.fp.write('\t\t\t<TaskPriority>%s</TaskPriority>\n'%(tsk.xTaskPriority));
            self.fp.write('\t\t\t<TaskStackSize>%s</TaskStackSize>\n'%(tsk.xTaskStackSize));
            self.fp.write('\t\t\t<TaskMaxActCnt>%s</TaskMaxActCnt>\n'%(tsk.xTaskMaxActivateCount));
            self.fp.write('\t\t\t<TaskAutoStart>%s</TaskAutoStart>\n'%(tsk.xTaskAutoStart));
            self.fp.write('\t\t\t<TaskPreemtable>%s</TaskPreemtable>\n'%(tsk.xTaskPreemtable));
            self.fp.write('\t\t\t<TaskWithInRes>%s</TaskWithInRes>\n'%(tsk.xTaskWithInRes));
            self.fp.write('\t\t\t<TaskInResName>%s</TaskInResName>\n'%(tsk.xTaskInResName));
            self.fp.write('\t\t\t<TaskEventList>\n');
            if(tsk.xTaskType=='EXTEND_TASK'):
                for ent in tsk.xTaskEventList:
                    self.fp.write('\t\t\t\t<TaskEvent name=\'%s\' mask=\'%s\'></TaskEvent>\n'%(ent.xEventName,ent.xEventMask));
            self.fp.write('\t\t\t</TaskEventList>\n');
            self.fp.write('\t\t</GaInOsTask>\n');
        self.fp.write('\t</GaInOsTaskCfg>\n');

    def GaInOsSaveResCfg(self):
        self.fp.write('\t<GaInOsResourceCfg>\n');
        for res in self.parent.pxGaInOSResList:
            self.fp.write('\t\t<GaInOsRes name=\'%s\' ceilprio=\'%s\'></GaInOsRes>\n'%(res.xResName,res.xResCeilPriority));
        self.fp.write('\t</GaInOsResourceCfg>\n\n');

    def GaInOsSaveInResCfg(self):
        self.fp.write('\t<GaInOsInternalResourceCfg>\n');
        for res in self.parent.pxGaInOSInResList:
            self.fp.write('\t\t<GaInOsInRes name=\'%s\' ceilprio=\'%s\'></GaInOsInRes>\n'%(res.xInResName,res.xInResCeilPriority));
        self.fp.write('\t</GaInOsInternalResourceCfg>\n\n');

    def GaInOsSaveCounterCfg(self):
        self.fp.write('\t<GaInOsCounterCfg>\n');
        for cnt in self.parent.pxGaInOSCounterCfgList:
            self.fp.write('\t\t<GaInOsCounter>\n');
            self.fp.write('\t\t\t<CounterName>%s</CounterName>\n'%(cnt.xCounterName));
            self.fp.write('\t\t\t<CounterMaxAllowValue>%s</CounterMaxAllowValue>\n'%(cnt.xCounterMaxAllowValue));
            self.fp.write('\t\t\t<CounterMinCycle>%s</CounterMinCycle>\n'%(cnt.xCounterMinCycle));
            self.fp.write('\t\t\t<CounterTickPerBase>%s</CounterTickPerBase>\n'%(cnt.xCounterTickPerBase));
            self.fp.write('\t\t</GaInOsCounter>\n'%());
        self.fp.write('\t</GaInOsCounterCfg>\n\n');

    def GaInOsSaveAlarmCfg(self):
        self.fp.write('\t<GaInOsAlarmCfg>\n');
        for alm in self.parent.pxGaInOSAlarmCfgList:
            self.fp.write('\t\t<GaInOsAlarm>\n');
            self.fp.write('\t\t\t<AlarmName>%s</AlarmName>\n'%(alm.xAlarmName));
            self.fp.write('\t\t\t<AlarmOwner>%s</AlarmOwner>\n'%(alm.xAlarmOwner));
            self.fp.write('\t\t\t<AlarmType>%s</AlarmType>\n'%(alm.xAlarmType));
            self.fp.write('\t\t\t<AlarmCbk>%s</AlarmCbk>\n'%(alm.xAlarmCbk));
            self.fp.write('\t\t\t<AlarmTask>%s</AlarmTask>\n'%(alm.xAlarmTask));
            self.fp.write('\t\t\t<AlarmEvent>%s</AlarmEvent>\n'%(alm.xAlarmEvent));
            self.fp.write('\t\t</GaInOsAlarm>\n');
        self.fp.write('\t</GaInOsAlarmCfg>\n\n');
    
    def GaInOsSaveSchedTblCfg(self):
        self.fp.write('\t<GaInOsScheduleTableCfg>\n');
        for tbl in self.parent.pxGaInOSScheduleTableList:
            self.fp.write('\t\t<GaInOsScheduleTable name=\'%s\' '%(tbl.xScheduleTableName));
            self.fp.write('repeatable=\'%s\' '%(tbl.xSchedTblRepeatable));
            self.fp.write('counter=\'%s\' '%(tbl.xSchedTblDrivingCounter));
            self.fp.write('autostartable=\'%s\' '%(tbl.xSchedTblAutostartable));
            self.fp.write('autostarttype=\'%s\' '%(tbl.xSchedTblAutostartType));
            self.fp.write('absrelvalue=\'%s\' '%(tbl.xSchedTblAbsRelValue));
            self.fp.write('finaldelay=\'%s\' '%(tbl.xSchedTblFinalDelay));
            self.fp.write('strategy=\'%s\' '%(tbl.xSchedTblSyncStrategy));
            self.fp.write('max_advance=\'%s\' '%(tbl.xSchedTblMaxAdvance));
            self.fp.write('max_retard=\'%s\' '%(tbl.xSchedTblMaxRetard));
            self.fp.write('precision=\'%s\'>\n'%(tbl.xSchedTblExplicitPrecision));
            for ep in tbl.xSchedTblEpList:
                self.fp.write('\t\t\t<ExpiryPoint offset=\'%s\'>\n'%(ep[0]));
                for epsub in ep[1]:
                    self.fp.write('\t\t\t\t<Action>%s</Action>\n'%(epsub));
                self.fp.write('\t\t\t</ExpiryPoint>\n');
            self.fp.write('\t\t</GaInOsScheduleTable>\n');
        self.fp.write('\t</GaInOsScheduleTableCfg>\n\n');
    
class GaInOsLoadXml():
    def __init__(self, parent, xmlFile):
        #保存传入的参数
        self.parent=parent;
        try:  
            self.xmlRoot= ET.parse(xmlFile).getroot();
        except Exception, e: 
            QMessageBox(QMessageBox.Information, 'GaInOS Info', 
                'Invalid Configure File');
            return -1;
        self.GaInOsLoadGeneralCfg();
        self.GaInOsLoadTaskCfg();
        self.GaInOsLoadInResCfg();
        self.GaInOsLoadResCfg();
        self.GaInOsLoadCounterCfg();
        self.GaInOsLoadAlarmCfg();
        self.GaInOsLoadSchedTblCfg();

    def GaInOsLoadGeneralCfg(self):
        cfgNode=self.xmlRoot.find('GaInOsGeneralCfg');
        self.parent.xGaInOSGeneralCfg.xOSCpuType=cfgNode.find('GaInOsCpuType').text;
        self.parent.xGaInOSGeneralCfg.xOSMaxIpl=int(cfgNode.find('GaInOsMaxIpl').text);
        self.parent.xGaInOSGeneralCfg.xOSMaxPriority=int(cfgNode.find('GaInOsMaxPriority').text);
        self.parent.xGaInOSGeneralCfg.xOSConfCls=cfgNode.find('GaInOsConfCls').text;
        self.parent.xGaInOSGeneralCfg.xOSSchedPolicy=cfgNode.find('GaInOsSchedPolicy').text;
        self.parent.xGaInOSGeneralCfg.xOSStatusLevel=cfgNode.find('GaInOsStatusLevel').text;
        self.parent.xGaInOSGeneralCfg.xOSUseAlarm=vIsTrue(cfgNode.find('GaInOsUseAlarm').text);
        self.parent.xGaInOSGeneralCfg.xOSUseInRes=vIsTrue(cfgNode.find('GaInOsUseInRes').text);
        self.parent.xGaInOSGeneralCfg.xOSIsr2UseRes=vIsTrue(cfgNode.find('GaInOsIsr2UseRes').text);
        self.parent.xGaInOSGeneralCfg.xOSUseRes=vIsTrue(cfgNode.find('GaInOsUseRes').text);
        
        #刷新界面
        self.parent.spbxMaxIpl.setValue(self.parent.xGaInOSGeneralCfg.xOSMaxIpl);
        self.parent.spbxMaxPrio.setValue(self.parent.xGaInOSGeneralCfg.xOSMaxPriority);
        self.parent.cmbxOSConfCls.setCurrentIndex(vGetConfClsIndex(self.parent.xGaInOSGeneralCfg.xOSConfCls));
        self.parent.cmbxStatus.setCurrentIndex(vGetStatusIndex(self.parent.xGaInOSGeneralCfg.xOSStatusLevel));
        self.parent.cmbxSchedPolicy.setCurrentIndex(vGetSchedIndex(self.parent.xGaInOSGeneralCfg.xOSSchedPolicy));
        self.parent.cbxRes.setChecked(self.parent.xGaInOSGeneralCfg.xOSUseRes);
        self.parent.cbxInRes.setChecked(self.parent.xGaInOSGeneralCfg.xOSUseInRes);
        self.parent.cbxIsrUseRes.setChecked(self.parent.xGaInOSGeneralCfg.xOSIsr2UseRes);
        self.parent.cbxAlarm.setChecked(self.parent.xGaInOSGeneralCfg.xOSUseAlarm);
        self.parent.cmbxCpuType.setCurrentIndex(vGetCpuTypeIndex(self.parent.xGaInOSGeneralCfg.xOSCpuType));
        if(self.parent.xGaInOSGeneralCfg.xOSCpuType=='MC9S12(X)'):
            self.parent.spbxMaxIpl.setRange(0, 7);
        if(self.parent.xGaInOSGeneralCfg.xOSCpuType=='ARM'):
            self.parent.spbxMaxIpl.setRange(0, 256);
        if(self.parent.xGaInOSGeneralCfg.xOSCpuType=='C166'):
            self.parent.spbxMaxIpl.setRange(0, 15);            
        #刷新报警器类型控件
        if(self.parent.xGaInOSGeneralCfg.xOSConfCls=='ECC1' or self.parent.xGaInOSGeneralCfg.xOSConfCls == 'ECC2'):
            self.parent.cmbxTskType.setDisabled(False);
            if(self.parent.cmbxAlarmType.count()==2):
                self.parent.cmbxAlarmType.addItem('ALARM_EVENT');
        elif(self.parent.xGaInOSGeneralCfg.xOSConfCls=='BCC1' or self.parent.xGaInOSGeneralCfg.xOSConfCls == 'BCC2'):
            self.parent.cmbxTskType.setDisabled(True);
            if(self.parent.cmbxAlarmType.count()==3):
                self.parent.cmbxAlarmType.removeItem(2);
        #刷新任务激活次数控件
        if(self.parent.xGaInOSGeneralCfg.xOSSchedPolicy=='MIXED_PREEMPTIVE_SCHEDULE'):
            self.parent.cbxTskPreemtable.setDisabled(False);
        else:
            self.parent.cbxTskPreemtable.setDisabled(True);

    def GaInOsLoadTaskCfg(self):
        del self.parent.pxGaInOSTaskCfgList;
        self.parent.pxGaInOSTaskCfgList=[];
        self.parent.xTaskNum=0;
        cfgNode=self.xmlRoot.find('GaInOsTaskCfg');
        for tskNode in cfgNode:
            tskName=tskNode.find('TaskName').text;
            tskPriority=int(tskNode.find('TaskPriority').text);
            tsk=GaInOsTask(tskName, tskPriority);
            tsk.xTaskType=tskNode.find('TaskType').text;
            tsk.xTaskStackSize=int(tskNode.find('TaskStackSize').text);
            tsk.TaskMaxActivateCount=int(tskNode.find('TaskMaxActCnt').text);
            tsk.xTaskAutoStart=vIsTrue(tskNode.find('TaskAutoStart').text);
            tsk.xTaskPreemtable=vIsTrue(tskNode.find('TaskPreemtable').text);
            tsk.xTaskWithInRes=vIsTrue(tskNode.find('TaskWithInRes').text);
            tsk.xTaskInResName=tskNode.find('TaskInResName').text;
            for eventNode in tskNode .find('TaskEventList'):
                ent=GaInOsEvent(eventNode.attrib['name'], eventNode.attrib['mask']);
                #ent.printInfo();
                tsk.xTaskEventList.append(ent);
                tsk.xTaskEventNum+=1;
            #分配有内部资源的任务应该为与头部。
            #但加载时默认认为xml文件中任务的顺序是预期值。
            self.parent.pxGaInOSTaskCfgList.append(tsk);
            self.parent.xTaskNum+=1;
            #tsk.printInfo();
        #刷新界面
        TreeIlem=self.parent.trGaInOsCfgList.topLevelItem(0);
        for index in range(0, TreeIlem.childCount()):
            temp=TreeIlem.takeChild(0);
            del temp;
        for tsk in self.parent.pxGaInOSTaskCfgList:
            defaultTskName=QString(tsk.xTaskName);
            tskTreeItem=QTreeWidgetItem(TreeIlem,QStringList(defaultTskName));
            for ent in tsk.xTaskEventList:
                defaultTskName=QString(ent.xEventName);
                QTreeWidgetItem(tskTreeItem,QStringList(defaultTskName));
        TreeIlem.setExpanded(True);

    def GaInOsLoadInResCfg(self):
        del self.parent.pxGaInOSInResList;
        self.parent.pxGaInOSInResList=[];
        self.parent.xInResNum=0;
        cfgNode=self.xmlRoot.find('GaInOsInternalResourceCfg');
        for inResNode in cfgNode:
            inRes=GaInOsInResource(inResNode.attrib['name'], 
                            int(inResNode.attrib['ceilprio'] ));
            self.parent.pxGaInOSInResList.append(inRes);
            self.parent.xInResNum+=1;
         #刷新界面
        TreeIlem=self.parent.trGaInOsCfgList.topLevelItem(2);
        for index in range(0, TreeIlem.childCount()):
            temp=TreeIlem.takeChild(0);
            del temp;
        for inRes in self.parent.pxGaInOSInResList:
            defaultName=QString(inRes.xInResName);
            QTreeWidgetItem(TreeIlem,QStringList(defaultName));
        TreeIlem.setExpanded(True);

    def GaInOsLoadResCfg(self):
        del self.parent.pxGaInOSResList;
        self.parent.pxGaInOSResList=[];
        self.parent.xResNum=0;
        cfgNode=self.xmlRoot.find('GaInOsResourceCfg');
        for resNode in cfgNode:
            res=GaInOsResource(resNode.attrib['name'], 
                            int(resNode.attrib['ceilprio'] ));
            self.parent.pxGaInOSResList.append(res);
            self.parent.xResNum+=1;
        #刷新界面
        TreeIlem=self.parent.trGaInOsCfgList.topLevelItem(1);
        for index in range(0, TreeIlem.childCount()):
            temp=TreeIlem.takeChild(0);
            del temp;
        for res in self.parent.pxGaInOSResList:
            defaultName=QString(res.xResName);
            QTreeWidgetItem(TreeIlem,QStringList(defaultName));
        TreeIlem.setExpanded(True);

    def GaInOsLoadCounterCfg(self):
        del self.parent.pxGaInOSCounterCfgList;
        self.parent.pxGaInOSCounterCfgList=[];
        cfgNode=self.xmlRoot.find('GaInOsCounterCfg');
        for cntNode in cfgNode:
            cntName=cntNode.find('CounterName').text;
            cnt=GaInOsCounter(cntName);
            cnt.xCounterMaxAllowValue=int(cntNode.find('CounterMaxAllowValue').text);
            cnt.xCounterMinCycle=int(cntNode.find('CounterMinCycle').text);
            cnt.xCounterTickPerBase=int(cntNode.find('CounterTickPerBase').text);
            self.parent.pxGaInOSCounterCfgList.append(cnt);
        self.parent.xCounterNum=len(self.parent.pxGaInOSCounterCfgList);
        #刷新界面
        TreeIlem=self.parent.trGaInOsCfgList.topLevelItem(3);
        for index in range(0, TreeIlem.childCount()):
            temp=TreeIlem.takeChild(0);
            del temp;
        for cnt in self.parent.pxGaInOSCounterCfgList:
            defaultName=QString(cnt.xCounterName);
            QTreeWidgetItem(TreeIlem,QStringList(defaultName));
        TreeIlem.setExpanded(True);

    def GaInOsLoadAlarmCfg(self):
        del self.parent.pxGaInOSAlarmCfgList;
        self.parent.pxGaInOSAlarmCfgList=[];
        cfgNode=self.xmlRoot.find('GaInOsAlarmCfg');
        for almNode in cfgNode:
            almName=almNode.find('AlarmName').text;
            almOwner=almNode.find('AlarmOwner').text;
            alm=GaInOsAlarm(almName, almOwner);
            alm.xAlarmType=almNode.find('AlarmType').text;
            alm.xAlarmCbk=almNode.find('AlarmCbk').text;
            alm.xAlarmTask=almNode.find('AlarmTask').text;
            alm.xAlarmEvent=almNode.find('AlarmEvent').text;
            self.parent.pxGaInOSAlarmCfgList.append(alm);
        self.parent.xAlarmNum=len(self.parent.pxGaInOSAlarmCfgList);
        #刷新界面
        TreeIlem=self.parent.trGaInOsCfgList.topLevelItem(4);
        for index in range(0, TreeIlem.childCount()):
            temp=TreeIlem.takeChild(0);
            del temp;
        for alm in self.parent.pxGaInOSAlarmCfgList:
            defaultName=QString(alm.xAlarmName);
            QTreeWidgetItem(TreeIlem,QStringList(defaultName));
        TreeIlem.setExpanded(True);

    def vDoCheckBool(self, str):
        """根据字符串判断真假"""
        if('True'==str):
            return True;
        else:
            return False;

    def GaInOsLoadSchedTblCfg(self):
        """加载schedule table的配置"""
        del self.parent.pxGaInOSScheduleTableList;
        self.parent.pxGaInOSScheduleTableList=[];
        self.parent.xSchedTblNum=0;
        cfgNode=self.xmlRoot.find('GaInOsScheduleTableCfg');
        for tblNode in cfgNode:
            self.parent.xSchedTblNum+=1;
            tbl=GaInOsScheduleTable(tblNode.attrib['name']);
            tbl.xSchedTblRepeatable=self.vDoCheckBool(tblNode.attrib['repeatable']);
            tbl.xSchedTblDrivingCounter=tblNode.attrib['counter'];
            tbl.xSchedTblAutostartable=self.vDoCheckBool(tblNode.attrib['autostartable']);
            tbl.xSchedTblAutostartType=tblNode.attrib['autostarttype'];
            tbl.xSchedTblAbsRelValue=int(tblNode.attrib['absrelvalue']);
            tbl.xSchedTblFinalDelay=int(tblNode.attrib['finaldelay']);
            tbl.xSchedTblSyncStrategy=tblNode.attrib['strategy'];
            tbl.xSchedTblMaxAdvance=int(tblNode.attrib['max_advance']);
            tbl.xSchedTblMaxRetard=int(tblNode.attrib['max_retard']);
            tbl.xSchedTblExplicitPrecision=int(tblNode.attrib['precision']);
            eplist=[];
            for epNode in tblNode:
                epsub=[int(epNode.attrib['offset']), []];
                for epsubNode in epNode:
                    epsub[1].append(epsubNode.text);
                eplist.append(epsub);
            tbl.xSchedTblEpList=eplist;
            self.parent.pxGaInOSScheduleTableList.append(tbl);
        #刷新界面
        TreeIlem=self.parent.trGaInOsCfgList.topLevelItem(5);
        for index in range(0, TreeIlem.childCount()):
            temp=TreeIlem.takeChild(0);
            del temp;
        for tbl in self.parent.pxGaInOSScheduleTableList:
            defaultName=QString(tbl.xScheduleTableName);
            QTreeWidgetItem(TreeIlem,QStringList(defaultName));
        TreeIlem.setExpanded(True);

class GaInOsNewXml():
    def __init__(self, parent, xmlFile):
        self.parent=parent;
        self.vDoResetGaInOsCfg();
        GaInOsSaveXml(parent, xmlFile);
        GaInOsLoadXml(parent, xmlFile);
        
    def vDoResetGaInOsCfg(self):
        self.parent.xGaInOSGeneralCfg=GaInOsGeneral();
        del self.parent.pxGaInOSTaskCfgList;
        del self.parent.pxGaInOSResList;
        del self.parent.pxGaInOSInResList;
        del self.parent.pxGaInOSCounterCfgList;
        del self.parent.pxGaInOSAlarmCfgList;
        self.parent.pxGaInOSTaskCfgList=[];
        self.parent.xTaskNum=0;
        self.parent.pxGaInOSCounterCfgList=[];
        self.parent.xCounterNum=0;
        self.parent.pxGaInOSAlarmCfgList=[];
        self.parent.xAlarmNum=0;
        self.parent.pxGaInOSResList=[];
        self.parent.xResNum=0;
        self.parent.pxGaInOSInResList=[];
        self.parent.xInResNum=0;
        self.parent.pxGaInOSScheduleTableList=[];
        self.parent.xSchedTblNum=0;
        
