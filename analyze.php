<?php
require('dbconnect.php');

exec("python3 analyze.py", $output);
var_dump($output);
?>