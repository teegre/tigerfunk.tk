let article = document.getElementsByTagName("article")[0];

window.onload = function() {
  let img = document.getElementsByClassName("loading")[0];
  article.removeChild(img);
}

let img = document.createElement("img");
if (isDarkMode())
  img.src = "/static/home/img/loading-dark.gif";
else
  img.src = "/static/home/img/loading-light.gif";

img.className = "loading";
article.appendChild(img);
