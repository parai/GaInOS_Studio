# -*- coding: utf-8 -*-
import os
import sys
import shutil 

class GaInOsGen():
    def __init__(self, path, AllCfg):
        #创建文件
        if os.path.lexists(path)!=True:
            os.mkdir(path);
        if os.path.isfile(path+'/CfgObj.h'):
            shutil.copy(path+'/CfgObj.h', path+'/CfgObj.h.bak');
        if os.path.isfile(path+'/CfgObj.c'):
            shutil.copy(path+'/CfgObj.c', path+'/CfgObj.c.bak');
        if os.path.isfile(path+'/Os_Cfg.h'):
            shutil.copy(path+'/Os_Cfg.h', path+'/Os_Cfg.h.bak');
        if os.path.isfile(path+'/CfgRdyQ.c'):
            shutil.copy(path+'/CfgRdyQ.c', path+'/CfgRdyQ.c.bak');
        if os.path.isfile(path+'/CfgSchedTbl.c'):
            shutil.copy(path+'/CfgSchedTbl.c', path+'/CfgSchedTbl.c.bak');
        self.fp_CfgObj_h=open(path+'/CfgObj.h', 'w');
        self.fp_CfgObj_c=open(path+'/CfgObj.c', 'w');
        self.fp_Os_Cfg_h=open(path+'/Os_Cfg.h', 'w');
        if(AllCfg.xGaInOSGeneralCfg.xOSConfCls=='ECC2' or
           AllCfg.xGaInOSGeneralCfg.xOSConfCls=='BCC2'):
            self.fp_CfgRdyQueue_c=open(path+'/CfgRdyQ.c', 'w');
        #if(len(AllCfg.pxGaInOSScheduleTableList)!=0):
        self.fp_CfgSchedTbl_c=open(path+'/CfgSchedTbl.c', 'w');
        #保存传入的参数
        self.xGaInOSGeneralCfg=AllCfg.xGaInOSGeneralCfg;
        self.pxGaInOSTaskCfgList=AllCfg.pxGaInOSTaskCfgList;
        self.pxGaInOSCounterCfgList=AllCfg.pxGaInOSCounterCfgList;
        self.pxGaInOSAlarmCfgList=AllCfg.pxGaInOSAlarmCfgList;
        self.pxGaInOSResList=AllCfg.pxGaInOSResList;
        self.pxGaInOSInResList=AllCfg.pxGaInOSInResList;
        self.pxGaInOSScheduleTableList=AllCfg.pxGaInOSScheduleTableList;
        self.vDoGenerateCfgFile();
        #关闭文件
        self.fp_CfgObj_h.close();
        self.fp_CfgObj_c.close();
        self.fp_Os_Cfg_h.close();
        if(AllCfg.xGaInOSGeneralCfg.xOSConfCls=='ECC2' or
           AllCfg.xGaInOSGeneralCfg.xOSConfCls=='BCC2'):
            self.fp_CfgRdyQueue_c.close();
        #if(len(self.pxGaInOSScheduleTableList)!=0):
        self.fp_CfgSchedTbl_c.close();

    def vDoGenerateCfgFile(self):
        self.vDoGenCfgObjH();
        self.vDoGenCfgObjC();
        self.vDoGenOsCfgH();
        if(self.xGaInOSGeneralCfg.xOSConfCls=='ECC2' or
           self.xGaInOSGeneralCfg.xOSConfCls=='BCC2'):
            self.vDoGenCfgRdyQueueC();
        if(len(self.pxGaInOSScheduleTableList)!=0):
            self.vDoGenCfgSchedTblC();

    def vDoGenCfgObjH(self):
        fp=self.fp_CfgObj_h;
        fp.write('#ifndef _CFGOBJ_H_\n#define _CFGOBJ_H_\n\n#include "Os.h"\n\n');
#For Internal Resource
        if(self.xGaInOSGeneralCfg.xOSUseInRes==True):
            fp.write('/* GaInOS Internal Resource Configuration */\n');
            id=0;
            for xInRes in self.pxGaInOSInResList:
                fp.write('#define %s %s\n'%(xInRes.xInResName,id));
                id+=1;
            fp.write('extern const PriorityType OSInResCeilPrioTable[cfgOS_INTERNAL_RESOURCE_NUM];\n')
            fp.write('extern const ResourceType OSTskInResIdTable[cfgOS_TASK_WITH_IN_RES_NUM];\n');
#For Resource
        if(self.xGaInOSGeneralCfg.xOSUseRes==True):
            fp.write('\n/* GaInOS Resource Configuration */\n');
            id=1;
            for xRes in self.pxGaInOSResList:
                fp.write('#define %s %s\n'%(xRes.xResName,id));
                id+=1;
            fp.write('extern const PriorityType OSResCeilPrioTable[cfgOS_RESOURCE_NUM];\n');
#For Alram
        #if(self.xGaInOSGeneralCfg.xOSUseAlarm==True):
        fp.write('\n/* GaInOS Counter And Alarm Configuration */\n');
        counterId=0;
        for cnt in self.pxGaInOSCounterCfgList:
            fp.write('#define %s %s\n'%(cnt.xCounterName,counterId));
            counterId+=1;
        alarmId=0;
        for alm in self.pxGaInOSAlarmCfgList:
            fp.write('#define %s %s\n'%(alm.xAlarmName,alarmId));
            alarmId+=1;
            if(alm.xAlarmType=='ALARM_CALLBACK'):
                fp.write('extern ALARMCALLBACK(%s);\t\t/* %s */\n'%(alm.xAlarmCbk,alm.xAlarmName));
        fp.write('%s\n%s\n%s\n%s\n%s\n%s\n\n'%(
            'extern const AlarmBaseType OSCounterBaseTable[cfgOS_COUNTER_NUM];',
            '#if(cfgOS_USE_ALARM == STD_TRUE)',
            'extern const AlarmClassType OSAlarmClassTable[cfgOS_ALARM_NUM];', 
            'extern const AlarmContainerType OSAlarmContainerTable[cfgOS_ALARM_NUM];', 
            'extern const CounterType OSAlarmOwnerTable[cfgOS_ALARM_NUM];', 
            '#endif'));
#For Task
        fp.write('/* GaInOS Task Configuration */\n')
        fp.write('%s\n%s\n%s\n%s\n\n'%(
            'extern const TaskStackRefType OSTaskStackTable[cfgOS_TASK_NUM];', 
            'extern const PriorityType     OSTaskInitPriorityTable[cfgOS_TASK_NUM];', 
            'extern const TaskEntryType    OSTaskEntryTable[cfgOS_TASK_NUM];', 
            'extern const BoolType         OSTaskAutoActivateTable[cfgOS_TASK_NUM];'));
        fp.write('%s\n%s\n%s\n\n'%(
            '#if (cfgOS_MULTIPLY_ACTIVATE == STD_TRUE)',
            'extern const uint8_t OSMaxActivateCountTable[cfgOS_TASK_NUM];', 
            '#endif'));
        fp.write('%s\n%s\n%s\n\n'%(
            '#if (cfgOS_CONFORMANCE_CLASS == ECC2) || (cfgOS_CONFORMANCE_CLASS == ECC1)',
            'extern const uint8_t OSTaskConfClassTable[cfgOS_TASK_NUM];',
            '#endif'));
        fp.write('%s\n%s\n%s\n\n'%(
            '#if (cfgOS_SCHEDULE_POLICY == MIXED_PREEMPTIVE_SCHEDULE)',
            'extern const BoolType OSTaskPreemtableTable[cfgOS_TASK_NUM];',
            '#endif'));
        fp.write('%s\n%s\n%s\n\n'%(
            '#if (cfgOS_CONFORMANCE_CLASS == ECC1 || cfgOS_CONFORMANCE_CLASS == ECC2)',
            'extern const uint8_t OSTskClsTypeTable[cfgOS_TASK_NUM];',
            '#endif',))
        xTaskId=0;
        for tsk in self.pxGaInOSTaskCfgList:
            fp.write('#define %s %s\n'%(tsk.xTaskName, xTaskId));
            if(tsk.xTaskType=='EXTEND_TASK'):
                for ent in tsk.xTaskEventList:
                    fp.write('#define %s %s\n'%(ent.xEventName,ent.xEventMask));
            fp.write('extern TASK( %s );\n'%(tsk.xTaskName));
            xTaskId=xTaskId+1;
#Schedule Table 
        fp.write('#if(cfgOS_SCHEDULE_TABLE_NUM > 0)\n');
        fp.write('extern const OsSchedTblCmdType* OSScheduleTable[cfgOS_SCHEDULE_TABLE_NUM];\n');
        fp.write('extern const OsScheduleTableType OSScheduleTableInfo[cfgOS_SCHEDULE_TABLE_NUM];\n');
        index=-1;
        for tbl in self.pxGaInOSScheduleTableList:
            index+=1;
            fp.write('#define %s %s\n'%(tbl.xScheduleTableName,index));
        fp.write('#endif  /* cfgOS_SCHEDULE_TABLE_NUM */\n');
        #end
        fp.write('\n#endif /* _CFGOBJ_H_ */\n\n\n');
        
    def vDoGenCfgObjC(self):
        fp=self.fp_CfgObj_c;
        fp.write('#include "CfgObj.h"\n#include "Serial.h"\n\n');
        if(self.xGaInOSGeneralCfg.xOSCpuType=='ARM920T'):
            fp.write('const TaskType G_INVALID_TASK=INVALID_TASK;\n\n');
#For Internal Resource
        if(self.xGaInOSGeneralCfg.xOSUseInRes==True):
            fp.write('/* GaInOS Internal Resource Configuration */\n');
            resCeil='';
            for xInRes in self.pxGaInOSInResList:
                resCeil+='\t%s,\t\t/* %s */\n'%(xInRes.xInResCeilPriority, xInRes.xInResName);
            fp.write('const PriorityType OSInResCeilPrioTable[cfgOS_INTERNAL_RESOURCE_NUM]=\n{\n%s};\n\n'%(resCeil));
            tskWithInRes='';
            for tsk in self.pxGaInOSTaskCfgList:
                if(tsk.xTaskWithInRes==True):
                    tskWithInRes+='\t%s,\t\t/* %s */\n'%(tsk.xTaskInResName, tsk.xTaskName);
            fp.write('const ResourceType OSTskInResIdTable[cfgOS_TASK_WITH_IN_RES_NUM]=\n{\n%s};\n\n'%(tskWithInRes));
#For Resource
        if(self.xGaInOSGeneralCfg.xOSUseRes==True):
            fp.write('\n/* GaInOS Resource Configuration */\n');
            resCeil='\tcfgOS_MAX_PRIORITY,\t\t /* RES_SCHEDULER */\n';
            for xRes in self.pxGaInOSResList:
                resCeil+='\t%s,\t\t/* %s */\n'%(xRes.xResCeilPriority, xRes.xResName);
            fp.write('const PriorityType OSResCeilPrioTable[cfgOS_RESOURCE_NUM]=\n{\n%s};\n\n'%(resCeil));
#For Alram
        fp.write('/* GaInOS Counter And Alarm Configuration */\n')
        cntBase='';
        for cnt in self.pxGaInOSCounterCfgList:
            cntBase+='\t{\t/* %s */\n\t\t%s,\t\t/* xMaxAllowedValue */\n'%(cnt.xCounterName, 
                                                                           cnt.xCounterMaxAllowValue);
            cntBase+='\t\t%s,\t\t/* xTicksPerBase */\n'%(cnt.xCounterTickPerBase);
            cntBase+='\t\t%s\t\t/* xMinCycle */\n\t},\n'%(cnt.xCounterMinCycle);
        fp.write('const AlarmBaseType OSCounterBaseTable[cfgOS_COUNTER_NUM]=\n{\n%s};\n\n'%(
                        cntBase));
        if(self.xGaInOSGeneralCfg.xOSUseAlarm==True):
            almCls=almOwner=almCon='';
            almCbk='';
            for alm in self.pxGaInOSAlarmCfgList:
                almCls+='\t%s,\t\t/* %s */\n'%(alm.xAlarmType, alm.xAlarmName);
                almOwner+='\t%s,\t\t/* %s */\n'%(alm.xAlarmOwner, alm.xAlarmName);
                if(alm.xAlarmType=='ALARM_CALLBACK'):
                    almCon+='\t(VoidType) AlarmCallBackEntry(%s),\t\t/* %s */\n'%(
                                alm.xAlarmCbk, alm.xAlarmName);
                    almCbk+='ALARMCALLBACK(%s){\n%s\n\n%s\n}\n'%(
                                alm.xAlarmCbk,
                                '/* Add Your Alarm Callback Code Here.*/', 
                                'printk("In %s().\\n");'%(alm.xAlarmCbk));
                elif(alm.xAlarmType=='ALARM_TASK'):
                    almCon+='\t(VoidType) %s,\t\t/* %s */\n'%(alm.xAlarmTask, alm.xAlarmName);
                elif(alm.xAlarmType=='ALARM_EVENT'):
                    almCon+='\t(VoidType)((VoidType)%s<<16U)|((VoidType)%s),\t\t/* %s */\n'%(
                                                     alm.xAlarmTask, alm.xAlarmEvent, alm.xAlarmName);
            fp.write('#if(cfgOS_USE_ALARM==STD_TRUE)\n');
            fp.write('const AlarmClassType OSAlarmClassTable[cfgOS_ALARM_NUM]=\n{\n%s};\n\n'%(almCls));
            fp.write('const CounterType OSAlarmOwnerTable[cfgOS_ALARM_NUM]=\n{\n%s};\n\n'%(almOwner));
            fp.write('const AlarmContainerType OSAlarmContainerTable[cfgOS_ALARM_NUM]=\n{\n%s};\n\n'%(almCon));
            fp.write('#endif');
#For Task
        fp.write('/* GaInOS Task Configuration */\n');
        #为任务分配内存
        stack=stackRef=priority=autoStart='';
        maxActCnt=preemtable=taskCls='';
        taskEntry=taskFun='';
        for tsk in self.pxGaInOSTaskCfgList:
            stack+='static TaskStackType g_%sStack[%s/4];\n'%(tsk.xTaskName, tsk.xTaskStackSize);
            stackRef+='\t{&g_%sStack[%s/4 -1]},\n'%(tsk.xTaskName, tsk.xTaskStackSize);
            priority+='\t%s,\t\t/* %s */\n'%(tsk.xTaskPriority, tsk.xTaskName);
            if(tsk.xTaskAutoStart ==True): 
                autoStart+='\tSTD_TRUE,\t\t/* %s */\n'%(tsk.xTaskName);
            else:
                autoStart+='\tSTD_FALSE,\t\t/* %s */\n'%(tsk.xTaskName);
            maxActCnt+='\t%s,\t\t/* %s */\n'%(tsk.xTaskMaxActivateCount, tsk.xTaskName);
            if(tsk.xTaskPreemtable==True):
                preemtable+='\tSTD_TRUE,\t\t/* %s */\n'%(tsk.xTaskName);
            else:
                preemtable+='\tSTD_FALSE,\t\t/* %s */\n'%(tsk.xTaskName);
            taskCls+='\t%s, \t\t/* %s */\n'%(tsk.xTaskType, tsk.xTaskName);
            taskEntry+='\tTaskEntry(%s),\n'%(tsk.xTaskName);
            taskFun+='TASK(%s){\n/* Add Your Task Code Here. */\n\n%s\n}\n\n'%(
               tsk.xTaskName, 
               '\tprintk("%s is running.\\r\\n");\n\t(void)TerminateTask();'%(tsk.xTaskName));
        fp.write('%s\n'%(stack));
        fp.write('const TaskStackRefType OSTaskStackTable[cfgOS_TASK_NUM]=\n{\n%s};\n\n'%(stackRef));
        fp.write('const PriorityType OSTaskInitPriorityTable[cfgOS_TASK_NUM]=\n{\n%s};\n\n'%(priority));
        fp.write('const BoolType OSTaskAutoActivateTable[cfgOS_TASK_NUM]=\n{\n%s};\n\n'%(autoStart));
        fp.write('%s\n%s\n{\n%s};\n%s\n\n'%(
            '#if (cfgOS_MULTIPLY_ACTIVATE == STD_TRUE)',
            'const uint8_t OSMaxActivateCountTable[cfgOS_TASK_NUM]=', 
            maxActCnt, 
            '#endif'));
        fp.write('%s\n%s\n{\n%s};\n%s\n\n'%(
            '#if (cfgOS_SCHEDULE_POLICY == MIXED_PREEMPTIVE_SCHEDULE)',
            'const BoolType OSTaskPreemtableTable[cfgOS_TASK_NUM]=', 
            preemtable, 
            '#endif'));
        fp.write('%s\n%s\n{\n%s};\n%s\n\n'%(
            '#if (cfgOS_CONFORMANCE_CLASS == ECC2 || cfgOS_CONFORMANCE_CLASS == ECC1)',
            'const uint8_t OSTskClsTypeTable[cfgOS_TASK_NUM] =', 
            taskCls, 
            '#endif'));
        fp.write('const TaskEntryType OSTaskEntryTable[cfgOS_TASK_NUM]=\n{\n%s};\n\n'%(taskEntry));
        if(self.xGaInOSGeneralCfg.xOSUseAlarm==True):
            fp.write(almCbk);   
        fp.write(taskFun);

    def vDoGenOsCfgH(self):
        fp=self.fp_Os_Cfg_h;
        fp.write('#ifndef _OS_CFG_H_\n#define _OS_CFG_H_\n#include "Os.h"\n\n');
        fp.write('#define cfgOS_MAX_IPL %s\n'%(self.xGaInOSGeneralCfg.xOSMaxIpl));
        fp.write('#define cfgOS_MAX_PRIORITY %s\n'%(self.xGaInOSGeneralCfg.xOSMaxPriority));
        fp.write('#define cfgOS_CONFORMANCE_CLASS %s\n'%(self.xGaInOSGeneralCfg.xOSConfCls));
        if(self.xGaInOSGeneralCfg.xOSConfCls=='ECC2' or self.xGaInOSGeneralCfg.xOSConfCls=='BCC2'):
            sumActCnt=0;
            for tsk in self.pxGaInOSTaskCfgList:
                sumActCnt+=tsk.xTaskMaxActivateCount;
            fp.write('#define cfgOS_SUM_ACTIVATES %s\n'%(sumActCnt));
        fp.write('#define cfgOS_STATUS_LEVEL %s\n'%(self.xGaInOSGeneralCfg.xOSStatusLevel));
        fp.write('#define cfgOS_SCHEDULE_POLICY %s\n'%(self.xGaInOSGeneralCfg.xOSSchedPolicy));
        fp.write('#define cfgOS_TASK_NUM %s\n\n'%(len(self.pxGaInOSTaskCfgList)));
        #普通资源配置
        fp.write('\n/* GaInOS Resource Configuration */\n');
        if(self.xGaInOSGeneralCfg.xOSUseRes==True):
            fp.write('#define cfgOS_USE_RESOURCE STD_TRUE\n');
            fp.write('#define cfgOS_RESOURCE_NUM %s\n'%(len(self.pxGaInOSResList)+1));
        else:
            fp.write('#define cfgOS_USE_RESOURCE STD_FALSE\n');
            fp.write('#define cfgOS_RESOURCE_NUM 0\n\n');
        #内部资源配置
        fp.write('\n/* GaInOS Internal Resource Configuration */\n');
        if(self.xGaInOSGeneralCfg.xOSUseInRes==True):
            fp.write('#define cfgOS_USE_INTERNAL_RESOURCE STD_TRUE\n');
            fp.write('#define cfgOS_INTERNAL_RESOURCE_NUM %s\n'%(len(self.pxGaInOSInResList)));
            num=0;
            for tsk in self.pxGaInOSTaskCfgList:
                if(tsk.xTaskWithInRes==True):
                    num+=1;
            fp.write('#define cfgOS_TASK_WITH_IN_RES_NUM %s\n'%(num));
        else:
            fp.write('#define cfgOS_USE_INTERNAL_RESOURCE STD_FALSE\n');
            fp.write('%s\n%s\n\n'%(
                '#define cfgOS_INTERNAL_RESOURCE_NUM 0',
                '#define cfgOS_TASK_WITH_IN_RES_NUM  0'));
        #中断ISR2是否使用普通资源的配置
        if(self.xGaInOSGeneralCfg.xOSIsr2UseRes==True):
            fp.write('#define cfgOS_ISR_USE_RES STD_TRUE\n');
        else:
            fp.write('#define cfgOS_ISR_USE_RES STD_FALSE\n\n');
        #Alarm的配置
        if(self.xGaInOSGeneralCfg.xOSUseAlarm==True):
            fp.write('/* GaInOS Counter And Alarm Configuration */\n');
            fp.write('#define cfgOS_USE_ALARM STD_TRUE\n');
        else:
            fp.write('#define cfgOS_USE_ALARM STD_FALSE\n'); 
        fp.write('#define cfgOS_COUNTER_NUM %s\n'%(len(self.pxGaInOSCounterCfgList)));
        fp.write('#define cfgOS_ALARM_NUM %s\n'%(len(self.pxGaInOSAlarmCfgList)));
        #Schedule Table 
        fp.write('#define cfgOS_SCHEDULE_TABLE_NUM %s\n'%(len(self.pxGaInOSScheduleTableList)));
        #GaInOS 的一些未配置项
        fp.write('\n/*Default Macro Defines Which You Can Change form 0 to 1 to include the Hooks or Stack Usage Check for GaInOS*/\n')
        fp.write('#define cfgOS_STACK_USAGE_CHECK 0\n');
        fp.write('#define cfgOS_HOOK_IN_KERNEL 0\n');
        fp.write('#define cfgOS_SHUT_DOWN_HOOK 0\n');
        fp.write('#define cfgOS_START_UP_HOOK 0\n');
        fp.write('#define cfgOS_ERROR_HOOK 0\n');
        fp.write('#define cfgOS_PRE_TASK_HOOK 0\n');
        fp.write('#define cfgOS_POST_TASK_HOOK 0\n\n');
        #end
        fp.write('/* For %s */\n'%(self.xGaInOSGeneralCfg.xOSCpuType));
        if(self.xGaInOSGeneralCfg.xOSCpuType=='MC9S12(X)'):
            fp.write('%s\n%s\n%s\n'%(
                'typedef uint8_t OsCpuSrType;', 
                'typedef uint8_t OsCpuIplType;', 
                '#endif /* _OS_CFG_H_ */' ));
        elif(self.xGaInOSGeneralCfg.xOSCpuType=='ARM920T'):
            fp.write('%s\n%s\n%s\n'%(
                'typedef uint32_t OsCpuSrType;', 
                'typedef uint32_t OsCpuIplType;', 
                '#endif /* _OS_CFG_H_ */' ));
        elif(self.xGaInOSGeneralCfg.xOSCpuType=='C166'):
            fp.write('%s\n%s\n%s\n\n\n'%(
                'typedef uint16_t OsCpuSrType;', 
                'typedef uint16_t OsCpuIplType;', 
                '#endif /* _OS_CFG_H_ */' ));
        elif(self.xGaInOSGeneralCfg.xOSCpuType=='Tri-Core'):
            fp.write('%s\n%s\n%s\n\n\n'%(
                'typedef uint32_t OsCpuSrType;', 
                'typedef uint8_t  OsCpuIplType;', 
                '#endif /* _OS_CFG_H_ */' ));

    def vDoGenCfgRdyQueueC(self):
        fp=self.fp_CfgRdyQueue_c;
        fp.write('#include "Os.h"\n\n');
        fp.write('#if (cfgOS_TASK_PER_PRIORITY == SEVERAL_TASKS_PER_PRIORITY )\n');
        fp.write('#    if(cfgOS_SUM_ACTIVATES > 0)\n\n');
        queuePtr=queueSize='';
        for prio in range(0, self.xGaInOSGeneralCfg.xOSMaxPriority+1):
            size=2;
            for tsk in self.pxGaInOSTaskCfgList:
                if(tsk.xTaskPriority==prio):
                    size+=tsk.xTaskMaxActivateCount;
            fp.write('static TaskType g_RdyQueueOfPriority%s[%s];\n'%(prio, size));
            queueSize+='\t%s,\t\t/* Priority %s*/\n'%(size, prio);
            queuePtr+='\tg_RdyQueueOfPriority%s,\n'%(prio);
        fp.write('static TaskType g_RdyQueueOfInvalidPriority[1]={INVALID_TASK};\n\n');
        queueSize+='\t1\t\t/* Invalid Priority */\n';
        queuePtr+='\tg_RdyQueueOfInvalidPriority\n';
        fp.write('const TaskRefType OSTskRdyQueuePtr[cfgOS_MAX_PRIORITY+2]=\n{\n%s};\n\n'%(queuePtr));
        fp.write('const uint8_t OSTskRdyQueueSize[cfgOS_MAX_PRIORITY+2]=\n{\n%s};\n\n'%(queueSize));
        fp.write('#    endif\n');
        fp.write('#endif\n\n')

    def vDoGenCfgSchedTblC(self):
        #配置为空直接退出
        if(len(self.pxGaInOSScheduleTableList)==0):
            return;
        fp=self.fp_CfgSchedTbl_c;
        fp.write('#include "Kernel.h"\n\n');
        fp.write('#if(cfgOS_SCHEDULE_TABLE_NUM > 0)\n');
        OsSchedTbl='const OsSchedTblCmdType* OSScheduleTable[cfgOS_SCHEDULE_TABLE_NUM]=\n{\n';
        OsSchedTblInfo='const OsScheduleTableType OSScheduleTableInfo[cfgOS_SCHEDULE_TABLE_NUM]=\n{\n';
        for tbl in self.pxGaInOSScheduleTableList:
            schedTbl=schedCmd='';
            OsSchedTbl+='\tg_%s,\n'%(tbl.xScheduleTableName);
            OsSchedTblInfo+='\t{\t\t/* %s */\n'%(tbl.xScheduleTableName);
            OsSchedTblInfo+='\t\t%s,\t\t/* xOsScheduleTableDuration */\n'%(tbl.xSchedTblEpList[len(tbl.xSchedTblEpList)-1][0]+tbl.xSchedTblFinalDelay);
            if(tbl.xSchedTblRepeatable==True):
                OsSchedTblInfo+='\t\tSTD_TRUE,\t\t/* xOsScheduleTableRepeating */\n';
            else:
                OsSchedTblInfo+='\t\tSTD_FALSE,\t\t/* xOsScheduleTableRepeating */\n';
            OsSchedTblInfo+='\t\tINVALID_OSAPPLICATION, \t\t/* xOsSchTblAccessingApplication */\n';
            OsSchedTblInfo+='\t\t%s,\t\t/* xOsScheduleTableCounterRef */\n'%(tbl.xSchedTblDrivingCounter);
            if(tbl.xSchedTblAutostartable==True):
                OsSchedTblInfo+='\t\tSTD_TRUE,\t\t/* xOsScheduleTableAutostart */\n';
            else:
                OsSchedTblInfo+='\t\tSTD_FALSE,\t\t/* xOsScheduleTableAutostart */\n';
            OsSchedTblInfo+='\t\t%s,\t\t/* xOsScheduleTableAutostartType */\n'%(tbl.xSchedTblAutostartType);
            OsSchedTblInfo+='\t\t%s,\t\t/* xOsScheduleTableAutostartValue */\n'%(tbl.xSchedTblAbsRelValue);
            OsSchedTblInfo+='\t\t%s,\t\t/* xOsScheduleTableSyncStrategy */\n'%(tbl.xSchedTblSyncStrategy);
            OsSchedTblInfo+='\t\t%s,\t\t/* xOsScheduleTableMaxAdvance */\n'%(tbl.xSchedTblMaxAdvance);
            OsSchedTblInfo+='\t\t%s,\t\t/* xOsScheduleTableMaxRetard */\n'%(tbl.xSchedTblMaxRetard);
            OsSchedTblInfo+='\t\t%s\t\t/* xOsScheduleTableExplicitPrecision */\n'%(tbl.xSchedTblExplicitPrecision);
            OsSchedTblInfo+='\t},\n';
            schedTbl+='static const OsSchedTblCmdType g_%s[%s]=\n{\n'%(tbl.xScheduleTableName, len(tbl.xSchedTblEpList)+1);
            index=0;
            for ep in tbl.xSchedTblEpList:
                schedCmd+='static void %s_CmdEp%s(void)\n{\n'%(tbl.xScheduleTableName, index);
                for epsub in ep[1]:
                    schedCmd+='\t(void)%s;\n'%(epsub);
                schedCmd+='\tOSMakeNextExpiryPointReady(%s);\n'%(tbl.xScheduleTableName);
                schedCmd+='}\n';
                schedTbl+='\t{\n\t\t%s,\n\t\t%s_CmdEp%s\n\t},\n'%(ep[0], tbl.xScheduleTableName, index)
                index+=1;
            #final delay时的处理
            schedTbl+='\t{\n\t\t%s,\n\t\t%s_CmdEp%s\n\t}\n};\n'%(
                tbl.xSchedTblEpList[len(tbl.xSchedTblEpList)-1][0]+tbl.xSchedTblFinalDelay, 
                tbl.xScheduleTableName, index);
            schedCmd+='static void %s_CmdEp%s(void)\n{\n'%(tbl.xScheduleTableName, index);
            schedCmd+='\tOSProcessScheduleTableFinalDelay(%s);\n'%(tbl.xScheduleTableName);
            schedCmd+='}\n';
            fp.write(schedCmd);
            fp.write(schedTbl);
            index+=1;
        OsSchedTbl=OsSchedTbl[0:-2]+'\n};\n';
        OsSchedTblInfo=OsSchedTblInfo[0:-2]+'\n};\n';
        fp.write(OsSchedTbl);
        fp.write(OsSchedTblInfo);
        fp.write('#endif  /* cfgOS_SCHEDULE_TABLE_NUM */\n');
