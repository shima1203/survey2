<?php
session_start();
session_destroy();
header('Location: /survey/login.php');
?>