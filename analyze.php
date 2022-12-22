<?php
exec("python analyze.py", $output);
var_dump($output);
?>