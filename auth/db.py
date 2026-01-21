import pymysql

def get_conn():
    return pymysql.connect(
        host="43.201.8.98",
        user="mixup",
        password="6404",
        database="project",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )