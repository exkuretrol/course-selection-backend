import string
from typing import List
from pypinyin import pinyin, Style
import re

def toZhuYin(word: string):
    se = pinyin(word, style=Style.BOPOMOFO)  #注音
    se = "".join([item for innerlist in se for item in innerlist])  #刪[]
    se = re.sub('[ˊˇˋ˙]','',se)
    return se

class NerToken:
  def __init__(self, word, ner, idx):
    self.word = word
    self.ner = ner
    self.idx = idx
  def __str__(self):
    return "NerToken(word='" + self.word + "', ner='" + self.ner + "', idx=[" + str(self.idx[0]) + ", " + str(self.idx[1]) + "]" + ")"

def ner_query(text: List[NerToken]):
    subject = []       #課程
    time_lesson = []   #時間_節
    time_week = []     #時間_週
    people = []        #老師
    department = []    #系別
    category = []      #選別
    grade = []         #年級
    campus = []        #校區
    # 老師課表不需要的別獨立出一個類別
    # curriculum = []    #課表
    credit = []        #學分
    semester = []      #學期
    education = []     #制別
    internship = []    #實習課
    graduate = []      #畢業班
    # location = []      #地點
    Class = []         #班級
    lesson = {'零':0,'一':1, '二':2, '三':3, '四':4, '五':5, '六':6, '七':7, '八':8, '九':9}
    Department = {'統之系': 17, '管理學院':'1152545657','國際企業學系':'57','國企系':'57','國企':'57','風險管理與保險學系':'56','風保系':'56','風保':'56', '會計學系':'52','會計系':'52','會計':'52','企業管理學系':'11','企管系':'11','企管':'11','財務金融學系':'54','財金系':'54', '財金':'54','資訊學院':'0513163637','資訊管理學系':'13','資管系':'13','資管':'13','資訊傳播工程學系':'16','資傳系':'16', '資傳':'16','資訊工程學系':'36','資工系':'36','資工':'36','電腦與通訊工程學系':'05','電通系':'05','電通':'05', '電子工程學系':'37','電子系':'37','電工系':'37','電子':'37','電工':'37','傳播學院':'26313233','廣播電視學系':'32','廣電系':'32', '廣電':'32','新聞學系':'33','新聞系':'33','新聞':'33','廣告暨策略行銷學系':'26','廣銷系':'26','廣銷':'26','新媒體暨傳播管理學系':'31', '新傳系':'31','新傳':'31','法律學院':'4165','法律學系':'41','法律系':'41','法律':'41','財金法律系':'65','財法系':'65','財法':'65', '觀光學院':'141819','觀光事業學系':'14','觀光系':'14','觀光':'14','休閒遊憩管理學系':'18','休憩系':'18','休憩':'18', '餐旅管理學系':'19','餐旅系':'19','餐旅':'19','教育暨應用語文學院':'4243444583','應用中國文學系':'43','應中系':'43','應中':'43', '應用英語學系':'42','應英系':'42','應英':'42','應用日語學系':'44','應日系':'44','應日':'44','教育研究所':'83','華語文教學學系':'45', '華教系':'45','華教':'45','設計學院':'040921232450','商業設計學系':'21','商設系':'21','商設':'21','商品設計學系':'23','品設系':'23', '品設':'23','數位媒體設計學系':'09','數媒系':'09','數媒':'09','都市規劃與防災學系':'04','都防系':'04','都防':'04','建築學系':'24', '建築系':'24','建築':'24','動漫文創設計學士學位學程':'50','動漫學程':'50','社會科學院':'083868','公共事務與行政管理學系':'68', '公事系':'68','公事':'68','諮商與工商心理學系':'08','心理系':'08','心理':'08','犯罪防治學系':'38','犯防系':'38','犯防':'38', '健康科技學院':'394067','生物科技學系':'39','生科系':'39','生科':'39','醫療資訊與管理學系':'40','醫管系':'40','醫管':'40', '生物醫學工程學系':'67','醫工系':'67','醫工':'67','國際學院':'252747485991','國際事務與外交學士學位學程':'59', '國際企業與貿易學士學位學程':'91','新聞與大眾傳播學士學位學程':'27','時尚與創新管理學士學位學程':'25','旅遊與觀光學士學位學程':'48', '資訊科技應用與管理學士學位學程':'47','金融科技學院':'172246','經濟與金融學系':'22','經濟系':'22','經濟':'22','應用統計與資料科學學系':'17', '統資系':'17','統資':'17','金融科技應用學士':'46','金科系':'46','金科':'46' } # people_count = 0 #老師數量 # subject_count = 0 #課程數量

    for sentence in text:
        # index = sentence.find(',')
        # word = sentence[15:index-1]     #抓word的字
        # if people_count == 1 :
        #     print('不好意思，最多只能輸入一名老師')
        #     break
        # elif subject_count == 1 :
        #     print('不好意思，最多只能輸入一個科目')
        #     break
        # else:
        word = sentence.word
        if 'SUBJECT' in sentence.ner:            #科目
            # subject_count += 1
            se = pinyin(word, style=Style.BOPOMOFO)  #注音
            se = "%%".join([item for innerlist in se for item in innerlist])  #刪[]
            se = re.sub('[ˊˇˋ˙]','',se)   #拿掉音調
            if 'ㄨㄟㄏㄜ' in se:
                se = se.replace('ㄨㄟㄏㄜ','web')
            if 'dyson' in se:
                se = se.replace('dyson','python')
            subject.append(se)
        elif 'TIME' in sentence.ner:             #時間
            word1 = word2 = '';
            if word == '早上' or word == '上午':
                word1 = '01020304'
            if word == '下午':
                word1 = '0506070809'
            if word == '晚上':
                word1 = '40506070'
            if '禮拜' in word:
                word2 = word.replace('禮拜','')
            if '星期' in word:
                word2 = word.replace('星期','')
            if '週' in word:
                word2 = word.replace('週','')
            #if 'ㄐㄧㄝ' in se or 'ㄊㄤ' in se:
            if '到' in word:
                t_index = word.find('到')
                t = ''
                b_index = t_index-1
                e_index = t_index+2

                if word[b_index] not in '123456789':
                    begin = lesson[word[b_index]][0]
                else :
                    begin = word[b_index]

                if word[e_index] not in '123456789':
                    end = lesson[word[e_index]][0]
                else :
                    end = word[e_index]
                
                for i in range(begin, end+1):
                    t = t + '0' + str(i)
                word1 = t

            if len(word1)>0:
                time_lesson.append(word1)
            else:
                time_week.append(word2)
            
        elif 'PEOPLE' in sentence.ner:           #老師
            # people_count += 1
            se = pinyin(word, style=Style.BOPOMOFO)  #注音
            l = [item for innerlist in se for item in innerlist]
            se = "%%".join(l)  #刪[]
            se = re.sub('[ˊˇˋ˙]','',se)   #拿掉音調
            # print(se)
            if 'ㄓㄨ%%ㄈㄥ' in se:
                print("A")
                people.append('ㄗㄨ%%ㄈㄥ')
            elif 'ㄇㄧㄥ%%ㄧㄤ' in se:
                print("B")
                people.append('ㄇㄧㄣ%%ㄧㄤ')
            else:
                people.append(se)
        elif 'DEPARTMENT' in sentence.ner:       #系
            # if word not in Department.keys():
            if '學院' in word:
                d = Department[word]
                for num in range(int(len(d)/2)):
                    department.append(d[num*2:num*2+2])
                continue
            else:
                department.append(Department[word])
        elif 'CATEGORY' in sentence.ner:         #選別
            word_zhuyin = toZhuYin(word)
            if toZhuYin('必修') == word_zhuyin:
                category.append('必修')
            if toZhuYin('選修') == word_zhuyin:
                category.append('選修')
            if toZhuYin('通識') == word_zhuyin:
                category.append('通識')
            if toZhuYin('教育') == word_zhuyin:
                category.append('教育')
        elif 'GRADE' in sentence.ner:            #年級
            if '年級' in word:
                word = word.replace('年級','')
            if '大' in word:
                word = word.replace('大','')
            if '一' in word:
                word = '1'
            if '二' in word or '兩' in word:
                word = '2'
            if '三' in word:
                word = '3'
            if '四' in word:
                word = '4'
            grade.append(word)
        elif 'CAMPUS' in sentence.ner:           #校區
            if '校區' in word:
                word = word.replace('校區','')
            se = pinyin(word, style=Style.BOPOMOFO)  #注音
            se = "".join([item for innerlist in se for item in innerlist])  #刪[]
            se = re.sub('[ˊˇˋ˙]','',se)   #拿掉音調
            if se == 'ㄐㄧㄏㄜ':
                word = '基河'
            elif se == 'ㄐㄧㄣㄇㄣ':
                word = '金門'
            elif se == 'ㄊㄠㄩㄢ':
                word = '桃園'
            elif se == 'ㄊㄞㄅㄟ':
                word = '台北'
            campus.append(word)
        # elif 'CURRICULUM' in sentence.ner:       #課表
        #     curriculum.append(word)
        #     #查課表?
        elif 'CREDIT' in sentence.ner:           #學分
            if '學分' in word:
                word = word.replace('學分','')
            if '一' in word:
                word = '1'
            if '二' in word or '兩' in word:
                word = '2'
            if '三' in word:
                word = '3'
            credit.append(word)
        elif 'SEMESTER' in sentence.ner:         #學期
            if '上' in word:
                word = '01'
            if '下' in word:
                word = '02'
            semester.append(word)
        elif 'INTERNSHIP' in sentence.ner:       #實習課
            word = '是'
            internship.append(word)
        elif 'GRADUATE' in sentence.ner:         #畢業班
            word = '是'
            graduate.append(word)
        # elif 'LOCATION' in sentence.ner:         #校園教室、大樓
            #桃
            # if 'sㄉㄨㄥ' in se or 'ㄗㄒㄩㄣㄉㄚㄌㄡ' in se or 'ㄕㄜㄎㄜㄉㄚㄌㄡ' in se:
            #     se = 'S'
            # if 'ㄧㄧㄉㄨㄥ' in se or 'eeㄉㄨㄥ' in se or 'ㄗㄨㄥㄏㄜㄐㄧㄠㄒㄩㄝㄉㄚㄌㄡ' in se:
            #     se = 'EE'
            # if 'aaㄉㄨㄥ' in se or 'ㄎㄜㄐㄧㄉㄚㄌㄡ' in se:
            #     se = 'AA'
            # if 'pㄉㄨㄥ' in se or 'ㄆㄧㄉㄨㄥ' in se or 'ㄍㄨㄢㄍㄨㄤㄩㄨㄣㄉㄚㄌㄡ' in se:
            #     se = 'P'
            # if 'ㄒㄧㄒㄧㄉㄨㄥ' in se or 'ccㄉㄨㄥ' in se or 'ㄗㄒㄩㄣㄨㄤㄌㄨㄉㄚㄌㄡ' in se:
            #     se = 'CC'
            # if 'mㄉㄨㄥ' in se or 'ㄕㄜㄐㄧㄉㄚㄌㄡ' in se:
            #     se = 'M'
            # if 'ㄅㄧㄅㄧㄉㄨㄥ' in se or 'bbㄉㄨㄥ' in se or 'ㄕㄜㄏㄨㄟㄎㄜㄒㄩㄝㄉㄚㄌㄡ' in se:
            #     se = 'BB'
            # #北
            # if 'bㄉㄨㄥ' in se or 'ㄅㄧㄉㄨㄥ' in se or 'ㄎㄨㄞㄐㄧㄉㄚㄌㄡ' in se or 'ㄈㄚㄒㄩㄝㄉㄚㄌㄡ' in se:
            #     se = 'B'
            # if 'ㄧㄉㄨㄥ' in se or 'eㄉㄨㄥ' in se or 'ㄍㄨㄛㄑㄧㄐㄧㄘㄞㄉㄚㄌㄡ' in se or 'ㄐㄧㄠㄩㄉㄚㄌㄡ' in se:
            #     se = 'E'
            # if 'ㄟㄑㄩㄉㄨㄥ' in se or 'hㄉㄨㄥ' in se or 'ㄔㄨㄢㄅㄛㄉㄚㄌㄡ' in se:
            #     se = 'H'
            # if 'ㄟㄈㄨㄉㄨㄥ' in se or 'fㄉㄨㄥ' in se or 'ㄑㄧㄍㄨㄢㄐㄧㄈㄥㄍㄨㄢㄉㄚㄌㄡ' in se:
            #     se = 'F'
            # if 'ㄉㄧㄉㄨㄥ' in se or 'ㄉㄧㄧㄉㄨㄥ' in se or 'dㄉㄨㄥ' in se or 'ㄇㄧㄥㄉㄠㄌㄡ' in se:
            #     se = 'D'
            # location.append(se)
        elif 'CLASS' in sentence.ner:            #班級
            se = pinyin(word, style=Style.BOPOMOFO)  #注音
            se = "".join([item for innerlist in se for item in innerlist])  #刪[]
            se = re.sub('[ˊˇˋ˙]','',se)   #拿掉音調
            if se == 'ㄐㄧㄚ':
                word = '甲'
            if se == 'ㄧ':
                word = '乙'
            if se == 'ㄅㄧㄥ':
                word = '丙'
            if se == 'ㄉㄧㄥ':
                word = '丁'
            Class.append(word)

    res = dict(people=people, category=category, grade=grade, department=department, time_lesson=time_lesson, time_week=time_week, campus=campus, subject=subject, credit=credit, semester=semester, education=education, internship=internship, graduate=graduate, stuclass=Class)
    print(res)

    sql = "SELECT * FROM `all_course_del` WHERE "
    cond = []
    # 制別
    # 科目代號
    # 科目名稱
    # 科目名稱注音	
    # 班級代號
    # 班級名稱
    # 任課教師
    # 任課教師注音	
    # 老師簡稱
    # 老師簡稱注音	
    # 上課日期／節次
    # 年級
    # 教室
    # 校區
    # 選別
    # 學分
    # 類別
    # 畢業班
    # 學期數
    # 說明
    # 實習課

    for k, v in res.items():
        # print(k, len(v))
        if k == 'subject' and len(v) > 0:
            for search in v:
                cond.append(f"`科目名稱注音` like '%%{search}%%'")
        if k == 'time_lesson' and len(v) > 0:
            for search in v:
                l = [f"`上課日期／節次` like '%%{search[i:i+2]}%%'" for i in range(0, len(search), 2)];
            cond.append('(' + ' or '.join(l) + ')');
        if k == 'time_week' and len(v) > 0:
            l = []
            for search in v:
                l.append(f"left(`上課日期／節次`, 1) = '{search}'")
            cond.append('(' + ' or '.join(l) + ')')
        if k == 'people' and len(v) > 0:
            for search in v:
                cond.append(f"`任課教師注音` like '%%{search}%%'")
        if k == 'department' and len(v) > 0:
            for search in v:
                cond.append("left(`班級代號`, 2) = '%s'"%(search))
        if k == 'category' and len(v) > 0:
            for search in v:
                cond.append("`選別` = '%s'"%(search))
        if k == 'grade' and len(v) > 0:
            for search in v:
                cond.append("`年級` = '%s'"%(search))
        # TODO: 校區注音還沒搞
        if k == 'campus' and len(v) > 0:
            for search in v:
                cond.append("`校區` = '%s'"%(search))
        # if k == 'curriculum' and len(v) > 0: #課表
        #     sql = "SELECT * FROM `TEST` WHERE " #課表怎麼印O.O
        if k == 'credit' and len(v) > 0:
            for search in v:
                cond.append("`學分` = '%s'"%(search))
        if k == 'semester' and len(v) > 0:
            for search in v:
                cond.append("`學期數` = '%s'"%(search))
        if k == 'education' and len(v) > 0:
            for search in v:
                cond.append("`制別` = '%s'"%(search))
        if k == 'internship' and len(v) > 0:
            for search in v:
                cond.append("`實習課` = '%s'"%(search))
        if k == 'graduate' and len(v) > 0:
            for search in v:
                cond.append("`畢業班` = '%s'"%(search))
        if k == 'Class' and len(v) > 0:
            for search in v:
                cond.append("`班級` = '%s'"%(search))
        # TODO: 先固定為上學期
        # cond.append("`學期數` = '上學期'");

    if len(cond) == 0:
        sql += "0";
    if len(cond) == 1:
        sql += cond[0];
        sql += " and `學期數` = '上學期'";
    if len(cond) > 1: 
        sql += ' and '.join(cond);
        sql += " and `學期數` = '上學期'";
    return sql