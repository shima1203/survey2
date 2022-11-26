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
var coordinates_list = [];
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

    coordinates_list.push(coordinate);
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


//クリック
var click_list = [];
function MouseClickFunc(e){
    // クライアント座標系を基点としたマウスカーソルの座標を取得
    var click_x = e.clientX;
    var click_y = e.clientY;

    // スクロール位置を取得
    var scroll_pos = DocumentGetScrollPosition(document);

    // スクロール位置を加算して、グローバル座標系に変換する
    click_x += scroll_pos.x;
    click_y += scroll_pos.y;

    //時間の計測
    var t = performance.now();
    var tr = t - startTime;
    tr = parseInt(tr);

    var click ={"x" : click_x, 
                "y" : click_y,
                "time" : tr
            };

    click_list.push(click);
    console.log('"click"   ', click);
}
// イベントのリッスンを開始する
if(document.addEventListener){
    // マウスを移動するたびに実行されるイベント
    document.addEventListener("click" , MouseClickFunc);
// アタッチイベントに対応している
}else if(document.attachEvent){
    // マウスを移動するたびに実行されるイベント
    document.attachEvent("onclick" , MouseClickFunc);
}


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
var background_list = [];
//ページが隠れたか
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
        console.log("page visible");
    }
    if (document.visibilityState === 'hidden') {
        console.log("page hidden");
    }
})
//ページの外にフォーカスが移動したか
window.addEventListener("blur", () => {
    console.log("page blur");
});
window.addEventListener("focus", () => {
    console.log("page focus");
});
//画面外へ移動したか
document.addEventListener("mouseleave", ()=>{
    console.log("mouseleave");
})
window.addEventListener("mouseenter", ()=>{
    console.log("mouseenter");
})




//選択肢の範囲にカーソルがとどまっている時間(onMouseOverイベント)



//選択(ラジオボタン)   *質問ごとにやるならquerySelectorをnullになるまでforで回す
var check_list = [];            //選択は統一してやる？
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
        target.addEventListener(`focus`, function () {
            //時間の計測
            var t = performance.now();
            var tr = t - startTime;
            tr = parseInt(tr);

            var check_textbox= {"question_id" : target.name,
                                "action" : "focus",
                                "time" : tr
            };
            console.log("focus   ", check_textbox, " flag:", target.checked);
        });
        target.addEventListener(`blur`, function () {
            //時間の計測
            var t = performance.now();
            var tr = t - startTime;
            tr = parseInt(tr);

            var check_textbox= {"question_id" : target.name,
                                "action" : "blur",
                                "time" : tr
            };
            console.log("blur   ", check_textbox, " flag:", target.checked);
        });
    }
})


//タイピング
window.addEventListener('load', function() {
    let text_boxes = document.querySelectorAll(`input[type='text']`);

    for (let target of text_boxes) {
        target.addEventListener(`input`, function () {
            //時間の計測
            var t = performance.now();
            var tr = t - startTime;
            tr = parseInt(tr);

            var type = {"question_id" : target.name,
                        "time" : tr
            };
            console.log("typed   ", type, " flag:", target.checked);
        });
    }
})


//使用デバイス(トラックボール・マウスパッドなど)        *要実装




//送信
function modifysubmit(event){
    const coordinates_send = document.createElement('input');
    const windowsize_send = document.createElement('input');

    coordinates_send.name = "coordinates";
    windowsize_send.name = "windowsize";

    coordinates_send.type = "hidden";
    windowsize_send.type = "hidden";

    coordinates_send.value = JSON.stringify(coordinates_list);
    windowsize_send.value =  JSON.stringify(windowsize_list);

    event.target.appendChild(coordinates_send);
    event.target.appendChild(windowsize_send);
}