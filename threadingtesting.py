import time
import threading

start = time.perf_counter()

def do_something(seconds):
    print(f"wait {seconds}s")
    time.sleep(seconds)
    print("done sleep")


threads = []

for _ in range(10):
    t = threading.Thread(target=do_something, args=[2])
    t.start()
    threads.append(t)

for thread in threads:
    thread.join()


# t1 = threading.Thread(target=do_something)
# t2 = threading.Thread(target=do_something)
# t1.start()
# t2.start()
#
# t1.join()
# t2.join()

finish = time.perf_counter()

print(f'finished in {round(finish-start, 2)}')
