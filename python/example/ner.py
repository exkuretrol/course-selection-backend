from dotenv import load_dotenv
from ckip_transformers.nlp import CkipNerChunker
from os import getenv
from pathlib import Path

load_dotenv()
model_name = getenv("model_name")

model_path = Path().parent.absolute().parent / model_name

print("Initializing drivers ... NER")
ner_driver = CkipNerChunker(model_name=model_path)
print("Initializing drivers ... done")

def format2object(ner_item):
    return [{
        "word": entity.word,
        "tag": entity.ner,
        "idx": [entity.idx[0], entity.idx[1]]
    } for entity in ner_item]

print("請輸入測試語句，如輸入 stop 則停止。")
while True:
    s = input()
    if (s == "stop"): break
    ner = ner_driver([s])
    print([format2object(ner_item) for ner_item in ner])
