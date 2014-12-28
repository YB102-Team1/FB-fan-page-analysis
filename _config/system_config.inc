<?php
// time zone setting
date_default_timezone_set('Asia/Taipei');

// error handle
ini_set('display_errors', 1);
error_reporting(E_ERROR | E_WARNING | E_PARSE);

// Exception handler
function exception_handler($exception) {

    echo "Uncaught exception: $exception->getMessage() \n";
    echo "<pre>";
    print_r(debug_backtrace());
    echo "</pre>";

}
set_exception_handler('exception_handler');

// root path
define(SITE_ROOT, $_SERVER['DOCUMENT_ROOT']);
define(ASSET_ROOT, SITE_ROOT.'/_asset');
define(CLASS_ROOT, SITE_ROOT.'/_class');
define(CONFIG_ROOT, SITE_ROOT.'/_config');
define(LAYOUT_ROOT, SITE_ROOT.'/_layout');
define(VIEW_ROOT, SITE_ROOT.'/_view');

// config files path
define(DB_CONFIG_FILE, CONFIG_ROOT.'/database_config.inc');
define(MODEL_TEMPLATE_FILE, CLASS_ROOT.'/template/ModelTemplate.php');
define(MODEL_TEMPLATE_GOD_FILE, CLASS_ROOT.'/template/ModelTemplateGod.php');
define(GLOBAL_VARIABLES_FILE, CONFIG_ROOT.'/global_variables.inc');
define(CLASS_LOADER_FILE, CONFIG_ROOT.'/class_loader.inc');

// include config files
require_once GLOBAL_VARIABLES_FILE;
require_once CLASS_LOADER_FILE;
?>