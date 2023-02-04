
  <?php 

require "connection.php";



  if (isset($_GET['random'])) {
      
    $random = $_GET['random'];

    $cart = mysqli_query($connection, "SELECT * FROM `db_cart` WHERE `code` = '$random'");?>



<?php while( $res = mysqli_fetch_assoc($cart) ) { ?>

<h1 style="text-align:center; margin-top:10rem"><?php echo $res['items']." X ".$res['quantity']."<br>"; } ?></h1>  


<?php }  ?>

