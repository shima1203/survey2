<?php
session_start();
require('dbconnect.php');
//前回からのセッション情報があるか確認
if (!isset($_SESSION['join'])) {
    header ('Location: register.php');
    exit();
}
$hash = password_hash($_SESSION['join']['password'], PASSWORD_BCRYPT);
//MySQLに入力データを登録
if(!empty($_POST)){
    $statement = $db->prepare('INSERT INTO Users SET name=?, email=?, pass_hash=?, created_at=NOW()');
    $statement->execute(array(
        $_SESSION['join']['name'],
        $_SESSION['join']['email'],
        $hash));
    unset($_SESSION['join']);
    header('Location: login.php');
    exit();
}
?>
<!DOCTYPE html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>confirmation</title>
        <!-- BootstrapのCSS読み込み -->
        <link href="/survey/css/bootstrap.min.css" rel="stylesheet">
        <link href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.8/css/all.css">
        <!-- jQuery読み込み -->
        <script src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
        <script src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        <!-- BootstrapのJS読み込み -->
        <script src="/survey/js/bootstrap.min.js"></script>
    </head>

    <body class="text-center">
    <div class="card">
    <article class="card-body">
    <h1 class="card-title text-center mb-4 mt-1">確認</h1>
        <form action="" method="post">
        
        <input type="hidden" name="action" value="submit">
        <div class="label">
            <p>name : 
            <span class="check"><?php echo (htmlspecialchars($_SESSION['join']['name'], ENT_QUOTES)); ?></span>
            </p>
            <p>email : 
            <span class="check"><?php echo (htmlspecialchars($_SESSION['join']['email'], ENT_QUOTES)); ?></span>
            </p>
            <p>password : 
            <span class="check">●●●●●●● </span>
        </p>
        <input type="button" onclick="location.href='resister.php?action=rewrite'" value="修正" name="rewrite" class="btn btn-outline-primary my-1">
        <input type="submit" onclick="location.href='login.php'" value="登録" name="registration" class="btn btn-outline-success my-1">
        </form>
        <p class="mt-2 mb-3 text-muted">&copy; 2022</p>
    </article>
    </div>
    </body>
</html>