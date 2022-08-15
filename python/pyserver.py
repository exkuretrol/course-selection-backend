from flask import Flask, request
from flask_cors import CORS, cross_origin
from pypinyin import Style, pinyin
from func.helper import findTeacherSubject
import json

app = Flask(__name__)
CORS(app, resources={
    r"/.*": {
        "origins": [
            "http://127.0.0.1:3000", 
            "http://localhost:3000"
        ]
    }
})

@app.route('/api/zhuyin', methods=['POST'])
def zhuyin():
    data = request.get_json()

    text = data['text']
    result = pinyin(text, style=Style.BOPOMOFO)
    result = [item for innerlist in result for item in innerlist]

    return json.dumps({"result": result})

@app.route('/api/filter', methods=['POST'])
def filter():
    req = request.get_json()
    text = req['text']
    sub, thr = findTeacherSubject(text)
    return json.dumps({"subject": sub, "teacher": thr})

if __name__ == "__main__":
    app.run(port=5000)
