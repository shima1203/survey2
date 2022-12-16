const startTime = performance.now();   //計測開始

var total = [];

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

    var scroll={"event" : "scroll",
                "x" : scroll_x, 
                "y" : scroll_y,
                "time" : tr};

    scroll_list.push(scroll);
    total.push(scroll);
    console.log(scroll);
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
    var client_x = e.clientX;
    var client_y = e.clientY;
    //ページ内の座標を取得
    var page_x = e.pageX;
    var page_y = e.pageY;

    // スクロール位置を取得
    var scroll_pos = DocumentGetScrollPosition(document);

    // スクロール位置を加算して、グローバル座標系に変換する
    client_x += scroll_pos.x;
    client_y += scroll_pos.y;
    distance += 1;

    //時間の計測
    var t = performance.now();
    var tr = t - startTime;
    tr = parseInt(tr);

    var coordinate={"event" : "mousemove",
                    "x" : client_x, 
                    "y" : client_y,
                    "time" : tr};

    coordinates_list.push(coordinate);
    total.push(coordinate);
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

    var click ={"event" : "click",
                "x" : click_x, 
                "y" : click_y,
                "time" : tr
            };

    click_list.push(click);
    total.push(click);
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
windowsize_list.push({"event" : "resizewindow", "x" : window_x, "y" : window_y, "time" : 0})
function resizeWindow(){
    window_x = window.innerWidth;
    window_y = window.innerHeight;

    //時間の計測
    var t = performance.now();
    var tr = t - startTime;
    tr = parseInt(tr);

    var windowsize={"event" : "resizewindow",
                    "x" : window_x,
                    "y" : window_y,
                    "time" : tr
    };
    windowsize_list.push(windowsize);
    total.push(windowsize);
    console.log('"windowsize"   ' , windowsize);
}
window.onresize = resizeWindow;


//バックグラウンド移動
var background_action_list = [];
function backgroundAction(action){
    //時間の計測
    var t = performance.now();
    var tr = t - startTime;
    tr = parseInt(tr);

    var background_action ={"event" : "movebackground",
                            "action" : action,
                            "time" : tr
    };

    background_action_list.push(background_action);
    total.push(background_action);
    console.log(background_action);
}
if(window.addEventListener){
    //ページが隠れたか
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') {
            var action = "page_visible";
            backgroundAction(action);
        }
        if (document.visibilityState === 'hidden') {
            var action = "page_hidden";
            backgroundAction(action);
        }
    })
    //ページの外にフォーカスが移動したか
    window.addEventListener("blur", () => {
        var action = "page_blur";
        backgroundAction(action);
    });
    window.addEventListener("focus", () => {
        var action = "page_focus";
        backgroundAction(action);
    });
    //画面外へ移動したか
    document.addEventListener("mouseleave", ()=>{
        var action = "mouse_leave";
        backgroundAction(action);
    })
    document.addEventListener("mouseenter", ()=>{
        var action = "mouse_enter";
        backgroundAction(action);
    })    
}


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

            var check_radio={"event" : "check",
                            "qtype" : "radio",
                            "question_id" : target.name,
                            "answer" : target.value,
                            "answer_value" : target.id,
                            "time" : tr
            };
            check_list.push(check_radio);
            total.push(check_radio);
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

            var check_checkbox={"event" : "check",
                                "qtype" : "check_box",
                                "question_id" : target.name,
                                "answer" : target.value,
                                "answer_value" : target.id,
                                "time" : tr
            };
            check_list.push(check_checkbox);
            total.push(check_checkbox);
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

            var check_textbox= {"event" : "check",
                                "qtype" : "text",
                                "question_id" : target.name,
                                "action" : "focus",
                                "time" : tr
            };
            check_list.push(check_textbox);
            total.push(check_textbox);
            console.log("focus   ", check_textbox, " flag:", target.checked);
        });
        target.addEventListener(`blur`, function () {
            //時間の計測
            var t = performance.now();
            var tr = t - startTime;
            tr = parseInt(tr);

            var check_textbox= {"event" : "check",
                                "qtype" : "text",
                                "question_id" : target.name,
                                "action" : "blur",
                                "time" : tr
            };
            check_list.push(check_textbox);
            total.push(check_textbox);
            console.log("blur   ", check_textbox, " flag:", target.checked);
        });
    }
})


//タイピング
var type_list = [];
window.addEventListener('load', function() {
    let text_boxes = document.querySelectorAll(`input[type='text']`);

    for (let target of text_boxes) {
        target.addEventListener(`input`, function () {
            //時間の計測
            var t = performance.now();
            var tr = t - startTime;
            tr = parseInt(tr);

            var type = {"event" : "type",
                        "question_id" : target.name,
                        "time" : tr
            };
            type_list.push(type);
            total.push(type);
            console.log("typed   ", type, " flag:", target.checked);
        });
    }
})


//選択肢の範囲にカーソルがとどまっている時間
var enter_leave_list = [];
window.addEventListener('load', function() {
    let questions = document.querySelectorAll(`li`);
    let items = document.querySelectorAll(`.items`);

    for (let target of questions) {
        target.addEventListener(`mouseenter`, function () {
            //時間の計測
            var t = performance.now();
            var tr = t - startTime;
            tr = parseInt(tr);

            var enter_question={"event" : "enter_leave",
                                "type" : "question",
                                "action" : "enter",
                                "question_id" : target.id,
                                "time" : tr
            };
            enter_leave_list.push(enter_question);
            total.push(enter_question);
            console.log("enter   ", enter_question);
        });
        target.addEventListener(`mouseleave`, function () {
            //時間の計測
            var t = performance.now();
            var tr = t - startTime;
            tr = parseInt(tr);

            var leave_question={"event" : "enter_leave",
                                "type" : "question",
                                "action" : "leave",
                                "question_id" : target.id,
                                "time" : tr
            };
            enter_leave_list.push(leave_question);
            total.push(leave_question);
            console.log("leave   ", leave_question);
        });
    }
    for (let target of items) {
        target.addEventListener(`mouseenter`, function () {
            //時間の計測
            var t = performance.now();
            var tr = t - startTime;
            tr = parseInt(tr);

            var enter_item={"event" : "enter_leave",
                            "type" : "item",
                            "action" : "enter",
                            "question_id" : target.name,
                            "time" : tr
            };
            enter_leave_list.push(enter_item);
            total.push(enter_item);
            console.log("enter   ", enter_item);
        });
        target.addEventListener(`mouseleave`, function () {
            //時間の計測
            var t = performance.now();
            var tr = t - startTime;
            tr = parseInt(tr);

            var leave_item={"event" : "enter_leave",
                            "type" : "item",
                            "action" : "leave",
                            "question_id" : target.name,
                            "time" : tr
            };
            enter_leave_list.push(leave_item);
            total.push(leave_item);
            console.log("leave   ", leave_item);
        });
    }
})


//使用デバイス(トラックボール・マウスパッドなど)        *要実装




//送信
function modifysubmit(event){
    const scroll_send = document.createElement('input');
    const coordinates_send = document.createElement('input');
    const click_send = document.createElement('input');
    const windowsize_send = document.createElement('input');
    const background_send = document.createElement('input');
    const check_send = document.createElement('input');
    const type_send = document.createElement('input');
    const enter_leave_send = document.createElement('input');
    const total_send = document.createElement('input');
    

    scroll_send.name = "scroll";
    coordinates_send.name = "coordinates";
    click_send.name = "click";
    windowsize_send.name = "windowsize";
    background_send.name = "background";
    check_send.name = "check";
    type_send.name = "type";
    enter_leave_send.name = "enter_leave";
    total_send.name = "total";

    scroll_send.type = "hidden";
    coordinates_send.type = "hidden";
    click_send.type = "hidden";
    windowsize_send.type = "hidden";
    background_send.type = "hidden";
    check_send.type = "hidden";
    type_send.type = "hidden";
    enter_leave_send.type = "hidden";
    total_send.type = "hidden";

    scroll_send.value = JSON.stringify(scroll_list);
    coordinates_send.value = JSON.stringify(coordinates_list);
    click_send.value = JSON.stringify(click_list);
    windowsize_send.value =  JSON.stringify(windowsize_list);
    background_send.value = JSON.stringify(background_action_list);
    check_send.value = JSON.stringify(check_list);
    type_send.value = JSON.stringify(type_list);
    enter_leave_send.value = JSON.stringify(enter_leave_list);
    total_send.value = JSON.stringify(total);


    event.target.appendChild(scroll_send);
    event.target.appendChild(coordinates_send);
    event.target.appendChild(click_send);
    event.target.appendChild(windowsize_send);
    event.target.appendChild(background_send);
    event.target.appendChild(check_send);
    event.target.appendChild(type_send);
    event.target.appendChild(enter_leave_send);
    event.target.appendChild(total_send);
}