answers = document.getElementsByClassName("ans_wrapper");
code = document.getElementById("qu").getAttribute("room_code");
for (let i = 0; i < 3; i++) {
  answers[i].addEventListener("click", () => {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/select", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(
      JSON.stringify({
        id: answers[i].getAttribute("ans_id"),
        code: code,
      })
    );
  });
}

const interval_function = (data) => {
  code = document.getElementById("qu").getAttribute("room_code");
  fetch("/data_json/" + code)
    .then((r) => r.json())
    .then((r) => {
      if (data.title != r.title) location.reload();
      if (r.incorect) {
        document.getElementById("incorect").style.display = "block";
      }
      if (r.corect) document.getElementById("corect").style.display = "block";
      if (r.img_url == "")
        document.getElementById("qu").classList.remove("question_wrapper");
      else document.getElementById("qu").classList.add("question_wrapper");
      ANS = document.getElementsByClassName("ans_wrapper");
      LET = document.getElementsByClassName("letter");
      selected = false;
      disable = r.disabled ? true : false;
      for (let i = 0; i < 3; i++) {
        if (r.answers[i].selected) {
          ANS[i].classList.add("selected-True");
          LET[i].classList.add("selectedL-True");
          selected = true;
        } else {
          ANS[i].classList.remove("selected-True");
          LET[i].classList.remove("selectedL-True");
        }
      }
      if (selected)
        document.getElementById("send").classList.remove("low_opac");
      else document.getElementById("send").classList.add("low_opac");
      if (disable) {
        document.getElementById("send").classList.add("low_opac");
        document.getElementById("next").classList.remove("low_opac");
        Letters = document.getElementsByClassName("letter");
        for (let i = 0; i < 3; i++) {
          if (r.answers[i].correct == "1")
            Letters[i].style.color = "rgb(73, 217, 29)";
          else Letters[i].style.color = "rgb(217, 58, 58)";
        }
      } else document.getElementById("next").classList.add("low_opac");
    });
};
document.getElementById("send").addEventListener("click", () => {
  ANS = document.getElementsByClassName("answer");
  code = document.getElementById("qu").getAttribute("room_code");
  js = [];
  for (let i = 0; i < 3; i++) {
    js.push(ANS[i].classList.contains("selected-True"));
  }
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/check_ans", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(
    JSON.stringify({
      code: code,
    })
  );
});

document.getElementById("next").addEventListener("click", () => {
  code = document.getElementById("qu").getAttribute("room_code");
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/next", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(JSON.stringify({code: code}));
});
