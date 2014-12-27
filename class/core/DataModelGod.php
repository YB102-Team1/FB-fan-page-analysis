<?php
abstract class DataModelGod {

    protected $db_obj;
    protected $table_name;

    public function __construct() {

        // intialize basic variables
        $this->db_obj = new DatabaseAccess();
        $this->table_name = strtolower(
            preg_replace('/([^\s])([A-Z])/',
            '\1_\2',
            str_replace('God', '', get_class($this)))
        );

    }// end function __construct

    public function getAll() {

        $sql = "SELECT * FROM $this->table_name";
        return $this->db_obj->select($sql);

    }// end function getAll

    public function getMaxId() {

        $max_id = 0;
        $sql = "SELECT MAX(id) max_id FROM $this->table_name";
        $result = $this->db_obj->select($sql);

        foreach ($result as $data) {

            $max_id = $data['max_id'];

        }// end foreach ($result as $data)

        return $max_id;

    }// end function getMaxId

    public function getInstanceId($property_array, $ignore_deleted = true) {

        $instance_id = 0;

        if ($ignore_deleted) {

            $sql = "SELECT id FROM $this->table_name WHERE is_deleted = 0 ";

        } else {// end if ($ignore_deleted)

            $sql = "SELECT id FROM $this->table_name WHERE 1 ";

        }// end if ($ignore_deleted) else

        foreach ($property_array as $property_key => $property_value) {

            $sql .= "AND $property_key = '$property_value' ";

        }// end foreach ($property_array as $property_key => $property_value)

        $result = $this->db_obj->select($sql);

        foreach ($result as $data) {

            $instance_id = $data['id'];

        }// end foreach ($result as $data)

        return $instance_id;

    }// end function getInstanceId

    public function create($class_property_array) {

        $now = date('Y-m-d H:i:s');

        $sql = "INSERT INTO $this->table_name ";
        $value_list = "";

        foreach ($class_property_array as $property_key => $property_value) {

            switch ($property_key) {

            case 'id':
            case 'is_deleted':
            case 'create_time':
            case 'modify_time':
            case 'delete_time':
                break;

            default:
                $sql .= "$property_key, ";
                $value_list .= "'$property_value', ";
                break;

            }

        }// end foreach ($class_property_array as $property_key => $property_value)

        $sql .= " create_time VALUES $value_list '$now'";

        return $this->db_obj->insert($sql);

    }// end function create

    public function __destruct() {

        $this->db_obj->close();
        unset($this->table_name);

    }// end function __destruct

}// end class DataModelGod
?>