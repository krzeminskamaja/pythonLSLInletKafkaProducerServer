from multiprocessing import Lock, Process, Queue, current_process, Value
import time
import queue

from ReceiveDataCallback import ReceiveLSLStreamToKafka # imported for using queue.Empty exception

class MultiprocessingCallback:

    def __init__(self,app):
        self.tasks_to_accomplish = Queue()
        self.tasks_that_are_done = Queue()
        self.appForLogging = app
        self.processes = []

    def initializeDeviceTypesAndProcesses(self, deviceTypes):
        self.activeDeviceTypes = deviceTypes
        self.processes = []
        number_of_task = len(self.activeDeviceTypes)
        for i in range(number_of_task):
            self.tasks_to_accomplish.put(self.activeDeviceTypes[i])
        self.appForLogging.logger.info('deviceTypes and Processes initialized')


    @staticmethod
    def take_job(outletType, tasks_to_accomplish,tasks_that_are_done,killEventSet,receiveLSLStreamToKafka=ReceiveLSLStreamToKafka()):
        topic = outletType
        topicElems = outletType.split('_')
        outletType = topicElems[len(topicElems)-1]
        print('take job: ')
        print(outletType)
        receiveLSLStreamToKafka.receiveFromInletProduceToKafka(outletType,topic,9092,killEventSet)
        return True


    def startListenerProcesses(self):
        number_of_processes = len(self.activeDeviceTypes)
        receiveLSLStreamToKafka = ReceiveLSLStreamToKafka()

        self.appForLogging.logger.info('about to create processes')
        # creating processes
        for w in range(number_of_processes):
            # give custom unique id by which we can kill them
            p = Process(name=self.activeDeviceTypes[w],target=MultiprocessingCallback.take_job, args=(self.activeDeviceTypes[w],self.tasks_to_accomplish,self.tasks_that_are_done,False,receiveLSLStreamToKafka))
            p.daemon = True
            self.processes.append(p)
            p.start()
            print('process created for device '+p.name)

        self.appForLogging.logger.info('processes created')
        return True
    
    def startListenerProcess(self,deviceType):
        receiveLSLStreamToKafka = ReceiveLSLStreamToKafka()
        self.activeDeviceTypes.append(deviceType)
        self.tasks_to_accomplish.put(deviceType)
        self.appForLogging.logger.info('about to create process')
        # give custom unique id by which we can kill them
        p = Process(name=deviceType,target=MultiprocessingCallback.take_job, args=(deviceType,self.tasks_to_accomplish,self.tasks_that_are_done,False,receiveLSLStreamToKafka))
        p.daemon = True
        self.processes.append(p)
        p.start()
        print('process created for device '+p.name)

        self.appForLogging.logger.info('processes created')
        return True
    
    def stopListenerProcesses(self):
        # completing process
        for p in self.processes:
            try:
                if(p.is_alive()):
                    p.terminate()
                    p.join(1)#force joining after 1 second
                    p.close()
            except:
                print('stop listener activeDeviceType removal exception')

        # print the output
        while not self.tasks_that_are_done.empty():
            self.appForLogging.logger.info(self.tasks_that_are_done.get())

        self.appForLogging.logger.info('processes stopped')
        print('all processes stopped')
        self.activeDeviceTypes = []
        self.processes = []
        return True
    
    def stopListenerProcess(self,listenerID):
        # completing process
        try:
            self.activeDeviceTypes.remove(list(filter(lambda x: x == listenerID,self.activeDeviceTypes))[0])
        except:
            print('stop listener activeDeviceType removal exception')
        
        p = list(filter(lambda x: x.name == listenerID,self.processes))
        for proc in p:
            try:
                if(proc.is_alive()):
                    proc.terminate()
                    proc.join(1)#force joining after 1 second
                    proc.close()
            except:
                print('exception on removing process')
        #self.processes.remove(lambda x: x.name == listenerID)
        print("processes stopped: "+listenerID)
        return True
    
    def getProcessStatus(self):
        print('printing processes names')
        listenerStatuses = []
        for p in self.processes:
            try:
                listenerStatuses.append({"name":p.name,
                                        "status":p.is_alive()})
            except ValueError as error:
                listenerStatuses.append({"name":p.name,
                                        "status":False})
        print('printed processes names')
        return listenerStatuses


