# -*- coding: utf-8 -*-
class GaInOsCfgCheck():
    def __init__(self, parent):
        #if True:No Error in configure
        #if False:Some thing wrong
        self.vCheckResult=True;
        #Message for information about the wrong point
        self.vCheckMessage='';
        #how much wrong point
        self.vCheckMessageSum=0;
        self.parent=parent;
        #开始检查
        self.vDoCheckTaskCfg();
        self.vDoCheckInResCfg();

    def vDoCheckTaskCfg(self):
        if(len(self.parent.pxGaInOSTaskCfgList)==0):
            self.vCheckResult=False;
            self.vCheckMessageSum+=1;
            self.vCheckMessage+='Error:No task configured!\n';
        for tsk in self.parent.pxGaInOSTaskCfgList:
            #检查任务名称的唯一性
            for tsk2 in self.parent.pxGaInOSTaskCfgList:
                if(tsk!=tsk2 and tsk.xTaskName==tsk2.xTaskName):
                    self.vCheckResult=False;
                    self.vCheckMessageSum+=1;
                    self.vCheckMessage+='Error:Task Name <%s> redefined!\n'%(tsk.xTaskName);
            #如果GaInOS最高任务为BCC1和BCC2，检查是否有任务的优先级重复
            if(self.parent.xGaInOSGeneralCfg.xOSConfCls=='BCC1' or
               self.parent.xGaInOSGeneralCfg.xOSConfCls=='ECC1'):
                for tsk2 in self.parent.pxGaInOSTaskCfgList:
                    if(tsk!=tsk2 and tsk.xTaskPriority==tsk2.xTaskPriority):
                        self.vCheckResult=False;
                        self.vCheckMessageSum+=1;
                        self.vCheckMessage+='Error:GaInOS Class Level is %s, but several tasks in Task <%s> Priority <%s>!\n'%(
                            self.parent.xGaInOSGeneralCfg.xOSConfCls,tsk.xTaskName, tsk.xTaskPriority);
            #检查任务是否配置了事件
            if(self.parent.xGaInOSGeneralCfg.xOSConfCls=='ECC1' or
               self.parent.xGaInOSGeneralCfg.xOSConfCls=='ECC2'):
                if(tsk.xTaskType=='EXTEND_TASK'):
                    if(len(tsk.xTaskEventList)==0):
                        self.vCheckMessage+='Warning:No Event Configured for Extended Task <%s> !\n'%(tsk.xTaskName);
                elif(len(tsk.xTaskEventList)>0):
                    self.vCheckMessage+='Warning:Do Event Configured for Basic Task <%s> !\n'%(tsk.xTaskName);

    def vDoCheckInResCfg(self):
        for xInRes in self.parent.pxGaInOSInResList:
            #检查内部资源优先级大于使用该资源所有任务的优先级，
            #并且其优先级上不应该有任务。
            xTaskNum=0;#统计使用内部资源的任务总数，必须大于等于2
            for tsk in self.parent.pxGaInOSTaskCfgList:
                if(tsk.xTaskWithInRes==True and
                   tsk.xTaskInResName==xInRes.xInResName):
                    xTaskNum+=1;
                    if(tsk.xTaskPriority>xInRes.xInResCeilPriority):
                        self.vCheckResult=False;
                        self.vCheckMessageSum+=1;
                        self.vCheckMessage+='Error:The Internal Resource <%s> Ceiling Priority Should be bigger than The Task <%s> Priority <%s>!\n'%(
                            xInRes.xInResName, tsk.xTaskName, tsk.xTaskPriority);
                else:
                    if(xInRes.xInResCeilPriority==tsk.xTaskPriority):
                        self.vCheckResult=False;
                        self.vCheckMessageSum+=1;
                        self.vCheckMessage+='Error:The Internal Resource <%s> Ceiling Priority Shoudn\'t be the same with the Task <%s> Priority <%s>!\n'%(
                            xInRes.xInResName, tsk.xTaskName, tsk.xTaskPriority);
            #检查使用该资源的任务总数是否大于等于2
            if(xTaskNum<2):
                self.vCheckResult=False;
                self.vCheckMessageSum+=1;
                self.vCheckMessage+='Error:Only One Or No Task Assigned To The Internal Resource <%s>!\n'%(
                    xInRes.xInResName);
            #检查内部资源名称，且其天花板优先级各部相同的唯一性
            for xInRes2 in self.parent.pxGaInOSInResList:
                if(xInRes!=xInRes2):
                    if(xInRes.xInResName==xInRes2.xInResName):
                        self.vCheckResult=False;
                        self.vCheckMessageSum+=1;
                        self.vCheckMessage+='Error:Do Has Several Internal Resource Have The Same Name <%s>!\n'%(xInRes.xInResName);
                    if(xInRes.xInResCeilPriority==xInRes2.xInResCeilPriority):
                        self.vCheckResult=False;
                        self.vCheckMessageSum+=1;
                        self.vCheckMessage+='Error:Do Internal Resource <%s> and <%s> have the same ceiling priority <%s>!\n'%(
                            xInRes.xInResName, xInRes2.xInResName, xInRes.xInResCeilPriority);

