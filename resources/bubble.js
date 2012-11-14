//TODO each ball property
//TODO convert song to ogg file

var isAnimating = false;    // Is animation on or off?
var animateRunning = false; // Are we in the animation loop?
var requiresRedraw = true;

//TODO array of balls
var ball;

var x=200;
var y=200;

var DX=1;
var DY=1;

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
    if (!animateRunning) animate(ball); // Only draw if we are not already drawing
}

  function Ball(color, radius, dx, dy)
  {
    this.radius  = radius;
    this.x = x;
    this.y  = y;
    this.dx  = dx;
    this.dy  = dy;
    this.color   = color;
    this.highlight = new Highlight(x-30, y-30, this);
  }

    //TODO: hacked to get a correct(ish) border location on the left and bottom
    //changes with ball state and potentially canvas size. Cant figure out how to 
    //do this correctly.
    Ball.prototype.Bounce = function (widthScale, heightScale)
  {   
    if (this.x  >= canvas.width*2.3 || this.x - this.radius <= 0) this.dx *= -1;
    if (this.y - this.radius <= 0 || this.y >= canvas.height*2.3) this.dy *= -1;
  }

    Ball.prototype.Create = function (widthScale, heightScale)
    {
    var grd = context.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.radius)
    grd.addColorStop(1, this.color);
    grd.addColorStop(0, "#DBF2FF");

    context.save();
    
    context.scale(widthScale, heightScale);
    context.beginPath();
    context.arc(this.x, this.y, this.radius, 0, 2 * Math.PI, false);
    context.fillStyle = grd;
    context.fill();
    context.lineWidth = 2;
    context.strokeStyle = "FFF5EE";
    context.stroke();
    context.restore();
    this.highlight.Create(widthScale, heightScale);
    }

  function Highlight(x, y, ball)
  {
    this.color = '#DBF2FF';
    this.x = x;
    this.y = y;
    this.radius = 12;
    this.ball = ball;
  }


     Highlight.prototype.Create = function (widthScale, heightScale)
  {
    var grd = context.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.radius)
    grd.addColorStop(1, this.ball.color);
    grd.addColorStop(.4, this.color);

    context.beginPath();
    context.save();
    context.scale(widthScale, heightScale);
    context.arc(this.x, this.y, this.radius, 0, 2 * Math.PI, false);
    context.fillStyle = grd;
    context.fill();
    context.restore();
   }


 //TODO change to ball[]
function animate(ball){
    if (isAnimating) { // Only draw if we are drawing
        animateRunning = true;
        try {
            if (requiresRedraw) {
                requiresRedraw = false;
                renderStatic();
            }
            var date = new Date();
            var time = date.getTime();
 
            // update
             var widthScale = Math.sin(time / 250) * .02 + 0.4;
             var heightScale = -1 * Math.sin(time / 250) * .02 + 0.4;

            // clear
             context.clearRect(0, 0, canvas.width, canvas.height);

            //ball animations
            ball.x -= ball.dx;
            ball.y -= ball.dy;
            ball.highlight.x -= ball.dx;
            ball.highlight.y -= ball.dy;
            ball.Create(widthScale, heightScale);
            ball.Bounce(widthScale, heightScale);
        } catch (e) {
            if (window.console && window.console.log)
                window.console.log(e); // for debugging
        }
    }
 
    // request new frame
    requestAnimFrame(function(){
        animate(ball);
        animateRunning = false;
    });
}

 
window.onload = function(){
    canvas = document.getElementById("myCanvas");
    context = canvas.getContext('2d');
    ball = new Ball("#8ED6FF", 65, DX, DY);
};