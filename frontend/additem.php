<?php
    
require "connection.php";

$store = $_GET['store']; 
$file = $_GET['file']; 
$value = $_GET['value']; 
$item = $_GET['item']; 
$type = $_GET['group']; 




if(isset($_GET['store'])){

    function generateRandomString($length = 4) {
    return substr(str_shuffle(str_repeat($x='0123456789', ceil($length/strlen($x)) )),1,$length);
    }
	$code = generateRandomString();
    mysqli_query($connection, "INSERT INTO `products` (`type`,`store`, `image`, `code`, `price`, `name`) 
    VALUES ('$type', '$store', '$file', 'PROD$code', '$value', '$item')"); 
     header('Location: https://www.wheels.works/'.$store.'/item');

    exit;

} else {  echo "Error";   } ?>



if request.method == "POST":
     #insert sql part here
            try:
                title = request.form['title']
                operation = request.form['operation']
                type = request.form['type']
                address = request.form['address']
                logo = save_images(request.files.get('file'))
                status = "Close"
                total_earnings = "0"
                email = session['token']

                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                sql = "INSERT INTO db_branch (store_name, operation, type, address, email, file, total_earnings, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, [title, operation, type, address, email, logo, total_earnings, status])

                conn.commit()

            except Exception as e:
                print(e)
            finally:
                cursor.close()
                conn.close()
            return redirect('/settings')