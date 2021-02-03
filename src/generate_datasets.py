import sqlite3


def generate():
    conn = sqlite3.connect('../private/doctors.db')
    c = conn.cursor()

    c.execute('drop table if exists doctor')
    c.execute('drop table if exists app')


    with open('../private/ap_to_db.sql', 'r') as f:
        table, dates = f.read().split(';', maxsplit=1)
        c.execute(table)
        c.execute(dates)

    with open('../private/Result_42.sql', 'r') as f:
        table, dates = f.read().split(';', maxsplit=1)
        c.execute(table)
        c.execute(dates)

    print(c.execute('select count(*) from app').fetchall())
    print(c.execute('select count(*) from doctor').fetchall())

    conn.close()

generate()
