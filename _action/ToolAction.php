<?php
class ToolAction {

    public function post($segments) {

        $action_id = $segments[0];

        switch ($action_id) {

        case 'create-model':

            $table_name = $_POST['table_name'];
            $column_array = array();

            foreach ($_POST as $key => $value) {

                switch ($key) {

                case 'table_name':
                case 'default_value_radio':
                    break;

                default:
                    $column_array[$key] = $value;
                    break;

                }// end switch ($key)

            }// end foreach ($_POST as $key => $value)

            $create_table = ModelHelper::createTable($table_name, $column_array);
            $create_class = ModelHelper::createClassFile($table_name, $column_array);
            $create_class_god = ModelHelper::createClassGodFile($table_name);

            if ($create_table && $create_class && $create_class_god) {

                ResponseMessenger::json('success');

            } else {// end if ($create_table && $create_class && $create_class_god)

                ResponseMessenger::json('fail');

            }// end if ($create_table && $create_class && $create_class_god) else

            break;

        case 'export-table':

            $table_list = $_POST['table_list'];
            $table_array = explode(',', $table_list);
            $success_table_array = array();
            $fail_table_array = array();

            foreach ($table_array as $table_name) {

                if (ModelHelper::createSQLFile($table_name)) {

                    array_push($success_table_array, $table_name);

                } else {// end if (ModelHelper::createSQLFile($table_name))

                    array_push($fail_table_array, $table_name);

                }// end if (ModelHelper::createSQLFile($table_name)) else

            }// end foreach ($table_array as $table_name)

            $message = '成功建立 '.count($success_table_array).' 個 SQL 檔案';
            $parameter = array(
                "success"=>implode(', ', $success_table_array),
                "fail"=>implode(', ', $fail_table_array)
            );

            ResponseMessenger::json('success', $message, $parameter);

            break;

        case 'eval-code':

            $code = $_POST['code'];
            include COMPONENT_ROOT.'/tool/eval-code.php';

            break;

        default:
            echo 'Undefined post action';
            break;

        }// end switch ($action_id)

    }// end function post

    public function get($segments) {

        $action_id = $segments[0];

        switch ($action_id) {

        default:
            echo 'Undefined get action';
            break;

        }// end switch ($action_id)

    }// end function get

}// end class ToolAction
?>