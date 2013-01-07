# -*- coding: utf-8 -*-
class GaInOsGeneral():
    def __init__(self):
        """
        """
        self.xOSCpuType='MC9S12(X)'
        self.xOSConfCls='BCC1';
        self.xOSMaxIpl=7;
        self.xOSMaxPriority=63;
        self.xOSSchedPolicy='FULL_PREEMPTIVE_SCHEDULE';
        self.xOSStatusLevel='OS_STATUS_STANDARD';
        self.xOSUseAlarm=False;
        self.xOSUseInRes=False;
        self.xOSIsr2UseRes=False;
        self.xOSUseRes=False;

class GaInOsEvent():
    def __init__(self, xName, xMask):
        self.xEventName=xName;
        self.xEventMask=xMask;
    
    def printInfo(self):
        print('%s,%s'%(self.xEventName, self.xEventMask));
    
class GaInOsTask():
    def __init__(self,xName,xPriority):
        self.xTaskName = xName;
        self.xTaskType  = 'BASIC_TASK';
        self.xTaskPriority  = xPriority;
        self.xTaskStackSize = 512;
        self.xTaskMaxActivateCount=1;
        self.xTaskAutoStart=True;
        self.xTaskPreemtable=True;
        self.xTaskEventList=[];
        self.xTaskEventNum=0;
        self.xTaskWithInRes=False;
        self.xTaskInResName=None;

    def printInfo(self):
        print('%s,%s,%s,%s,%s,%s,%s'%(self.xTaskName, self.xTaskType,self.xTaskPriority, 
                                self.xTaskStackSize, self.xTaskMaxActivateCount, 
                                self.xTaskAutoStart , self.xTaskPreemtable));

class GaInOsCounter():
    def __init__(self, xName):
        self.xCounterName=xName;
        self.xCounterMaxAllowValue=65535;
        self.xCounterMinCycle=1;
        self.xCounterTickPerBase=1;

    def printInfo(self):
        print('%s,%s,%s,%s'%(self.xCounterName, self.xCounterMaxAllowValue, 
            self.xCounterMinCycle, self.xCounterTickPerBase));

class GaInOsAlarm():
    def __init__(self, xName, xOwner):
        self.xAlarmName=xName;
        self.xAlarmOwner=xOwner;
        self.xAlarmType='ALARM_CALLBACK';
        self.xAlarmCbk='%s_Cbk'%(xName);
        self.xAlarmTask=None;
        self.xAlarmEvent=None;

    def printInfo(self):
        print('%s,%s,%s,%s,%s,%s'%(
            self.xAlarmName, self.xAlarmOwner, self.xAlarmType, 
            self.xAlarmCbk, self.xAlarmTask, self.xAlarmEvent));

class GaInOsResource():
    def __init__(self, xName, xPriority):
        self.xResName=xName;
        self.xResCeilPriority=xPriority;
        
    def printInfo(self):
        print('%s,%s'%(self.xResName, self.xResCeilPriority));

class GaInOsInResource():
    def __init__(self, xName, xPriority):
        self.xInResName=xName;
        self.xInResCeilPriority=xPriority;

    def printInfo(self):
        print('%s,%s'%(self.xInResName, self.xInResCeilPriority));

class GaInOsScheduleTable():
    def __init__(self, xName):
        self.xScheduleTableName=xName;
        self.xSchedTblRepeatable=True;
        self.xSchedTblAutostartable=False;
        self.xSchedTblDrivingCounter='';
        self.xSchedTblAutostartType='RELATIVE';
        self.xSchedTblAbsRelValue=0;
        self.xSchedTblFinalDelay=10;
        self.xSchedTblSyncStrategy='EXPLICIT';
        self.xSchedTblMaxAdvance=2;
        self.xSchedTblMaxRetard=2;
        self.xSchedTblExplicitPrecision=0;
        #Schedule table expiry point list
        #为了简单处理，利用链表特性
        #[
        #   [offset,['ActivateTask(vTask1)',..]],
        #   [offset,['ActivateTask(vTask2)',..]],
        #   ....
        #]
        self.xSchedTblEpList=[];
    def printInfo(self):
        print('%s,%s'%(self.xScheduleTableName,self.xSchedTblEpList))
    def toString(self):
        #转换为字符串信息并返回
        str='';
        index=0;
        str+='Schedule Table Repeatable:<%s>.\n'%(self.xSchedTblRepeatable);
        str+='Schedule Table Driving Counter is <%s>.\n'%(self.xSchedTblDrivingCounter);
        str+='Schedule Table Autostartable:<%s>.\n'%(self.xSchedTblAutostartable);
        if(self.xSchedTblAutostartable==True):
            str+='Autostarting Type is <%s>.\n'%(self.xSchedTblAutostartType);
            str+='Will be autostarted at value <%s>.\n'%(self.xSchedTblAbsRelValue);
        str+='Schedule Table Final Delay is <%s> Ticks.\n'%(self.xSchedTblFinalDelay);
        str+='Schedule Table Sync Strategy is <%s>.\n'%(self.xSchedTblSyncStrategy);
        str+='Schedule Table Max Advance is <%s> Ticks.\n'%(self.xSchedTblMaxAdvance);
        str+='Schedule Table Max Retard is <%s> Ticks.\n'%(self.xSchedTblMaxRetard);
        str+='Schedule Table Explicit Precision is <%s> Ticks.\n'%(self.xSchedTblExplicitPrecision);
        for ep in self.xSchedTblEpList:
            str+='(Expiry Point %s(offset=%s)\n'%(index, ep[0]);
            index+=1;
            for epsub in ep[1]:
                str+=' # %s\n'%(epsub);
            str+=')\n';
        return str;
