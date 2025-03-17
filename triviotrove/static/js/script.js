// Select DOM elements
const scoreDisplay = document.getElementById("score");
const wordDisplay = document.getElementById("word");
const guessInput = document.getElementById("guess");
const submitButton = document.getElementById("submit");
const newWordButton = document.getElementById("new-word");
const popup = document.getElementById("popup");
const toggleDarkModeBtn = document.getElementById("toggle-dark-mode");
const timerDisplay = document.createElement("p"); // Timer Element
timerDisplay.id = "timer";
document.getElementById("container").prepend(timerDisplay); // Add timer to UI

let originalWord = "";
let scrambledWord = "";
let score = 0;
let timer;
let timeLeft = 60;

/* ==========================
   Fetch & Display Scrambled Word
=========================== */
function fetchNewWord() {
  fetch("/get_new_word/")
    .then((response) => response.json())
    .then((data) => {
      if (data.original && data.scrambled) {
        originalWord = data.original;
        scrambledWord = data.scrambled;
        wordDisplay.textContent = scrambledWord;
        guessInput.value = "";
        resetTimer(); // Reset timer when a new word is fetched
      } else {
        console.error("Invalid response data:", data);
      }
    })
    .catch((error) => console.error("Error fetching word:", error));
}

/* ==========================
   Timer Functions
=========================== */

/* ==========================
   Timer Functions
=========================== */
function startTimer() {
  timeLeft = 30;
  updateTimerDisplay();

  timer = setInterval(() => {
    timeLeft--;
    updateTimerDisplay();

    if (timeLeft <= 0) {
      clearInterval(timer);

      // Deduct a point when time runs out
      if (score > 0) {
        score--;
      }
      scoreDisplay.textContent = score; // Update score display

      // Check if the player lost
      if (score === 0) {
        showPopup("❌ You lost! Score reset to 0.", "error");
      } else {
        showPopup("⏳ Time's up! You lost 1 point.", "error");
      }

      fetchNewWord(); // Get a new word when time runs out
    }
  }, 1000);
}

function updateTimerDisplay() {
  timerDisplay.textContent = `⏳ Time Left: ${timeLeft}s`;
}

function resetTimer() {
  clearInterval(timer);
  startTimer();
}

/* ==========================
   Check Answer
=========================== */
function checkGuess() {
  const userGuess = guessInput.value.trim().toLowerCase();

  if (!userGuess) {
    showPopup("⚠️ Please enter a guess!", "warning");
    return;
  }

  if (userGuess === originalWord) {
    score++;
    scoreDisplay.textContent = score;
    showPopup("Correct!🎉 +1 Point", "success");
    clearInterval(timer); // Stop timer
    setTimeout(fetchNewWord, 2000); // Load new word after 2s
  } else {
    showPopup("❌ Incorrect! Try again", "error");
  }

  guessInput.value = "";
}

/* ==========================
   Show Popup Message
=========================== */
function showPopup(message, type) {
  popup.textContent = message;
  popup.className = `popup show ${type}`;

  setTimeout(() => {
    popup.classList.remove("show", type);
  }, 2000);
}

/* ==========================
   Dark Mode Toggle
=========================== */
function toggleDarkMode() {
  document.body.classList.toggle("dark-mode");
  let darkModeIcon = toggleDarkModeBtn.querySelector("i");

  if (document.body.classList.contains("dark-mode")) {
    localStorage.setItem("dark-mode", "enabled");
    darkModeIcon.classList.replace("fa-moon", "fa-sun");
  } else {
    localStorage.setItem("dark-mode", "disabled");
    darkModeIcon.classList.replace("fa-sun", "fa-moon");
  }
}

/* ==========================
   Initialize Page
=========================== */
document.addEventListener("DOMContentLoaded", () => {
  if (wordDisplay && guessInput && submitButton && newWordButton && popup) {
    // Load initial word
    fetchNewWord();

    // Load dark mode preference
    if (localStorage.getItem("dark-mode") === "enabled") {
      document.body.classList.add("dark-mode");
      toggleDarkModeBtn
        .querySelector("i")
        .classList.replace("fa-moon", "fa-sun");
    }

    // Event Listeners
    submitButton.addEventListener("click", checkGuess);
    newWordButton.addEventListener("click", fetchNewWord);
    toggleDarkModeBtn.addEventListener("click", toggleDarkMode);
  } else {
    console.error("One or more required elements are missing.");
  }
});
