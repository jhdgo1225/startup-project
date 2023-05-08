const textarea = document.querySelector("#notebook");
const letterCnt = document.querySelector("#check-block > span");
const checkBtn = document.querySelector("#contents-check");
const resultBtn = document.querySelector("#mobile-and-tablet-only");

const handleKeyUp = () => {
  const inputText = textarea.value;
  letterCnt.innerText = `글자 수: ${inputText.length}`;
};

const startChecker = () => {
  if (textarea.value.trim().length > 0 && window.innerWidth < 1025) {
    resultBtn.style.display = "inline-block";
  }
};

textarea.addEventListener("keyup", handleKeyUp);
textarea.focus();

checkBtn.addEventListener("click", startChecker);
