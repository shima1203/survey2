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
    header('Location: login.php/?action=mouse_result3');
    exit();
}


$questionnaire_id = 1;
$answer_id = $_GET["answer_id"];

//回答情報
$answers_pre=$db->prepare('SELECT * FROM Answers WHERE answer_id=?');
$answers_pre->execute(array($answer_id));
$answers=$answers_pre->fetchAll();
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
        <style>
            .pie {
                position: relative;
                margin-right: auto;
                margin-left: auto;
                width: 300px;
                height: 300px;
                border-radius: 50%;
            }

            .pie span {
                position: absolute;
                top: 50%;
                right: 50px;
                transform: translateY(-50%);
                color: #fff;
                font-size: 26px;
                font-weight: 700;
            }
        </style>
    </head>

    <body>
        <?php 
        foreach($questions as $question){
            echo $question["title"] . "<br>";
        }?>


    </body>

    <div class="pie" style="background-image: conic-gradient(#d5525f 0% 60%, #d9d9d9 60% 100%);"><span>60%</span></div>
</html>