function draw_coordinates(coordinates,canvas){
    if (canvas.getContext) {
      const context = canvas.getContext("2d");//2次元描画

      context.beginPath();
      context.moveTo(coordinates[0]["x"],coordinates[0]["y"]);

      for(var i in coordinates){
        var x = coordinates[i]["x"];
        var y = coordinates[i]["y"];
        var time = coordinates[i]["time"];
        setTimeout(drawLine, time, x, y, context);
      }
    }
};

function draw_click(click,canvas){
    if (canvas.getContext) {
      const context = canvas.getContext("2d");//2次元描画

      context.beginPath();
      context.moveTo(click[0]["x"],click[0]["y"]);

      for(var i in click){
        var x = click[i]["x"];
        var y = click[i]["y"];
        var time = click[i]["time"];
        setTimeout(drawRec, time, x, y, context);
      }
    }
};

function resize(windowsize,window){
  for(var k in windowsize){
    var window_x = windowsize[k]["x"];
    var window_y = windowsize[k]["y"];
    var window_time = windowsize[k]["time"];
    setTimeout(resize_window , window_time, window_x, window_y, window);
  }
}



function drawLine(x,y,context){
  context.lineTo(x,y);
  context.moveTo(x,y);
  context.closePath();
  context.stroke();
}

function drawRec(x,y,context){
  context.rect(x-3, y-3, 6, 6);
  context.fill();
}

function resize_window(window_x, window_y,window){
  console.log(window_x, window_y);
  window.resizeTo(window_x, window_y);
}




let newWindow = open('result_mouse_new.php', '_blank', 'width=600,height=400');
const canvas = window.document.getElementById("canvas");
const canvas_new = newWindow.document.getElementById("canvas");
if( newWindow ) {
  console.log('正常に開きました');
}
else {
  console.log('正常に開けませんでした！');
  newWindow.close();
}

window.addEventListener('load', function() {
  console.log("loaded");
  draw_coordinates(coordinates,canvas);
  draw_click(click,canvas);
  resize(windowsize,window);
});
newWindow.addEventListener('load', function() {
  console.log("loaded");
  draw_coordinates(coordinates,canvas_new);
  draw_click(click,canvas_new);
  resize(windowsize,newWindow);
});



