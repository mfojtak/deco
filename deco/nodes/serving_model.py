from deco.nodes import Transform
import aiohttp

class ServingModel(Transform):
    def __init__(self, name, url):
        super().__init__(name)
        self.url = url
    def _load(self):
        pass
    def _unload(self):
        pass
    async def _predict(self, input):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url + ":predict", json={"instances": input}) as resp:
                res = await resp.json()
                return res
    async def _info(self):
        url = "{}/metadata".format(self.url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                res = await resp.json()
                return res