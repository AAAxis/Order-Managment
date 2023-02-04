<?php if(isset($_GET['text'])) {
    
    require "connection.php";

    mysqli_query($connection, "INSERT INTO `db_comments` ( `email`, `text`, `branch`)
    VALUES ('".$_GET['email']."','".$_GET['text']."', '".$_GET['token']."')");
     
    header('Location: https://www.wheels.works/newchat?token='.$_GET['token'].'&email='.$_GET['email']); } 
    else { include "sidebar.php";  if(isset($_GET['email'])) : 
    

/**
	 * Get either a Gravatar URL or complete image tag for a specified email address.
	 *
	 * @param string $email The email address
	 * @param string $s Size in pixels, defaults to 80px [ 1 - 2048 ]
	 * @param string $d Default imageset to use [ 404 | mp | identicon | monsterid | wavatar ]
	 * @param string $r Maximum rating (inclusive) [ g | pg | r | x ]
	 * @param boole $img True to return a complete IMG tag False for just the URL
	 * @param array $atts Optional, additional key/value attributes to include in the IMG tag
	 * @return String containing either just a URL or a complete image tag
	 * @source https://gravatar.com/site/implement/images/php/
	 */
	function get_gravatar( $token, $s = 80, $d = 'mp', $r = 'g', $img = false, $atts = array() ) {
		$url = 'https://www.gravatar.com/avatar/';
		$url .= md5( strtolower( trim( $token ) ) );
		$url .= "?s=$s&d=$d&r=$r";
		if ( $img ) {
			$url = '<img src="' . $url . '"';
			foreach ( $atts as $key => $val )
				$url .= ' ' . $key . '="' . $val . '"';
			$url .= ' />';	} return $url; } 

?>

        <link rel="stylesheet" href="static/style.css">
        
      <div style="padding: 20px;border: 2px solid #4CAF50;">
          <h4>My Private Room </h4><h6><?php echo $_GET['email'] ?></h6>
  
      <form action="" method="GET">
    <input type="hidden" name="token" value="<?php echo $_GET['token'] ?>">
    <input type="hidden" name="email" value="<?php echo $_GET['email'] ?>">
      <input type="text" name="text" placeholder="Enter Message...."><br><br>
       
      <input name="submit" type="submit" value="Send">
      
        </form>
        </div>


  <?php $comments = mysqli_query($connection, "SELECT * FROM `db_comments` 
   WHERE `branch` = '".$_GET['token']."' AND `email` = '".$_GET['email']."' ORDER BY `db_comments`.`date` DESC ");

        while($com = mysqli_fetch_assoc($comments)) { 

          $token = $com['email']; 

          $default = "https://www.getfoundquick.com/wp-content/uploads/2014/01/Capture-1.jpg";
        
          $size = 40;
          
          $grav_url = "https://www.gravatar.com/avatar/" . md5( strtolower( trim($token ) ) ) . "?d=" . urlencode($default) . "&s=" . $size; ?>

<div class="box">
<img src="<?php echo $grav_url; ?>"  style="width:100%;">
  <p><?php echo $com['text']; ?></p>
  <span class="time-right"><?php echo $com['email'];?></span>
</div>
    

     
     
<?php } else : ?>
       
              
<div style="padding: 30px;border: 1px solid #4CAF50;"><h2>New Chat</h2>
  
  <form action="messages.php" method="GET">
<input type="hidden" name="token" value="<?php echo $_GET['token'] ?>">
  <input type="email" name="email" placeholder="Enter Email...."><br><br>
   
  <input name="submit" type="submit" value="Send">
</form>
</div>
  
        <?php endif; }?>
</body>
</html>

          
  
       