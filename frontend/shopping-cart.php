<?php session_start();
require_once("dbcontroller.php");
include "sidebar.php"; 

$db_handle = new DBController();
if(!empty($_GET["action"])) {
switch($_GET["action"]) {
	case "add":
		?><div style="margin:3rem; class="box"><a href="shopping-cart.php?token=<?php echo $_GET['token'] ?>&action=placeorder#popup1"><i class="fas fa-shopping-cart"> My Cart</i></a></div><?php
			
		if(!empty($_POST["quantity"])) {

			$productByCode = $db_handle->runQuery("SELECT * FROM products WHERE code='".$_GET["code"]."'");
			$itemArray = array($productByCode[0]["code"]=>array('name'=>$productByCode[0]["name"], 'code'=>$productByCode[0]["code"], 'quantity'=>$_POST["quantity"], 'price'=>$productByCode[0]["price"], 'image'=>$productByCode[0]["image"]));
			
			if(!empty($_SESSION["cart_item"])) {
					if(in_array($productByCode[0]["code"],array_keys($_SESSION["cart_item"]))) {
					foreach($_SESSION["cart_item"] as $k => $v) {
							if($productByCode[0]["code"] == $k) {
								if(empty($_SESSION["cart_item"][$k]["quantity"])) {
									$_SESSION["cart_item"][$k]["quantity"] = 0;
								}
								$_SESSION["cart_item"][$k]["quantity"] += $_POST["quantity"];
							}
					}
				} else {
					$_SESSION["cart_item"] = array_merge($_SESSION["cart_item"],$itemArray);
				}
			} else {
				$_SESSION["cart_item"] = $itemArray;
			}
		}
	break;
	case "remove":


		if(empty($_SESSION["cart_item"]))
						unset($_SESSION["cart_item"]);
			
		if(!empty($_SESSION["cart_item"])) {
	?><div style="margin:3rem; class="box"><a href="shopping-cart.php?token=<?php echo $_GET['token'] ?>&action=placeorder#popup1"><i class="fas fa-shopping-cart"> My Cart</i></a></div><?php
	
			foreach($_SESSION["cart_item"] as $k => $v) {
					if($_GET["code"] == $k)
				
						unset($_SESSION["cart_item"][$k]);				
					
			}
		}
	break;
	case "empty":
		unset($_SESSION["cart_item"]);
	break;	
	case "placeorder":

	function generateRandomString($length = 10) {
    return substr(str_shuffle(str_repeat($x='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', ceil($length/strlen($x)) )),1,$length);
    }
	$random = generateRandomString();
    $token = $_GET['token'];

    require "connection.php";

      if(is_array($_SESSION["cart_item"]))  
      {  
		
		$result = "INSERT INTO `db_order` (`store`, `code`, `status`) 
		VALUES ( '$token', '$random', 'Ordering')";  
		mysqli_query($connection, $result);

           foreach($_SESSION["cart_item"] as $row => $value)  
           {    
                $name = mysqli_real_escape_string($connection, $value["name"]);  
                $quantity = mysqli_real_escape_string($connection, $value["quantity"]);  
                $cart = "INSERT INTO `db_cart` (`code`, `items`, `quantity`) 
				VALUES ('$random', '$name', '$quantity')";  
                mysqli_query($connection, $cart);

           }  
           

				?>


				<div id="popup1" class="overlay">
				<div class="popup">
					<h3>My Order</h3>
					<a class="close" href="#">&times;</a>
					<div class="content">
					<div id="shopping-cart">

<a id="btnEmpty"  href="shopping-cart.php?token=<?php echo $_GET['token'];?>&action=empty">Empty Cart</a>

<?php
if(isset($_SESSION["cart_item"])){
    $total_quantity = 0;
    $total_price = 0;
?>	
<table class="tbl-cart" cellpadding="5" cellspacing="1">
<tbody>
<tr>
<th style="text-align:left;">Name</th>
<th style="text-align:right;" >Quantity</th>
<th style="text-align:right;">Price</th>
<th  >Remove</th>
</tr>	
<?php		
    foreach ($_SESSION["cart_item"] as $item ){
        $item_price = $item["quantity"]*$item["price"];
		?>
				<tr>
				<td><img width="100" height="100"src="https://www.wheels.works/static/images/users/<?php echo $item["image"]; ?>"  class="cart-item-image" /><?php echo $item["name"]; ?></td>
		
				<td style="text-align:right;"><?php echo $item["quantity"]; ?></td>
			
				<td  style="text-align:right;"><?php echo "$ ". number_format($item_price); ?></td>
				<td style="text-align:center;"><a href="shopping-cart.php?token=<?php echo $_GET["token"]; ?>&action=remove&code=<?php echo $item["code"]; ?>" class="btnRemoveAction"><img src="imgs/icon-delete.png" alt="Remove Item" /></a></td>
				</tr>
				<?php
				$total_quantity += $item["quantity"];
				$total_price += ($item["price"]*$item["quantity"]);
			   
           
		}
		?>

<tr>
<td  align="right">Total:</td>
<td align="right"><?php echo $total_quantity; ?></td>
<td align="right" ><strong><?php echo "$ ".number_format($total_price); ?></strong></td>
<td></td>
</tr>
</tbody>

</table>

<a id="btnEmpty" style="margin-right:3px; color:green; border-color: green;" href="place-order.php?token=<?php echo $_GET['token']?>&order=<?php echo $random ?>&total=<?php echo $total_price ?>">Send Order</a>
  <?php
} else {
?>
<div style = "color: white;" class="no-records">Your Cart is Empty</div>
<?php 
}
?>
</div>			
					</div>
				</div>
			</div> <?php

      }  

 
	break;	
}
}

?>
<link href="static/cart.css" type="text/css" rel="stylesheet" />

<body>



<div style="margin: 0 auto; 
        
        float: center; 
        margin-left: 5rem;" id="product-grid">

	<?php

	$product_array = $db_handle->runQuery("SELECT * FROM `products` WHERE `store` = '".$_GET['token']."'");
	if (!empty($product_array)) { 
		foreach($product_array as $key=>$value){
	?>
		<div class="product-item">
			<form method="POST" action="shopping-cart.php?token=<?php echo $_GET["token"]; ?>&action=add&code=<?php echo $product_array[$key]["code"]; ?>">
			<div class="product-image"><img width="250" height="200" src="https://www.wheels.works/static/images/users/<?php echo $product_array[$key]["image"]; ?>"></div>
			<div class="product-tile-footer">
			<div style="color:white;" class="product-title"><?php echo $product_array[$key]["name"]; ?></div>
			<div class="product-price"><?php echo "$".$product_array[$key]["price"]; ?></div>
		
			<div class="cart-action"><input type="text" class="product-quantity" name="quantity" value="1" size="2" /><input type="submit" value="Add to Cart" class="btnAddAction" /></div>
			</div>
			</form>
		</div>
	<?php
		}
	}
	?>
</div>
</body>

<style>
    


h1 {
  text-align: center;
  font-family: Tahoma, Arial, sans-serif;
  color: #06D85F;
  margin: 80px 0;
}



.button {
  font-size: 1em;
  padding: 5px;
  color: black;
 text-decoration: none;
  cursor: pointer;

}


.overlay {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.7);
  transition: opacity 500ms;
  visibility: hidden;
  opacity: 0;
}
.overlay:target {
  visibility: visible;
  opacity: 1;
}

.popup {
  margin: 50px auto;
  padding: 20px;
  background: #fff;
  border-radius: 5px;
  width: 50%;
  position: relative;
  transition: all 5s ease-in-out;
}

.popup h2 {
  margin-top: 0;
  color: #333;
  font-family: Tahoma, Arial, sans-serif;
}
.popup .close {
  position: absolute;
  top: 20px;
  right: 30px;
  transition: all 200ms;
  font-size: 30px;
  font-weight: bold;
  text-decoration: none;
  color: #333;
}
.popup .close:hover {
  color: #06D85F;
}
.popup .content {
  max-height: 20%;
  overflow: auto;
}

@media screen and (max-width: 700px){
  .box{
    width: 80%;
  }
  .popup{
    width: 85%;
  }
}
    
</style>
</html>