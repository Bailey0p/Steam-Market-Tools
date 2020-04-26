import time
import concurrent.futures

start = time.perf_counter()

def do_something(seconds):
    print(f"wait {seconds}s")
    time.sleep(seconds)
    return "done sleep"#if we still want to print this we need to grab value from return method
#submit method = 1 at a time, schedules a function to be executed and return a future object


with concurrent.futures.ThreadPoolExecutor() as executor:
    secs = [1,2,3,4,5]
    results = executor.map(do_something, secs)#returns results in the order they were started
    for result in results:
        print(result)



finish = time.perf_counter()

print(f'finished in {round(finish-start, 2)}')
