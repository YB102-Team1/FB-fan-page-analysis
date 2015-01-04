<?php
include $_SERVER['DOCUMENT_ROOT'].'/_config/system_config.inc';
include DB_CONFIG_FILE;

echo '<pre>';

$connection = mysqli_connect($database_host, $database_user, $database_password);

// check connection
echo 'Check connection:'.PHP_EOL;
if (mysqli_connect_errno()) {

    echo 'Failed to connect to MySQL: '.mysqli_connect_error();
    throw new RuntimeException();

}
echo 'Success!'.PHP_EOL.PHP_EOL;

// create database
echo 'Create database:'.PHP_EOL;
$database_selected = mysqli_select_db($connection, $database_name);
if (!$database_selected) {

    $sql = "CREATE DATABASE $database_name";
    if (!mysqli_query($connection, $sql)) {

        echo "Error when creating database `$database_name`: ".mysql_error().PHP_EOL;
        exit;

    }

}
echo 'Success!'.PHP_EOL.PHP_EOL;

// create tables
echo 'Create tables:'.PHP_EOL;
$db_obj = new DatabaseAccess();
$new_table_array = array();
foreach (glob(TABLE_SQL_ROOT.'/*.sql') as $sql_file) {

    $new_table_array[] = str_replace('.sql', '', str_replace(TABLE_SQL_ROOT.'/', '', $sql_file));

}
foreach ($new_table_array as $table_name) {

    echo '`'.$table_name.'`...';
    if (ModelHelper::importTable($table_name)) {

        echo 'ok'.PHP_EOL;

        // sync table data
        $sql_path = DATA_SQL_ROOT.'/'.$table_name.'.sql';
        if (file_exists($sql_path)) {

            echo "\tTruncate `$table_name` data...";
            $sql = "TRUNCATE $table_name";
            if ($db_obj->query($sql)) {

                echo 'ok'.PHP_EOL;

            } else {

                echo 'fail'.PHP_EOL;

            }
            echo "\tImport `$table_name` data...";
            $sql = file_get_contents($sql_path);
            if ($db_obj->query($sql)) {

                echo 'ok'.PHP_EOL;

            } else {

                echo 'fail'.PHP_EOL;

            }

        }

    } else {

        echo 'fail'.PHP_EOL;

    }

}

echo '</pre>';
?>