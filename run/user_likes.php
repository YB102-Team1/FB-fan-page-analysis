<?php
function user_likes($start = 0, $end = 0) {
    $file_prefix = 'user_likes_57613404340_';
    $link = new mysqli('localhost', 'team1', 'yb102', 'YB102_Team1');
    $link->query("SET NAMES UTF8");
    for ($segment = $start; $segment <= $end; $segment++) {
        echo $segment.'<br>';
        $file_path = $_SERVER['DOCUMENT_ROOT'].'/_asset/data/user_likes/purified/'.$file_prefix.sprintf('%05d', $segment).'.csv';
        $file = @fopen($file_path, "r");
        while (!feof($file)) {
            $data_string = fgets($file);
            str_replace("\n", "", $data_string);
            $data_array = explode(',', $data_string);
            if (   count($data_array) >= 2
                && strpos($data_string, 'l.facebook.com') === FALSE
                && strpos($data_string, 'apps.facebook.com') === FALSE
            ) {
                $fb_user_id = $data_array[0];
                $fb_fan_page_id = $data_array[count($data_array) - 1];
                $now = date('Y-m-d H:i:s', time()+25200);
                if ($fb_user_id) {
                    $insert_sql = "INSERT INTO `fb_user_likes` (`segment`, `fb_user_id`, `fb_fan_page_id`, `create_time`, `modify_time`) VALUES ('$segment', '$fb_user_id', '$fb_fan_page_id', '$now', '$now')";
                    $link->query($insert_sql);
                }
            }
        }
        fclose($file);
    }
}

// user_likes(1, 9);
// user_likes(81, 82);
// user_likes(161, 162);
user_likes(241, 241);
// user_likes(321, 321);
// user_likes(401, 402);
?>