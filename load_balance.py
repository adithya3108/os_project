import multiprocessing
import time
import queue

# Simulated task function
def task(task_id, task_duration, task_priority):
    print(f"Task {task_id} with priority {task_priority} started on core {multiprocessing.current_process().name}")
    time.sleep(task_duration)
    print(f"Task {task_id} with priority {task_priority} completed on core {multiprocessing.current_process().name}")
    return task_id

def load_balancer(tasks):
    # Get the number of CPU cores available in the system
    num_cores = multiprocessing.cpu_count()
    # Create a pool of worker processes, one for each CPU core
    # This allows tasks to be executed concurrently on multiple cores
    pool = multiprocessing.Pool(processes=num_cores)

    # Create a list of processor queues for tasks
    processor_queues = [queue.PriorityQueue() for _ in range(num_cores)]

    for task_id, (duration, priority) in enumerate(tasks):
        processor_id = task_id % num_cores  # Assign tasks in a round-robin manner
        processor_queues[processor_id].put((priority, task_id, duration))

    def print_processor_queues():
        for i, processor_queue in enumerate(processor_queues):
            print(f"Processor {i} Queue: {list(processor_queue.queue)}")

    for i, processor_queue in enumerate(processor_queues):
        print(f"Processor {i} Initial Queue: {list(processor_queue.queue)}")

    while any(not queue.empty() for queue in processor_queues):
        for i, processor_queue in enumerate(processor_queues):
            if not processor_queue.empty():
                priority, task_id, task_duration = processor_queue.get()
                print(f"Task {task_id} with priority {priority} transferred to core {i}")
                result = pool.apply(task, args=(task_id, task_duration, task_id))
                print(f"Task {result} with priority {priority} returned on core {i}")
                print_processor_queues()

if __name__ == "__main__":
    # Simulated list of tasks with durations and priorities
     tasks = [
        (3, 2),  # Task 0 with duration 3 and priority 2
        (2, 3),  # Task 1 with duration 2 and priority 3
        (4, 1),  # Task 2 with duration 4 and priority 1
        (1, 4),  # Task 3 with duration 1 and priority 4
        (5, 2),  # Task 4 with duration 5 and priority 2
        (2, 2),  # Task 5 with duration 2 and priority 2
        (3, 3),  # Task 6 with duration 3 and priority 3
        (4, 1)   # Task 7 with duration 4 and priority 1
        # Add more tasks as needed
    ]
     load_balancer(tasks)







    
