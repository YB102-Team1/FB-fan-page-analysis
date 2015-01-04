<?php
class SiteHelper {

    public static function getNavBar($type, $url) {

        switch ($type) {

        case 'tool':
            $nav_array = array(
                "PHP Test" => "/tool/php-test.php",
                "Table" => array(
                    "Create Table" => "/tool/create-table.php",
                    "Export Table" => "/tool/export-table.php",
                    "Import Table" => "/tool/import-table.php"
                ),
                "Data" => array(
                    "Export Data" => "/tool/export-data.php",
                    "Sync Data" => "/tool/sync-data.php"
                ),
                "PHP Info" => "/tool/phpinfo.php"
            );
            break;

        }// end switch ($type)

        include COMPONENT_ROOT.'/navbar.php';

    }// end function getNavBar

}// end class SiteHelper
?>