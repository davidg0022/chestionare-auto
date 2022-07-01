from flask import Flask, jsonify, redirect, render_template, request
from random import choice, shuffle, randint
import json
import os
from copy import copy
# with open('semnale_luminoase.json',encoding='utf-8') as json_file:
#     data = json.load(json_file)



port = int(os.environ.get('PORT', 5000))
app = Flask(__name__)
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

data = get_data()[0]
i = 0

question = copy(data)

@app.route("/data_json", methods = ["GET", "POST"])
def get_data():
    return jsonify(question)

@app.route("/select", methods = ["GET", "POST"])
def select():
    if question["disabled"] == True:
        return redirect("/")
    id = request.get_json()["id"]
    question["answers"][id]["selected"] = not question["answers"][id]["selected"]
    print(question["answers"])
    return redirect("/")

@app.route("/next", methods = ["POST"])
def next():
    global question
    if question["disabled"] != True:
        return redirect("/")
    question["corect"] = question["incorect"] = question["disabled"] = False
    question["answers"][0]["selected"] = question["answers"][1]["selected"] = question["answers"][2]["selected"] = False
    question = choice(data)
    while len(question["answers"]) != 3:
        question = choice(data)
 
@app.route("/check_ans", methods = ["GET", "POST"])
def check_ans():
    if question["disabled"] == True:
        return redirect("/")
     
    ok = False 
    for t in range(3):
        if question["answers"][t]["selected"] == True:
            ok = True
    if not ok:
        return redirect("/")
    question["disabled"] = True

    for t in range(3):
        if question["answers"][t]["selected"] == True and question["answers"][t]["correct"] == "0" or question["answers"][t]["selected"] == False and question["answers"][t]["correct"] == "1" :
            question["incorect"] = True
            return redirect("/")
    question["corect"] = True
    
    return redirect("/")

@app.route("/", methods = ["GET", "POST"])
def index():
    # global questions, i, error
    return render_template("index.html", question = question)


if __name__ == '__main__':

    port = 5000 + randint(0, 999)
    print(port)
    url = "http://127.0.0.1:{0}".format(port)
    print(url)
    app.run()