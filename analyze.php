<?php
require('dbconnect.php');

$questionnaire_id = 3;

//回答
$answers_pre=$db->prepare('SELECT * FROM Answers');
$answers_pre->execute(array());
$answers=$answers_pre->fetchAll();
//回答データ
$answerdata_pre=$db->prepare('SELECT * FROM AnswerData');
$answerdata_pre->execute(array());
$answerdata=$answerdata_pre->fetchAll();
//アンケート情報
$questionnaires=$db->prepare('SELECT * FROM Questionnaires WHERE questionnaire_id=?');
$questionnaires->execute(array($questionnaire_id));
$questionnaire=$questionnaires->fetch();
//質問情報
$questions_pre=$db->prepare('SELECT * FROM Questions WHERE questionnaire_id=?');
$questions_pre->execute(array($questionnaire_id));
$questions=$questions_pre->fetchAll();

$click = [];
foreach($answerdata as $data){
    array_push($click, $data["click"]);
}
$command = "python3 analyze.py $click[0]";
exec($command, $output);
var_dump($output);
?>