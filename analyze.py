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

questionnaire_id = 3


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

# マウスの平均スピードを返す関数
def mouse_speed(coordinates=[]):
    sum_mous = 0
    i = 0
    time_tmp  = coordinates[0]['time']
    for coordinate in coordinates:
        if(coordinate['time'] - time_tmp <= 1000):             # １秒以内でイベントが発生している場合、マウスが連続で動いていると考える
            sum_mous += coordinate['time'] - time_tmp
            i += 1
        time_tmp  = coordinate['time']
    return(sum_mous/i)


# クリックイベント直前のマウスのスピードを返す関数
def mouse_speed_click_pre(coordinates_ori=[], clicks_ori=[]):
    coordinates = coordinates_ori.copy()
    clicks = clicks_ori.copy()
    click_pre_list = []
    tmp = []
    time_close = 500
    time_tmp = coordinates[0]['time']
    for click in clicks:
        i = 0
        for coordinate in coordinates:
            if(coordinate['time'] <= click['time'] and coordinate['time'] >= click['time'] - time_close):
                if(coordinate['time'] - time_tmp <= 1000):
                    click_pre_list.append(coordinate['time'] - time_tmp)
                    tmp.append(coordinate['time'])
            if(coordinate['time'] > click['time']):
                break
            time_tmp = coordinate['time']
            i += 1
        for j in range(i):
            del coordinates[0]
        # print('click_pre_list : ', len(click_pre_list))
        # print('coordinates_list : ', len(coordinates))
        # print('----------------------------------')
    # time_close以内のマウスイベントの数を返す
    # return(len(click_pre_list))

    # time_close以内のマウス速度の平均を返す
    time_sum = 0
    j = 0
    for click_pre in click_pre_list:
        time_sum += click_pre
        j += 1
    return(time_sum / j)

# クリックイベント直前のマウスのイベント数を返す関数
def mouse_event_click_pre(coordinates_ori=[], clicks_ori=[]):
    coordinates = coordinates_ori.copy()
    clicks = clicks_ori.copy()
    click_pre_list = []
    tmp = []
    time_close = 500
    time_tmp = coordinates[0]['time']
    for click in clicks:
        i = 0
        for coordinate in coordinates:
            if(coordinate['time'] <= click['time'] and coordinate['time'] >= click['time'] - time_close):
                if(coordinate['time'] - time_tmp <= 1000):
                    click_pre_list.append(coordinate['time'] - time_tmp)
                    tmp.append(coordinate['time'])
            if(coordinate['time'] > click['time']):
                break
            time_tmp = coordinate['time']
            i += 1
        for j in range(i):
            del coordinates[0]
    # time_close以内のマウスイベントの数を返す
    return(len(click_pre_list))

# クリックイベント直後のマウスのスピードを返す関数
def mouse_speed_click_rear(coordinates_ori=[], clicks_ori=[]):
    coordinates = coordinates_ori.copy()
    clicks = clicks_ori.copy()
    click_pre_list = []
    tmp = []
    time_close = 500
    time_tmp = coordinates[0]['time']
    for click in clicks:
        i = 0
        for coordinate in coordinates:
            if(coordinate['time'] >= click['time'] and coordinate['time'] <= click['time'] + time_close):
                if(coordinate['time'] - time_tmp <= 1000):
                    click_pre_list.append(coordinate['time'] - time_tmp)
                    tmp.append(coordinate['time'])
            if(coordinate['time'] > click['time'] + time_close):
                break
            time_tmp = coordinate['time']
            i += 1
        for j in range(i):
            del coordinates[0]
    # time_close以内のマウスイベントの数を返す
    # return(len(click_pre_list))

    # time_close以内のマウス速度の平均を返す
    time_sum = 0
    j = 0
    for click_pre in click_pre_list:
        time_sum += click_pre
        j += 1
    return(time_sum / j)

# クリックイベント直後のマウスのイベント数を返す関数
def mouse_event_click_rear(coordinates_ori=[], clicks_ori=[]):
    coordinates = coordinates_ori.copy()
    clicks = clicks_ori.copy()
    click_pre_list = []
    tmp = []
    time_close = 500
    time_tmp = coordinates[0]['time']
    for click in clicks:
        i = 0
        for coordinate in coordinates:
            if(coordinate['time'] >= click['time'] and coordinate['time'] <= click['time'] + time_close):
                if(coordinate['time'] - time_tmp <= 1000):
                    click_pre_list.append(coordinate['time'] - time_tmp)
                    tmp.append(coordinate['time'])
            if(coordinate['time'] > click['time'] + time_close):
                break
            time_tmp = coordinate['time']
            i += 1
        for j in range(i):
            del coordinates[0]
    # time_close以内のマウスイベントの数を返す
    return(len(click_pre_list))

# スクロールイベント直後のマウスのスピードを返す関数
def mouse_speed_scroll_rear(coordinates_ori=[], scrolls_ori=[]):
    coordinates = coordinates_ori.copy()
    scrolls = scrolls_ori.copy()
    scroll_pre_list = []
    tmp = []
    time_close = 500
    coordinate_time_tmp = coordinates[0]['time']
    scroll_time_tmp = scrolls[0]['time']
    for scroll in scrolls:
        i = 0
        if(scroll['time'] - scroll_time_tmp <= 1000 and scroll['time'] - scroll_time_tmp != 0):
            for coordinate in coordinates:
                if(coordinate['time'] >= scroll['time'] and coordinate['time'] <= scroll['time'] + time_close):
                    if(coordinate['time'] - coordinate_time_tmp <= 1000):
                        scroll_pre_list.append(coordinate['time'] - coordinate_time_tmp)
                        tmp.append(coordinate['time'])
                if(coordinate['time'] > scroll['time'] + time_close):
                    break
                coordinate_time_tmp = coordinate['time']
                i += 1
            for j in range(i):
                del coordinates[0]
        scroll_time_tmp = scroll['time']
    # time_close以内のマウスイベントの数を返す
    # return(len(click_pre_list))

    # time_close以内のマウス速度の平均を返す
    time_sum = 0
    j = 0
    for scroll_pre in scroll_pre_list:
        time_sum += scroll_pre
        j += 1
    return(time_sum / j)

# スクロールイベント直後のマウスのイベント数を返す関数
def mouse_event_scroll_rear(coordinates_ori=[], scrolls_ori=[]):
    coordinates = coordinates_ori.copy()
    scrolls = scrolls_ori.copy()
    scroll_pre_list = []
    tmp = []
    time_close = 500
    coordinate_time_tmp = coordinates[0]['time']
    scroll_time_tmp = scrolls[0]['time']
    for scroll in scrolls:
        i = 0
        if(scroll['time'] - scroll_time_tmp <= 1000 and scroll['time'] - scroll_time_tmp != 0):
            for coordinate in coordinates:
                if(coordinate['time'] >= scroll['time'] and coordinate['time'] <= scroll['time'] + time_close):
                    if(coordinate['time'] - coordinate_time_tmp <= 1000):
                        scroll_pre_list.append(coordinate['time'] - coordinate_time_tmp)
                        tmp.append(coordinate['time'])
                if(coordinate['time'] > scroll['time'] + time_close):
                    break
                coordinate_time_tmp = coordinate['time']
                i += 1
            for j in range(i):
                del coordinates[0]
        scroll_time_tmp = scroll['time']
    # time_close以内のマウスイベントの数を返す
    return(len(scroll_pre_list))






data_set = []
for i in range(len(answer_id_list)):
    data_tmp = {}
    # data_tmp['answer_id'] = answer_id_list[i]               # 後で消す
    data_tmp['target'] = int(answers_dict[answer_id_list[i]][30])
    data_tmp['click_amount'] = len(click_dict[answer_id_list[i]])
    data_tmp['mouse_amount'] = len(coordinates_dict[answer_id_list[i]])
    data_tmp['mouse_ave'] = mouse_speed(coordinates_dict[answer_id_list[i]])
    data_tmp['mouse_speed_click_pre'] = mouse_speed_click_pre(coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]])
    data_tmp['mouse_event_click_pre'] = mouse_event_click_pre(coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]])
    data_tmp['mouse_speed_click_rear'] = mouse_speed_click_rear(coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]])
    data_tmp['mouse_event_click_rear'] = mouse_event_click_rear(coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]])
    data_tmp['mouse_speed_scroll_rear'] = mouse_speed_scroll_rear(coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])
    data_tmp['mouse_event_scroll_rear'] = mouse_event_scroll_rear(coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])
    data_tmp['ratio_mouse_speed_click_pre'] = mouse_speed_click_pre(coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]])/mouse_speed(coordinates_dict[answer_id_list[i]])      #通常のマウススピードとクリック直前のマウススピードの比較
    data_tmp['ave_mouse_event_click_pre'] = mouse_event_click_pre(coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]])/len(click_dict[answer_id_list[i]])        # １クリックあたりの平均マウスイベント数(クリック直前)
    data_tmp['ratio_mouse_speed_click_rear'] = mouse_speed_click_rear(coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]])/mouse_speed(coordinates_dict[answer_id_list[i]])      #通常のマウススピードとクリック直後のマウススピードの比較
    data_tmp['ratio_mouse_speed_click_pre_and_rear'] = mouse_speed_click_rear(coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]])/mouse_speed_click_pre(coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]])     # speed rear / pre
    data_tmp['ave_mouse_event_click_rear'] = mouse_event_click_rear(coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]])/len(click_dict[answer_id_list[i]])        # １クリックあたりの平均マウスイベント数(クリック直後)
    data_tmp['ratio_mouse_event_click_pre_and_rear'] = mouse_event_click_rear(coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]])/mouse_event_click_pre(coordinates_dict[answer_id_list[i]], click_dict[answer_id_list[i]])     # event rear / pre
    data_tmp['ratio_mouse_speed_scroll_rear'] = mouse_speed_scroll_rear(coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/mouse_speed(coordinates_dict[answer_id_list[i]])   #通常のマウススピードとスクロール直後のマウススピードの比較
    data_tmp['ave_mouse_event_scroll_rear'] = mouse_event_scroll_rear(coordinates_dict[answer_id_list[i]], scroll_dict[answer_id_list[i]])/len(scroll_dict[answer_id_list[i]])      # １スクロールあたりの平均マウスイベント数(スクロール直後)


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
df_a = df[df['target'] == 0].loc[:,['ratio_mouse_speed_click_pre','ratio_mouse_speed_click_rear','ave_mouse_event_click_pre','ave_mouse_event_click_rear','ratio_mouse_event_click_pre_and_rear','ratio_mouse_speed_scroll_rear','ave_mouse_event_scroll_rear']]
print(df_a)
sum_click_amount = 0
sum_mouse_amount = 0
sum_mouse_speed_click_pre = 0
j = 0
for data in data_set:
    if data['target'] == 0:
        # print(data, )
        j += 1
        sum_click_amount += data['click_amount']
        sum_mouse_amount += data['mouse_amount']
        sum_mouse_speed_click_pre +=data['mouse_speed_click_pre']
print('----------average----------')
print("click_amount:", sum_click_amount/j)
print("mouse_amount:", sum_mouse_amount/j)
print("mouse_speed_click_pre:",sum_mouse_speed_click_pre/j)
print(' ')
sum_click_amount = 0
sum_mouse_amount = 0
sum_mouse_speed_click_pre = 0
j = 0

print(len(df_a))
print(len(df_a.query('ratio_mouse_speed_click_rear < 1.1')))

print('＜適当＞')
df_b = df[df['target'] == 1].loc[:,['ratio_mouse_speed_click_pre','ratio_mouse_speed_click_rear','ave_mouse_event_click_pre','ave_mouse_event_click_rear','ratio_mouse_event_click_pre_and_rear','ratio_mouse_speed_scroll_rear','ave_mouse_event_scroll_rear']]
print(df_b)
for data in data_set:
    if data['target'] == 1:
        # print(data)
        j += 1
        sum_click_amount += data['click_amount']
        sum_mouse_amount += data['mouse_amount']
        sum_mouse_speed_click_pre +=data['mouse_speed_click_pre']
print('----------average----------')
print("click_amount:", sum_click_amount/j)
print("mouse_amount:", sum_mouse_amount/j)
print("mouse_speed_click_pre:",sum_mouse_speed_click_pre/j)

print(len(df_b))
print(len(df_b.query('ratio_mouse_speed_click_rear < 1.1')))




# 入力(各特徴量の値)に対して0~1にスケーリングした値を返す
def func_click_amount(click_amount):
    return click_amount/100

predict = []

for i in range(len(answer_id_list)):
    predict.append(func_click_amount(data_set[i]['click_amount']))
















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

# df = sns.load_dataset('titanic')
# X = df.loc[:, (df.columns!='survived') & (df.columns!='alive')]
# X = pd.get_dummies(X, drop_first=True)
# y = df['survived']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

import lightgbm as lgb
model = lgb.LGBMClassifier(boosting_type='gbdt', max_depth=5, random_state=0)

eval_set = [(X_test, y_test)]
callbacks = []
callbacks.append(lgb.early_stopping(stopping_rounds=10))
callbacks.append(lgb.log_evaluation())
model.fit(X_train, y_train, eval_set=eval_set, callbacks=callbacks)


from sklearn import metrics
y_pred = model.predict_proba(X_test)
metrics.log_loss(y_test, y_pred)

# lgb.plot_metric(model)
# lgb.plot_importance(model)
plt.show()



