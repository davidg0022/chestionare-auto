import sqlite3

conn = sqlite3.connect("data.db")

conn.execute("""CREATE TABLE questions(
                id INTEGER NOT NULL PRIMARY KEY,
                type text,
                img_url text,
                title text
)""")


conn.execute("""CREATE TABLE answers(
                id INTEGER NOT NULL PRIMARY KEY,
                question_id INTEGER,
                answer_text text,
                corect INTEGER
)""")

conn.execute("""CREATE TABLE active_questions(
                id INTEGER NOT NULL PRIMARY KEY,
                url_code text,
                question_title text,
                img_url text,
                disabled INTEGER,
                corect INTEGER,
                incorect INTEGER
)""")

conn.execute("""CREATE TABLE active_questions_answers(
            id INTEGER NOT NULL PRIMARY KEY,
            url_code text,
            selected INTEGER,
            corect INTEGER,
            answer_text text,
            question_id INTEGER NOT NULL
)""")

conn.execute("""CREATE TABLE room_codes
(   
    id INTEGER NOT NULL PRIMARY KEY,
    url_code text
)""")




q = conn.execute("SELECT count(*) from questions")
print(q.fetchall())