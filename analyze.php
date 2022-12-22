<?php
$command = "export LANG=ja_JP.UTF-8;python /survey/analyz.py";
exec($command, $output);

foreach($output as $o){
    echo $o . '<br>';
}
?>