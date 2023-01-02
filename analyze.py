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

data_set = []
for i in range(len(answer_id_list)):
    data_tmp = {}
    data_tmp['target'] = answers_dict[answer_id_list[i]][30]
    data_tmp['click_amount'] = len(click_dict[answer_id_list[i]])
    data_tmp['mouse_amount'] = len(coordinates_dict[answer_id_list[i]])
    data_set.append(data_tmp)







# <--------特徴量重要度の表示-------->
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold

# iris データセットを読み込む
iris = datasets.load_iris()
X = iris['data']
y = iris['target']

# 説明変数をpandas.DataFrameに入れ、カラム名を付ける
df_X = pd.DataFrame(X, columns=iris['feature_names'])

# カテゴリー変数を作成
# sepal（がく）の面積から4区分のカテゴリーを作成
df_X['sepal_cat'] = df_X['sepal length (cm)'] * df_X['sepal width (cm)']
df_X['sepal_cat'] = pd.qcut(df_X['sepal_cat'], 4, labels=False)
df_X['sepal_cat'] = df_X['sepal_cat'].astype('category')

# カテゴリー変数を作成
# petal（花びら）の面積から4区分のカテゴリーを作成
df_X['petal_cat'] = df_X['petal length (cm)'] * df_X['petal width (cm)']
df_X['petal_cat'] = pd.cut(df_X['petal_cat'], 4, labels=False)
df_X['petal_cat'] = df_X['petal_cat'].astype('category')

# 学習データとテストデータに分ける
X_train, X_test, y_train, y_test = train_test_split(df_X, y,
                                                    test_size=0.2,
                                                    random_state=0,
                                                    stratify=y)

# 学習データを、学習用と検証用に分ける
X_train, X_eval, y_train, y_eval = train_test_split(X_train, y_train,
                                                    test_size=0.2,
                                                    random_state=1,
                                                    stratify=y_train)


# カテゴリー変数
categorical_features = {*sorted(['sepal_cat', 'petal_cat'])}


# データを格納する
# 学習用
lgb_train = lgb.Dataset(X_train, y_train,
                        categorical_feature=categorical_features,
                        free_raw_data=False)
# 検証用
lgb_eval = lgb.Dataset(X_eval, y_eval, reference=lgb_train,
                       categorical_feature=categorical_features,
                       free_raw_data=False)

# パラメータを設定
params = {'task': 'train',                # 学習、トレーニング ⇔　予測predict
          'boosting_type': 'gbdt',        # 勾配ブースティング
          'objective': 'multiclass',      # 目的関数：多値分類、マルチクラス分類
          'metric': 'multi_logloss',      # 分類モデルの性能を測る指標
          'num_class': 3,                 # 目的変数のクラス数
          'learning_rate': 0.02,          # 学習率（初期値0.1）
          'num_leaves': 23,               # 決定木の複雑度を調整（初期値31）
          'min_data_in_leaf': 1,          # データの最小数（初期値20）
         }

# 学習
evaluation_results = {}                                     # 学習の経過を保存する箱
model = lgb.train(params,                                   # 上記で設定したパラメータ
                  lgb_train,                                # 使用するデータセット
                  num_boost_round=1000,                     # 学習の回数
                  valid_names=['train', 'valid'],           # 学習経過で表示する名称
                  valid_sets=[lgb_train, lgb_eval],         # モデル検証のデータセット
                  evals_result=evaluation_results,          # 学習の経過を保存
                  categorical_feature=categorical_features, # カテゴリー変数を設定
                  early_stopping_rounds=20,                 # アーリーストッピング
                  verbose_eval=10)                          # 学習の経過の表示(10回毎)

# 最もスコアが良いときのラウンドを保存
optimum_boost_rounds = model.best_iteration

# テストデータで予測
y_pred = model.predict(X_test, num_iteration=model.best_iteration)
y_pred_max = np.argmax(y_pred, axis=1)

# Accuracy の計算
accuracy = sum(y_test == y_pred_max) / len(y_test)
print('accuracy:', accuracy)

# feature importanceを表示
importance = pd.DataFrame(model.feature_importance(), index=df_X.columns, columns=['importance'])
display(importance)





# 縦軸：クリックの回数　横軸：集中->1　適当->0






# 保存を実行
connection.commit()
# 接続を閉じる
connection.close()


# クラス化しようかな