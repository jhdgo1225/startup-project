const textarea = document.querySelector("#notebook");
const letterCnt = document.querySelector("#check-block > span");
const checkBtn = document.querySelector("#contents-check");
const resultContainer = document.querySelector("#mato");
let resultBtn;

const handleKeyUp = () => {
  const inputText = textarea.value;
  letterCnt.innerText = `글자 수: ${inputText.length}`;
};

const handleCheckBtn = () => {
  if (textarea.value.trim().length < 30) {
    console.log("30자 이상 입력해주세요!");
    return;
  }

  if (checkBtn.classList.contains("checked")) {
    checkBtn.innerText = "검 사";
    checkBtn.classList.remove("checked");
    resultContainer.removeChild(resultBtn);
    return;
  }
  resultBtn = document.createElement("button");
  resultBtn.innerText = "결과 확인 ⬆︎";
  resultBtn.classList.add("mobile-and-tablet-only");
  checkBtn.innerText = "다시쓰기";
  checkBtn.classList.add("checked");
  console.log(textarea.value);
  if (window.innerWidth <= 1024) {
    resultContainer.append(resultBtn);
  }
};

const handleResize = () => {
  if (checkBtn.classList.contains("checked")) {
    if (window.innerWidth > 1024) {
      resultContainer.removeChild(resultBtn);
    } else {
      resultContainer.append(resultBtn);
    }
  }
};

textarea.addEventListener("keyup", handleKeyUp);
textarea.focus();
checkBtn.addEventListener("click", handleCheckBtn);
window.addEventListener("resize", handleResize);
