pop_up = document.getElementById("pop-up");
pop_up.addEventListener("click", (element) => {
  if (element.target === pop_up) pop_up.style.display = "none";
});
document.getElementById("join").addEventListener("click", () => {
  pop_up.style.display = "flex";
});
document.getElementById("join1").addEventListener("click", () => {
  code = document.getElementById("room_code");
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/room_join", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(
    JSON.stringify({
      code: code.value,
    })
  );
});
document.getElementById("join1").addEventListener("click", () => {
  pop_up.style.display = "none";
});
