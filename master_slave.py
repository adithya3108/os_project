import multiprocessing
import queue
import psutil  # Import the psutil library

def slave_function(task_queue, result_queue):
    while True:
        try:
            task = task_queue.get(timeout=1)
            # Perform the task
            process_name = multiprocessing.current_process().name
            process_pid = multiprocessing.current_process().pid
            processor_id = psutil.Process(process_pid).cpu_affinity()[0]  # Get the processor ID
            result = f"Processed {task} by {process_name} (PID: {process_pid}, Processor ID: {processor_id}, slave)"
            result_queue.put(result)
        except queue.Empty:
            break

def master_slave_processing(tasks, num_workers):
    task_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()

    for task in tasks:
        task_queue.put(task)

    processes = []
    for _ in range(num_workers):
        process = multiprocessing.Process(target=slave_function, args=(task_queue, result_queue))
        process.start()
        processes.append(process)

    # Master process
    master_name = multiprocessing.current_process().name
    master_pid = multiprocessing.current_process().pid
    print(f"Master process name: {master_name} (PID: {master_pid})")

    for process in processes:
        process.join()

    results = []
    while not result_queue.empty():
        result = result_queue.get()
        results.append(result)

    return results

if __name__ == "__main__":
    tasks = ["Task1", "Task2", "Task3", "Task4", "Task5", "Task6", "Task7", "Task8"]
    num_workers = 3

    results = master_slave_processing(tasks, num_workers)

    for result in results:
        print(result)
# Rest of the code remains the same

'''
import multiprocessing
import queue

def slave_function(task_queue, result_queue):
    while True:
        try:
            task = task_queue.get(timeout=1)
            # Perform the task
            result = f"Processed {task} by {multiprocessing.current_process().name} (PID: {multiprocessing.current_process().pid}, slave)"
            result_queue.put(result)
        except queue.Empty:
            break

def master_slave_processing(tasks, num_workers):
    task_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()

    for task in tasks:
        task_queue.put(task)

    processes = []
    for _ in range(num_workers):
        process = multiprocessing.Process(target=slave_function, args=(task_queue, result_queue))
        process.start()
        processes.append(process)

    # Master process
    master_name = multiprocessing.current_process().name
    master_pid = multiprocessing.current_process().pid
    print(f"Master process name: {master_name} (PID: {master_pid})")

    for process in processes:
        process.join()

    results = []
    while not result_queue.empty():
        result = result_queue.get()
        results.append(result)

    return results

if __name__ == "__main__":
    tasks = ["Task1", "Task2", "Task3", "Task4", "Task5", "Task6", "Task7", "Task8"]
    num_workers = 3

    results = master_slave_processing(tasks, num_workers)

    for result in results:
        print(result)
'''
