# MySQLdbのインポート
import MySQLdb

# データベースへの接続とカーソルの生成
connection = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='ルートのパスワード',
    db='python_db')
cursor = connection.cursor()

# ここに実行したいコードを入力します

# 保存を実行
connection.commit()

# 接続を閉じる
connection.close()


# クラス化しようかな