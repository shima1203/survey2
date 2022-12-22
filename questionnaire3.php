<?php
session_start();
require('dbconnect.php');
$questionnaire_id = 3;

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
            //header('Location: /survey/questionnaire3.php/?action=rewrite');
            //exit();
            $_POST[$question['question_id']] = " ";
        }

        //DBにINSERT
        $message1=$db->prepare('INSERT INTO Answers SET answer_id=?, questionnaire_id=?, question_id=?, answer=?, flag_delete=0, created_at=NOW()');
        $message1->execute(array($answer_id, $questionnaire_id, $question['question_id'], $answer));


    }    
    $message2=$db->prepare('INSERT INTO AnswerData SET answer_id=?, questionnaire_id=?, scroll=?, coordinates=?, click=?, windowsize=?, background=?, checking=?, type=?, enter_leave=?, total=?, device=?, created_at=NOW()');
    $message2->execute(array($answer_id, $questionnaire_id, $_POST["scroll"], $_POST["coordinates"], $_POST["click"], $_POST["windowsize"], $_POST["background"], $_POST["check"], $_POST["type"], $_POST["enter_leave"], $_POST["total"], $user_device));
    header('Location: /survey/questionnaire_confirmation.php');
    exit();
}

//スマホの場合
if($user_device == 'smartphone' || $user_device == 'phone'){
    //header('Location: /survey/questionnaire3.php');
    echo "このサイトはスマホ未対応です";
    exit();
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
            <div class="card-header" style="background-color: rgba(100,100,100,.1);font-size:20px">
                <?php echo $questionnaire['title'] ?><br><br>
                <ul style="text-align:left; font-size:15px">
                    <li style="font-size:15px">このアンケートは高専生活アンケートを模して作成したものです。実際の高専生活アンケートとは異なりますのでご注意ください</li>
                    <li style="font-size:15px">回答内容は外部に漏れることもありますし、秘密にされる保証はありませんので、知られたく内容を答えないようにお願いいたします</li>
                    <li style="font-size:15px">また、良くも悪くも回答内容は見ませんので、いじめ等に関して真面目に相談されても対応しかねます。ご了承ください</li>
                </ul>
                <p style="text-align:left; font-size:15px">
                    &lt;回答方法&gt;<br>
                    1回目:しっかり問題文を読んで”集中して”回答ください　この際、「集中」を最初に選択ください<br>
                    本当に思っていることを愚直に回答する必要はありませんが、実際のアンケートに答えているつもりで集中して回答ください<br>
                    2回目:問題文を読まず、選択肢も適当に回答ください　この際、「適当」を最初に選択ください<br><br>

                    ※回答時は全画面表示で、できる限りマウスを使用していただくようお願いいたします<br>
                    ※マウス以外のポインティングデバイスを使用される方は、最後の質問で使用したデバイスをお答えください<br><br>

                    計測項目：マウス座標/クリック座標/スクロール/ノード間のマウスの出入り/バックグラウンドへの移動/選択肢の選択・変更/タイプ/ウィンドウサイズ
        </p>
            </div>
                <article class="card-body">
                    <form action='' method="post" onsubmit = "modifysubmit(event)">
                        <div class="edit">
                            <div class="form-group text-left">
                                <?php $q_number = 1;
                                foreach($questions as $question){ ?>
                                <li style="word-break : break-all;" id=<?php echo'"'. $question['question_id'].'"' ?>><?php echo $question['title'] ?></li></br>
                                <div class="items">
                                <?php if($question["qtype"] == "radio"){?>
                                    <a><?php $items = explode(",", $question['items']); 
                                        foreach($items as $item => $i){
                                            echo '<label for="'. $question['question_id'].'.'. $items[$item] .'"><input type="radio" name="'. $question['question_id']. '" value="' .$item . '" id="'. $question['question_id'].'.'. $items[$item] . '">' . $i . '</label>' . "<br />";
                                        }
                                        echo '<label for="'. $question['question_id'].'.'. '-1.未選択' .'" style="display: none;"><input type="radio" name="'. $question['question_id']. '" value="' . '-1' . '" id="'. $question['question_id'].'.'. '-1.未選択' . '" checked="checked" style="display: none;">' . '未選択' . '</label>';
                                        ?>
                                    </a>
                                <?php }elseif($question["qtype"] == "text"){?>
                                    <div class="form-group text-left">
                                        <td style="position:relative">
                                            <label style="width:80%; box-sizing:border-box"><input type="text" style="width:80%; box-sizing:border-box" name= <?php echo '"' . $question['question_id'] . '"'?>></label>
                                        </td>
                                    </div>
                                <?php }?>
                                </div>
                                <br><br><br>
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