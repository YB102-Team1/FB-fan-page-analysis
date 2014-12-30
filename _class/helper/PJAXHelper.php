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

    public static function run($page_title, $file_path, $http_param = array()) {

        if (self::isPJAX() && self::getPJAXContainer() == '#main-section') {

            echo "<title>$page_title</title>";
            include VIEW_ROOT.$file_path;

        } else {// end if (self::isPJAX() && self::getPJAXContainer() == '#main-section')

            $view_path = VIEW_ROOT.$file_path;
            include LAYOUT_ROOT.'/main-layout.php';

        }// end if (self::isPJAX() && self::getPJAXContainer() == '#main-section') else

    }// end function run

}// end class PJAXHelper
?>