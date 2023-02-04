<?php
$token = $_GET['token'];    

    if(isset($_COOKIE['admin']) == 'true')
        setcookie('admin', 'true', time() -3600, '/');
    else
        setcookie('admin', 'true', time() + 3600, '/');

    header('Location: shopping-cart.php?token='.$token);
?>