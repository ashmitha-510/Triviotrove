function showPopup(message, isCorrect) {
  const popup = document.getElementById("popup");
  popup.textContent = message;

  // Remove previous styles
  popup.classList.remove("correct", "incorrect");

  // Apply correct or incorrect style
  if (isCorrect) {
    popup.classList.add("correct");
  } else {
    popup.classList.add("incorrect");
  }

  // Show popup
  popup.style.display = "block";
  popup.style.opacity = "1";

  // Hide after 2 seconds
  setTimeout(() => {
    popup.style.opacity = "0";
    setTimeout(() => {
      popup.style.display = "none";
    }, 300); // Delay for fade-out effect
  }, 2000);
}

// Example Usage
// showPopup("Correct!", true);  // Green popup
// showPopup("Incorrect!", false);  // Red popup
