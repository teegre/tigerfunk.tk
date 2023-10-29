let media = document.getElementsByClassName("media")[0];

window.onload = function() {
  if (media) {
    let img = document.getElementsByClassName("loading")[0];
    media.removeChild(img);
  }
}

if (media) {
  let img = document.createElement("img");
  if (isDarkMode())
    img.src = "/static/home/img/loading-dark.gif";
  else
    img.src = "/static/home/img/loading-light.gif";

  img.className = "loading";
  media.appendChild(img);
}
