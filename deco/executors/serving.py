from quart import Quart, jsonify, request
import json

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

class Serving:
    def __init__(self, name, nodes, port=4000):
        self.port = port
        self.name = name
        self.nodes = {}
        for node in nodes:
            self.nodes[node.name] = node
        app = Quart(self.name)
        app.json_encoder = NumpyEncoder

        @app.route('/status', methods=['GET'])
        async def status():
            res = []
            for node in self.nodes.values():
                res.append({"name": node.name, "status": node.status.name})
            return jsonify(res)
        
        @app.route('/nodes/<name>/status', methods=['GET'])
        def node_status(name):
            node = self.nodes[name]
            return jsonify(node.status.name)
        
        @app.route('/nodes/<name>/info', methods=['GET'])
        async def node_info(name):
            node = self.nodes[name]
            info = await node.info()
            return jsonify(info)

        @app.route('/nodes/<name>/eval', methods=['POST'])
        async def node_predict(name):
            content = await request.get_json()
            node = self.nodes[name]
            res = await node.eval(content)
            return jsonify(res)
        
        self.app = app
    
    def run(self):
        self.app.run(host='0.0.0.0',debug=True,port=self.port)