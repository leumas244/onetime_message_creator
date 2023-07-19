document.querySelectorAll(".copy-link").forEach((copyLinkParent) => {
    const inputField = copyLinkParent.querySelector(".copy-link-input");
    const copyButton = copyLinkParent.querySelector(".copy-link-button");
    const text = inputField.value;
    const inputType = inputField.type
  
    inputField.addEventListener("focus", () => inputField.select());
  
    copyButton.addEventListener("click", () => {
      inputField.select();
      navigator.clipboard.writeText(text);
  
      inputField.value = "Kopiert!";
      inputField.type = "text";
      setTimeout(() => (inputField.type = inputType), 1000);
      setTimeout(() => (inputField.value = text), 1000);
    });
  });