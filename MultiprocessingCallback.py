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
    def take_job(tasks_to_accomplish,tasks_that_are_done,killEventSet,receiveLSLStreamToKafka=ReceiveLSLStreamToKafka()):
        try:
            '''
                try to get task from the queue. get_nowait() function will 
                raise queue.Empty exception if the queue is empty. 
                queue(False) function would do the same task also.
            '''
            task = tasks_to_accomplish.get_nowait()
        except Exception as e:
            print('exception: ',e)
        else:
            '''
                if no exception has been raised, add the task completion 
                message to task_that_are_done queue
            '''
            print('task: ',task)
            receiveLSLStreamToKafka.receiveFromInletProduceToKafka(task,'quickstart-events',9092,killEventSet)
            tasks_that_are_done.put(task + ' is done by ' + current_process().name)
            time.sleep(.5)
        return True


    def startListenerProcesses(self):
        number_of_processes = len(self.activeDeviceTypes)
        receiveLSLStreamToKafka = ReceiveLSLStreamToKafka()

        self.appForLogging.logger.info('about to create processes')
        # creating processes
        for w in range(number_of_processes):
            # give custom unique id by which we can kill them
            p = Process(name=self.activeDeviceTypes[w],target=MultiprocessingCallback.take_job, args=(self.tasks_to_accomplish,self.tasks_that_are_done,False,receiveLSLStreamToKafka))
            p.daemon = True
            self.processes.append(p)
            p.start()

        self.appForLogging.logger.info('processes created')
        return True
    
    def startListenerProcess(self,deviceType):
        receiveLSLStreamToKafka = ReceiveLSLStreamToKafka()
        self.activeDeviceTypes.append(deviceType)
        self.tasks_to_accomplish.put(deviceType)
        self.appForLogging.logger.info('about to create process')
        # give custom unique id by which we can kill them
        p = Process(name=deviceType,target=MultiprocessingCallback.take_job, args=(self.tasks_to_accomplish,self.tasks_that_are_done,False,receiveLSLStreamToKafka))
        p.daemon = True
        self.processes.append(p)
        p.start()

        self.appForLogging.logger.info('processes created')
        return True
    
    def stopListenerProcesses(self):
        # completing process
        for p in self.processes:
            p.terminate()
            p.join(1)#force joining after 1 second
            p.close()

        # print the output
        while not self.tasks_that_are_done.empty():
            self.appForLogging.logger.info(self.tasks_that_are_done.get())

        self.appForLogging.logger.info('processes stopped')
        print('processes stopped')
        self.activeDeviceTypes = []
        self.processes = []
        return True
    
    def stopListenerProcess(self,listenerID):
        # completing process
        self.activeDeviceTypes.remove(list(filter(lambda x: x == listenerID,self.activeDeviceTypes))[0])
        p = list(filter(lambda x: x.name == listenerID,self.processes))[0]
        print("p: "+p.name)
        p.terminate()
        p.join(1)#force joining after 1 second
        p.close()
        self.processes.remove(lambda x: x.name == listenerID)
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

