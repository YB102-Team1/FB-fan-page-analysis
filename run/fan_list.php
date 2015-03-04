<?php
$file_prefix = 'fan_list_57613404340_';
$link = new mysqli('localhost', 'team1', 'yb102', 'YB102_Team1');
$link->query("SET NAMES UTF8");
for ($segment = 1; $segment <= 487; $segment++) {
    $file_path = $_SERVER['DOCUMENT_ROOT'].'/_asset/data/fan_list/'.$file_prefix.sprintf('%05d', $segment).'.csv';
    $file = @fopen($file_path, "r");
    while (!feof($file)) {
        $data_string = fgets($file);
        str_replace("\n", "", $data_string);
        $data_array = explode(',', $data_string);
        $column1 = $data_array[0];
        $column2 = $data_array[1];
        $column3 = $data_array[2];
        $now = date('Y-m-d H:i:s', time()+25200);
        if ($column1) {
            $insert_sql = "INSERT INTO `fb_user` (`segment`, `fb_user_id`, `name`, `path`, `create_time`, `modify_time`) VALUES ('$segment', '$column1', '$column2', '$column3', '$now', '$now')";
            echo "INSERT INTO `fb_user` (`segment`, `fb_user_id`, `name`, `path`, `create_time`, `modify_time`) VALUES ('$segment', '$column1', '$column2', '$column3', '$now', '$now')".'<br>';
            $link->query($insert_sql);
        }
    }
    fclose($file);
}
?>