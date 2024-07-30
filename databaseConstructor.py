import sqlite3

#  This program is the database interface for the pillbox server side
#  setup constructs the database from scratch (not overriding unless different connection)
#  write adds a new timestamp to the database
#  read pulls a timestamp from the database
#  delete deletes a specific timestamp

connection = sqlite3.connect('/home/tal176/python scripts/pillboxDatabase.db')
cursor = connection.cursor()
dayDict = {"1":"sunday" , "2":"monday" , "3":"tuesday" , "4":"wednsday" , "5":"thursday" , "6":"friday" , "7":"saturday"}

def setup():
    todaysIndexFile = open("todaysIndex.txt" , "w")
    todaysIndexFile.write("0")
    todaysIndexFile.close()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sunday(
        med,
        hour,
        minute
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS monday(
        med,
        hour,
        minute
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tuesday(
        med,
        hour,
        minute
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wednsday(
        med,
        hour,
        minute
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS thursday(
        med,
        hour,
        minute
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS friday(
        med,
        hour,
        minute
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saturday(
        med,
        hour,
        minute
    )
    """)
    connection.commit()

def delete(day,hour,minute):
    day = dayDict[str(day)]
    cursor.execute(f"""DELETE FROM {day} WHERE hour = {hour} AND minute = {minute}""")
    connection.commit()

def write(timestamp):
    if timestamp[0] == 1:
        cursor.execute("""
        INSERT INTO sunday VALUES('{}',{},{})
        """.format(timestamp[3],timestamp[1],timestamp[2]))
    if timestamp[0] == 2:
        cursor.execute("""
        INSERT INTO monday VALUES('{}',{},{})
        """.format(timestamp[3],timestamp[1],timestamp[2]))
    if timestamp[0] == 3:
        cursor.execute("""
        INSERT INTO tuesday VALUES('{}',{},{})
        """.format(timestamp[3],timestamp[1],timestamp[2]))
    if timestamp[0] == 4:
        cursor.execute("""
        INSERT INTO wednsday VALUES('{}',{},{})
        """.format(timestamp[3],timestamp[1],timestamp[2]))
    if timestamp[0] == 5:
        cursor.execute("""
        INSERT INTO thursday VALUES('{}',{},{})
        """.format(timestamp[3],timestamp[1],timestamp[2]))
    if timestamp[0] == 6:
        cursor.execute("""
        INSERT INTO friday VALUES('{}',{},{})
        """.format(timestamp[3],timestamp[1],timestamp[2]))
    if timestamp[0] == 7:
        cursor.execute("""
        INSERT INTO saturday VALUES('{}',{},{})
        """.format(timestamp[3],timestamp[1],timestamp[2]))
    connection.commit()

def read(day,index):
    day = dayDict[str(day)]
    if(len(cursor.execute(f"SELECT med FROM {day}").fetchall()) <= index):
        return 0
    meds = cursor.execute(f"SELECT med FROM {day}").fetchall()[index][0]
    hours = cursor.execute(f"SELECT hour FROM {day}").fetchall()[index][0]
    minutes = cursor.execute(f"SELECT minute FROM {day}").fetchall()[index][0]
    return list([meds, hours, minutes])

# ts = [3, 5, 50, "4"]
# write(ts)
# meds, hour, minute = read(3,1)
# print(hour , minute)
# delete(3,5,50)
