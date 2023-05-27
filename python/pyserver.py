from flask import Flask, request, make_response
from flask_cors import CORS
from pypinyin import Style, pinyin
from func.ner_query import ner_query
import json
from ckip_transformers.nlp import CkipNerChunker
from sqlalchemy import create_engine, exc
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from os import getenv
from pathlib import Path

selection_status_file = Path().parent.absolute() / "output" / "latest.csv"

load_dotenv()
model_name = getenv('model_name')

url = f"mysql+pymysql://{getenv('user')}:{getenv('pass')}@{getenv('host')}:{getenv('port')}/NER"

engine = create_engine(url, pool_recycle=3600)

print("Initializing drivers ... NER")
ner_driver = CkipNerChunker(model_name=model_name)
print("Initializing drivers ... done")

app = Flask(__name__)
CORS(app,
     resources={
         r"/.*": {
             "origins": ["http://127.0.0.1:3000", "http://localhost:3000"]
         }
     })


@app.route('/api/zhuyin', methods=['POST'])
def zhuyin():
    data = request.get_json()

    text = data['text']
    result = pinyin(text, style=Style.BOPOMOFO)
    result = [item for innerlist in result for item in innerlist]

    return json.dumps({"result": result})


@app.route('/api/ner', methods=['POST'])
def ner():
    req = request.get_json()
    if len(req['text']) == 0:
        return json.dumps({"result": ""})

    if (req['multiple']):
        text = req['text']
    else:
        # add outer list
        text = [req['text']]

    ner = ner_driver(text)

    def format2object(ner_item):
        return [{
            "word": entity.word,
            "tag": entity.ner,
            "idx": [entity.idx[0], entity.idx[1]]
        } for entity in ner_item]

    query_statement = ner_query(ner[0])
    try:
        query_result = pd.read_sql_query(query_statement, engine)
        # 科目名稱,科目代號,班級代號,班級名稱,開班／選課人數
        tdf = pd.read_csv(selection_status_file,
                          dtype={
                              '科目名稱': 'str',
                              '科目代號': 'str',
                              '班級代號': 'str',
                              '班級名稱': 'str',
                              '開班／選課人數': 'str'
                          })
        tdf.drop(["科目名稱", "班級名稱"], inplace=True, axis=1)
        query_result = pd.merge(query_result, tdf, on=[
                                '科目代號', '班級代號'], how='left')
        print(query_result)
        query_result = query_result.to_json(orient='split', force_ascii=False)
        query_result = json.loads(query_result)
        response = {
            "status": "success",
            "result": [format2object(nerr) for nerr in ner],
            "tbl": query_result,
            "sql": query_statement
        }
        return make_response(json.dumps(response), 200)
    except exc.SQLAlchemyError:
        response = {
            "status": "error",
            "sql": query_statement,
        }
        return make_response(json.dumps(response), 400)


@app.route('/api/queryById', methods=['POST'])
def query():
    try:
        req = request.get_json()
        course_list = ", ".join([str(i) for i in req['courses']])
        query_statement = f"SELECT * FROM `all_course_del` WHERE `No.` in ({course_list}) ;"
        query_result = pd.read_sql_query(query_statement,
                                         engine).to_json(orient='split')
        query_result = json.loads(query_result)
        return make_response(
            json.dumps({
                "status": "success",
                "tbl": query_result,
                "sql": query_statement
            }), 200)
    except exc.SQLAlchemyError:
        return make_response(
            json.dumps({
                "status": "error",
                "sql": query_statement
            }), 400)


@app.route('/api/uploadcirriculum', methods=['POST'])
def cirriculum():
    try:
        html_doc = request.files['File'].read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        # css selector: body > div:nth-child(1) > table:nth-child(10)

        table = soup.select_one('body table[bordercolor="#77BBFF"]').prettify()

        converters = {
            '班級代號': str,
            '科目代號／科目名稱': str,
            '選別': str,
            '教室': str,
            '學分': str,
            '是否正課': str,
            '星期': str,
            '起節次': str,
            '終節次': str
        }

        print(pd.read_html(table, header=0, converters=converters)[0])
        df = pd.read_html(table, header=0, converters=converters)[0]

        df2 = df.dropna()

        newdf = df2["科目代號／科目名稱"].str.split("　", expand=True)
        newdf2 = df2.copy()

        newdf2[["科目代號", "科目名稱"]] = newdf

        df3 = newdf2.drop("科目代號／科目名稱", axis=1)

        df3: pd.DataFrame = df3[df3.columns[[8, 9, 0, 1, 2, 3, 4, 5, 6, 7]]]

        return make_response(
            json.dumps({
                "status": "success",
                "tbl": json.loads(df3.to_json(orient='split'))
            }), 200)
    except:
        return make_response(json.dumps({"status": "error"}), 400)


if __name__ == "__main__":
    app.run(port=5000)
