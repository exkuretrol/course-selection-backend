from flask import Flask, request
from flask_cors import CORS, cross_origin
from pypinyin import Style, pinyin
from func.helper import findTeacherSubject
import json
from ckip_transformers.ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker

print("Initializing drivers ... NER")
ner_driver = CkipNerChunker(model_name="./test-ner3600")
print("Initializing drivers ... done")

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


@app.route('/api/ner', methods=['POST'])
def ner():
    req = request.get_json()
    if (req['multiple']):
        text = req['text']
    else:
        text = [req['text']]

    ner = ner_driver(text)

    def format2json(ner_item):
        return [
            {
                "word": entity.word,
                "tag": entity.ner,
                "idx": [entity.idx[0], entity.idx[1]]
            } for entity in ner_item
        ]
    
    return json.dumps({"result": [format2json(nerr) for nerr in ner]});

if __name__ == "__main__":
    app.run(port=5000)
