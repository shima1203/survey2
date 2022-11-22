const startTime = performance.now();   //計測開始

// スクロール位置を取得する関数
function DocumentGetScrollPosition(document_obj){
    return{
        x:document_obj.body.scrollLeft || document_obj.documentElement.scrollLeft,
        y:document_obj.body.scrollTop  || document_obj.documentElement.scrollTop
    };
}

var distance = 0;
var coordinates = [];
// マウスを移動するたびに実行される関数
function MouseMoveFunc(e){
    // クライアント座標系を基点としたマウスカーソルの座標を取得
    var mouse_x = e.clientX;
    var mouse_y = e.clientY;

    // スクロール位置を取得
    var scroll_pos = DocumentGetScrollPosition(document);

    // スクロール位置を加算して、グローバル座標系に変換する
    mouse_x += scroll_pos.x;
    mouse_y += scroll_pos.y;
    distance += 1;

    //時間の計測
    var t = performance.now();
    var tr = t - startTime;
    tr = parseInt(tr);

    var coordinate={"x" : mouse_x, 
                    "y" : mouse_y,
                    "time" : tr};

    coordinates.push(coordinate);
    console.log(coordinate);
}


// イベントのリッスンを開始する
if(document.addEventListener){
    // マウスを移動するたびに実行されるイベント
    document.addEventListener("mousemove" , MouseMoveFunc);
// アタッチイベントに対応している
}else if(document.attachEvent){
    // マウスを移動するたびに実行されるイベント
    document.attachEvent("onmousemove" , MouseMoveFunc);
}
//setInterval(MouseMoveFunc, 100);    <-なぜか動かない



//送信
function modifysubmit(event){
    const coordinates_send = document.createElement('input');

    coordinates_send.name = "coordinates";

    coordinates_send.type = "hidden";

    coordinates_send.value = JSON.stringify(coordinates);


    event.target.appendChild(coordinates_send);
}