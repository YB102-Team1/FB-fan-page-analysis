<?php
$file_prefix = 'user_likes_57613404340_';
$link = new mysqli('localhost', 'team1', 'yb102', 'YB102_Team1');
$link->query("SET NAMES UTF8");
for ($segment = 1; $segment <= 1; $segment++) {
    $file_path = $_SERVER['DOCUMENT_ROOT'].'/_asset/data/user_likes/'.$file_prefix.sprintf('%05d', $segment).'.csv';
    $file = @fopen($file_path, "r");
    while (!feof($file)) {
        $data_string = fgets($file);
        str_replace("\n", "", $data_string);
        $data_array = explode(',', $data_string);
        $fb_user_id = $data_array[0];
        if (count($data_array) == 2) {
            $fb_fan_page_id = $data_array[1];
        } else {
            $fb_fan_page_id = $data_array[2];
        }
        $now = date('Y-m-d H:i:s', time()+25200);
        if ($column1) {
            $insert_sql = "INSERT INTO `fb_user_likes` (`segment`, `fb_user_id`, `fb_fan_page_id`, `create_time`, `modify_time`) VALUES ('$segment', '$fb_user_id', '$fb_fan_page_id', '$now', '$now')";
            echo "INSERT INTO `fb_user_likes` (`segment`, `fb_user_id`, `fb_fan_page_id`, `create_time`, `modify_time`) VALUES ('$segment', '$fb_user_id', '$fb_fan_page_id', '$now', '$now')".'<br>';
            $link->query($insert_sql);
        }
    }
    fclose($file);
}
?>