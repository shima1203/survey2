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
        console.log(x,y);
        setTimeout(drawLine, time, x, y, context);
      }
    }
};

function drawLine(x,y,context){
  context.lineTo(x,y);
  context.moveTo(x,y);
  context.closePath();
  context.stroke();
}

draw(coordinates);