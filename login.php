<?php
session_start();
require('dbconnect.php');


//MySQLのデータと照らし合わせる
if(!empty($_POST)) {
    if(($_POST['email'] != '') && ($_POST['password'] != '')) {
        $login = $db->prepare('SELECT * FROM Users WHERE email=?');
        $login->execute(array($_POST['email']));
        $member=$login->fetch();
        
        if(password_verify($_POST['password'],$member['pass_hash'])) {
            $_SESSION['user_id'] = $member['user_id'];
            $_SESSION['time'] =time();
            if($_GET['action'] == 'mouse_result1'){
                header('Location: /survey/mouse_result1.php');
                exit();
            }elseif($_GET['action'] == 'result'){
                header('Location: /survey/result.php');
                exit();
            }elseif($_GET['action'] == 'mouse_result2'){
                header('Location: /survey/mouse_result2.php');
                exit();
            }elseif($_GET['action'] == 'result_mouse'){
                header('Location: /survey/mresult_mouse.php');
                exit();
            }elseif($_GET['action'] == 'mouse_result3'){
                header('Location: /survey/mouse_result3.php');
                exit();
            }elseif($_GET['action'] == 'create_questionnaire'){
                header('Location: /survey/create_questionnaire.php');
                exit();
            }else{
                header('Location: /survey/questionnaire2.php');
                exit();
            }
        } else {
            $error['login']='failed';
        } 
    } else {
        $error['login'] ='blank';
    }
} 

?>

<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>login</title>
        <!-- BootstrapのCSS読み込み -->
        <link href="/survey/css/bootstrap.min.css" rel="stylesheet">
        <link href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.8/css/all.css">      
    </head>

    <body class="text-center">
    <div class="card mx-auto"style="width: 25rem;top:75px">
    <div class="card-header" style="background-color: rgba(100,100,100,.1);font-size:20px">ログイン</div>
    <article class="card-body">
        <form class="w-75 mx-auto" action='' method="post">
            <div class="form-group">
            <div class="input-group">
                <div class="input-group-prepend">
                    <span class="input-group-text"> <i class="fa fa-user"></i> </span>
                </div>
                <input class="form-control" type="name" name="name" value="<?php echo htmlspecialchars($_POST['name']??"", ENT_QUOTES); ?>" placeholder="ユーザーID" autofocus required/>
            </div></div>
            <div class="form-group">
            <div class="input-group">
                <div class="input-group-prepend">
                    <span class="input-group-text"> <i class="fa fa-envelope"></i> </span>
                </div>
                <input class="form-control" type="name" name="email" value="<?php echo htmlspecialchars($_POST['email']??"", ENT_QUOTES); ?>" placeholder="email" required/>
            </div></div>
            <div class="form-group">
            <div class="input-group">
                <div class="input-group-prepend">
                    <span class="input-group-text"> <i class="fa fa-lock"></i> </span>
                </div>
                <input class="form-control" type="password" name="password" value="<?php echo htmlspecialchars($_POST['password']??"", ENT_QUOTES); ?>"placeholder="パスワード" required/>
            </div></div>
            
            <script>var errormessage = []</script>
            <?php if (isset($error['login']) &&  ($error['login'] =='blank')): ?>
                <p class="error" role="alert">name,email,passwordを入力してください</p>
                <script>errormessage.push('name,email,password')</script>
                <script src="/survey/error.js"></script>
            <?php endif; ?>
        
            <?php if( isset($error['login']) &&  $error['login'] =='failed'): ?>
                <p class="alert alert-danger" role="alert">emailかpasswordが間違っています</p>
                <script>errormessage.push('正しいemail,password')</script>
                <script src="/survey/error.js"></script>
            <?php endif; ?>
        
            <div class="login2"><input type="submit" value="login" class="btn btn-outline-primary my-1"></div>
        
        </form>
        <p class="mt-2 mb-3 text-muted">&copy; 2022</p>
    </article>
    </div>
    </body>
</html>