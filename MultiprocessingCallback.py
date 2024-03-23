from multiprocessing import Lock, Process, Queue, current_process
import time
import queue

from ReceiveDataCallback import ReceiveLSLStreamToKafka # imported for using queue.Empty exception

class MultiprocessingCallback:

    def __init__(self):
        self.tasks_to_accomplish = Queue()
        self.tasks_that_are_done = Queue()

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


    def startListenerProcesses(self,inletType=['EEG','ET']):
        number_of_task = len(inletType)
        number_of_processes = len(inletType)
        processes = []
        receiveLSLStreamToKafka = ReceiveLSLStreamToKafka()

        for i in range(number_of_task):
            self.tasks_to_accomplish.put(inletType[i])

        print('about to create processes')
        # creating processes
        for w in range(number_of_processes):
            p = Process(target=MultiprocessingCallback.take_job, args=(self.tasks_to_accomplish,self.tasks_that_are_done,receiveLSLStreamToKafka))
            processes.append(p)
            p.start()

        # completing process
        for p in processes:
            p.join()

        # print the output
        while not self.tasks_that_are_done.empty():
            print(self.tasks_that_are_done.get())

        return True
    
