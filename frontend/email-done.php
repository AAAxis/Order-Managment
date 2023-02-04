<?php include "sidebar.php";

    $order = $_GET['order'];
    $token = $_GET['token'];


$branches = mysqli_query($connection, "SELECT * FROM `db_branch` ");
$orders = mysqli_query($connection, "SELECT * FROM `db_order` WHERE `code` = '$order' AND `status` = 'Open' ORDER BY `db_order`.`create_date` DESC"); 
$cart = mysqli_query($connection, "SELECT * FROM `db_cart`"); ?>



<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN" crossorigin="anonymous"></script>

<body>
<div class="container" style="width:100%;">

     
<table class="table table-striped">

    <thead>
       <tr >

          <th scope="col">Cart</th>
          <th scope="col">Contact</th>
          <th scope="col">Name</th>
          <th scope="col">Address</th>
          <th scope="col">Total</th>

         </tr>
</thead> 
        <?php while( $ord = mysqli_fetch_assoc($orders) ) { 
      $code = $ord['code'];
    $order_cat = false;
  
    while ($cat = mysqli_fetch_assoc($cart))
    {
      if( $cat['code'] == $code)
      {
        $order_cat = $cat['items'];
        break;
      }
    }
    
     
 ?>

<td>


<div class="box"><a style="color:black; text-decoration:none;"  href="show-cart.php?token=<?php echo $_GET['token']?>&random=<?php echo $code ?>"><i class="fas fa-shopping-cart"></i></a></div>

</td>


    <td><?php echo $ord['phone']; ?></td>
          <td><?php echo $ord['name']; ?></td>
        <td><?php echo $ord['address']; ?></td>
        <td><?php echo $ord['summary']; ?></td>
   
  
       </tr> 
  
<?php }  ?>
  
</table>   
