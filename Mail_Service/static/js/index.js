const baseUrlIndex = window.location.protocol + "//" + window.location.host + "/api";
const integrationDiv = document.querySelector(".composition__item_simple-integration");
const notificationsDiv = document.querySelector(".composition__item_real-time-notifications");
const staticDiv = document.querySelector(".composition__item_static");
const safetyDiv = document.querySelector(".composition__item_safety");
const telegramDiv = document.querySelector(".composition__item_tg");
const aboutPochtmen = document.querySelector(".about-pochtman-link");
let authorUser = document.querySelector(".navbar__username");
let authorId = authorUser.getAttribute("data-user-id");
// getNotifications(authorId);
// запрос на новые уведомления

let timeId = setTimeout(function notificationUpdates() {
    getNotifications();
    timeId = setTimeout(notificationUpdates, 15000);
}, 1000);



integrationDiv.addEventListener("click", function(e) {
    window.scrollTo({ top: 700, behavior: 'smooth'});
});

notificationsDiv.addEventListener("click", function(e) {
    window.scrollTo({ top: 1150, behavior: 'smooth'});
});

telegramDiv.addEventListener("click", function(e) {
    window.scrollTo({ top: 1150, behavior: 'smooth'});
});

staticDiv.addEventListener("click", function(e) {
    window.scrollTo({ top: 1550, behavior: 'smooth'});
});

safetyDiv.addEventListener("click", function(e) {
    window.scrollTo({ top: 2050, behavior: 'smooth'});
});

aboutPochtmen.addEventListener("click", function(e) {
  window.scrollTo({ top: 2650, behavior: 'smooth'});
});


var carousel = document.querySelector('.carousel');
var carouselContent = document.querySelector('.carousel-content');
var slides = document.querySelectorAll('.slide');
var arrayOfSlides = Array.prototype.slice.call(slides);
var carouselDisplaying;
var screenSize;
setScreenSize();
var lengthOfSlide;

function addClone() {
   var lastSlide = carouselContent.lastElementChild.cloneNode(true);
   lastSlide.style.left = (-lengthOfSlide) + "px";
   carouselContent.insertBefore(lastSlide, carouselContent.firstChild);
}
// addClone();

function removeClone() {
  var firstSlide = carouselContent.firstElementChild;
  firstSlide.parentNode.removeChild(firstSlide);
}

function moveSlidesRight() {
  var slides = document.querySelectorAll('.slide');
  var slidesArray = Array.prototype.slice.call(slides);
  var width = 0;

  slidesArray.forEach(function(el, i){
    el.style.left = width + "px";
    width += lengthOfSlide;
  });
  addClone();
}
moveSlidesRight();

function moveSlidesLeft() {
  var slides = document.querySelectorAll('.slide');
  var slidesArray = Array.prototype.slice.call(slides);
  slidesArray = slidesArray.reverse();
  var maxWidth = (slidesArray.length - 1) * lengthOfSlide;

  slidesArray.forEach(function(el, i){
    maxWidth -= lengthOfSlide;
    el.style.left = maxWidth + "px";
  });
}

window.addEventListener('resize', setScreenSize);

function setScreenSize() {
  if ( window.innerWidth >= 500 ) {
    carouselDisplaying = 4;
  } else if ( window.innerWidth >= 300 ) {
    carouselDisplaying = 2;
  } else {
    carouselDisplaying = 1;
  }
  getScreenSize();
}

function getScreenSize() {
  var slides = document.querySelectorAll('.slide');
  var slidesArray = Array.prototype.slice.call(slides);
  lengthOfSlide = ( carousel.offsetWidth  / carouselDisplaying );
  var initialWidth = -lengthOfSlide;
  slidesArray.forEach(function(el) {
    el.style.width = lengthOfSlide + "px";
    el.style.left = initialWidth + "px";
    initialWidth += lengthOfSlide;
  });
}


var rightNav = document.querySelector('.nav-right');
rightNav.addEventListener('click', moveLeft);

var moving = true;
function moveRight() {
  if ( moving ) {
    moving = false;
    var lastSlide = carouselContent.lastElementChild;
    lastSlide.parentNode.removeChild(lastSlide);
    carouselContent.insertBefore(lastSlide, carouselContent.firstChild);
    removeClone();
    var firstSlide = carouselContent.firstElementChild;
    firstSlide.addEventListener('transitionend', activateAgain);
    moveSlidesRight();
  }
}

function activateAgain() {
  var firstSlide = carouselContent.firstElementChild;
  moving = true;
  firstSlide.removeEventListener('transitionend', activateAgain);
}

var leftNav = document.querySelector('.nav-left');
leftNav.addEventListener('click', moveRight);

// var moveLeftAgain = true;

function moveLeft() {
  if ( moving ) {
    moving = false;
    removeClone();
    var firstSlide = carouselContent.firstElementChild;
    firstSlide.addEventListener('transitionend', replaceToEnd);
    moveSlidesLeft();
  }
}

function replaceToEnd() {
  var firstSlide = carouselContent.firstElementChild;
  firstSlide.parentNode.removeChild(firstSlide);
  carouselContent.appendChild(firstSlide);
  firstSlide.style.left = ( (arrayOfSlides.length -1) * lengthOfSlide) + "px";
  addClone();
  moving = true;
  firstSlide.removeEventListener('transitionend', replaceToEnd);
}




carouselContent.addEventListener('mousedown', seeMovement);

var initialX;
var initialPos;
function seeMovement(e) {
  initialX = e.clientX;
  getInitialPos();
  carouselContent.addEventListener('mousemove', slightMove);
  document.addEventListener('mouseup', moveBasedOnMouse);
}

function slightMove(e) {
  if ( moving ) {
    var movingX = e.clientX;
    var difference = initialX - movingX;
    if ( Math.abs(difference) < (lengthOfSlide/4) ) {
      slightMoveSlides(difference);
    }  
  }
}

function getInitialPos() {
  var slides = document.querySelectorAll('.slide');
  var slidesArray = Array.prototype.slice.call(slides);
  initialPos = [];
  slidesArray.forEach(function(el){
    var left = Math.floor( parseInt( el.style.left.slice(0, -2 ) ) ); 
    initialPos.push( left );
  });
}

function slightMoveSlides(newX) {
  var slides = document.querySelectorAll('.slide');
  var slidesArray = Array.prototype.slice.call(slides);
  slidesArray.forEach(function(el, i){
    var oldLeft = initialPos[i];
    el.style.left = (oldLeft + newX) + "px";
  });
}

function moveBasedOnMouse(e) { 
  var finalX = e.clientX;
  if ( initialX - finalX > 0) {
    moveRight();
  } else if ( initialX - finalX < 0 ) {
    moveLeft();
  }
  document.removeEventListener('mouseup', moveBasedOnMouse);
  carouselContent.removeEventListener('mousemove', slightMove);
}

async function getNotifications() {
    // console.log(localStorage.getItem("token"));
    let response = await fetch(`${baseUrlIndex}/notifications/count`, {
      method: 'GET',
      headers: {
          'Content-Type': 'application/json',
          'Authorization' : `Token ${localStorage.getItem("token")}`
          }
      });
      let result = await response.json();
      let total = result.count;
      console.log(total);
      await addNotifyBlock(total);

};

async function addNotifyBlock(total) {
  const notifyPoint = document.querySelector('.navbar__notification');
  if (total === 0) {
      notifyPoint.style.display = 'none';
      document.querySelector('.navbar__notification_count').textContent = "";
  } else {
      notifyPoint.style.display = 'block';
      document.querySelector('.navbar__notification_count').textContent = total;
  }
};
