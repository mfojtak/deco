from deco.sources import Dataset
import threading, queue

def produce(input: Dataset, q: queue.Queue, stop: threading.Event):
    for item in input:
        q.put(item)
        if stop.is_set():
            break


class Cache(Dataset):
    def __init__(self, input):
        pass
    def __iter__(self):
        q = queue.Queue(100)
        input = self.inputs()
        self.stop = threading.Event()
        t = threading.Thread(target=produce, args=(input, q, self.stop))
        t.start()
        try:
            while(t.is_alive() or not q.empty()):
                try:
                    item = q.get(timeout=1)
                    yield item
                except queue.Empty:
                    pass
        except:
            self.stop.set()
        t.join()

def cache(self):
    return Cache(self)

Dataset.cache = cache