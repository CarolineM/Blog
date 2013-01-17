//for mobile
$(function() {
	if(jQuery.browser.mobile) {
		element = document.getElementById("myCanvas");
		element.style.height = '100%';
	}
});


var isAnimating = false;    // Is animation on or off?
var animateRunning = false; // Are we in the animation loop?

// check if it's an ipad
var isiPad = navigator.userAgent.match(/iPad/i) != null;

var balls = new Array();
var colors = new Array();
var sound;

var DX=.3;
var DY=1;
var bouceFactor = 2;
var numBalls = 12;
var startY;

var numSmallBalls = 80;
var smallDX = .3;
var smallDY = 1;

var time = 0;

var alpha = 1.0;

var canvas;
var context;
var maxX;
var minX;
var rad;


window.requestAnimFrame = (function(callback){
    return window.requestAnimationFrame ||
    window.webkitRequestAnimationFrame ||
    window.mozRequestAnimationFrame ||
    window.oRequestAnimationFrame ||
    window.msRequestAnimationFrame ||
    function(callback){ 
        {
          window.setTimeout(callback, 1000 / 60);
        }
    };
})();

function stopAnimating() {  // Stop animating/drawing
    isAnimating = false;
}

function startAnimating() { // Start animating/drawing
    isAnimating = true;
    if (!animateRunning) animate(balls); // Only draw if we are not already drawing
}

  function Ball(color, radius, dx, dy, x, y)
  {
    this.radius  = radius;
    this.x = x;
    this.y  = y;
    this.dx  = dx;
    this.dy  = dy;
    this.color   = color;
    this.delete = false;
    this.donotmod = false;
    if (radius > 10) {
        this.highlight = new Highlight(x-rad/2, y-rad/2, this);
    }
  }


    Ball.prototype.Bounce = function ()
  {   
    if (this.x + this.radius >= canvas.width || this.x - this.radius <= 0) {
        this.dx *= -1;
    }
    if (this.y - this.radius <= 0 || this.y + this.radius >= canvas.height) {
        this.dy *= -1;
    }
    //bounce off of other balls
    for (var i = 0; i < balls.length; i++) {
        var checkball = balls[i];
        if (checkball != this) {
            if ((isXWithinTheBall(checkball.x + checkball.radius, this) || 
                isXWithinTheBall(checkball.x - checkball.radius, this)) &&
                (isYWithinTheBall(checkball.y + checkball.radius, this) || 
                isYWithinTheBall(checkball.y - checkball.radius, this))) {
                if (!this.donotmod) {
                    this.dx *= -1;
                    this.dy *= -1;
                    this.donotmod = true;
                }
            }
            }
        }
  }

  function isOffScreen(ball) {
    return (ball.x < 0) || (ball.x  > canvas.width) || 
            (ball.y < 0) || (ball.y > canvas.height);
  }

  function isXWithinTheBall(x, ball) {
        return (x > ball.x - ball.radius) && 
                (x <= ball.x + ball.radius)    

  }

  function isYWithinTheBall(y, ball) {
        return (y > ball.y - ball.radius) && 
                (y <= ball.y + ball.radius)
  }

   function clickBall(e) {
        var posx = 0;
        var posy = 0;
        if (!e) var e = window.event;
        if (e.pageX || e.pageY)     {
            posx = e.pageX;
            posy = e.pageY;
         }
        else  {
            posx = e.clientX + document.body.scrollLeft
                + document.documentElement.scrollLeft;
            posy = e.clientY + document.body.scrollTop
                + document.documentElement.scrollTop;
    }
        posx -= canvas.offsetLeft;
        posy -= canvas.offsetTop;
        getClickedBall(posx, posy);
    }

    //TODO refactor duplicate code
    function getClickedBall(x, y) {
        for(var i = 0; i < balls.length; i++) {
            var checkball = balls[i];
            if ((isXWithinTheBall(x, checkball) &&
                (isYWithinTheBall(y, checkball)))) {
                checkball.delete = true;
                //TODO animate pop
                if (sound) {
                	var click=sound.cloneNode();
                	click.play();
                }
            }
        }
    }

    Ball.prototype.Create = function ()
    {
        var grd = context.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.radius);
        grd.addColorStop(1, this.color);
        grd.addColorStop(0, "#DBF2FF");

        context.save();
        context.beginPath();
        context.arc(this.x, this.y, this.radius, 0, 2 * Math.PI, false);
        context.fillStyle = grd;
        context.fill();
        context.lineWidth = 2;

        context.strokeStyle = "black";
        context.stroke();
        context.restore();
        
        if (this.highlight) {
             this.highlight.Create();
         }
    }

  function Highlight(x, y, ball)
  {
    this.color = '#DBF2FF';
    this.x = x;
    this.y = y;
    this.radius = ball.radius*.2;
    this.ball = ball;
  }


     Highlight.prototype.Create = function ()
  {
    var grd = context.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.radius)
    grd.addColorStop(1, this.ball.color);
    grd.addColorStop(.4, this.color);

    context.beginPath();
    context.save();
    context.arc(this.x, this.y, this.radius, 0, 2 * Math.PI, false);
    context.fillStyle = grd;
    context.fill();
    context.restore();
   }

function genRandomColor() {
    var color = Math.floor(Math.random()*colors.length);
    return colors[color];
}

function addSmallerBalls() {
    for (var i = 0; i < numSmallBalls; i++) {
        if (i < numSmallBalls/2) {
            balls[balls.length] = new Ball(genRandomColor(), 8, smallDX, smallDY, 20, i*20);
        }
        else {
            balls[balls.length] = new Ball(genRandomColor(), 8, smallDX, smallDY, canvas.width - 20, i*20);
        }
    }
}

function renderText(content, x, y, opacity) {
    context.save();
    context.fillStyle = "rgba(51, 255, 51, " + alpha + ")";
    context.font = '50px fantasy';
    context.textBaseline = 'bottom';
    context.fillText(content, x, y);
    context.restore();
}


function animate(balls){
    if (isAnimating) { // Only draw if we are drawing
        animateRunning = true;
        time++;
        try {

            // clear
             context.clearRect(0, 0, canvas.width, canvas.height);

              //ball animations
                for(var i = 0; i < balls.length; i++) {
                    var ball = balls[i];
                    ball.x -= ball.dx;
                    ball.y -= ball.dy;
                    ball.donotmod = false;
                    if (ball.highlight) {
                        ball.highlight.x -= ball.dx;
                        ball.highlight.y -= ball.dy;
                    }
                    ball.Create();
                    ball.Bounce();
                    //check delete
                    if (ball.delete || isOffScreen(ball)) {
                        if (ball.delete && ball.radius < 10)  {
                            balls.splice(i, 1);
                            i--;
                        }
                        else {
                            var color=genRandomColor();
                            var xval=Math.floor(100 + Math.random()*(canvas.width - 100))
                            var yval=Math.floor(100 + Math.random()*(canvas.height - 100))
                            balls[i] = new Ball(color, ball.radius, ball.dx * -1, ball.dy * -1, xval, yval);
                        }
                 }
                }

                if (time == 2500) {
                    addSmallerBalls();
                    alpha = 1.0;
                }
                if (time < 100) {
                    renderText("Click to unstick", canvas.width/4, canvas.height/2 - 50, alpha);
                    alpha = alpha - 0.01;
                }
                if (time >= 2600 && time <= 2800) {
                    renderText("Remove the small ones!", canvas.width/5, canvas.height/2, alpha);
                    alpha = alpha - 0.001;
                }
                if (time > 2800) {
                    renderText(balls.length - numBalls, 40, 80, alpha);
                    if (alpha < 1.0) {
                        alpha = alpha + 0.01;
                    }
                }
        } catch (e) {
            if (window.console && window.console.log) {
               window.console.log(e); // for debugging
           }
    }
    }
 
    // request new frame
    requestAnimFrame(function(){
        animate(balls);
        animateRunning = false;
    });
}

 
window.onload = function(){
    canvas = document.getElementById("myCanvas");
    context = canvas.getContext('2d');
    rad = canvas.width*.05;
    minX = canvas.width/((numBalls+2)*rad)
    maxX = canvas.width - minX;
    //TODO block click on pause
    canvas.addEventListener('click', clickBall, false);
    startY = canvas.height/2;
    if (!jQuery.browser.mobile && !isiPad) {
    	sound = new Audio("resources/music/Pop.mp3");
        sound.preload = 'auto';
        sound.load();
    }

    colors[0] = "#C61AFF";
    colors[1] = "#FFE494";
    colors[11] = "#FFB3FF";
    colors[3] = "#1AFFC6";
    colors[4] = "#1AC6FF";
    colors[5] = "#FF1AC6";
    colors[6] = "#8ED6FF";
    colors[7] = "#D9B3FF";
    colors[8] = "#FFB3FF";
    colors[9] = "#94AFFF";
    colors[10] = "#1AFFC6";
    colors[2] = "#FF75BA";

    var xfactor = ((canvas.width - rad*2) / numBalls);
    for (var i = 0; i < numBalls; i++) {
        DX= (-DX);
        DY= (-DY);
        balls[i] = new Ball(colors[i], rad, DX, DY, (xfactor* (i + 1)), startY);
    }
};