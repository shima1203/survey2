<?php
$command = "export LANG=ja_JP.UTF-8;python /survey/analyze.py";
exec($command, $output);

foreach($output as $o){
    echo $o . '<br>';
}
?>