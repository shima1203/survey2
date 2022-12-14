function draw(coordinates){
  const canvas = newWindow.document.getElementById("canvas");
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
  newWindow.resizeTo(window_x, window_y);
}

let newWindow = open('result_mouse_new.php', '_blank', 'width=600,height=400');
if( newWindow ) {
  console.log('正常に開きました');
}
else {
  console.log('正常に開けませんでした！');
  newWindow.close();
}
newWindow.onload =console.log("loaded"); 
newWindow.document.addEventListener('load', function() {
  console.log("loaded");
  draw(coordinates);
  resize(windowsize);
});




