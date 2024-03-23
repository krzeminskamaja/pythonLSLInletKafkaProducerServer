from multiprocessing import Lock, Process, Queue, current_process
import time
import queue

from ReceiveDataCallback import ReceiveLSLStreamToKafka # imported for using queue.Empty exception


def take_job(tasks_to_accomplish, tasks_that_are_done, inletType='ET',receiveLSLStreamToKafka=ReceiveLSLStreamToKafka()):
    while True:
        try:
            '''
                try to get task from the queue. get_nowait() function will 
                raise queue.Empty exception if the queue is empty. 
                queue(False) function would do the same task also.
            '''
            task = tasks_to_accomplish.get_nowait()
        except queue.Empty:

            break
        else:
            '''
                if no exception has been raised, add the task completion 
                message to task_that_are_done queue
            '''
            print(task)
            receiveLSLStreamToKafka.receiveFromInletProduceToKafka(inletType,'quickstart-events',9092)
            tasks_that_are_done.put(task + ' is done by ' + current_process().name)
            time.sleep(.5)
    return True


def main():
    inletType=['EEG','ET']
    number_of_task = len(inletType)
    number_of_processes = len(inletType)
    tasks_to_accomplish = Queue()
    tasks_that_are_done = Queue()
    processes = []
    receiveLSLStreamToKafka = ReceiveLSLStreamToKafka()

    for i in range(number_of_task):
        tasks_to_accomplish.put("Task no " + str(i))

    # creating processes
    for w in range(number_of_processes):
        p = Process(target=take_job, args=(tasks_to_accomplish, tasks_that_are_done,inletType[w],receiveLSLStreamToKafka))
        processes.append(p)
        p.start()

    # completing process
    for p in processes:
        p.join()

    # print the output
    while not tasks_that_are_done.empty():
        print(tasks_that_are_done.get())

    return True


if __name__ == '__main__':
    main()