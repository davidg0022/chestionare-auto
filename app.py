from flask     import redirect, render_template, request
from random    import randint

from database  import db, ActiveQuestions, Answers, ActiveQuestionsAnswers, RoomCodes, Questions
from utilities import create_room, get_answer, get_question, create_app


app = create_app()


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


@app.route("/room/<code>", methods = ["GET"])
def room(code):
    question = get_question(code)
    return render_template("room.html", question = question)

@app.route("/data_json/<code>", methods = ["GET"])
def get_data(code):
    return get_question(code)


@app.route("/select", methods = [ "POST"])
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


@app.route("/check_ans", methods = [ "POST"])
def check_ans():

    code = request.get_json()["code"]
    question = ActiveQuestions.query.filter_by(_url_code = code).first()

    if question._disabled == True:
        return redirect("/")

    ok = False
    answers = get_answer(code = code)

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


if __name__ == '__main__':

    app.run()