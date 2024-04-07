from multiprocessing import Lock, Process, Queue, current_process
import time
import queue

from ReceiveDataCallback import ReceiveLSLStreamToKafka # imported for using queue.Empty exception

class MultiprocessingCallback:

    def __init__(self,app):
        self.tasks_to_accomplish = Queue()
        self.tasks_that_are_done = Queue()
        self.appForLogging = app

    def initializeDeviceTypesAndProcesses(self, deviceTypes):
        self.activeDeviceTypes = deviceTypes
        self.processes = []
        number_of_task = len(self.activeDeviceTypes)
        for i in range(number_of_task):
            self.tasks_to_accomplish.put(self.activeDeviceTypes[i])
        self.appForLogging.logger.info('deviceTypes and Processes initialized')


    @staticmethod
    def take_job(tasks_to_accomplish,tasks_that_are_done,receiveLSLStreamToKafka=ReceiveLSLStreamToKafka()):
        while True:
            try:
                '''
                    try to get task from the queue. get_nowait() function will 
                    raise queue.Empty exception if the queue is empty. 
                    queue(False) function would do the same task also.
                '''
                task = tasks_to_accomplish.get_nowait()
            except Exception as e:
                print('exception: ',e)
                break
            else:
                '''
                    if no exception has been raised, add the task completion 
                    message to task_that_are_done queue
                '''
                print('task: ',task)
                receiveLSLStreamToKafka.receiveFromInletProduceToKafka(task,'quickstart-events',9092)
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
            p = Process(target=MultiprocessingCallback.take_job, args=(self.tasks_to_accomplish,self.tasks_that_are_done,receiveLSLStreamToKafka))
            self.processes.append(p)
            p.start()

        self.appForLogging.logger.info('processes created')
        return True
    
    def stopListenerProcesses(self):
        # completing process
        for p in self.processes:
            p.join()

        # print the output
        while not self.tasks_that_are_done.empty():
            self.appForLogging.logger.info(self.tasks_that_are_done.get())

        self.appForLogging.logger.info('processes stopped')
        return True
    
