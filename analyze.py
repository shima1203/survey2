# MySQLdbのインポート
import MySQLdb

# データベースへの接続とカーソルの生成
connection = MySQLdb.connect(
    host='localhost',
    user='ubuntu',
    passwd='Aquos.123',
    db='survey')
cursor = connection.cursor()

# ここに実行したいコードを入力します
cursor.execute("SELECT * FROM AnswerData")
# fetchall()で全件取り出し
answer_data = cursor.fetchall()


answer_id_list = []
questionnaire_id_list = []
scroll_list = []
coordinates_list = []
click_list = []
windowsize_list = []
baclground_list = []
checking_list = []
type_list = []
enter_leave_list = []
total_list = []
device_list = []
created_at_list = []
for answer_data_line in answer_data:
    answer_id_list.append(answer_data_line[0])
    questionnaire_id_list.append(answer_data_line[1])
    
print(answer_id_list)










# 保存を実行
connection.commit()
# 接続を閉じる
connection.close()


# クラス化しようかな