<?php
    
require "connection.php";

    $token = $_GET['token']; 
    $store_name = $_GET['title']; 
    $operation = $_GET['operation']; 
 
    $address = $_GET['address']; 
    $email = $_GET['email']; 
    $file = $_GET['logo']; 


if(isset($_GET['token'])){ 
    
    mysqli_query($connection, "INSERT INTO `db_branch` (`token`, `store_name`, `operation`, `address`, `email`, `file`) 
    VALUES ('$token', '$store_name', '$operation', '$address', '$email', '$file')");
    
    header('Location: https://www.wheels.works/settings');

    exit;

} else 

{  echo "INSERT INTO `db_branch` (`token`, `store_name`, `operation`, `type`, `address`, `email`, `file`) VALUES ('$token', '$store_name', '$operation', '$type', '$address', '$email', '$file')";  

               

            }?>



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