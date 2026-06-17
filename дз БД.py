import psycopg2



def create_db(cur):
    cur.execute("""
        DROP TABLE IF EXISTS Phones;
        DROP TABLE IF EXISTS Clients;
        """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Clients(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE
        );
        """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Phones(
        id SERIAL PRIMARY KEY,
        clients_id INTEGER NOT NULL REFERENCES Clients(id) ON DELETE CASCADE,
        phone VARCHAR(15)
        );
        """)

def add_client(cur, first_name, last_name, email, phones=None):
    cur.execute("""
        INSERT INTO Clients(first_name, last_name, email) VALUES(%s, %s, %s) RETURNING id;
        """, (first_name, last_name, email)
        )
    client_id = cur.fetchone()[0]

    if phones:
        for phone in phones:
            cur.execute("""
                INSERT INTO Phones(clients_id, phone) VALUES(%s, %s);
                """, (client_id, phone)
            )
    return client_id

def add_phone(cur, client_id, phone):
    cur.execute("""
        INSERT INTO Phones(clients_id, phone) VALUES(%s, %s);
        """, (client_id, phone)
        )

def change_client(cur, client_id, first_name=None, last_name=None, email=None, phones=None):
    fields=[]
    values=[]

    if first_name is not None:
        fields.append("first_name = %s")
        values.append(first_name)
    if last_name is not None:
        fields.append("last_name = %s")
        values.append(last_name)
    if email is not None:
        fields.append("email = %s")
        values.append(email)
    if phones is not None:
        fields.append("phone = %s")
        values.append(phones)

    if not fields:
        print("Нечего обновлять")
        return

    values.append(client_id)
    query = f"UPDATE Clients SET {', '.join(fields)} WHERE id = %s"
    cur.execute(query, values)

def delete_phone(cur, client_id, phone):
    cur.execute("""
        DELETE FROM Phones WHERE clients_id = %s AND phone = %s;
        """, (client_id, phone)
        )

def delete_client(cur, client_id):
    cur.execute(
        """
        DELETE FROM Clients WHERE id = %s;
        """, (client_id,)
    )

def find_client(cur, first_name=None, last_name=None, email=None, phone=None):
    query = """
        SELECT c.id, c.first_name, c.last_name, c.email, array_agg(p.phone) FILTER (WHERE p.phone IS NOT NULL) AS phones
        FROM Clients c
        LEFT JOIN Phones p ON c.id = p.clients_id
        WHERE 1=1
    """
    params = []

    if first_name is not None:
        query += f"AND c.first_name ILIKE %s"
        params.append(f"%{first_name}%")
    if last_name is not None:
        query += f"AND c.last_name ILIKE %s"
        params.append(f"%{last_name}%")
    if email is not None:
        query += f"AND c.email ILIKE %s"
        params.append(f"%{email}%")
    if phone is not None:
        query += f"AND p.phone ILIKE %s"
        params.append(f"%{phone}%")

    query += " GROUP BY c.id;"

    cur.execute(query, params)
    return cur.fetchall()

with psycopg2.connect(database="clients_db", user="postgres", password="Er63mk1xc") as conn:
    with conn.cursor() as cur:
        create_db(cur)
        conn.commit()
        print("Структура БД создана\n")

        id1 = add_client(cur, "Иван", "Иванов", "ivan@mail.ru", phones=["+79001112233", "+79004445566"])
        id2 = add_client(cur, "Петр", "Петров", "petr@mail.ru")
        id3 = add_client(cur, "Анна", "Смирнова", "anna@mail.ru", phones=["+79117778899"])
        conn.commit()
        print(f"Клинты добавлены с id: {id1}, {id2}, {id3}\n")

        add_phone(cur, id2, "+79001234567")
        add_phone(cur, id2, "+79009998877")
        conn.commit()
        print("Петру добавлены 2 номера телефона\n")

        change_client(cur, id1, first_name = "Иоанн", email = "ioann@gmail.com")
        conn.commit()
        print("Иван переименован в Иоанна, email изменен\n")

        delete_phone(cur, id2, "+79001234567")
        conn.commit()
        print("Один телефон Петра удален\n")

        delete_client(cur, id3)
        conn.commit()
        print("Анна Смирнова удалена (её телефоны удалены каскадно)\n")

        print("🔍 Поиск по фамилии 'Петров':")
        for row in find_client(cur, last_name="Петров"):
            print(f"   {row}")

        print("\n🔍 Поиск по телефону (часть номера):")
        for row in find_client(cur, phone="777"):
            print(f"   {row}")

        print("\n🔍 Поиск по email:")
        for row in find_client(cur, email="anna@mail.ru"):
            print(f"   {row}")

        print("\n📋 Итоговый список клиентов:")
        for row in find_client(cur):
            print(f"   {row}")