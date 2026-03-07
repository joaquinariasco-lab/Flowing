from flask import Flask, request, jsonify

app = Flask(__name__)

TRACES = []

@app.route("/trace", methods=["POST"])
def receive_trace():
    data = request.json
    TRACES.append(data)
    return {"status": "ok"}

@app.route("/traces")
def get_traces():
    return jsonify(TRACES)

if __name__ == "__main__":
    print("Flowing trace server running on port 9000")
    app.run(port=9000)
