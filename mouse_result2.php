<?php
session_start();
require('dbconnect.php');

//ログイン状態をチェック
if (isset($_SESSION['user_id']) && ($_SESSION['time'] + 3600 > time())) {
  $_SESSION['time'] = time();
  // ユーザー情報
  $members=$db->prepare('SELECT * FROM Users WHERE user_id=?');
  $members->execute(array($_SESSION['user_id']));
  $member=$members->fetch();
  //アンケート情報
  $questionnaires=$db->prepare('SELECT * FROM Questionnaires WHERE questionnaire_id=?');
  $questionnaires->execute(array($questionnaire_id));
  $questionnaire=$questionnaires->fetch();
  //質問情報
  $questions=$db->prepare('SELECT * FROM Questions WHERE questionnaire_id=?');
  $questions->execute(array($questionnaire_id));
  $question=$questions->fetch();

  } else {
    header('Location: login.php/?action=mouse_result2');
  exit();
}

if($_SESSION['user_id'] != 1){
  echo "<h1>permission denied</h1>";
  echo "<h3>お使いのアカウントにページへのアクセス権限がありません </h3>";
  exit();
}


$questionnaire_id = 1;
$answer_id = $_GET["answer_id"];

//回答
$answers_pre=$db->prepare('SELECT * FROM Answers WHERE answer_id=?');
$answers_pre->execute(array($answer_id));
$answers=$answers_pre->fetchAll();
//回答データ
$answerdata_pre=$db->prepare('SELECT * FROM AnswerData WHERE answer_id=?');
$answerdata_pre->execute(array($answer_id));
$answerdata=$answers_pre->fetch();
//アンケート情報
$questionnaires=$db->prepare('SELECT * FROM Questionnaires WHERE questionnaire_id=?');
$questionnaires->execute(array($questionnaire_id));
$questionnaire=$questionnaires->fetch();
//質問情報
$questions_pre=$db->prepare('SELECT * FROM Questions WHERE questionnaire_id=?');
$questions_pre->execute(array($questionnaire_id));
$questions=$questions_pre->fetchAll();
?>


<!DOCTYPE html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>マウス動作ログ確認ページ</title>
        <!-- BootstrapのCSS読み込み -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
        <link href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.8/css/all.css">      
        <meta name="viewport" content="width=device-width, initial-scale=1.5", user-scalable=yes>
        <div style = "width:600px;height:0px;"></div>

        <style>
            .bg-ddd {
                background-size: 40px;
                background-color:rgba(120,170,140);
            }
            .box1 {
                background-color: rgba(50,255,50,.1);
            }
            .canvas-wrapper {
                position: relative;
                z-index:1;
            }
            .canvas-wrapper canvas {
                position: absolute;
                top: 0;
                left: 0;
                z-index:1;
            }
        </style>
    </head>



    <!-- canvas作成 -->
    <div class="canvas-wrapper">
        <canvas id="canvas" width="1920" height="10000">canvas要素をサポートしていません。</canvas>
    </div>
    

    <!-- 座標をjavascriptに渡す -->
    <?php
        $coordinates=$answerdata["coordinates"];
    ?>
    
    <script type="text/javascript">
        var coordinates=JSON.parse('<?php echo $coordinates; ?>');//jsonをparseしてJavaScriptの変数に代入
    </script>

    <!-- 外部ファイル読込 -->
    <script type="text/javascript" src="/survey/mouse_movement.js"></script>




  <!-- ここからアンケート -->

  <body class="text-center box1" >
    <div class="card mx-auto"style="width: 40%;top:150px">
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
                  <li style="font-size:14pt"><b><?php echo "Q" . $q_number; ?></b></li>
                  <label class="control-label" style="font-size:14pt"><?php echo $question['title'] ?></label></br>
                  <?php if($question["qtype"] == "radio"){?>
                    <a><?php $items = explode(",", $question['items']); 
                    foreach($items as $item => $i){
                      echo '<label for="' . $items[$item] .'"><input type="radio" name="'. $question['question_id']. '" value="' .$item . '" id="' . $items[$item] . '">' . $i . '</label>' . "<br />";
                    }
                  ?>
                  </a>
                  <?php }elseif($question["qtype"] == "text"){?>
                    <div class="form-group text-left">
                      <td style="position:relative">
                        <input type="text" style="width:80%; box-sizing:border-box" name= <?php echo '"' . $question['question_id'] . '"'?>>
                      </td>
                    </div>
                  <?php }?>
                  <br />
                  <?php $q_number++;
                } ?>
              </div>
              <div class="form-group text-left">
                <li> <label class="control-label6">当アンケートへのご意見をお書きください</label></li>
                <td style="position:relative">
                  <input type="text" style="width:80%; box-sizing:border-box">
                </td>
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
      <div style = "width:600px;height:3000px;"></div>
      
    </div>  
  </body>

  <!-- ここまでアンケート -->
</html>
