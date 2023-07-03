import psycopg2
from psycopg2.sql import SQL, Identifier

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients(
            client_id SERIAL PRIMARY KEY,
            name VARCHAR(40) NOT NULL,
            surname VARCHAR(60) NOT NULL,
            email VARCHAR(60) NOT NULL UNIQUE);""")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phones(
            id SERIAL PRIMARY KEY,
            phone DECIMAL UNIQUE CHECK (phone <= 99999999999),
            client_id INTEGER REFERENCES clients(client_id)
            );""")
        conn.commit()



 
def add_client(conn, name, surname, email, phones=None):
        cur.execute("""
            INSERT INTO clients(name, surname, email) 
            VALUES(%s, %s, %s)
            RETURNING client_id, name, surname, email;
            """, (name, surname, email))
        return cur.fetchall()

 
def add_phone(conn, client_id, phone):
        cur.execute("""
            INSERT INTO phones (client_id, phone)
            VALUES (%s, %s)
            RETURNING client_id, phone;
            """,(client_id, phone))
        return cur.fetchall()


def change_client(conn, client_id, name=None, surname=None, email=None):
    arg_list = {'name': name, "surname": surname, 'email': email}
    for key, arg in arg_list.items():
        if arg:
            cur.execute(SQL("UPDATE clients SET {}=%s WHERE client_id=%s").format(Identifier(key)), (arg, client_id))
    cur.execute("""
            SELECT * FROM clients
            WHERE client_id=%s
            """, client_id)
    return cur.fetchall()

    
def change_phone(conn, client_id, phone):
       arg_list = {'phone': phone, }
       for key, arg in arg_list.items():
        if arg:
            conn.execute(SQL("UPDATE phones SET {}=%s WHERE client_id=%s").format(Identifier(key)), (arg, client_id))
       conn.execute("""
            SELECT * FROM phones
            WHERE client_id=%s
            """, (client_id))
       return cur.fetchall()

def delete_phone(conn, client_id, phone=None):
    cur.execute("""
            DELETE FROM phones
            WHERE client_id=%s
            """, (client_id,))
    cur.execute("""
            SELECT * FROM phones
            """, (phone, client_id))
    return cur.fetchall()

def delete_client(conn, client_id, name=None, surname=None, email=None, phone=None):
    cur.execute("""
            DELETE FROM clients
            WHERE client_id=%s
            """, (client_id,))
    cur.execute("""
            SELECT * FROM clients
            """, (name, surname, email,client_id))
    return cur.fetchall()

def find_client(conn, name=None, surname=None, email=None, phone=None):
    """Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)"""
    cur.execute("""
    SELECT c.client_id, c.name, c.surname, c.email, p.phone FROM clients c LEFT JOIN phones p ON c.client_id = p.client_id WHERE name=%s OR surname=%s 
    OR email=%s OR p.phone=%s;
    """, (name, surname, email, phone))
    return cur.fetchall()


conn = psycopg2.connect(database="dz_post_py_db", user="postgres", password="24081612")   
create_db(conn)

with conn.cursor() as cur:
    # print(add_client(cur, 'Ivan', 'Lavrenov', 'lavrenov@gmail.com'))
    # print (add_phone(cur, '4', '89235643891'))
    # print (change_client(cur, '1', 'Igor', 'Vakhin', 'vakhin@mail.com'))  
    # print(change_phone(cur, '1', '89121320456'))    
    # print(delete_phone( cur, 1)) 
    # print(delete_client(cur, 1))
    print(find_client(cur,'Ivan'))
    conn.commit()  
