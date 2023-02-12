import MySQLdb
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import warnings
warnings.filterwarnings('ignore')
import IPython
import lightgbm as lgb

from function import mince_data,mouse_speed,mouse_speed_period,mouse_speed_click_pre,mouse_event_click_pre,mouse_speed_click_rear,mouse_event_click_rear,mouse_speed_scroll_rear,mouse_event_scroll_rear,test

questionnaire_id = 3

# mode
# 1:クリック直前
# 2:クリック直後
# 3:スクール直後
# 4:選択直前
# 5:選択直後
# 6:スクロール直後(0~3000)
mode = 6

# データベースへの接続とカーソルの生成
connection = MySQLdb.connect(
    host='localhost',
    user='ubuntu',
    passwd='Aquos.123',
    db='survey')
cursor = connection.cursor()

cursor.execute("SELECT * FROM Answers")
answers_list = cursor.fetchall()
cursor.execute("SELECT * FROM AnswerData")
answer_data_list = cursor.fetchall()

# 保存を実行
connection.commit()
# 接続を閉じる
connection.close()


# 回答を辞書型に
answers_dict = {}
answer_id = 0
for answers_line in answers_list:
    if(answers_line[1] == questionnaire_id and answers_line[4] == 0):
        if(answer_id != answers_line[0]):
            answers_dict[answers_line[0]] = {answers_line[2] : answers_line[3]}
            answer_id = answers_line[0]
        else:
            answers_dict[answers_line[0]].update({answers_line[2] : answers_line[3]})

# アンサーデータを辞書型に
answer_id_list = []
questionnaire_id_dict = {}
scroll_dict = {}
coordinates_dict = {}
click_dict = {}
windowsize_dict = {}
background_dict = {}
checking_dict = {}
type_dict = {}
enter_leave_dict = {}
total_dict = {}
device_dict = {}
created_at_dict = {}
for answer_data_line in answer_data_list:
    if(answer_data_line[0] in answers_dict):                   # <-delete除去,questionnaireid=3
        answer_id_list.append(answer_data_line[0])
        questionnaire_id_dict[answer_data_line[0]] = answer_data_line[1]
        scroll_dict[answer_data_line[0]] = json.loads(answer_data_line[2])
        coordinates_dict[answer_data_line[0]] = json.loads(answer_data_line[3])
        click_dict[answer_data_line[0]] = json.loads(answer_data_line[4])
        windowsize_dict[answer_data_line[0]] = json.loads(answer_data_line[5])
        background_dict[answer_data_line[0]] = json.loads(answer_data_line[6])
        checking_dict[answer_data_line[0]] = json.loads(answer_data_line[7])
        type_dict[answer_data_line[0]] = json.loads(answer_data_line[8])
        enter_leave_dict[answer_data_line[0]] = json.loads(answer_data_line[9])
        total_dict[answer_data_line[0]] = json.loads(answer_data_line[10])
        device_dict[answer_data_line[0]] = answer_data_line[11]
        created_at_dict[answer_data_line[0]] = answer_data_line[12]




# <--------------------ここからはデータセットの作成-------------------->
print("--------------------データ--------------------")

data_set = []
for i in range(len(answer_id_list)):
    data_tmp = {}
    # data_tmp['answer_id'] = answer_id_list[i]               # 後で消す
    data_tmp['target'] = int(answers_dict[answer_id_list[i]][30])
    data_tmp['click_amount'] = len(click_dict[answer_id_list[i]])
    data_tmp['mouse_amount'] = len(coordinates_dict[answer_id_list[i]])
    data_tmp['mouse_ave'] = mouse_speed(100,coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])
    data_tmp['mouse_speed_click_pre'] = mouse_speed_click_pre(500, 0, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])
    data_tmp['mouse_event_click_pre'] = mouse_event_click_pre(coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]])
    data_tmp['mouse_speed_click_rear'] = mouse_speed_click_rear(0, 500, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]])
    data_tmp['mouse_event_click_rear'] = mouse_event_click_rear(coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]])
    data_tmp['mouse_speed_scroll_rear'] = mouse_speed_scroll_rear(0, 500, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])
    data_tmp['mouse_event_scroll_rear'] = mouse_event_scroll_rear(coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])
    data_tmp['ratio_mouse_speed_click_pre'] = data_tmp['mouse_speed_click_pre']/data_tmp['mouse_ave']                                                                               #通常のマウススピードとクリック直前のマウススピードの比較
    data_tmp['ave_mouse_event_click_pre'] = mouse_event_click_pre(coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]])/len(click_dict[answer_id_list[i]])            #１クリックあたりの平均マウスイベント数(クリック直前)
    data_tmp['ratio_mouse_speed_click_rear'] = data_tmp['mouse_speed_click_rear']/data_tmp['mouse_ave']                                                                             #通常のマウススピードとクリック直後のマウススピードの比較
    data_tmp['ratio_mouse_speed_click_pre_and_rear'] = data_tmp['mouse_speed_click_rear']/data_tmp['mouse_speed_click_pre']                                                         # speed rear / pre
    data_tmp['ave_mouse_event_click_rear'] = mouse_event_click_rear(coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]])/len(click_dict[answer_id_list[i]])          #１クリックあたりの平均マウスイベント数(クリック直後)
    data_tmp['ratio_mouse_event_click_pre_and_rear'] = mouse_event_click_rear(coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]])/mouse_event_click_pre(coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]])     # event rear / pre
    data_tmp['ratio_mouse_speed_scroll_rear'] = data_tmp['mouse_speed_scroll_rear']/data_tmp['mouse_ave']                                                                           #通常のマウススピードとスクロール直後のマウススピードの比較
    data_tmp['ave_mouse_event_scroll_rear'] = mouse_event_scroll_rear(coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/len(scroll_dict[answer_id_list[i]])      #１スクロールあたりの平均マウスイベント数(スクロール直後)

    if(mode == 1):
        # クリック直前
        data_tmp['1000~900'] = mouse_speed_click_pre(1000, 900, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['900~800'] = mouse_speed_click_pre(900, 800, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['800~700'] = mouse_speed_click_pre(800, 700, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['700~600'] = mouse_speed_click_pre(700, 600, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['600~500'] = mouse_speed_click_pre(600, 500, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['500~400'] = mouse_speed_click_pre(500, 400, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['400~300'] = mouse_speed_click_pre(400, 300, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['300~200'] = mouse_speed_click_pre(300, 200, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['200~100'] = mouse_speed_click_pre(200, 100, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['100~0'] = mouse_speed_click_pre(100, 0, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
    
    if(mode == 2):
        # クリック直後
        data_tmp['0~100'] = mouse_speed_click_rear(0, 100, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['100~200'] = mouse_speed_click_rear(100, 200, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['200~300'] = mouse_speed_click_rear(200, 300, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['300~400'] = mouse_speed_click_rear(300, 400, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['400~500'] = mouse_speed_click_rear(400, 500, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['500~600'] = mouse_speed_click_rear(500, 600, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['600~700'] = mouse_speed_click_rear(600, 700, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['700~800'] = mouse_speed_click_rear(700, 800, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['800~900'] = mouse_speed_click_rear(800, 900, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['900~1000'] = mouse_speed_click_rear(900, 1000, coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
    
    if(mode == 3):
        # スクロール直後
        data_tmp['0~100'] = mouse_speed_scroll_rear(0, 100, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['100~200'] = mouse_speed_scroll_rear(100, 200, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['200~300'] = mouse_speed_scroll_rear(200, 300, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['300~400'] = mouse_speed_scroll_rear(300, 400, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['400~500'] = mouse_speed_scroll_rear(400, 500, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['500~600'] = mouse_speed_scroll_rear(500, 600, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['600~700'] = mouse_speed_scroll_rear(600, 700, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['700~800'] = mouse_speed_scroll_rear(700, 800, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['800~900'] = mouse_speed_scroll_rear(800, 900, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['900~1000'] = mouse_speed_scroll_rear(900, 1000, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
    
    if(mode == 4):
        # 選択直前
        data_tmp['1000~900'] = mouse_speed_click_pre(1000, 900, coordinates_dict[answer_id_list[i]], checking_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['900~800'] = mouse_speed_click_pre(900, 800, coordinates_dict[answer_id_list[i]], checking_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['800~700'] = mouse_speed_click_pre(800, 700, coordinates_dict[answer_id_list[i]], checking_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['700~600'] = mouse_speed_click_pre(700, 600, coordinates_dict[answer_id_list[i]], checking_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['600~500'] = mouse_speed_click_pre(600, 500, coordinates_dict[answer_id_list[i]], checking_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['500~400'] = mouse_speed_click_pre(500, 400, coordinates_dict[answer_id_list[i]], checking_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['400~300'] = mouse_speed_click_pre(400, 300, coordinates_dict[answer_id_list[i]], checking_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['300~200'] = mouse_speed_click_pre(300, 200, coordinates_dict[answer_id_list[i]], checking_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['200~100'] = mouse_speed_click_pre(200, 100, coordinates_dict[answer_id_list[i]], checking_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['100~0'] = mouse_speed_click_pre(100, 0, coordinates_dict[answer_id_list[i]], checking_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
    
    if(mode == 5):
        # 選択直後
        data_tmp['0~100'] = mouse_speed_click_rear(0, 100, coordinates_dict[answer_id_list[i]], checking_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['100~200'] = mouse_speed_click_rear(100, 200, coordinates_dict[answer_id_list[i]], checking_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['200~300'] = mouse_speed_click_rear(200, 300, coordinates_dict[answer_id_list[i]], checking_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['300~400'] = mouse_speed_click_rear(300, 400, coordinates_dict[answer_id_list[i]], checking_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['400~500'] = mouse_speed_click_rear(400, 500, coordinates_dict[answer_id_list[i]], checking_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['500~600'] = mouse_speed_click_rear(500, 600, coordinates_dict[answer_id_list[i]], checking_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['600~700'] = mouse_speed_click_rear(600, 700, coordinates_dict[answer_id_list[i]], checking_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['700~800'] = mouse_speed_click_rear(700, 800, coordinates_dict[answer_id_list[i]], checking_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['800~900'] = mouse_speed_click_rear(800, 900, coordinates_dict[answer_id_list[i]], checking_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['900~1000'] = mouse_speed_click_rear(900, 1000, coordinates_dict[answer_id_list[i]], checking_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
    
    if(mode == 6):
        # スクロール直後(0~3000)
        # data_tmp['0~100'] = mouse_speed_scroll_rear(0, 300, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        # data_tmp['100~200'] = mouse_speed_scroll_rear(300, 600, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        # data_tmp['200~300'] = mouse_speed_scroll_rear(600, 900, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        # data_tmp['300~400'] = mouse_speed_scroll_rear(900, 1200, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        # data_tmp['400~500'] = mouse_speed_scroll_rear(1200, 1500, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        # data_tmp['500~600'] = mouse_speed_scroll_rear(1500, 1800, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        # data_tmp['600~700'] = mouse_speed_scroll_rear(1800, 2100, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        # data_tmp['700~800'] = mouse_speed_scroll_rear(2100, 2400, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        # data_tmp['800~900'] = mouse_speed_scroll_rear(2400, 2700, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        # data_tmp['900~1000'] = mouse_speed_scroll_rear(2700, 3000, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['0~100'] = mouse_speed_scroll_rear(0, 100, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['100~200'] = mouse_speed_scroll_rear(100, 200, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['200~300'] = mouse_speed_scroll_rear(200, 300, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['300~400'] = mouse_speed_scroll_rear(300, 400, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['400~500'] = mouse_speed_scroll_rear(400, 500, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['500~600'] = mouse_speed_scroll_rear(500, 600, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['600~700'] = mouse_speed_scroll_rear(600, 700, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['700~800'] = mouse_speed_scroll_rear(700, 800, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['800~900'] = mouse_speed_scroll_rear(800, 900, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['900~1000'] = mouse_speed_scroll_rear(900, 1000, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['1000~1100'] = mouse_speed_scroll_rear(1000, 1100, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['1100~1200'] = mouse_speed_scroll_rear(1100, 1200, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['1200~1300'] = mouse_speed_scroll_rear(1200, 1300, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['1300~1400'] = mouse_speed_scroll_rear(1300, 1400, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['1400~1500'] = mouse_speed_scroll_rear(1400, 1500, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['1500~1600'] = mouse_speed_scroll_rear(1500, 1600, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['1600~1700'] = mouse_speed_scroll_rear(1600, 1700, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['1700~1800'] = mouse_speed_scroll_rear(1700, 1800, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['1800~1900'] = mouse_speed_scroll_rear(1800, 1900, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['1900~2000'] = mouse_speed_scroll_rear(1900, 2000, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['2000~2100'] = mouse_speed_scroll_rear(2000, 2100, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['2100~2200'] = mouse_speed_scroll_rear(2100, 2200, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['2200~2300'] = mouse_speed_scroll_rear(2200, 2300, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['2300~2400'] = mouse_speed_scroll_rear(2300, 2400, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']  
        data_tmp['2400~2500'] = mouse_speed_scroll_rear(2400, 2500, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['2500~2600'] = mouse_speed_scroll_rear(2500, 2600, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['2600~2700'] = mouse_speed_scroll_rear(2600, 2700, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['2700~2800'] = mouse_speed_scroll_rear(2700, 2800, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['2800~2900'] = mouse_speed_scroll_rear(2800, 2900, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
        data_tmp['2900~3000'] = mouse_speed_scroll_rear(2900, 3000, coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/data_tmp['mouse_ave']
    
    
    data_set.append(data_tmp)


df = pd.DataFrame(data = data_set)
X = df.loc[:, (df.columns !='target')]
# X = pd.get_dummies(X, drop_first=True)
y = df['target']

print('＜集中＞')
print(df[df['target'] == 0])
print(" ")
print('＜適当＞')
print(df[df['target'] == 1])
print(" ")








# <--------------------ヒューリスティックに予測してみる-------------------->
print("--------------------予測結果--------------------")

print('＜集中＞')
#df_a = df[df['target'] == 0].loc[:,['ratio_mouse_speed_click_pre','ratio_mouse_speed_click_rear','ratio_mouse_speed_scroll_rear']]
if(mode == 1 or mode == 4):
    df_a = df[df['target'] == 0].loc[:,['1000~900','900~800','800~700','700~600','600~500','500~400','400~300','300~200','200~100','100~0']]
if(mode == 2 or mode == 3 or mode == 5):
    df_a = df[df['target'] == 0].loc[:,['0~100','100~200','200~300','300~400','400~500','500~600','600~700','700~800','800~900','900~1000']]
if(mode == 6):
    df_a = df[df['target'] == 0].loc[:,['0~100','100~200','200~300','300~400','400~500','500~600','600~700','700~800','800~900','900~1000','1000~1100','1100~1200','1200~1300','1300~1400','1400~1500','1500~1600','1600~1700','1700~1800','1800~1900','1900~2000','2000~2100','2100~2200','2200~2300','2300~2400','2400~2500','2500~2600','2600~2700','2700~2800','2800~2900','2900~3000']]
print(df_a)
sum_click_amount = 0
sum_mouse_amount = 0
sum_ratio_mouse_speed_click_pre = 0
sum_ratio_mouse_speed_click_rear = 0
sum_ratio_mouse_speed_click_pre_and_rear = 0
sum_ratio_mouse_speed_scroll_rear = 0
j = 0
for data in data_set:
    if data['target'] == 0:
        # print(data, )
        j += 1
        sum_click_amount += data['click_amount']
        sum_mouse_amount += data['mouse_amount']
        sum_ratio_mouse_speed_click_pre += data['ratio_mouse_speed_click_pre']
        sum_ratio_mouse_speed_click_rear += data['ratio_mouse_speed_click_rear']
        sum_ratio_mouse_speed_click_pre_and_rear += data['ratio_mouse_speed_click_pre_and_rear']
        sum_ratio_mouse_speed_scroll_rear += data['ratio_mouse_speed_scroll_rear']
print('----------average----------')
print("click_amount:", sum_click_amount/j)
print("mouse_amount:", sum_mouse_amount/j)
print("ratio_mouse_speed_click_pre:",sum_ratio_mouse_speed_click_pre/j)
print("ratio_mouse_speed_click_rear:",sum_ratio_mouse_speed_click_rear/j)
print("ratio_mouse_speed_click_pre_and_rear:",sum_ratio_mouse_speed_click_pre_and_rear/j)
print("ratio_mouse_speed_scroll_rear:",sum_ratio_mouse_speed_scroll_rear/j)
print(' ')
sum_click_amount = 0
sum_mouse_amount = 0
sum_ratio_mouse_speed_click_pre = 0
sum_ratio_mouse_speed_click_rear = 0
sum_ratio_mouse_speed_click_pre_and_rear = 0
sum_ratio_mouse_speed_scroll_rear = 0
j = 0


print('＜適当＞')
#df_b = df[df['target'] == 1].loc[:,['ratio_mouse_speed_click_pre','ratio_mouse_speed_click_rear','ratio_mouse_speed_scroll_rear']]
if(mode == 1 or mode == 4):
    df_b = df[df['target'] == 1].loc[:,['1000~900','900~800','800~700','700~600','600~500','500~400','400~300','300~200','200~100','100~0']]
if(mode == 2 or mode == 3 or mode == 5 or mode == 6):
    df_b = df[df['target'] == 1].loc[:,['0~100','100~200','200~300','300~400','400~500','500~600','600~700','700~800','800~900','900~1000']]
print(df_b)
for data in data_set:
    if data['target'] == 1:
        # print(data)
        j += 1
        sum_click_amount += data['click_amount']
        sum_mouse_amount += data['mouse_amount']
        sum_ratio_mouse_speed_click_pre += data['ratio_mouse_speed_click_pre']
        sum_ratio_mouse_speed_click_rear += data['ratio_mouse_speed_click_rear']
        sum_ratio_mouse_speed_click_pre_and_rear += data['ratio_mouse_speed_click_pre_and_rear']
        sum_ratio_mouse_speed_scroll_rear += data['ratio_mouse_speed_scroll_rear']
print('----------average----------')
print("click_amount:", sum_click_amount/j)
print("mouse_amount:", sum_mouse_amount/j)
print("ratio_mouse_speed_click_pre:",sum_ratio_mouse_speed_click_pre/j)
print("ratio_mouse_speed_click_rear:",sum_ratio_mouse_speed_click_rear/j)
print("ratio_mouse_speed_click_pre_and_rear:",sum_ratio_mouse_speed_click_pre_and_rear/j)
print("ratio_mouse_speed_scroll_rear:",sum_ratio_mouse_speed_scroll_rear/j)



# 入力(各特徴量の値)に対して0~1にスケーリングした値を返す


# 箱ひげ図の描画

plt.style.use('default')
sns.set()
sns.set_style('whitegrid')
sns.set_palette('Set3')
plt.rcParams["font.size"] = 30

# 縦横転置
df_a_t = df_a.T
df_b_t = df_b.T
# pandasDataFrame -> list
la = df_a_t.values.tolist()
lb = df_b_t.values.tolist()
# plt.boxplot(la, showmeans=True, boxprops=dict(color='black', linewidth=1),medianprops=dict(color='black', linewidth=1),whiskerprops=dict(color='black', linewidth=1),capprops=dict(color='black', linewidth=1),flierprops=dict(markeredgecolor='black', markeredgewidth=1))
# plt.boxplot(lb, showmeans=True, boxprops=dict(color='blue', linewidth=1),medianprops=dict(color='blue', linewidth=1),whiskerprops=dict(color='blue', linewidth=1),capprops=dict(color='blue', linewidth=1),flierprops=dict(markeredgecolor='blue', markeredgewidth=1))
# plt.ylim(0, 0.5)

# merge the two data frames to one data frame
df_a_melt = pd.melt(df_a)
df_a_melt['species'] = 'concentrated answer'
df_b_melt = pd.melt(df_b)
df_b_melt['species'] = 'sloppy answer'
df_marged = pd.concat([df_a_melt, df_b_melt], axis=0)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
sns.boxplot(x='variable', y='value', data=df_marged, hue='species', palette='Dark2', ax=ax)

params = {'legend.fontsize': 25,
        'legend.handlelength': 3}

plt.rcParams.update(params)
ax.set_xlabel('time  [ms]')
ax.set_ylabel('ratio')
ax.set_ylim(-0.02, 0.6)
ax.legend()











# <--------------------LightGBMで学習して予測-------------------->
print("--------------------LightGBMの学習結果--------------------")

# データフレームを綺麗に出力する関数
def display(*dfs, head=True):
    for df in dfs:
        IPython.display.display(df.head() if head else df)
# 特徴量重要度を棒グラフでプロットする関数 
def plot_feature_importance(df): 
    n_features = len(df)                              # 特徴量数(説明変数の個数) 
    df_plot = df.sort_values('importance')            # df_importanceをプロット用に特徴量重要度を昇順ソート 
    f_importance_plot = df_plot['importance'].values  # 特徴量重要度の取得 
    plt.barh(range(n_features), f_importance_plot, align='center') 
    cols_plot = df_plot['feature'].values             # 特徴量の取得 
    plt.yticks(np.arange(n_features), cols_plot)      # x軸,y軸の値の設定
    plt.xlabel('Feature importance')                  # x軸のタイトル
    plt.ylabel('Feature')                             # y軸のタイトル

# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

# import lightgbm as lgb
# model = lgb.LGBMClassifier(boosting_type='gbdt', max_depth=5, random_state=0)

# eval_set = [(X_test, y_test)]
# callbacks = []
# callbacks.append(lgb.early_stopping(stopping_rounds=10))
# callbacks.append(lgb.log_evaluation())
# model.fit(X_train, y_train, eval_set=eval_set, callbacks=callbacks)


# from sklearn import metrics
# y_pred = model.predict_proba(X_test)
# metrics.log_loss(y_test, y_pred)

# lgb.plot_metric(model)
# lgb.plot_importance(model)
plt.show()
