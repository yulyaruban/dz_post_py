
import psycopg2
 
 
def create_db(conn):
 
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS clients(
        client_id INTEGER UNIQUE PRIMARY KEY,
        name VARCHAR(40),
        surname VARCHAR(60),
        email VARCHAR(60));""")
    cur.execute("""CREATE TABLE IF NOT EXISTS phones(
        id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES customers(client_id),
        phone VARCHAR(12)
        );""")
    conn.commit() 
 
def add_client(conn, client_id, name, surname, email, phones=None):
 
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO clients(client_id, name, surname, email) VALUES(%s, %s, %s, %s);
    """, (client_id, name, surname, email))
    conn.commit()
    cur.execute("""
    SELECT * FROM clients;
    """)
    print(cur.fetchall())
    cur.execute("""
    INSERT INTO phones(client_id, phone) VALUES(%s, %s);
    """, (client_id, phones))
    conn.commit()
    cur.execute("""
    SELECT * FROM phones;
    """)
    print(cur.fetchall())
 
 
def add_phone(conn, client_id, phone):
 
    cur = conn.cursor()
    cur.execute("""
    UPDATE phones SET phone=%s WHERE client_id=%s;
    """, (phone, client_id))
    conn.commit()  

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    cur = conn.cursor()
    cur.execute("""
    UPDATE clients SET first_name= %s, last_name= %s, email= %s 
    where client_id= %s;
    """, (client_id, first_name, last_name, email)) 
    cur.execute("""
    UPDATE phones SET phones= %s
    where client_id= %s;
    """, (client_id, phones)) 

def delete_phone(conn, client_id, phone):
    cur = conn.cursor()
    cur.execute("""DELETE FROM phones WHERE client_id = %s;""", (client_id,))
    conn.commit()

def delete_client(conn, client_id):
    cur = conn.cursor()
    cur.execute("""DELETE FROM clients WHERE client_id = %s;""", (client_id,))
    cur.execute("""DELETE FROM phones WHERE client_id = %s;""", (client_id,))
    conn.commit()


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    cur = conn.cursor()
        
    pass
    


with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    pass  # вызывайте функции здесь

conn.close()
   