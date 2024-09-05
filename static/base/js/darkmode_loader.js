var darkMode = localStorage.getItem("darkMode");
if (darkMode == null) {
  if (
    window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches
  ) {
    document.documentElement.classList.add("darkmode");
    localStorage.setItem("darkMode", "enabled");
  } else {
    localStorage.setItem("darkMode", "disabled");
  }
}

if (darkMode === 'enabled') {
    document.documentElement.classList.add('darkmode');
    localStorage.setItem('darkMode', 'enabled');
}