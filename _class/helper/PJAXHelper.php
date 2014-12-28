<?php
class PJAXHelper {

    public static function isPJAX() {

        if (   array_key_exists('HTTP_X_PJAX', $_SERVER)
            && $_SERVER['HTTP_X_PJAX'] === 'true'
        ) {

            return true;

        } else {// end if(...)

            return false;

        }// end if(...) else

    }// end function isPJAX

    public static function getPJAXContainer() {

        return $_SERVER['HTTP_X_PJAX_CONTAINER'];

    }// end function getPJAXContainer

    public static function run($page_title, $file_path) {

        if (self::isPJAX() && self::getPJAXContainer() == '#main-section') {

            echo "<title>$page_title</title>\n";
            include VIEW_ROOT.$file_path;

        } else {

            $view_path = VIEW_ROOT.$file_path;
            include LAYOUT_ROOT.'/main-layout.php';

        }

    }// end function run

}// end class PJAXHelper
?>