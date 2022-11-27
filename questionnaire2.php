<?php
session_start();
require('dbconnect.php');
$questionnaire_id = 2;


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

//アンケート情報
$questionnaires=$db->prepare('SELECT * FROM Questionnaires WHERE questionnaire_id=?');
$questionnaires->execute(array($questionnaire_id));
$questionnaire=$questionnaires->fetch();
//質問情報
$questions_pre=$db->prepare('SELECT * FROM Questions WHERE questionnaire_id=?');
$questions_pre->execute(array($questionnaire_id));
$questions=$questions_pre->fetchAll();
//DBに追加
if (!empty($_POST)){
    //answer_idの作成
    require('uuid_v4_factory.php');
    $answer_id = UuidV4Factory::generate();

    foreach($questions as $question){
        //解答の取得
        $answer=$_POST[$question['question_id']];
        if($_POST[$question['question_id']] == null){
            header('Location: /survey/questionnaire2.php/?action=rewrite');
            exit();
        }

        //DBにINSERT
        $message=$db->prepare('INSERT INTO Answers SET answer_id=?, questionnaire_id=?, question_id=?, answer=?, coordinates=?, created_at=NOW()');
        $message->execute(array($answer_id, $questionnaire_id, $question['question_id'], $answer, $_POST["coordinates"]));
        
    }
        header('Location: /survey/questionnaire_confirmation.php');
        exit();
}

//スマホの場合
if($user_device == 'smartphone' || $user_device == 'phone'){
    header('Location: /survey/questionnaire2-sm.php');
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
        </style>
    </head>
    

    <!-- 外部ファイル読込 -->
    <script type="text/javascript" src="/survey/backScript2.js"></script>
    

<!-- ここからアンケート -->

    <body class="text-center box1" >
        <div class="card mx-auto"style="width: 750px;top:150px">
        <div class="card-header" style="background-color: rgba(120,170,140);font-size:20px">
            <h1 class="text-white bg-ddd h-30">しましまアンケート</h1>
        </div>
        <div class="card-header" style="background-color: rgba(100,100,100,.1);font-size:20px"><?php echo $questionnaire['title'] ?></div>
            <article class="card-body">
            <form action='' method="post" onsubmit = "modifysubmit(event)">
                <div class="edit">
                <div class="form-group text-left">
                    <?php $q_number = 1;
                    foreach($questions as $question){ ?>
                    <li style="word-break : break-all;"><?php echo $question['title'] ?></li></br>
                    <?php if($question["qtype"] == "radio"){?>
                        <a><?php $items = explode(",", $question['items']); 
                        foreach($items as $item => $i){
                        echo '<label for="' . $items[$item] .'"><input type="radio" name="'. $question['question_id']. '" value="' .$item . '" id="' . $items[$item] . '">' . $i . '</input></label>' . "<br />";
                        }
                    ?>
                    </a>
                    <?php }elseif($question["qtype"] == "text"){?>
                        <div class="form-group text-left">
                        <td style="position:relative">
                            <input type="text" style="width:80%; box-sizing:border-box" name= <?php echo '"' . $question['question_id'] . '"'?> value=" ">
                        </td>
                        </div>
                    <?php }?>
                    <br />
                    <?php $q_number++;
                    } ?>
                </div>
                
                <?php if($_GET['action'] == 'rewrite'){
                    ?><script>alert('アンケートの項目全てにお答えください')</script><?php
                } ?>
                </div>
                <div class="login2"><input type="submit" item="送信する" class="btn btn-outline-primary my-1">
            </form>
            </article>
        </div>
        <div style = "width:600px;height:200px;"></div>
        <div style = "text-align:center;">※アンケート回答中の動作等をデータとして収集させていただきます。ご了承ください。</div>
        <div style = "width:600px;height:50px;"></div>
        
        </div>  
    </body>

<!-- ここまでアンケート -->
</html>