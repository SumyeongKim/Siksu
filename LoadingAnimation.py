import threading
import time
import sys
import itertools

def start_animation(stop_event):
    t = threading.Thread(target=animate, args=(stop_event,))
    t.start()
    return t

def end_animation(t, stop_event):
    stop_event.set()
    t.join()
    stop_event.clear()

def animate(stop_event):
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if stop_event.is_set():
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     \n')