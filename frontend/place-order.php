<?php require "connection.php";

//ADD RANDOM ORDER
$token = $_GET['token'];
$order = $_GET['order'];
$total = $_GET['total'];


if(isset($_GET['total'])){

   //UPDATE TOTAL
   mysqli_query($connection, "UPDATE `db_order` SET `summary` = '$total' WHERE `code` = '$order'");


$branches = mysqli_query($connection, "SELECT * FROM `db_branch` WHERE `store` = '$token'");
$orders = mysqli_query($connection, "SELECT * FROM `db_order` WHERE `code` = '$order'");
  
include "sidebar.php"; ?>

    <script>
function myFunction() {
  // Get the checkbox
  var checkBox = document.getElementById("myCheck");
  // Get the output text
  var text = document.getElementById("text");

  // If the checkbox is checked, display the output text
  if (checkBox.checked == true){
    text.style.display = "none";
  } else {
    text.style.display = "block";
  }
}


function openForm() {
  document.getElementById("myForm").style.display = "block";
}

function closeForm() {
  document.getElementById("myForm").style.display = "none";
}
</script>

    <style>


/* Full-width input fields */
.form-container input[type=text], .form-container input[type=password] {
 
  padding: 15px;
  margin: auto 0;
  border: none;
  width:100%;
  background: #f1f1f1;
}

/* When the inputs get focus, do something */
.form-container input[type=text]:focus, .form-container input[type=password]:focus {
  background-color: #ddd;
  outline: none;
}

/* Set a style for the submit/login button */
.form-container .btn {
  background-color: #04AA6D;
  color: white;
  padding: 16px 20px;
  border: none;
  cursor: pointer;
  margin-bottom:10px;
  opacity: 0.8;
}

/* Add a red background color to the cancel button */
.form-container .cancel {
  background-color: red;
}

/* Add some hover effects to buttons */
.form-container .btn:hover, .open-button:hover {
  opacity: 1;
}
</style>

</head>
<body>



<div class="form-popup" id="myForm">
  <form style="margin:2rem;"action="order-status.php" method="GET" class="form-container">

    <input type="hidden" name="token" value="<?php echo $token?>" required />
    <input type="hidden" name="order" value="<?php echo $order?>" required />
        <input type="hidden" name="total" value="<?php echo $total?>" required />
 
    <label for="name"><b>Full Name</b></label> <br>
    <input type="text" placeholder="Enter  Name" name="name" required><br>

    <label for="phone"><b>Phone</b></label> <br>
    <input type="text" placeholder="Enter Phone" name="phone" required><br>

    <label for="text"><b>Text</b></label> <br>
    <input type="text" placeholder="Enter Text" name="text" required><br>
    
     <label for="email"><b>Email</b></label> <br>
        <input  type="text"  name="email" placeholder="Email Address" required><br><br>

   
    Take Away <input type="checkbox" id="myCheck" value="Take Away" onclick="myFunction()">
        <br><br><input id="text" style="display:block" type="text"  name="address" placeholder="Address"><br><br>


    <button type="submit" name="submit" value="Submit" class="btn">Send</button>
  <button class="btn cancel" onclick='window.history.go(-1); return false;' type="button">
         Back</button>

  </form>
</div>


    <?php } else { echo "Error"; }?>





