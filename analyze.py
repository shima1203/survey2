import MySQLdb
import json

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
    

# アンサーデータを辞書型に   <-deleteされた回答を除去したい
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
    if(answers_dict[answer_data_line[0]] in answers_dict):
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
        
for tmp in scroll_dict[answer_id_list[0]]:
    print(tmp["y"])

print(answer_id_list)








# 保存を実行
connection.commit()
# 接続を閉じる
connection.close()


# クラス化しようかな