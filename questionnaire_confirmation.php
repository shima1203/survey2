<?php
session_start();
require('dbconnect.php');

//ユーザーエージェントの判定
$user_device = '';
// HTTP リクエストヘッダーが持っているユーザーエージェントの文字列を取得
$useragent = $_SERVER['HTTP_USER_AGENT'];
if((strpos($useragent, 'Android') !== false) &&
    (strpos($useragent, 'Mobile') !== false) ||
    (strpos($useragent, 'iPhone') !== false) ||
    (strpos($useragent, 'iPad') !== false) ||
    (strpos($useragent, 'Windows Phone') !== false)){
    // スマホからアクセスしている場合
    $user_device = 'smartphone';
}elseif((strpos($useragent, 'DoCoMo') !== false) ||
    (strpos($useragent, 'KDDI') !== false) ||
    (strpos($useragent, 'SoftBank') !== false) ||
    (strpos($useragent, 'Vodafone') !== false) ||
    (strpos($useragent, 'J-PHONE') !== false)){
    // ガラケーからアクセスしている場合
    $user_device = 'phone';
}else{
    // パソコンからアクセスしている場合
    $user_device = 'pc';
}
?>

<!DOCTYPE html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>しましまアンケート</title>
        <!-- BootstrapのCSS読み込み -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
        <link href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.8/css/all.css">      
        <meta name="viewport" content="width=device-width, initial-scale=1.0", user-scalable=yes>
        <div style = "width:600px;height:0px;"></div>
        <link rel="icon" sizes="16x16" href="/favicon.ico" />

        <style>
        .bg-ddd {
            background-size: 40px;
            background-color:rgba(120,170,140);
        }
        .box1 {
        background-color: rgba(50,255,50,.1);
        }
        li {
        margin-left: 0em;
        text-indent: 0em;
        font-size:14pt;
        }
        .smartphonesize {
        width : 80vw;
        top : 10vh;
        }
        </style>
    </head>
    



<!-- ここからアンケート -->

    <body class="text-center box1" >
        <?php
        if($user_device == 'smartphone' || $user_device == 'phone'){
            echo '<div class="card mx-auto smartphonesize">';
        }else{
            echo '<div class="card mx-auto"style="width: 750px;top:150px">';
        }
        ?>
        <div class="card-header" style="background-color: rgba(120,170,140);font-size:20px">
            <?php
            if($user_device == 'smartphone' || $user_device == 'phone'){
                echo '<h1 class="text-white bg-ddd h-30">しましま<br>アンケート</h1>';
            }else{
                echo '<h1 class="text-white bg-ddd h-30">しましまアンケート</h1>';
            }
            ?>
        </div>
        <div class="card-header" style="background-color: rgba(100,100,100,.1);font-size:20px"></div>
            <article class="card-body">ご協力ありがとうございました</article>
        </div>
        <div style = "width:600px;height:200px;"></div>
        <div style = "width:600px;height:3000px;"></div>
        
        </div>  
    </body>

<!-- ここまでアンケート -->
</html>