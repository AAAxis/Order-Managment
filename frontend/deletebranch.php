<?php
    
require "connection.php";
$delete = $_GET['delete']; 

if(isset($_GET['delete'])){

    mysqli_query($connection, "DELETE FROM `db_branch` WHERE `file` = '$delete'");
    header('Location: https://www.wheels.works/settings');
    exit;

} else 

{
                echo 'Error';
            }?>




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