import sqlite3
import os
import json
conn = sqlite3.connect("data.db")
# conn.execute("DROP TABLE questions")
# conn.execute("DROP TABLE answers")
# conn.execute("""CREATE TABLE questions(
#                 id INTEGER NOT NULL PRIMARY KEY,
#                 type text,
#                 img_url text,
#                 title text
# )""")


# conn.execute("""CREATE TABLE answers(
#                 id INTEGER NOT NULL PRIMARY KEY,
#                 question_id INTEGER,
#                 answer_text text,
#                 corect INTEGER
# )""")
# exit(2)


# conn.execute("DROP TABLE active_questions")
# conn.execute("DROP TABLE active_questions_answers")
# conn.execute("DROP TABLE room_codes")
# conn.execute("""CREATE TABLE active_questions(
#                 id INTEGER NOT NULL PRIMARY KEY,
#                 url_code text,
#                 question_title text,
#                 img_url text,
#                 disabled INTEGER,
#                 corect INTEGER,
#                 incorect INTEGER
# )""")
# conn.execute("""CREATE TABLE active_questions_answers(
#             id INTEGER NOT NULL PRIMARY KEY,
#             url_code text,
#             selected INTEGER,
#             corect INTEGER,
#             answer_text text,
#             question_id INTEGER NOT NULL
# )""")
# conn.execute("""CREATE TABLE room_codes
# (   
#     id INTEGER NOT NULL PRIMARY KEY,
#     url_code text
# )""")
# q = conn.execute("SELECT * from room_codes")
# q = conn.execute("DELETE from room_codes")


def get_data():
    files = [f for f in os.listdir('.') if os.path.isfile(f) and ".json" in f and f != "current.json"]
    data = []
    for f in files:
        with open(f,encoding='utf-8') as json_file:
            temp = json.load(json_file)
            for q in temp:
                # print(str(f[:-5]))
                # exit(0)
                t = f[:-5]
                q["type"] = t
                
                try:
                    if len(q["answers"]) == 3:
                        data.append(q)
                except:
                    continue
    return data

# data = get_data()
# index = 1
# for q in data:
#     q["title"].replace("\"","\"\"")
#     print(q["title"])
#     conn.execute(f"""INSERT INTO questions (type, img_url, title) VALUES ("{q["type"]}", "{q["img_url"]}", "{q["title"].replace('"','""')}")""")
#     for ans in q["answers"]:
#         conn.execute(f"""INSERT INTO answers (question_id,answer_text,corect) VALUES({index}, "{ans["text"]}",{ans["correct"]})""")
#     index += 1

q = conn.execute("SELECT * from room_codes")
print(q.fetchall())
conn.commit()