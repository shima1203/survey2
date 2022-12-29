# MySQLdbのインポート
import MySQLdb

# データベースへの接続とカーソルの生成
connection = MySQLdb.connect(
    host='localhost',
    user='ubuntu',
    passwd='Aquos.123',
    db='survey')
cursor = connection.cursor()

cursor.execute("SELECT * FROM AnswerData")
answer_data = cursor.fetchall()
cursor.execute("SELECT * FROM Answers")
answers = cursor.fechall()


answer_id_list = []
questionnaire_id_list = []
scroll_list = []
coordinates_list = []
click_list = []
windowsize_list = []
background_list = []
checking_list = []
type_list = []
enter_leave_list = []
total_list = []
device_list = []
created_at_list = []
for answer_data_line in answer_data:
    answer_id_list.append(answer_data_line[0])
    questionnaire_id_list.append(answer_data_line[1])
    scroll_list.append(answer_data_line[2])
    coordinates_list.append(answer_data_line[3])
    click_list.append(answer_data_line[4])
    windowsize_list.append(answer_data_line[5])
    background_list.append(answer_data_line[6])
    checking_list.append(answer_data_line[7])
    type_list.append(answer_data_line[8])
    enter_leave_list.append(answer_data_line[9])
    total_list.append(answer_data_line[10])
    device_list.append(answer_data_line[11])
    created_at_list.append(answer_data_line[12])
    
print(click_list)










# 保存を実行
connection.commit()
# 接続を閉じる
connection.close()


# クラス化しようかな