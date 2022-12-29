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
print(answer_data[0])



# 保存を実行
connection.commit()
# 接続を閉じる
connection.close()


# クラス化しようかな