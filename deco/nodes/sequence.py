from deco.nodes import Transform

class Sequence(Transform):
    def __init__(self, name, nodes):
        super().__init__(name)
        self.nodes = nodes
    def _load(self):
        pass
    def _unload(self):
        pass
    async def _eval(self, input):
        cur_input = input
        for node in self.nodes:
            output = await node.eval(cur_input)
            cur_input = output
        return output
    async def _info(self):
        infos = []
        for node in self.nodes:
            infos.append(node.info())
        return infos