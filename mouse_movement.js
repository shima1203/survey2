function draw(coordinates){
  const canvas = document.getElementById("canvas");
    if (canvas.getContext) {
      const context = canvas.getContext("2d");//2次元描画

      //background color
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

function resize(windowsize){
  for(var k in windowsize){
    var window_x = windowsize[k]["x"];
    var window_y = windowsize[k]["y"];
    var window_time = windowsize[k]["time"];
    setTimeout(resize_window , window_time, window_x, window_y);
  }
}

function drawLine(x,y,context){
  context.lineTo(x,y);
  context.moveTo(x,y);
  context.closePath();
  context.stroke();
}

function resize_window(window_x, window_y){
  console.log(window_x, window_y);
  window.resizeTo(window_x, window_y);
}



resize(windowsize);