<?php
exec("python analyze.py", $output);
 
print_r($output);
?>