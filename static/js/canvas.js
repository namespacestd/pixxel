
// Adapted from:
// http://codetheory.in/html5-canvas-drawing-lines-with-smooth-edges/

$(document).ready(function() {

    var canvas = document.querySelector('#paint');
    var ctx = canvas.getContext('2d');
    
    var sketch = document.querySelector('#sketch');
    var sketch_style = getComputedStyle(sketch);
    canvas.width = parseInt(sketch_style.getPropertyValue('width'));
    canvas.height = parseInt(sketch_style.getPropertyValue('height'));
    
    
    // Creating a tmp canvas
    var tmp_canvas = document.createElement('canvas');
    var tmp_ctx = tmp_canvas.getContext('2d');
    tmp_canvas.id = 'tmp_canvas';
    tmp_canvas.width = canvas.width;
    tmp_canvas.height = canvas.height;
    
    sketch.appendChild(tmp_canvas);

    var mouse = {x: 0, y: 0};
    var last_mouse = {x: 0, y: 0};
    
    // Pencil Points
    var ppts = [];
    
    /* Mouse Capturing Work */
    tmp_canvas.addEventListener('mousemove', function(e) {
        mouse.x = typeof e.offsetX !== 'undefined' ? e.offsetX : e.layerX;
        mouse.y = typeof e.offsetY !== 'undefined' ? e.offsetY : e.layerY;
    }, false);
    
    h = parseInt(document.getElementById("paint").getAttribute("height"));
    w = parseInt(document.getElementById("paint").getAttribute("width"));
    ctx.fillStyle = "#eeeeee";
    ctx.fillRect(0,0,w,h);

    /* Drawing on Paint App */
    tmp_ctx.lineWidth = 5;
    tmp_ctx.lineJoin = 'round';
    tmp_ctx.lineCap = 'round';
    tmp_ctx.strokeStyle = 'blue';
    tmp_ctx.fillStyle = 'blue';
    
    tmp_canvas.addEventListener('mousedown', function(e) {
        document.onselectstart = function() { return false; } // disable drag-select
        document.onmousedown = function() { return false; } // disable drag-select
        tmp_canvas.addEventListener('mousemove', onPaint, false);
        
        mouse.x = typeof e.offsetX !== 'undefined' ? e.offsetX : e.layerX;
        mouse.y = typeof e.offsetY !== 'undefined' ? e.offsetY : e.layerY;
        
        ppts.push({x: mouse.x, y: mouse.y});
        
        onPaint();
    }, false);
    
    tmp_canvas.addEventListener('mouseup', function() {
        tmp_canvas.removeEventListener('mousemove', onPaint, false);
        
        // Writing down to real canvas now
        ctx.drawImage(tmp_canvas, 0, 0);
        // Clearing tmp canvas
        tmp_ctx.clearRect(0, 0, tmp_canvas.width, tmp_canvas.height);
        
        // Emptying up Pencil Points
        ppts = [];
    }, false);
    
    var onPaint = function() {
        
        // Saving all the points in an array
        ppts.push({x: mouse.x, y: mouse.y});
        
        if (ppts.length < 4) {
            var b = ppts[0];
            tmp_ctx.beginPath();
            tmp_ctx.arc(b.x, b.y, tmp_ctx.lineWidth / 2, 0, Math.PI * 2, !0);
            tmp_ctx.fill();
            tmp_ctx.closePath();
        }
        else {
            // Tmp canvas is always cleared up before drawing.
            tmp_ctx.clearRect(0, 0, tmp_canvas.width, tmp_canvas.height);
            
            tmp_ctx.beginPath();
            tmp_ctx.moveTo(ppts[0].x, ppts[0].y);
            
            for (var i = 1; i < ppts.length - 2; i++) {
                var c = (ppts[i].x + ppts[i + 1].x) / 2;
                var d = (ppts[i].y + ppts[i + 1].y) / 2;
                
                tmp_ctx.quadraticCurveTo(ppts[i].x, ppts[i].y, c, d);
            }
            
            // For the last 2 points
            tmp_ctx.quadraticCurveTo(
                ppts[i].x,
                ppts[i].y,
                ppts[i + 1].x,
                ppts[i + 1].y
            );
            tmp_ctx.stroke();
        }
    };

    $('#thickness').slider({
        change: function(e,ui) {
            tmp_ctx.lineWidth = ui.value;
        },
        value: 3,
        min: 1.5,
        max: 20,
        step: 0.5
    });

    $('#opacity').slider({
        change: function(e,ui) {
            tmp_ctx.globalAlpha = ui.value;
        },
        value: 0.95,
        min: 0.05,
        max: 1,
        step: 0.05
    });

    $('#submit-drawing-form').submit(function(e) {
        var dataURL = canvas.toDataURL();
        $('#image_data').val(dataURL);
    });
    
    $('#red').click(function() {
        tmp_ctx.strokeStyle = 'red';
        tmp_ctx.fillStyle = 'red';
    });
    $('#blue').click(function() {
        tmp_ctx.strokeStyle = 'blue';
        tmp_ctx.fillStyle = 'blue';
    });
    
    $('#clear').click(function() {
        ctx.clearRect(0, 0, tmp_canvas.width, tmp_canvas.height);
    });
});