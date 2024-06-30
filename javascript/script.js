function confirmDelete() {
  return confirm("本当に消去しますか？");
}

function confirmLogout() {
  return confirm("ログアウトしてよろしいですか？");
}

function enableSubmitButton() {
  var content = document.getElementById("memoContent").value;
  var submitButton = document.getElementById("submitButton");

  if (content.trim() === "") {
    submitButton.disabled = true;
  } else {
    submitButton.disabled = false;
  }
}

function validateForm() {
  var content = document.getElementById("memoContent").value;
  if (content.trim() === "") {
    alert("テキストを入力してください。");
    return false;
  }
  return true;
}
