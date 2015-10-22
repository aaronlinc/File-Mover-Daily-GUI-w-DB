import sqlite3, datetime

# Connect to database
conn = sqlite3.connect('record.db')


def createTable():
    conn.execute("CREATE TABLE if not exists \
        fileCheck( \
        ID INTEGER PRIMARY KEY AUTOINCREMENT, \
        DATE TEXT, \
        TIME TEXT \
        );")

def newRecordMan(date, time):
    val_str = "'{}', '{}'".format(date, time)

    sql_str = "INSERT INTO fileCheck \
        (DATE, TIME)\
        VALUES ({});".format(val_str)
    print sql_str
    conn.execute(sql_str)
    conn.commit()
    return conn.total_changes

# Creates new Record At Current Time
def newRecordTime():
    date = datetime.datetime.now().strftime("%m/%d/%y")
    time = datetime.datetime.now().strftime("%I:%M %p")
    newRecordMan(date, time)
    
def viewAll():
    # Create sql string
    sql_str = "SELECT * from fileCheck"
    cursor = conn.execute(sql_str)

    # Get data from cursor in array
    rows = cursor.fetchall()
    return rows

# Displays Last record in a formated string
def viewLast():
    sql_str = "SELECT date, time from fileCheck\
        ORDER BY ID DESC \
        LIMIT 1"
    cursor = conn.execute(sql_str)

    rows = cursor.fetchall()
    last_commit = "Last Transfer Performed: {} at {}."\
                  .format(str(rows[0][0]), str(rows[0][1]))
    return last_commit

def deleteRow(change_id):
    sql_str = "DELET from fileCheck where ID={}"\
              .format(change_id)
    conn.execute(sql_str)
    conn.commit()
    return conn.total_changes


