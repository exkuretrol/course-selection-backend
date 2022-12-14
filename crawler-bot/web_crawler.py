import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep, strftime
from pathlib import Path
from schedule import run_pending, repeat, every

output_dir = Path().parent.absolute() / "output"
if not (output_dir.exists()):
    output_dir.mkdir()

def crawl_cirriculum(semester: int) -> None:
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

            r = requests.post(
                "https://www.mcu.edu.tw/student/new-query/sel-query/qslist_1.asp",
                cookies=semester_cookie,
                data=form_data,
            )

            r.encoding = "big5"

            soup = BeautifulSoup(r.text, 'html.parser')
            table = soup.select_one("table").prettify()

            # TODO: add exception here.
            df = pd.read_html(table, header=0)[0]
            df[["科目代號", "科目名稱"]] = df["科目"].str.strip().str.split(pat=" ",
                                                                  n=1,
                                                                  expand=True)
            df[["班級代號", "班級名稱"]] = df["班級"].str.strip().str.split(pat=" ",
                                                                  n=1,
                                                                  expand=True)
            df = df.copy()[["科目名稱", "科目代號", "班級代號", "班級名稱", "開班／選課人數"]]
            df_full = pd.concat([df_full, df], ignore_index=True)

            sleep(5)
    except ValueError as err:
        print(err)

    # TODO: join by class id, subject id and semester?
    output_file = output_dir / f"semester_{semester}.csv"
    df_full.to_csv(output_file, index=False)

@repeat(every(5).minutes)
def crawl_all_cirrisulum() -> None:
    crawl_cirriculum(semester=1)
    crawl_cirriculum(semester=2)
    semester_1_csv = output_dir / "semester_1.csv"
    semester_2_csv = output_dir / "semester_2.csv"
    latest_csv = output_dir / "latest.csv"
    
    semester_1_df = pd.read_csv(semester_1_csv, header=0)
    semester_2_df = pd.read_csv(semester_2_csv, header=0)

    if (semester_1_csv.exists()):
        semester_1_csv.unlink()

    if (semester_2_csv.exists()):
        semester_2_csv.unlink()

    if (latest_csv.exists()):
        latest_csv.rename(output_dir / f"latest_{strftime('%Y-%m-%d %H:%M')}.csv")

    pd.concat([semester_1_df, semester_2_df]).to_csv(latest_csv, index=False)
    print(f"{strftime('%Y-%m-%d %H:%M')}執行完畢")

while True:
    run_pending()
    sleep(1)
