<?php
class ModelAction {

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

                }//end switch ($key)

            }// end foreach ($_POST as $key => $value)

            $create_table = ModelHelper::createTable($table_name, $column_array);
            $create_class = ModelHelper::createClassFile($table_name, $column_array);
            $create_class_god = ModelHelper::createClassGodFile($table_name);

            if ($create_table && $create_class && $create_class_god) {

                return ResponseMessenger::json('success');

            } else {// end if ($create_table && $create_class && $create_class_god)

                return ResponseMessenger::json('fail');

            }//end if ($create_table && $create_class && $create_class_god) else

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

}// end class ModelAction
?>