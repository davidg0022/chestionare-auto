from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# SQL database tables

# Answers and Questions tables are constat tables (no delete/update/insert queryes)

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