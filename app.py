from flask import Flask, jsonify, redirect, render_template, request
from random import choice, shuffle, randint
import json
import os
from copy import copy
# with open('semnale_luminoase.json',encoding='utf-8') as json_file:
#     data = json.load(json_file)



port = int(os.environ.get('PORT', 5000))

def get_data():
    files = [f for f in os.listdir('.') if os.path.isfile(f) and ".json" in f]
    data = []
    # for f in files:
    with open(files[0],encoding='utf-8') as json_file:
        temp = json.load(json_file)
        for q in temp:
            data.append(q)
    # shuffle(data)
    return data

data = [
  {
    "corect": False,
    "incorect": False,
    "disabled": False,
    "title": "În cazul unui accident în care victima şi-a pierdut cunoştinţa, prima măsură va fi:",
    "answers": [
      {
        "text": "să administraţi medicamente din trusa de prim ajutor;",
        "correct": "0",
        "selected": False
      },
      {
        "text": "să imobilizaţi eventualele fracturi;",
        "correct": "0",
        "selected": False
      },
      {
        "text": "să controlaţi respiraţia şi bătăile inimii.",
        "correct": "1",
        "selected": False
      }
    ],
    "img_url": ""
  },
  {
    "corect": False,
    "incorect": False,
    "disabled": False,
    "title": "Hemoragia nazală se poate opri dacă accidentatul:",
    "answers": [
      {
        "text": "stă culcat cu capul pe spate;",
        "correct": "0",
        "selected": False
      },
      {
        "text": "stă în picioare şi îşi strânge ambele nări timp de aproximativ 5-10 minute;",
        "correct": "1",
        "selected": False
      },
      {"text": "ridică mâna dreaptă.", "correct": "0", "selected": False}
    ],
    "img_url": ""
  }]
question = data[0]
i = 0

    
app = Flask(__name__)

@app.route("/data_json", methods = ["GET", "POST"])
def get_data():
    global question
    return question

@app.route("/select", methods = ["GET", "POST"])
def select():
    global question
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
    global question
    return render_template("index.html", question = question)


if __name__ == '__main__':
    
    port = 5000 + randint(0, 999)
    print(port)
    url = "http://127.0.0.1:{0}".format(port)
    print(url)

    app.run()