
from flask import Flask, jsonify
import json
from pathlib import Path

app = Flask(__name__)


data_file = Path(__file__).with_name("eg5.json")


@app.route("/api/helloWorld", methods=["GET"])
def hello_world():
    return jsonify({"message": "Hello World"})


@app.route("/api/json", methods=["GET"])
def get_json():
    try:
        with open(data_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": f"{data_file.name} not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
