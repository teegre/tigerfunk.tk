function isDarkMode() {
  let cookies = document.cookie.split(";");
  for (var i=0; i<cookies.length; i++) {
    let cookie = cookies[i].split("=");
    let key = cookie[0].trim();
    let value = cookie[1];
    if (key === "dark-mode") {
      if (value === "true")
        return true;
      else
        return false;
    }
  }

  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)
    return true;
  return false;
}

function toggleDarkMode() {
  const darkMode = document.querySelector("#dark-mode");
  const darkModeBtn = document.getElementById("dark-mode-button");
  if (!darkMode.disabled) {
    if (darkModeBtn)
      darkModeBtn.innerText = "thème:jour";
    darkMode.disabled = true;
    document.cookie = "dark-mode=false; samesite=lax; path=/";
  } else {
    if (darkModeBtn)
      darkModeBtn.innerText = "thème:nuit";
    darkMode.disabled = false;
    document.cookie = "dark-mode=true; samesite=lax; path=/";
  }
}

if (isDarkMode()) toggleDarkMode();
