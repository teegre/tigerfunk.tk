function isDarkMode() {
  let cookies = document.cookie.split(";");
  for (var i=0; i<cookies.length; i++) {
    let cookie = cookies[i].split("=");
    let key = cookie[0].trim();
    let value = cookie[1];
    if (key === "dark-mode") {
      if (value === "true")
        return 1;
      else
        return 2;
    }
  }
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)
    return 1
  return 0;
}

function toggleDarkMode() {
  let css = document.getElementById("dark-mode");
  if (!css) {
    // Load dark mode
    let head = document.getElementsByTagName("head")[0];
    let css = document.createElement("link");
    css.rel = "stylesheet";
    css.type = "text/css";
    css.href = "/static/home/css/style-dark.css";
    css.setAttribute("id", "dark-mode");
    head.appendChild(css);
    let darkModeBtn = document.getElementById("dark-mode-button");
    if (darkModeBtn)
      document.getElementById("dark-mode-button").innerText = "thème:nuit";
    document.cookie = "dark-mode=true; samesite=lax; path=/";
  } else {
    // Unload dark mode
    css.parentNode.removeChild(css);
    document.getElementById("dark-mode-button").innerText = "thème:jour"
    document.cookie = "dark-mode=false; samesite=lax; path=/";
  }
}

if (isDarkMode() === 1)
  toggleDarkMode();
