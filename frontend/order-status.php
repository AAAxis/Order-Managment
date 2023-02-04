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
  <a href="#" style="text-decoration:none; color:black;" class="w3-left w3-padding">Check Out</a>

</header>


<?php  if (isset($_GET['order'])) {

    //ADD POST
    $order = $_GET['order'];
    $token = $_GET['token'];
    $text = $_GET['text'];
    $phone = $_GET['phone'];
    $name = $_GET['name'];
    $address = $_GET['address'];
    $total = $_GET['total'];
    $email = $_GET['email'];

    if (empty($address)) {
      $address = 'Take Away';

      mysqli_query($connection, "UPDATE `db_order` SET `phone` = '$phone', `email` = '$email', `name` = '$name', `text` = '$text', `address` = '$address', `status` = 'Open' WHERE `code` = '$order'");

    } else {
      mysqli_query($connection, "UPDATE `db_order` SET `phone` = '$phone', `email` = '$email', `name` = '$name', `text` = '$text', `address` = '$address', `status` = 'Open' WHERE `code` = '$order'");
    }

  }
    


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


    <td ><?php echo $ord['phone']; ?></td>
          <td><?php echo $ord['name']; ?></td>
        <td><?php echo $ord['address']; ?></td>
        <td><?php echo $ord['summary']; ?></td>
   
  
       </tr> 
  
<?php }  ?>
  
</table>   


   

<div id="smart-button-container">
      <div style="text-align: center;">
        <div id="paypal-button-container"></div>
      </div>
    </div>
  <script src="https://www.paypal.com/sdk/js?client-id=sb&enable-funding=venmo&currency=USD" data-sdk-integration-source="button-factory"></script>
  <script>
    function initPayPalButton() {
      paypal.Buttons({
        style: {
          shape: 'rect',
          color: 'gold',
          layout: 'vertical',
          label: 'paypal',
          
        },

        createOrder: function(data, actions) {
          return actions.order.create({
            purchase_units: [{"amount":{"currency_code":"USD","value":<?php echo $total ?>}}]
          });
        },

        onApprove: function(data, actions) {
          return actions.order.capture().then(function(orderData) {
            
            // Full available details
            console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));

            // Show a success message within this page, e.g.
            const element = document.getElementById('paypal-button-container');
            element.innerHTML = '';
            element.innerHTML = '<h3>Thank you for your payment!</h3><a style="text-decoration:none; color:red; " href="https://www.wheels.works/payment?token=<?php echo $token ?>&order=<?php echo $order ?>&email=<?php echo $email ?>">Send Recipe Email</a> ';

          
            
          });
        },

        onError: function(err) {
          console.log(err);
        }
      }).render('#paypal-button-container');
    }
    initPayPalButton();
  </script>