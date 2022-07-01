from flask import Flask, jsonify, redirect, render_template, request
from random import choice, shuffle
import json
import os
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

app = Flask(__name__)

i = 0

question = data[i]

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