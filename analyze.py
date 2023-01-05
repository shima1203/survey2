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




# <--------ここからはデータセットの作成-------->
print("--------------------データ--------------------")

data_set = []
for i in range(len(answer_id_list)):
    data_tmp = {}
    data_tmp['target'] = int(answers_dict[answer_id_list[i]][30])
    data_tmp['click_amount'] = len(click_dict[answer_id_list[i]])
    data_tmp['mouse_amount'] = len(coordinates_dict[answer_id_list[i]])
    data_set.append(data_tmp)

df = pd.DataFrame(data = data_set)
X = df.loc[:, (df.columns !='target')]
# X = pd.get_dummies(X, drop_first=True)
y = df['target']

print(df)
print(" ")

# <--------ヒューリスティックに予測-------->
print("--------------------予測結果--------------------")

# 入力(各特徴量の値)に対して0~1にスケーリングした値を返す
def func_click_amount(click_amount):
    return click_amount/100


predict = []

for i in range(len(answer_id_list)):
    predict.append(func_click_amount(data_set[i]['click_amount']))

tmp1 = 0
tmp2 = 0
j = 0
for tmp in data_set:
    if tmp['target'] == 0:
        print(tmp, )
        j += 1
        tmp1 += tmp['click_amount']
print("ave:", tmp1/j)
j = 0
for tmp in data_set:
    if tmp['target'] == 1:
        print(tmp)
        j += 1
        tmp2 += tmp['click_amount']
print("ave:", tmp2/j)





















# <--------LightGBMで学習して予測-------->
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

lgb.plot_metric(model)
lgb.plot_importance(model)
plt.show()

# 縦軸：クリックの回数　横軸：集中->1　適当->0









# クラス化しようかな