from functools import reduce
from pypinyin import pinyin, Style
import pandas as pd

subject = pd.read_csv("func/課程注音.csv")
teacher = pd.read_csv("func/老師注音.csv")

def findTeacherSubject(text: str) -> tuple:
    sub = None
    thr = None

    result = pinyin(text, style=Style.BOPOMOFO)
    BOPOMOFO = "".join([item for innerlist in result for item in innerlist])
    repls = ('ˊ', ''), ('ˇ', ''), ('ˋ', ''), ('˙', ''), (' ', '')
    BOPOMOFO_NOPUN = reduce(lambda a, kv: a.replace(*kv), repls, BOPOMOFO)

    for i in range(len(subject)):
        find_loc = BOPOMOFO_NOPUN.find(subject['去聲調_class'][i])
        if find_loc != -1:
            sub = subject['class'][i]
            break
            
    for i in range(len(teacher)):
        find_loc = BOPOMOFO_NOPUN.find(teacher['去聲調_teacher'][i])
        if find_loc != -1:
            thr = teacher['teacher'][i]
            break
        
    return (sub, thr)