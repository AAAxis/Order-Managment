<!DOCTYPE html>
<html>
    <head>
      <?php require "connection.php";?>
      <script src="static/script.js"></script>
        <script src="https://kit.fontawesome.com/003aac0f2b.js" crossorigin="anonymous"></script>
      <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>My Store</title>

    </head>
  <body>

  <!-- Top menu on small screens -->
<header  class="w3-container  w3-white w3-xlarge w3-padding-16">
  <a href="#" style="text-decoration:none; color:black;" class="w3-right w3-padding">Home</a>
  <a href="javascript:void(0)" class="w3-left w3-button w3-white" onclick="w3_open()">☰</a>
</header>


<?php  $select = $_GET['token']; 

if(isset($_GET['token'])) {

$branches = mysqli_query($connection, "SELECT * FROM `db_branch` WHERE `token` = '$select'" ); }

 while( $brn = mysqli_fetch_assoc($branches) ) { ?>

<nav class="w3-sidebar w3-bar-block w3-dark-grey w3-animate-left w3-text-white w3-collapse w3-top w3-center" style="z-index:3;width:300px;font-weight:bold" id="mySidebar"><br>
     
        <?php if(isset($_COOKIE['admin']) == 'true') :?>
        
         <a style="text-decoration:none; color: white;" href="#"> <h3 class="w3-padding-20 w3-center"><b><?php echo $brn['store_name']; ?></b></h3></a>
          <a  onclick="w3_close()" href="#"><img src="https://www.wheels.works/static/images/users/<?php echo $brn['file']; ?>" height="100px" width="100px"></a><br><br>
         <br>
       
  <a href="myorders.php?token=<?php echo $_GET['token'] ?>" onclick="w3_close()" class="w3-bar-item w3-button">Orders History</a>
  <a href="logout.php?token=<?php echo $_GET['token'] ?>"  onclick="w3_close()" class="w3-bar-item w3-button">Log Out</a>
 
       <hr>
     
        <?php else : ?>

          <a style="text-decoration:none; color:white;" href="#"> <h3 class="w3-padding-20 w3-center"><b><?php echo $brn['store_name']; ?></b></h3></a>
          <a  onclick="w3_close()" href="#"><img src="https://www.wheels.works/static/images/users/<?php echo $brn['file']; ?>" height="100px" width="100px"></a><br><br>
    
        <form  action="login.php?token=<?php echo $_GET['token'] ?>" method="POST" >
        
            <input  style= "width:260px; margin:10px;"   name="email" placeholder="Email" required >
            
            <input   style= "width:260px; margin:10px;" type="password" name="password" placeholder="Password" >
            
            <input  style= "width:80px; margin:10px;" name="submit" type="submit" value="Login">
            
            </form>
           
            <hr>
  

<?php endif; ?>
       
<a href="shopping-cart.php?token=<?php echo $_GET['token'] ?>" onclick="w3_close()" class="w3-bar-item w3-button">New Order</a> 
<a href="messages.php?token=<?php echo $_GET['token'] ?>" onclick="w3_close()" class="w3-bar-item w3-button">Messages</a>
<a href="https://www.wheels.works" onclick="w3_close()" class="w3-bar-item w3-button">About</a>

        <?php } ?><hr>

     </nav>

<!-- Overlay effect when opening sidebar on small screens -->
<div class="w3-overlay w3-hide-large w3-animate-opacity" onclick="w3_close()" style="cursor:pointer" title="close side menu" id="myOverlay"></div>
   <!-- !PAGE CONTENT! -->
   <div class="w3-main" style="margin-left:310px; margin-top:10px;">