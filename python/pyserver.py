from flask import Flask, request
from flask_cors import CORS, cross_origin
from pypinyin import Style, pinyin
from func.helper import findTeacherSubject
from func.ner_query import ner_query
import json
from ckip_transformers.ckip_transformers.nlp import CkipNerChunker

model_name = "./test-ner3696"

print("Initializing drivers ... NER")
ner_driver = CkipNerChunker(model_name=model_name)
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
    print(req);
    if len(req['text']) == 0: return json.dumps({"result": ""});
    if (req['multiple']):
        text = req['text'];
    else:
        text = [req['text']];
    
    
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
    # return json.dumps({"result": ""});

if __name__ == "__main__":
    app.run(port=5000)
