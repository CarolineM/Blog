//TODO each ball property
//TODO convert song to ogg file


var isAnimating = false;    // Is animation on or off?
var animateRunning = false; // Are we in the animation loop?
var requiresRedraw = true;

//TODO array of balls
var balls = new Array();
var colors = new Array();

var DX=.3;
var DY=.2;
var bouceFactor = 2;
var numBalls = 12;
var startY;
var maxX = 1600;
var minX = 100;

var canvas;
var context;

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
    this.bouncedx = false;
    this.bouncedy = false;
    this.highlight = new Highlight(x-15, y-15, this);
  }


    Ball.prototype.Bounce = function ()
  {   
    if (this.x + this.radius >= canvas.width || this.x - this.radius <= 0) {
        this.dx *= -1;
        return;
    }
    if (this.y - this.radius <= 0 || this.y + this.radius >= canvas.height) {
        this.dy *= -1;
        return;
    }
    //bounce off of other balls
    for (var i = 0; i < balls.length; i++) {
        var checkball = balls[i];
        if (checkball != this) {
            if (isXWithinTheBall(checkball.x + checkball.radius, this)) {
                //this.bouncedx = true;
                this.dx *= -1;
            }
            if (isYWithinTheBall(checkball.y + checkball.radius, this)) {
                //this.bouncedy = true;
                this.dy *= -1;
            }
        }
    }
  }

  function isXWithinTheBall(x, ball) {
        return (x > ball.x - ball.radius) && 
                (x <= ball.x + ball.radius)    

  }

  function isYWithinTheBall(y, ball) {
        return (y > ball.y - ball.radius) && 
                (y <= ball.y + ball.radius)
  }
//TODO not doing anything yet
   function clickBall(e) {
        var posx = 0;
        var posy = 0;
        if (!e) var e = window.event;
        if (e.pageX || e.pageY)     {
            posx = e.pageX;
            posy = e.pageY;
         }
        else if (e.clientX || e.clientY)    {
            posx = e.clientX + document.body.scrollLeft
                + document.documentElement.scrollLeft;
            posy = e.clientY + document.body.scrollTop
                + document.documentElement.scrollTop;

        posx -= gCanvasElement.offsetLeft;
        posy -= gCanvasElement.offsetTop;
    }
    // posx and posy contain the mouse position relative to the document
    // Do something with this information
        alert(posx);
    }

    function getClickedBall(x, y) {
        for(var i = 0; i < balls.length; i++) {

        }

    }

    Ball.prototype.Create = function ()
    {
        var grd = context.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.radius)
        grd.addColorStop(1, this.color);
        grd.addColorStop(0, "#DBF2FF");

        context.save();
    
        //context.scale(widthScale, heightScale);
        context.beginPath();
        context.arc(this.x, this.y, this.radius, 0, 2 * Math.PI, false);
        context.fillStyle = grd;
        context.fill();
        context.lineWidth = 2;
        context.strokeStyle = "FFF5EE";
        context.stroke();
        context.restore();
        this.highlight.Create();
    }

  function Highlight(x, y, ball)
  {
    this.color = '#DBF2FF';
    this.x = x;
    this.y = y;
    this.radius = 6;
    this.ball = ball;
  }


     Highlight.prototype.Create = function ()
  {
    var grd = context.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.radius)
    grd.addColorStop(1, this.ball.color);
    grd.addColorStop(.4, this.color);

    context.beginPath();
    context.save();
    //context.scale(widthScale, heightScale);
    context.arc(this.x, this.y, this.radius, 0, 2 * Math.PI, false);
    context.fillStyle = grd;
    context.fill();
    context.restore();
   }


function animate(balls){
    if (isAnimating) { // Only draw if we are drawing
        animateRunning = true;
        //try {
            if (requiresRedraw) {
                requiresRedraw = false;
                //TODO:
                //renderStatic();
            }

            // clear
             context.clearRect(0, 0, canvas.width, canvas.height);

            //ball animations
            for(var i = 0; i < balls.length; i++) {
                var ball = balls[i];
                ball.x -= ball.dx;
                ball.y -= ball.dy;
                ball.highlight.x -= ball.dx;
                ball.highlight.y -= ball.dy;
                ball.Create();
                ball.Bounce();

                /**if (ball.bouncedx) {
                    ball.bouncedx = false;
                    ball.dx /= bouceFactor;
                }
                if (ball.bouncedy) {
                    ball.bouncedy = false;
                    ball.dy /= bouceFactor;
                }**/
            }
        /**} catch (e) {
            if (window.console && window.console.log) {
               window.console.log(e); // for debugging
           }
        }**/
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
    canvas.addEventListener('click', clickBall, false);
    startY = canvas.height/2;

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

    var xfactor = ((canvas.width - 30) / numBalls);
    for (var i = 0; i < numBalls; i++) {
        DX= (-DX);
        DY= (-DY);
        balls[i] = new Ball(colors[i], 30, DX, DY, (xfactor* (i + 1)), startY);
    }
};