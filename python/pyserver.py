from flask import Flask, request
from pypinyin import Style, pinyin
import json

app = Flask(__name__)

@app.route('/zhuyin', methods=['POST'])
def zhuyin():
    data = request.get_json()
    print(request)
    print(data)

    text = data['text']
    result = pinyin(text, style=Style.BOPOMOFO)
    result = [item for innerlist in result for item in innerlist]

    return json.dumps({"result": result})

if __name__ == "__main__":
    app.run(port=5000)
