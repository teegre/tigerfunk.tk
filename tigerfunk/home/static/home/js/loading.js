let media = document.getElementsByClassName("media")[0];

window.onload = function() {
  if (media) {
    let fig = document.getElementsByClassName("loading")[0];
    media.removeChild(fig);
  }
}

if (media) {
  let fig = document.createElement("figure");
  let img = document.createElement("img");
  let cap = document.createElement("figcaption");
  if (isDarkMode())
    img.src = "/static/home/img/loading-dark.gif";
  else
    img.src = "/static/home/img/loading-light.gif";

  fig.className = "loading";
  cap.className = "loading-text";
  cap.innerText = "Attendez...";
  fig.appendChild(img);
  fig.appendChild(cap);
  media.appendChild(fig);
}
