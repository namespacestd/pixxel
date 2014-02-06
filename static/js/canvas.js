var isDown, context, rect, points;

$(document).ready(function() {
    
    var canvas = document.getElementById('canvas');
    context = canvas.getContext('2d');

    canvas.width = 500;
    canvas.height = 400;

    context.fillStyle = "rgb(47,149,237)";
    context.strokeStyle = "rgb(47,149,237)";
    context.lineWidth = 3;
    rect = getCanvasRect(canvas);
    isDown = false;

    $('#canvas').mousedown(function(e) {
        points = new Array();
        var x = e.clientX;
        var y = e.clientY;
        document.onselectstart = function() { return false; } // disable drag-select
        document.onmousedown = function() { return false; } // disable drag-select
        isDown = true;
        x -= rect.x;
        y -= rect.y - getScrollY();
        points[0] = new Point(x, y);
        context.fillRect(x,y,3,3);
    });

    $('#canvas').mousemove(function(e) {
        var x = e.clientX;
        var y = e.clientY;
        if (isDown) {
            x -= rect.x;
            y -= rect.y - getScrollY();
            points[points.length] = new Point(x, y); // append
            drawConnectedPoint(points.length - 2, points.length - 1);
        }
    });

    $('#canvas').mouseup(function(e) {
        var x = e.clientX;
        var y = e.clientY;
        document.onselectstart = function() { return true; } // enable drag-select
        document.onmousedown = function() { return true; } // enable drag-select
        if(isDown) {
            isDown = false;
        }
    });

});

function getCanvasRect(canvas)
{
    var w = canvas.width;
    var h = canvas.height;

    var cx = canvas.offsetLeft;
    var cy = canvas.offsetTop;
    while (canvas.offsetParent != null)
    {
        canvas = canvas.offsetParent;
        cx += canvas.offsetLeft;
        cy += canvas.offsetTop;
    }
    return {x: cx, y: cy, width: w, height: h};
}

function getScrollY()
{
    var scrollY = 0;
    if (typeof(document.body.parentElement) != 'undefined')
    {
        scrollY = document.body.parentElement.scrollTop; // IE
    }
    else if (typeof(window.pageYOffset) != 'undefined')
    {
        scrollY = window.pageYOffset; // FF
    }
    return scrollY;
}

function drawConnectedPoint(from, to)
{
    context.beginPath();
    context.moveTo(points[from].X, points[from].Y);
    context.lineTo(points[to].X, points[to].Y);
    context.closePath();
    context.stroke();
}

function Point(x, y)
{
    this.X = x;
    this.Y = y;
}

function Rectangle(x, y, width, height)
{
    this.X = x;
    this.Y = y;
    this.Width = width;
    this.Height = height;
}