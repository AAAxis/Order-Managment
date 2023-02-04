<?php
require "connection.php";
$username = $_POST['email'];
$password = $_POST['password'];
$token = $_GET['token'];
$error = '';

    // When form submitted, check and create user session.
    if (isset($_POST['email'])) {
        $username = stripslashes($_REQUEST['email']); // removes backslashes
        $username = mysqli_real_escape_string($connection, $username);

        // Check user is exist in the database

        $query = "SELECT * FROM `db_branch` WHERE `email`='$username'";
        $result = mysqli_query($connection, $query) or die(mysql_error());
        $rows = mysqli_num_rows($result);
        if ($rows == 1) {

            // Redirect to user dashboard page
            if (($password) == 'Admin')

                header('Location: cookie.php?token='.$token);
                
        } else { echo 'Password Incorrect'; }

    } else { echo 'Email Incorrect'; }
