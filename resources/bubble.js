//TODO each ball property
var x=200;
var y=200;

var DX=3;
var DY=3;

var canvas;
var context;

window.requestAnimFrame = (function(callback){
    return window.requestAnimationFrame ||
    window.webkitRequestAnimationFrame ||
    window.mozRequestAnimationFrame ||
    window.oRequestAnimationFrame ||
    window.msRequestAnimationFrame ||
    function(callback){
        window.setTimeout(callback, 1000 / 60);
    };
})();

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

    Ball.prototype.Bounce = function (widthScale, heightScale)
  {
    if (this.x*widthScale + this.radius*widthScale*1.29 >= canvas.width || this.x - this.radius <= 0) this.dx *= -1;
    if (this.y - this.radius <= 0 || this.y*heightScale + this.radius*heightScale*1.39 >= canvas.height) this.dy *= -1;
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
 
    // request new frame
    requestAnimFrame(function(){
        animate(ball);
    });
}

 
window.onload = function(){
    canvas = document.getElementById("myCanvas");
    context = canvas.getContext('2d');
    var ball = new Ball("#8ED6FF", 65, DX, DY);
    animate(ball);
};