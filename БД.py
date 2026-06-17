import psycopg2 as pg


with pg.connect(database="test", user="postgres", password="Er63mk1xc") as conn:
    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE домашка;
            DROP TABLE курс;
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS курс(
            id SERIAL PRIMARY KEY,
            name VARCHAR(40) UNIQUE
        );
        """)
        cur.execute(""" 
            CREATE TABLE IF NOT EXISTS домашка(
            id SERIAL PRIMARY KEY,
            number INTEGER NOT NULL,
            description TEXT NOT NULL,
            курс_id INTEGER NOT NULL REFERENCES курс(id) 
        );
        """)
        conn.commit()

        cur.execute("""
            INSERT INTO курс(name) VALUES('Python');
        """)
        conn.commit()

        cur.execute("""
            INSERT INTO курс(name) VALUES('Lava') RETURNING id, name;
        """)
        print(cur.fetchone())

        cur.execute("""
            INSERT INTO домашка(number, description, курс_id) VALUES(1, 'просто дз', 1)
        """)
        conn.commit()

        cur.execute("""
            SELECT * FROM курс;
        """)
        print('курсы:', cur.fetchall())

        cur.execute("""
            SELECT * FROM курс;
        """)
        print(cur.fetchone())

        cur.execute("""
            SELECT * FROM курс;
        """)
        print(cur.fetchmany(3))

        cur.execute("""
            SELECT name FROM курс;
        """)
        print(cur.fetchall())

        cur.execute("""
            SELECT id FROM курс WHERE name = 'Python';
        """)
        print(cur.fetchone())

        cur.execute("""
            SELECT id FROM курс WHERE name = '{}';
        """.format("Python"))        # - плохой метод
        print(cur.fetchone())

        cur.execute("""
            SELECT id FROM курс WHERE name=%s;
        """, ("Python",))        # - хороший метод
        print(cur.fetchone())

        def get_course_id(cursor, name:str) -> int:
            cursor.execute("""
                SELECT id FROM курс WHERE name=%s;            
                """, (name,))
            return cur.fetchone()[0]

        python_id = get_course_id(cur, 'Python')
        print('python_id =', python_id)

        cur.execute("""
            INSERT INTO домашка(number, description, курс_id) VALUES(%s, %s, %s);
            """, (2, "задание последнее", python_id))
        conn.commit()

        cur.execute("""
                SELECT * FROM домашка;
                """)
        print(cur.fetchall())

        cur.execute("""
                    UPDATE курс SET name=%s WHERE id=%s;
                    """, ("Python Advanced", python_id))
        cur.execute("""
                    SELECT * FROM курс;
                    """)
        print(cur.fetchall())

        cur.execute("""
                    DELETE FROM домашка WHERE id=%s;
                    """, (1,))
        cur.execute("""
                    SELECT * FROM домашка;
                    """)
        print(cur.fetchall())