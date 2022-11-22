<?php
try {
    $db = new PDO ('mysql:dbname=survey; host=localhost; charset=utf8', 'ubuntu', 'Aquos.123');
} catch (PDOException $e) {
    echo 'DB接続エラー' . $e->getMessage;
}
?>