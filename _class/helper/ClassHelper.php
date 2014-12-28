<?php
class ClassHelper {

    public static function createModelTable($table_name, $columns_array) {

        include DB_CONFIG_FILE;

        $connection = mysqli_connect($database_host, $database_user, $database_password);

        $variable_list = "";

        foreach ($columns_array as $column => $attributes) {

            switch ($column) {

            case 'id':
            case 'is_deleted':
            case 'create_time':
            case 'modify_time':
            case 'delete_time':
                break;

            default:
                $variable_list .= '    `'.$table_name.'` '.$attributes.', ';
                break;

            }// end switch ($column)

        }// end foreach ($columns_array as $column => $attributes)

        $sql = 'CREATE TABLE IF NOT EXISTS `'.$table_name.'` ( '.
               '    `id` int(11) unsigned NOT NULL, '.
               $variable_list.
               '    `is_deleted` tinyint(1) unsigned NOT NULL DEFAULT \'0\', '.
               '    `create_time` datetime NOT NULL, '.
               '    `modify_time` datetime NOT NULL DEFAULT \'0000-00-00 00:00:00\', '.
               '    `delete_time` datetime NOT NULL DEFAULT \'0000-00-00 00:00:00\' '.
               ') ENGINE=InnoDB DEFAULT CHARSET=utf8;';
        mysqli_query($connection, $sql);
        $sql = "ALTER TABLE `test_table` ADD PRIMARY KEY (`id`);";
        mysqli_query($connection, $sql);
        $sql = "ALTER TABLE `test_table` MODIFY `id` int(11) unsigned NOT NULL AUTO_INCREMENT;";
        mysqli_query($connection, $sql);

    }// end function createModelTable

    public static function createModelFile($table_name, $columns_array) {

        $class_name = str_replace(' ', '', ucwords(str_replace('_', ' ', $table_name)));
        $class_path = CLASS_ROOT.'/model/'.$class_name.'.php';
        $class_content = str_replace('Class', $class_name, file_get_contents(MODEL_TEMPLATE_FILE));

        $variable_list = "";

        foreach ($columns_array as $column => $attributes) {

            switch ($column) {

            case 'id':
            case 'is_deleted':
            case 'create_time':
            case 'modify_time':
            case 'delete_time':
                break;

            default:
                $variable_list .= "    protected \$$column;\n";
                break;

            }// end switch ($column)

        }// end foreach ($columns_array as $column => $attributes)

        return file_put_contents($class_path, str_replace('    #variables#', $variable_list, $class_content));

    }// end function createModelFile

    public static function createModelGodFile($table_name) {

        $class_name = str_replace(' ', '', ucwords(str_replace('_', ' ', $table_name)));
        $god_class_path = CLASS_ROOT.'/model/'.$class_name.'God.php';
        $god_class_content = str_replace('Class', $class_name, file_get_contents(MODEL_TEMPLATE_GOD_FILE));

        return file_put_contents($god_class_path, $god_class_content);

    }// end function createModelGodFile

}
?>