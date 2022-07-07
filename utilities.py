from database import db, ActiveQuestions, Answers, ActiveQuestionsAnswers, RoomCodes, Questions
from flask import Flask
from random import randint, shuffle
import string


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app


def create_room():
    random_question = randint(1, 1180)
    question = Questions.query.filter_by(_id = random_question).first()
    answers = Answers.query.filter_by(_question_id = question._id).all()

    # Make sure that we have different Room Codes
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