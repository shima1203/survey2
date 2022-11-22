<?php //email重複除外 いつか
session_start();
?><script>var errormessage = []</script><?php
require('dbconnect.php');
if (!empty($_POST) ){
    if ($_POST['name'] == "" ) {
        $error['name'] = 'blank';
        ?>
        <script>errormessage.push('name')</script>
        <?php
    }
    if ($_POST['email'] == "" ) {
        $error['email'] = 'blank';
        ?>
        <script>errormessage.push('email')</script>
        <?php
    }
    if ($_POST['password'] == "" ) {
        $error['password'] = 'blank';
        ?>
        <script>errormessage.push('password')</script>
        <?php
    }
    if ($_POST['password2'] == "" ) {
        $error['password2'] = 'blank';
        ?>
        <script>errormessage.push('Re-enter password')</script>
        <?php
    }
    if ((strlen($_POST['password'] )< 6) &&( strlen($_POST['password'] )> 0)) {
        $error['password'] = 'length';
        ?>
        <script>errormessage.push('6文字以上のpassword')</script>
        <?php
    }
    if (($_POST['password'] != $_POST['password2']) && ($_POST['password2'] != "")){
        $error['password2'] = 'difference';
        ?>
        <script>errormessage.push('同じpassword')</script>
        <?php
    }
    if(!empty($error)) {
        ?>
        <script src="/survey/error.js"></script>
        <?php
    }
    if(empty($error)) {
        $_SESSION['join'] = $_POST;
        header('Location:/survey/resister2.php?');
        exit();
    }
}
if(isset($_SESSION['join']) && isset($_REQUEST['action']) && ($_REQUEST['action'] == 'rewrite') ){
    $_POST =$_SESSION['join'];
}

//ユーザーエージェントの判定
$user_device = '';
// HTTP リクエストヘッダーが持っているユーザーエージェントの文字列を取得
$useragent = $_SERVER['HTTP_USER_AGENT'];
if((strpos($useragent, 'Android') !== false) &&
    (strpos($useragent, 'Mobile') !== false) ||
    (strpos($useragent, 'iPhone') !== false) ||
    (strpos($useragent, 'iPad') !== false) ||
    (strpos($useragent, 'Windows Phone') !== false)){
    // スマホからアクセスしている場合
    $user_device = 'smartphone';
}elseif((strpos($useragent, 'DoCoMo') !== false) ||
    (strpos($useragent, 'KDDI') !== false) ||
    (strpos($useragent, 'SoftBank') !== false) ||
    (strpos($useragent, 'Vodafone') !== false) ||
    (strpos($useragent, 'J-PHONE') !== false)){
    // ガラケーからアクセスしている場合
    $user_device = 'phone';
}else{
    // パソコンからアクセスしている場合
    $user_device = 'pc';
}
?>

<!DOCTYPE html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>register</title>
        <!-- BootstrapのCSS読み込み -->
        <link href="/survey/css/bootstrap.min.css" rel="stylesheet">
        <link href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.8/css/all.css">       
    </head>

    <body class="text-center">
        <div class="card">
            <article class="card-body">
                <h2 class="card-title text-center mb-4 mt-1" style="color:#1e90ff; font-weight:lighter; opacity: 1.0;">新規登録</h2>
                <?php
                if($user_device == 'smartphone' || $user_device == 'phone'){
                    echo '<form action="" method="post" enctype="multipart/form-data" class="registrationform mx-auto">';
                }else{
                    echo '<form action="" method="post" enctype="multipart/form-data" class="registrationform w-25 mx-auto">';
                }
                ?>
                    <div class="form-group">
                        <div class="input-group">
                            <div class="input-group-prepend">
                                <span class="input-group-text"> <i class="fa fa-user"></i> </span>
                            </div>
                            <input class="form-control" type="name" name="name" value="<?php echo htmlspecialchars($_POST['name']??"", ENT_QUOTES); ?>" placeholder="ユーザーID" autofocus required/></input>
                        </div>
                    </div>  
                    <?php if (isset($error['name']) && ($error['name'] == "blank")): ?>
                        <p class="error">nameを入力してください</p>
                    <?php endif; ?>
                        
                    <div class="form-group">
                        <div class="input-group">
                            <div class="input-group-prepend">
                                <span class="input-group-text"> <i class="fa fa-envelope"></i> </span>
                            </div>
                            <input class="form-control" type="name" name="email" value="<?php echo htmlspecialchars($_POST['email']??"", ENT_QUOTES); ?>" placeholder="email" required/></input>
                        </div>
                    </div>
                    <?php if (isset($error['email']) && ($error['email'] == "blank")): ?>
                        <p class="error">emailを入力してください</p>
                    <?php endif; ?>
                    
                    <div class="form-group">
                        <div class="input-group">
                            <div class="input-group-prepend">
                                <span class="input-group-text"> <i class="fa fa-lock"></i> </span>
                            </div>
                            <input class="form-control" type="password" name="password" value="<?php echo htmlspecialchars($_POST['password']??"", ENT_QUOTES); ?>" placeholder="パスワード" required/></input>
                        </div>
                    </div>
                    <?php if (isset($error['password']) && ($error['password'] == "blank")): ?>
                        <p class="password"> passwordを入力してください</p>
                    <?php endif; ?>
                    <?php if (isset($error['password']) && ($error['password'] == "length")): ?>
                        <p class="alert alert-danger" role="alert"> 6文字以上で指定してください</p>
                    <?php endif; ?>
                    
                    <div class="form-group">
                        <div class="input-group">
                            <div class="input-group-prepend">
                                <span class="input-group-text"> <i class="fa fa-lock"></i> </span>
                            </div>
                            <input class="form-control" type="password" name="password2" value="<?php echo htmlspecialchars($_POST['password2']??"", ENT_QUOTES); ?>" placeholder="パスワード再入力" required/></input>
                        </div>
                    </div>
                    <?php if (isset($error['password2']) && ($error['password2'] == "blank")): ?>
                        <p class="error"> passwordを入力してください</p>
                    <?php endif; ?>
                    <?php if (isset($error['password2']) && ($error['password2'] == "difference")): ?>
                        <p class="alert alert-danger" role="alert"> パスワードが上記と違います</p>
                    <?php endif; ?>
                        
                    <div class="login2"><input type="submit" value="確認" class="btn btn-outline-primary my-1"></div>
                </form>
                <p class="mt-2 mb-3 text-muted">&copy; 2022</p>
            </article>
        </div>
    </body>
</html>