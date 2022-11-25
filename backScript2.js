const startTime = performance.now();   //計測開始

// スクロール位置
function DocumentGetScrollPosition(document_obj){
    return{
        x:document_obj.body.scrollLeft || document_obj.documentElement.scrollLeft,
        y:document_obj.body.scrollTop  || document_obj.documentElement.scrollTop
    };
}
var scroll_list = [];
function ScrollFunc(){
    // スクロール位置を取得
    var scroll_pos = DocumentGetScrollPosition(document);

    // スクロール位置を加算して、グローバル座標系に変換する
    var scroll_x = scroll_pos.x;
    var scroll_y = scroll_pos.y;

    //時間の計測
    var t = performance.now();
    var tr = t - startTime;
    tr = parseInt(tr);

    var scroll={"x" : scroll_x, 
                "y" : scroll_y,
                "time" : tr};

    scroll_list.push(scroll);
    console.log('"scroll"   ', scroll);
}
// イベントのリッスンを開始する
if(document.addEventListener){
    // マウスを移動するたびに実行されるイベント
    document.addEventListener("scroll" , ScrollFunc);
// アタッチイベントに対応している
}else if(document.attachEvent){
    // マウスを移動するたびに実行されるイベント
    document.attachEvent("onscroll" , ScrollFunc);
}


var distance = 0;
var coordinates = [];
// マウス移動
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
    console.log('"coordinate"   ', coordinate);
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


//ウィンドウサイズ変更
var window_x = window.innerWidth;
var window_y = window.innerHeight;
var screen_x = screen.availWidth;
var screen_y = screen.availHeight;
var windowsize_list = [];
windowsize_list.push({"x" : window_x, "y" : window_y, "time" : 0})
function resizeWindow(){
    window_x = window.innerWidth;
    window_y = window.innerHeight;

    //時間の計測
    var t = performance.now();
    var tr = t - startTime;
    tr = parseInt(tr);

    var windowsize={"x" : window_x,
                    "y" : window_y,
                    "time" : tr
    };
    windowsize_list.push(windowsize);
    console.log('"windowsize"   ' , windowsize);
}
window.onresize = resizeWindow;


//バックグラウンド移動(時間)
//画面外への移動(出た時間と戻ってきた時間)



//選択(ラジオボタン)   (質問ごとにやるならquerySelectorをnullになるまでforで回す)
window.addEventListener('load', function() {
    let radio_btns = document.querySelectorAll(`input[type='radio']`);

    for (let target of radio_btns) {
        target.addEventListener(`change`, function () {
            //時間の計測
            var t = performance.now();
            var tr = t - startTime;
            tr = parseInt(tr);

            var check_radio={"question_id" : target.name,
                            "answer" : target.value,
                            "answer_value" : target.id,
                            "time" : tr
            };
            console.log("checked   ", check_radio, " flag:", target.checked);
        });
    }
})


//選択(チェックボックス)
window.addEventListener('load', function() {
    let check_boxes = document.querySelectorAll(`input[type='checkbox']`);

    for (let target of check_boxes) {
        target.addEventListener(`change`, function () {
            //時間の計測
            var t = performance.now();
            var tr = t - startTime;
            tr = parseInt(tr);

            var check_checkbox={"question_id" : target.name,
                                "answer" : target.value,
                                "answer_value" : target.id,
                                "time" : tr
            };
            console.log("checked   ", check_checkbox, " flag:", target.checked);
        });
    }
})


//選択(テキストボックス)
window.addEventListener('load', function() {
    let text_boxes = document.querySelectorAll(`input[type='text']`);

    for (let target of text_boxes) {
        target.addEventListener(`change`, function () {
            //時間の計測
            var t = performance.now();
            var tr = t - startTime;
            tr = parseInt(tr);

            var check_textbox={"question_id" : target.name,
                                "time" : tr
            };
            console.log("checked   ", check_textbox, " flag:", target.checked);
        });
    }
})

//タイピング





//送信
function modifysubmit(event){
    const coordinates_send = document.createElement('input');
    const windowsize_send = document.createElement('input');

    coordinates_send.name = "coordinates";
    windowsize_send.name = "windowsize";

    coordinates_send.type = "hidden";
    windowsize_send.type = "hidden";

    coordinates_send.value = JSON.stringify(coordinates);
    windowsize_send.value =  JSON.stringify(windowsize_list);

    event.target.appendChild(coordinates_send);
    event.target.appendChild(windowsize_send);
}