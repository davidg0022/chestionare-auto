from flask import Flask, jsonify, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import choice, random, shuffle, randint
import json
import os
import string
# with open('semnale_luminoase.json',encoding='utf-8') as json_file:
#     data = json.load(json_file)



def get_data():
    files = [f for f in os.listdir('.') if os.path.isfile(f) and ".json" in f]
    data = []
    for f in files:
        with open(f,encoding='utf-8') as json_file:
            temp = json.load(json_file)
            for q in temp:
                data.append(q)
    shuffle(data)
    return data

    
data = get_data()
# question = data[0]
# json_string = json.dumps(question,ensure_ascii=False)
# with open('current.json', 'w', encoding="utf-8") as outfile:
#     outfile.write(json_string)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Answers(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    _question_id = db.Column("question_id", db.Integer)
    _corect = db.Column("corect", db.Integer)
    _answer_text = db.Column("answer_text", db.String(200))


class Questions(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    _type = db.Column("type", db.String(200))
    _img_url = db.Column("img_url", db.String(200))
    _title = db.Column("title", db.String(200))

class RoomCodes(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    _url_code = db.Column("url_code",db.String(200))

    def __init__(self, url_code):
        self._url_code = url_code 

class ActiveQuestions(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    _url_code = db.Column("url_code",db.String(200))
    _question_title = db.Column("question_title",db.String(200))
    _img_url = db.Column("img_url",db.String(200))
    _disabled = db.Column("disabled", db.Integer)
    _corect = db.Column("corect", db.Integer)
    _incorect = db.Column("incorect", db.Integer)

    def __init__(self, url_code, question_title, img_url) -> None:
        self._url_code = url_code
        self._disabled = False
        self._corect = False
        self._incorect = False
        self._img_url = img_url
        self._question_title = question_title

class ActiveQuestionsAnswers(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    _url_code = db.Column("url_code",db.String(200))
    _answer_text = db.Column("answer_text",db.String(200))
    _selected = db.Column("selected", db.Integer)
    _corect = db.Column("corect", db.Integer)
    _question_id = db.Column("question_id", db.Integer)
    
    def __init__(self, url_code, answer_text, corect, id) -> None:
        self._url_code = url_code
        self._corect = corect
        self._selected = False
        self._answer_text = answer_text
        self._question_id = id

def create_room():
    random_question = randint(1, 1180)
    question = Questions.query.filter_by(_id = random_question).first()
    answers = Answers.query.filter_by(_question_id = question._id).all()
    while True:
        code = list(string.ascii_lowercase + string.digits)
        shuffle(code)
        code = "".join(code)[:5]
        temp = RoomCodes.query.filter_by(_url_code = code).all()
        if len(temp):
            continue
        else:
            room_code = RoomCodes(code)
            db.session.add(room_code)
            # db.session.commit()
            break
    
    new_room = ActiveQuestions(code, question._title, question._img_url)
    db.session.add(new_room)
    for ans in answers:
        new_ans = ActiveQuestionsAnswers(code, ans._answer_text, ans._corect, ans._id)
        db.session.add(new_ans)
    db.session.commit()
    return code


def get_question(code):
    data = {"code":code}
    question = ActiveQuestions.query.filter_by(_url_code = code).first()
    answers =  ActiveQuestionsAnswers.query.filter_by(_url_code = code).all()
    data["title"] = question._question_title
    data["incorect"] = question._incorect
    data["corect"] = question._corect
    data["disabled"] = question._disabled
    data["img_url"] = question._img_url
    data["answers"] = []
    for ans in answers:
        temp = {}
        temp["selected"] = ans._selected
        temp["text"] = ans._answer_text
        temp["correct"] = ans._corect
        temp["id"] = ans._id
        data["answers"].append(temp)
    return data

def get_answer(id = "", code = ""):
    if id:
        return ActiveQuestionsAnswers.query.filter_by(_id = id).first()
    return ActiveQuestionsAnswers.query.filter_by(_url_code = code).all()

@app.route("/data_json/<code>", methods = ["GET", "POST"])
def get_data(code):
    return get_question(code)


@app.route("/select", methods = ["GET", "POST"])
def select():
    id = request.get_json()["id"]
    code = request.get_json()["code"]
    question = get_question(code)
    if question["disabled"] == True:
        return redirect("/")
    
    answer = get_answer(id = id)
    answer._selected = not answer._selected
    db.session.commit()
    return redirect("/")


@app.route("/next", methods = ["POST"])
def next():
    code = request.get_json()["code"]
    old_question = ActiveQuestions.query.filter_by(_url_code = code).first()
    old_question_answers = ActiveQuestionsAnswers.query.filter_by(_url_code = code).all()
    if old_question._disabled != True:
        return redirect("/")
    random_question = randint(1, 1180)
    new_question = Questions.query.filter_by(_id = random_question).first()
    new_question_answers = Answers.query.filter_by(_question_id = new_question._id).all()
    
    old_question._question_title = new_question._title
    old_question._img_url = new_question._img_url
    old_question._disabled = False
    old_question._corect = False
    old_question._incorect = False
    for i in range(3):
        old_question_answers[i]._selected = False
        old_question_answers[i]._corect = new_question_answers[i]._corect
        old_question_answers[i]._answer_text = new_question_answers[i]._answer_text
    db.session.commit()
    return redirect("/")


@app.route("/check_ans", methods = ["GET", "POST"])
def check_ans():
    code = request.get_json()["code"]
    question = ActiveQuestions.query.filter_by(_url_code = code).first()
    if question._disabled == True:
        return redirect("/")
    ok = False
    answers = get_answer(code = code)
    print(answers)
    for ans in answers:
        if ans._selected == True:
            ok = True
            break
    if not ok:
        return redirect("/")
    question._disabled = True

    for ans in answers:
        if ans._selected != ans._corect:
            question._incorect = True
            db.session.commit()
            return redirect("/")

    question._corect = True
    db.session.commit()
    return redirect("/")

@app.route("/room/<code>", methods = ["GET", "POST"])
def room(code):
    # code = "4bk2i"
    # code1 = "0u6jl"
    question = get_question(code)
    return render_template("room.html", question = question)

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    join = request.form.get("join")
    if join == "1":
        code = request.form.get("room_code").lower()
        temp = RoomCodes.query.filter_by(_url_code = code).all()
        if len(temp) == 1:
            return redirect(f"/room/{code}")
        return render_template("index.html", error = "Invalid Code Room")
    if join == "0":
        code = create_room()
        return redirect(f"/room/{code}")
    return redirect("/")
if __name__ == '__main__':
    app.run()