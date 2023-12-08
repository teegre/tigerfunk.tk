var audio = document.getElementById("audio");
var tracks = audio.children.length;
var currentTrackIndex = 0;
var play_btn = document.querySelector(".main-play-btn");
var trackTitle = document.querySelector(".title");
var trackElapsed = document.querySelector(".elapsed");
var trackDuration = document.querySelector(".duration");
var pageTitle = document.title;

audio.ontimeupdate = onTimeUpdate;

audio.onloadedmetadata = function() {
  trackDuration.innerHTML = this.getTime(this.audio.duration)
}.bind(this);

this.makePlaylist();
this.updateTrackInfo();

play_btn.addEventListener("click", togglePlay)

audio.addEventListener("ended", function () {
  updateTrackInfo();
  currentTrackIndex++;
  if (currentTrackIndex < tracks) {
    loadTrack(currentTrackIndex);
    togglePlay();
  } else {
    currentTrackIndex = 0;
    loadTrack(0);
    trackElapsed.innerText = "00:00";
  }
  updateTrackInfo();
})

function getTime(d) {
  var min = parseInt(parseInt(d)/60);
  var sec = parseInt(d)%60;
  if (min < 10) min = "0" + min;
  if (sec < 10) sec = "0" + sec;
  return min + ":" + sec;
}

function makePlaylist() {
  let index = 0;
  var playlist = document.getElementById("playlist");

  for (const track of audio.children) {
    var li = document.createElement("li");
    var btn = document.createElement("button");
    var trackTitle = document.createElement("div");
    var trackDuration = document.createElement("div");

    li.setAttribute("class", "track");
    btn.setAttribute("class", "play-btn-" + index);
    btn.innerHTML = "<img src='/static/home/img/play.svg'>";
    trackTitle.setAttribute("class", "track-title");
    trackDuration.setAttribute("class", "track-duration");

    btn.addEventListener("click", (function(idx) {
      return function () {
        if (idx != currentTrackIndex) {
          audio.pause();
          updateTrackInfo();
          loadTrack(idx);
        }
        togglePlay();
      };
    })(index));

    const title = track.getAttribute("data-track-title");
    const duration = track.getAttribute("data-track-duration");
    trackTitle.innerText = title;
    trackDuration.innerText = duration;
    
    li.append(btn, trackTitle, trackDuration);
    playlist.appendChild(li);

    index++;
  }
}

function onTimeUpdate() {
  var t = audio.currentTime;
  trackElapsed.innerText = getTime(t) + " /";
}

function updateTrackInfo() {
  var currentTrack = audio.children[currentTrackIndex]
  var btn = document.getElementsByClassName("play-btn-" + currentTrackIndex)[0];
  trackTitle.innerText = currentTrack.getAttribute("data-track-title");
  trackDuration.innerText = currentTrack.getAttribute("data-track-duration");
  if (audio.paused) {
    play_btn.innerHTML = "<img src='/static/home/img/play.svg'>";
    btn.innerHTML = "<img src='/static/home/img/play.svg'>";
    document.title = pageTitle;
  } else {
    play_btn.innerHTML = "<img src='/static/home/img/pause.svg'>";
    btn.innerHTML = "<img src='/static/home/img/pause.svg'>";
    document.title = " ▶ " + trackTitle.innerText + " | " + pageTitle;
  }
}

function togglePlay() {
  if (audio.paused) {
    audio.play();
  } else {
    audio.pause();
  }
  updateTrackInfo();
}

function loadTrack(idx) {
  currentTrackIndex = idx;
  audio.src = audio.children[idx].src;
}
