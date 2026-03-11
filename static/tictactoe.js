document.addEventListener("DOMContentLoaded", function () {
  const boxes = document.querySelectorAll(".square");
  const guess = document.querySelector("#guess");
  const X = document.querySelector("#X");
  const O = document.querySelector("#O");
  const new_game = document.querySelector("#New_Game");
  const message = document.querySelector("#text_string");
  const form = document.querySelector("#TicTacToe-form");
  form.onsubmit = (event) => {
    event.preventDefault();
    let row = 0;
    let column = 0;
    fetch("/", {
      method: "POST",
      body: new FormData(form),
    })
      .then((response) => response.json())
      .then((data) => {
        message.innerHTML = data.string;
        boxes.forEach((box) => {
          box.placeholder = data.board[row][column];
          column += 1;
          if (column === 3) {
            row += 1;
            column = 0;
          }
        });
        if (data.string === "AI is thinking...") {
          setTimeout(() => {
            form.dispatchEvent(new Event("submit", { cancelable: true }));
          }, 800);
        }
        if (
          data.string === "Draw." ||
          data.string === "AI Wins!" ||
          data.string === "You win!"
        ) {
          disableBoxes(boxes, new_game);
        } else {
          enableBoxes(boxes, new_game);
        }
        if (X.style.display != "none") {
          disableOnlyBoxes(boxes);
        }
        if (data.string === "Your move." || data.string === "Invalid move.") {
          enableBoxes(boxes, new_game);
        } else {
          disableOnlyBoxes(boxes);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };
  X.onclick = () => {
    X.value = "X";
    O.value = "";
    X.style.display = "none";
    O.style.display = "none";
    message.innerHTML = "Your move.";
    boxes.forEach((box) => {
      box.style.display = "flex";
    });
    enableBoxes(boxes, new_game);
  };
  O.onclick = () => {
    O.value = "O";
    X.value = "";
    X.style.display = "none";
    O.style.display = "none";
    boxes.forEach((box) => {
      box.style.display = "flex";
    });
    enableBoxes(boxes, new_game);
    form.dispatchEvent(new Event("submit", { cancelable: true }));
  };
  boxes.forEach((box) => {
    box.onclick = () => {
      guess.value = box.id;
      form.dispatchEvent(new Event("submit", { cancelable: true }));
    };
  });
  new_game.addEventListener("click", function () {
    X.style.display = "inline";
    O.style.display = "inline";
    X.value = "";
    O.value = "";
    disableBoxes(boxes, new_game);
  });
});
function disableOnlyBoxes(boxes) {
  boxes.forEach((box) => {
    box.setAttribute("disabled", "disabled");
    box.style.cursor = "not-allowed";
  });
}
function disableBoxes(boxes, new_game) {
  boxes.forEach((box) => {
    box.setAttribute("disabled", "disabled");
    box.style.cursor = "not-allowed";
  });
  new_game.style.display = "flex";
}
function enableBoxes(boxes, new_game) {
  boxes.forEach((box) => {
    box.removeAttribute("disabled");
    box.style.cursor = "pointer";
  });
  new_game.style.display = "none";
}
