<?php
class ModelHelper {

    public static function createTable($table_name, $column_array) {

        $db_obj = new DatabaseAccess();
        $exist_table_array = $db_obj->getAllTables();

        if (!in_array($table_name, $exist_table_array)) {

            $variable_list = "";

            foreach ($column_array as $column_name => $attribute) {

                switch ($column_name) {

                case 'id':
                case 'is_deleted':
                case 'create_time':
                case 'modify_time':
                case 'delete_time':
                    break;

                default:
                    $variable_list .= '`'.$column_name.'` '.$attribute.', ';
                    break;

                }// end switch ($column_name)

            }// end foreach ($column_array as $column_name => $attribute)

            $sql = 'CREATE TABLE IF NOT EXISTS `'.$table_name.'` ( '.
                       '`id` int(11) unsigned NOT NULL, '.
                       $variable_list.
                       '`is_deleted` tinyint(1) unsigned NOT NULL DEFAULT \'0\', '.
                       '`create_time` datetime NOT NULL, '.
                       '`modify_time` datetime NOT NULL DEFAULT \'0000-00-00 00:00:00\', '.
                       '`delete_time` datetime NOT NULL DEFAULT \'0000-00-00 00:00:00\' '.
                   ') ENGINE=InnoDB DEFAULT CHARSET=utf8;';
            $create_result = $db_obj->query($sql);
            $sql = "ALTER TABLE `test_table` ADD PRIMARY KEY (`id`);";
            $primary_key_result = $db_obj->query($sql);
            $sql = "ALTER TABLE `test_table` MODIFY `id` int(11) unsigned NOT NULL AUTO_INCREMENT;";
            $auto_increment_result = $db_obj->query($sql);

            unset($db_obj);

            return $create_result && $primary_key_result && $auto_increment_result;

        } else {// end if (!in_array($table_name, $exist_table_array))

            unset($db_obj);

            return false;

        }// end if (!in_array($table_name, $exist_table_array)) else

    }// end function createTable

    public static function createClassFile($table_name, $column_array) {

        $class_name = str_replace(' ', '', ucwords(str_replace('_', ' ', $table_name)));
        $class_path = CLASS_ROOT.'/model/'.$class_name.'.php';

        if (!file_exists($class_path)) {

            $class_content = str_replace('Class', $class_name, file_get_contents(CLASS_TEMPLATE_FILE));
            $variable_list = "";

            foreach ($column_array as $column_name => $attribute) {

                switch ($column_name) {

                case 'id':
                case 'is_deleted':
                case 'create_time':
                case 'modify_time':
                case 'delete_time':
                    break;

                default:
                    $variable_list .= "    protected \$$column_name;".PHP_EOL;
                    break;

                }// end switch ($column_name)

            }// end foreach ($column_array as $column_name => $attribute)

            return file_put_contents($class_path, str_replace('    #variables#'.PHP_EOL, $variable_list, $class_content));

        } else {// end if (!file_exists($class_path))

            return false;

        }// end if (!file_exists($class_path)) else

    }// end function createClassFile

    public static function createClassGodFile($table_name) {

        $class_name = str_replace(' ', '', ucwords(str_replace('_', ' ', $table_name)));
        $class_god_path = CLASS_ROOT.'/model/'.$class_name.'God.php';

        if (!file_exists($class_god_path)) {

            $class_god_content = str_replace('Class', $class_name, file_get_contents(CLASS_GOD_TEMPLATE_FILE));

            return file_put_contents($class_god_path, $class_god_content);

        } else {// end if (!file_exists($class_god_path))

            return false;

        }// end if (!file_exists($class_god_path)) else

    }// end function createClassGodFile

    public static function createActionFile($type_name) {

        $action_name = str_replace(' ', '', ucwords(str_replace('-', ' ', $type_name)));
        $action_path = CLASS_ROOT.'/'.$class_name.'Action.php';

        if (!file_exists($action_path)) {

            $action_content = str_replace('Type', $action_name, file_get_contents(ACTION_TEMPLATE_FILE));

            return file_put_contents($action_path, $action_content);

        } else {// end if (!file_exists($action_path))

            return false;

        }// end if (!file_exists($action_path)) else

    }// end function createActionFile

    public static function createSQLFile($table_name) {

        $sql_path = ASSET_ROOT.'/sql/'.$table_name.'.sql';

        if (!file_exists($sql_path)) {

            $sql_content = str_replace('???', $table_name, file_get_contents(SQL_TEMPLATE_FILE));
            $db_obj = new DatabaseAccess();
            $column_array = $db_obj->getTableColumns($table_name);
            $column_list = "";
            foreach ($column_array as $column_name => $attribute) {

                $column_list .= "    `$column_name` $attribute,".PHP_EOL;

            }// end foreach ($column_array as $column_name => $attribute)

            return file_put_contents($sql_path, str_replace('    ...'.PHP_EOL, $column_list, $sql_content));

        } else {// end if (!file_exists($sql_path))

            return false;

        }// end if (!file_exists($sql_path)) else

    }// end function createSQLFile

}// end class ModelHelper
?>