from abc import ABC, abstractmethod
import itertools
_current_context = None
class Dataset(ABC):
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._inputs = []
        obj._outputs = []
        for val in list(kwargs.values()) + list(args):
            if isinstance(val, Dataset):
                obj._inputs.append(val)
                val._outputs.append(obj)
        obj._iters = obj._inputs.copy()
        if _current_context:
            _current_context.add_node(obj)
        return obj
    
    def inputs(self):
        for inp in set(self._inputs):
            inp.handle_tee()
        if len(self._inputs) == 1:
            return self._iters[0]
        return zip(*self._iters)

    def swap_tee(self, input, tee_input):
        for i, inp in enumerate(self._inputs):
            if inp is input:
                if isinstance(self._iters[i], Dataset):
                    self._iters[i] = tee_input
                    break

    def handle_tee(self):
        if len(self._outputs) > 1:
            tees = itertools.tee(self, len(self._outputs))
            for out, tee in zip(self._outputs, tees):
                out.swap_tee(self, tee)

    @abstractmethod
    def __iter__(self):
        pass
    def eval(self):
        res = []
        for item in self:
            res.append(item)
        if len(res) == 1:
            return res[0]
        return res 