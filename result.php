<?php
session_start();
require('dbconnect.php');

$questionnaire_id = 1;

//ログイン許可ユーザー
$user1 = array();
$user2 = array();
array_push($user1, ["0","ubuntu"],["1","shima"]);
array_push($user2, ["8","Rena0301"],["17","ponta"]);

//ログイン状態をチェック
if (isset($_SESSION['user_id']) && ($_SESSION['time'] + 3600 > time())) {
    $_SESSION['time'] = time();
    // ユーザー情報
    $members=$db->prepare('SELECT * FROM Users WHERE user_id=?');
    $members->execute(array($_SESSION['user_id']));
    $member=$members->fetch();
} else {
    header('Location: login.php/?action=result');
    exit();
}

//アンケート情報
$questionnaire_pre=$db->prepare('SELECT * FROM Questionnaires');
$questionnaire_pre->execute();
$questionnaires=$questionnaire_pre->fetchALL();
//回答情報
$answers_pre=$db->prepare('SELECT * FROM Answers WHERE questionnaire_id=? ORDER BY created_at, question_id');
$answers_pre->execute(array($questionnaire_id));
$answers=$answers_pre->fetchAll();
//アンケート情報
$questionnaire_pre=$db->prepare('SELECT * FROM Questionnaires WHERE questionnaire_id=?');
$questionnaire_pre->execute(array($questionnaire_id));
$questionnaire=$questionnaire_pre->fetchAll();
//質問情報
$questions_pre=$db->prepare('SELECT * FROM Questions WHERE questionnaire_id=?');
$questions_pre->execute(array($questionnaire_id));
$questions=$questions_pre->fetchAll();

//閲覧権限の確認
$ex1 = 0;
foreach($user1 as $user){
    if($user[0] == $member['user_id']){
        $ex1 = 1;
    }
}
$ex2 = 0;
foreach($user2 as $user){
    if($user[0] == $member['user_id']){
        $ex2 = 2;
        
    }
}
if($questionnaire_id == 1 && $ex1 == 0){
    echo "<!DOCTYPE html>";
    echo "<h1>permission denied</h1>";
    echo "<h3>お使いのアカウントにページへのアクセス権限がありません </h3>";
    echo "</html>";
    exit();
}
if($questionnaire_id == 2 && $ex2 == 0){
    echo "<!DOCTYPE html>";
    echo "<h1>permission denied</h1>";
    echo "<h3>お使いのアカウントにページへのアクセス権限がありません </h3>";
    echo "</html>";
    exit();
}
?>


<!DOCTYPE html>
<html lang="ja">
    <head>
        <title>アンケート結果</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
        <link href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.8/css/all.css">      
        <meta name="viewport" content="width=device-width, initial-scale=1.0", user-scalable=yes>
        <div style = "width:600px;height:0px;"></div>
        <link rel="icon" sizes="16x16" href="/favicon.ico" />
    </head>
    <body>
        <table border="1">
            <tr>
                <th>answer_id</th>
                <th>questionnaire_id</th>
                <?php 
                foreach($questions as $question){
                    echo "<th>", $question["title"], "</th>";
                }?>
                <th>created_at</th>
                <th>coordinates</th>
            </tr>

            <?php
            $ans_list = [];
            foreach($answers as $answer) {
                if(!array_key_exists($answer['answer_id'], $ans_list)) {
                    $ans_list[$answer['answer_id']] = array(
                        "base_data"=>$answer,
                        "answers"=>[]
                    );
                }

                $ans_list[$answer['answer_id']]['answers'][$answer['question_id']] = $answer['answer'];
            }

            foreach($ans_list as $answer) {
                if($answer['base_data']['flag_delete'] == 0){
                    echo "<tr>";
                    echo "<td>" . $answer['base_data']['answer_id'] . "</td>";
                    echo "<td>" . $answer['base_data']['questionnaire_id'] . "</td>";
                    
                    $i = 0;
                    foreach($answer['answers'] as $ans) {
                        if($questions[$i]['qtype'] == "radio"){
                            $items = explode(",", $questions[$i]['items']);
                            echo "<td>" . $items[$ans] . "</td>";
                        }else{
                            echo "<td>" . $ans . "</td>";
                        }
                        
                        $i++;
                    }

                    echo "<td>" . $answer['base_data']['created_at'] . "</td>";
                    
                    echo '<td align="center">', '<button onclick="location.href=\'/survey/result_mouse.php?answer_id=' . $answer['base_data']['answer_id'] . '\'">click here</button>'. "</td>";
                    echo '<td align="center">', '<button onclick="location.href=\'/survey/result.php?delete_id=' . $answer['base_data']['answer_id'] . '\'">delete</button>'. "</td>";
                    echo "</tr>";
                }
            }
            ?>
        </table>
        <a href="logout.php" style="position:absolute; top:0; right:0;">logout</a>
    </body>
</html>
