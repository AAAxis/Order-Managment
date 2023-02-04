<?php
    
require "connection.php";
$delete = $_GET['prod']; 
$token = $_GET['token']; 

if(isset($_GET['prod'])){

    mysqli_query($connection, "DELETE FROM `products` WHERE `image` = '$delete'");
    
    header('Location: https://www.wheels.works/'.$token.'/item');
    exit;

} else 

{  echo 'Error';   }?>




###Python Example#####

conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                sql = "DELETE FROM db_branch WHERE id = %s"
                cursor.execute(sql, [id])

                conn.commit()

            except Exception as e:
                print(e)
            finally:
                cursor.close()
                conn.close()