from time import sleep
import requests
from bs4 import BeautifulSoup
import pandas as pd


def crawl_cirriculum(semester: int):
    df_full = pd.DataFrame(columns=["科目名稱", "科目代號", "班級代號", "班級名稱", "開班／選課人數"])
    try:
        if (semester > 2 or semester < 1):
            raise ValueError("請輸入介於 1 與 2 之間的數字")
        semester_cookie = {"ggdb": str(semester)}

        school = {
            "台北校區": "1",
            "桃園校區": "2",
            "金門校區": "3",
            "連江專班": "4",
            "基河校區": "5"
        }
        dict
        for k, v in school.items():
            form_data = [
                ('sch', v),  # 校區 1 ~ 5
                # ('dept1', '36'),      # 學系
                # ('sel', '1'),         # 選別
                # ('f26', '0'),         # 制別 e.g. 大學部
                # ('wk1', '1'),         # 日期篩選，與 ssec、esec 是一組的，也可以分開使用
                # ('ssec1', '6'),       # 開始節次
                # ('esec1', '8'),       # 結束節次
            ]

            print(f"處理{k}中...")
            r = requests.post(
                "https://www.mcu.edu.tw/student/new-query/sel-query/qslist_1.asp",
                cookies=semester_cookie,
                data=form_data,
            )

            r.encoding = "big5"

            soup = BeautifulSoup(r.text, 'html.parser')
            table = soup.select_one("table").prettify()

            df = pd.read_html(table, header=0)[0]
            df[["科目代號", "科目名稱"]] = df["科目"].str.strip().str.split(pat=" ",
                                                                  n=1,
                                                                  expand=True)
            df[["班級代號", "班級名稱"]] = df["班級"].str.strip().str.split(pat=" ",
                                                                  n=1,
                                                                  expand=True)
            df = df.copy()[["科目名稱", "科目代號", "班級代號", "班級名稱", "開班／選課人數"]]
            df_full = pd.concat([df_full, df], ignore_index=True)

            print("修眠5秒")
            sleep(5)
    except ValueError as err:
        print(err)

    df_full.to_csv("latest.csv", index=False)


if __name__ == "__main__":
    crawl_cirriculum(semester=1)
