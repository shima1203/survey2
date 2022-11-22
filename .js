const startTime = performance.now();   //計測開始

// スクロール位置を取得する関数
function DocumentGetScrollPosition(document_obj){
    return{
        x:document_obj.body.scrollLeft || document_obj.documentElement.scrollLeft,
        y:document_obj.body.scrollTop  || document_obj.documentElement.scrollTop
    };
}

var distance = 0;
var mouse_x = 0;
var mouse_y = 0;
// マウスを移動するたびに実行される関数
function MouseMoveFunc(e){
    // クライアント座標系を基点としたマウスカーソルの座標を取得
    mouse_x = e.clientX;
    mouse_y = e.clientY;

    // スクロール位置を取得
    var scroll_pos = DocumentGetScrollPosition(document);

    // スクロール位置を加算して、グローバル座標系に変換する
    mouse_x += scroll_pos.x;
    mouse_y += scroll_pos.y;
    distance += 1;
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
setInterval(MouseMoveFunc, 100);


//マウス速度
var totalX= 0;
var totalY= 0;
var moveX= 0;
var moveY= 0;
var speed= 0;
var total= 0;
var speed_ave= 0;
var i= 0;
document.addEventListener("mousemove", function(ev){
    totalX += Math.abs(ev.movementX);
    totalY += Math.abs(ev.movementY);
    speed += Math.abs(ev.movementY) + Math.abs(ev.movementX);
    moveX += ev.movementX;
    moveY += ev.movementY;
}, false);
setInterval(function(){
    if(speed!=0){
        total += speed;
        i++;
    }
    speed_ave = total / i;
    console.log(`Speed : ${speed}px/s  Speed_ave : ${speed_ave}px/s`)
    moveX= moveY= totalX= totalY= speed= 0;
}, 100);


//スクロール速度
var scroll_amount = 0;
var scroll_total = 0;
var scroll_ave = 0;
var nowscroll = 0;
var rescroll = 0;
var j = 0;
setInterval(function(){
    nowscroll = DocumentGetScrollPosition(document);
    scroll_amount = Math.abs(nowscroll.y - rescroll);
    rescroll = nowscroll.y;
    if(scroll_amount != 0){
        scroll_total += scroll_amount;
        j++;
    }
    scroll_ave = scroll_total / j;
    console.log(`scrollSpeed : ${scroll_amount}px/s  scroll_ave : ${scroll_ave}px/s`)
    scroll_amount= 0;
}, 100);


//タイプ速度
var retypeTime = 0;
var nowtypeTime = 0;
var typeTime = 0;
var totaltypeTime = 0;
var avetypeTime = 0;
var k = 0
var l = 0;
window.addEventListener('DOMContentLoaded', function(){
    // input要素を取得
    var input_name = document.getElementById("message");
    // イベントリスナーでイベント「change」を登録
    input_name.addEventListener("change",function(){
        //   console.log("Change action");
        //   console.log(this.value);
        avetypeTime = totaltypeTime / k;
        console.log(avetypeTime);
        l = 0;
    });

    // イベントリスナーでイベント「input」を登録
    input_name.addEventListener("input",function(){
        //   console.log("Input action");
        //   console.log(this.value);
        if(l == 0){
            retypeTime = performance.now();
            l = 1;
        }else{
            nowtypeTime = performance.now();
            typeTime = nowtypeTime - retypeTime;
            totaltypeTime += typeTime;
            console.log(typeTime);
            retypeTime = performance.now();
            k++;
        }
    });
});





var pagehide = 0;
//バックグラウンド
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
        console.log("コンテンツが表示された");
    }
    if (document.visibilityState === 'hidden') {
        console.log("コンテンツがバックグラウンドになった");
    }
})
window.addEventListener("blur", () => {
    console.log("ページからフォーカスが外れた");
    pagehide ++;
});


//送信
function modifysubmit(event){
    const data1 = document.createElement('input');
    const data2 = document.createElement('input');
    const dis = document.createElement('input');
    const hide = document.createElement('input');
    const answerTime = document.createElement('input');
    const mouse_ave = document.createElement('input');
    const avescroll = document.createElement('input');
    const type_ave = document.createElement('input');
    const concentration = document.createElement('input');

    data1.name = "mouseX";
    data2.name = "mouseY";
    dis.name = "distance";
    hide.name = "pagehide";
    answerTime.name = "answerTime";
    mouse_ave.name = "mouse_ave";
    avescroll.name = "scroll_ave"
    type_ave.name = 'type_ave';
    concentration.name = "concentration";

    data1.type = "hidden";
    data2.type = "hidden";
    dis.type = "hidden";
    hide.type = "hidden";
    answerTime.type = "hidden";
    mouse_ave.type = "hidden";
    avescroll.type = "hidden";
    type_ave.type = 'hiddenn';
    concentration.type = "hidden";

    data1.value = mouse_x;
    data2.value = mouse_y;
    dis.value = distance;
    hide.value = pagehide;
    const endTime = performance.now();
    answerTime.value = endTime - startTime;
    mouse_ave.value = speed_ave;
    avescroll.value = scroll_ave;
    type_ave.value = avetypeTime;


    if(answerTime.value > 10000){
        concentration.value = 2;
    }else{
        concentration.value = 1;
    }

    event.target.appendChild(data1);
    event.target.appendChild(data2);
    event.target.appendChild(dis);
    event.target.appendChild(hide);
    event.target.appendChild(answerTime);
    event.target.appendChild(mouse_ave);
    event.target.appendChild(avescroll);
    event.target.appendChild(type_ave);
    event.target.appendChild(concentration);

}


//javascriptの変数をPHPに送る
