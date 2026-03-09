import pymysql

conn = pymysql.connect(host='localhost', user='root', password='', database='copymart')
cursor = conn.cursor()

cursor.execute('DESCRIBE users')
cols = [r[0] for r in cursor.fetchall()]
print('Columnas actuales:', cols)

if 'permissions' not in cols:
    cursor.execute("ALTER TABLE users ADD COLUMN permissions JSON NULL AFTER created_at")
    conn.commit()
    print('Columna permissions agregada.')
else:
    print('Columna permissions ya existe.')

conn.close()
