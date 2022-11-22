<?php
session_start();
require('dbconnect.php');
//ログイン状態をチェック
if (isset($_SESSION['user_id']) && ($_SESSION['time'] + 3600 > time())) {
    $_SESSION['time'] = time();
    // ユーザー情報
    $members=$db->prepare('SELECT * FROM Users WHERE user_id=?');
    $members->execute(array($_SESSION['user_id']));
    $member=$members->fetchAll();
    //アンケート情報
    $questionnaire_pre=$db->prepare('SELECT * FROM Questionnaires');
    $questionnaire_pre->execute();
    $questionnaires=$questionnaire_pre->fetchAll();
    
    } else {
    header('Location: login.php/?action=create_questionnaire');
    exit();
}

if($_SESSION['user_id'] != 1){
    echo "<!DOCTYPE html>";
    echo "<h1>permission denied</h1>";
    echo "<h3>お使いのアカウントにページへのアクセス権限がありません </h3>";
    echo "</html>";
    exit();
}

//DBに追加
if (!empty($_POST)){
    //DBにINSERT
    $questionnaire_id = $_POST["questionnaire_id"];
    $message=$db->prepare('INSERT INTO Questions SET questionnaire_id=?, title=?, qtype=?, items=?');
    $message->execute(array($questionnaire_id, $_POST["title"], $_POST["qtype"], $_POST["items"]));
    header('Location: /survey/create_questionnaire.php');
    exit();
}

?>


<!DOCTYPE html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>しましまアンケート作成ページ</title>
        <!-- BootstrapのCSS読み込み -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
        <link href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.8/css/all.css">      
        <meta name="viewport" content="width=device-width, initial-scale=1.5", user-scalable=yes>
        <div style = "width:600px;height:50px;"></div>

        <style>
            .bg-ddd {
            background-size: 40px;
            background-color:rgba(120,170,140);
            }
            .content_bg_red{
            position: absolute;
            width: calc(90%);
            height: 50%;
            background-color: rgba(50,255,50,.1);
            top: 0;
            right: 0;
            z-index: 2;
            }
            #wrap{
            background: #999
            }
            .box1 {
            margin: 10%;
            background-color: rgba(50,255,50,.1);
            }
        </style>
    </head>

    <body class=content_bg_red>
        <form action='' method="post">
            <div class="form-group">
                <li> 
                    <label class="control-label">アンケートID</label>
                </li>
                <p> 
                    <select name="questionnaire_id" required> 
                        <option value="">選択してください</option>
                        <?php if(isset($questionnaires["questionnaire_id"])){
                            echo "<option>" . $questionnaires["questionnaire_id"] . "</option>";
                        }else{
                            foreach($questionnaires as $q){
                                echo "<option>" . $q["questionnaire_id"] . "</option>";
                            }
                        }?>
                    </select>
                </p>
            </div>
            <div>
                <li> 
                    <label class="control-label">タイトル</label>
                </li>
                <textarea name="title" cols='80' rows='1'><?php echo htmlspecialchars($message??"", ENT_QUOTES); ?></textarea>
                
                <li> 
                    <label class="control-label">選択肢</label>
                </li>
                <textarea name="items" cols='80' rows='1'><?php echo htmlspecialchars($message??"", ENT_QUOTES); ?></textarea>

                <li> 
                    <label class="control-label">タイプ</label>
                </li>
                <div class="form-group text-left">
                    <label><input type="radio" name="qtype" value="radio">radio</label>
                    <br />
                    <label><input type="radio" name="qtype" value="checkbox">checkbox</label>
                    <br />
                    <label><input type="radio" name="qtype" value="text">text</label>
                    <br />
                    <label><input type="radio" name="qtype" value="number">number</label>
                    <br />
                    <label><input type="radio" name="qtype" value="data">data</label>
                    <br />
                    <label><input type="radio" name="qtype" value="file">file</label>
                </div>
            </div>
            <?php $something; ?>
            <div><input type="submit" item="送信する" class="btn btn-outline-primary my-1"></div>
        </form>
        <a href="logout.php" style="position:absolute; top:1; right:0;">logout</a>
    </body>
</html>