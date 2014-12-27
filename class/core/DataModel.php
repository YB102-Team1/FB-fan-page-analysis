<?php
abstract class DataModel {

    protected $db_obj;
    protected $table_name;
    protected $id;
    protected $is_deleted;
    protected $create_time;
    protected $modify_time;
    protected $delete_time;

    public function __construct($id) {

        if (empty($id)) {

            throw new Exception('Exception: '.get_class($this).' id is empty.');

        } else {// end if (empty($id))

            // intialize basic variables
            $this->db_obj = new DatabaseAccess();
            $this->id = $id;
            $this->table_name = strtolower(
                preg_replace('/([^\s])([A-Z])/',
                '\1_\2',
                get_class($this))
            );

            // get object data
            $sql = "SELECT * FROM ".$this->table_name." WHERE id = '".$this->id."'";
            $class_property_array = $this->db_obj->select($sql);
            foreach ($class_property_array as $property_key => $property_value) {

                switch ($property_key) {

                case 'id':
                case 'is_deleted':
                case 'create_time':
                case 'modify_time':
                case 'delete_time':
                    break;

                default:
                    $this->$property_key = $property_value;
                    break;

                }// end switch ($property_key)

            }// end foreach ($class_property_array as $property_key => $property_value)

        }// end if (empty($id)) else


    }// end function __construct

    public function __get($key)
    {

        if ($key == 'db_obj') {

            return null;

        } else {// end if ($key == 'db_obj')

            return isset($this->$key) ? $this->$key : null;

        }// end if ($key == 'db_obj') else

    }// end function __get

    public function __set($key, $value)
    {

        if ($key != 'db_obj' || $key != 'table_name') {

            $this->$key = $value;

        }// end if ($key != 'db_obj' || $key != 'table_name')

    }// end function __set

    public function save() {

        $class_property_array = get_object_vars($this);
        $now = date('Y-m-d H:i:s');
        $sql = "UPDATE $this->table_name SET ";

        foreach ($class_property_array as $property_key => $property_value) {

            switch ($property_key) {

            case 'db_obj':
            case 'table_name':
            case 'id':
            case 'is_deleted':
            case 'create_time':
            case 'modify_time':
            case 'delete_time':
                break;

            default:
                $sql .= "$property_key = '$property_value', ";
                break;

            }// end switch($property_key)

        }// end foreach ($class_property_array as $property_key => $property_value)

        $sql .= "modify_time = '$now' WHERE id = '$this->id'";

        return $this->db_obj->update($sql);

    }// end function save

    public function destroy($type = 'mark') {

        $now = date('Y-m-d H:i:s');

        if ($type == 'mark') {

            $sql = "UPDATE $this->table_name SET ".
                   "is_deleted = 1, ".
                   "modify_time = '$now', ".
                   "delete_time = '$now' ".
                   "WHERE id = '$this->id'";

            return $this->db_obj->update($sql);

        } else if ($type == 'clear') {// end if ($type == 'mark')

            $sql = "DELETE FROM $this->table_name WHERE id = '$this->id'";

            return $this->db_obj->delete($sql);

        }// end if ($type == 'mark') else if ($type == 'clear')

    }// end function destroy

    public function recover() {

        $now = date('Y-m-d H:i:s');

        $sql = "UPDATE $this->table_name SET ".
               "is_deleted = 0, ".
               "modify_time = '$now', ".
               "delete_time = '0000-00-00 00:00:00' ".
               "WHERE id = '$this->id'";
        return $this->db_obj->update($sql);

    }// end function recover

    public function __destruct() {

        $class_property_array = get_object_vars($this);

        foreach ($class_property_array as $property_key => $property_value) {

            switch ($property_key) {

            case 'db_obj':
                $this->db_obj->close();
                break;

            default:
                unset($this->$property_key);
                break;

            }// end switch($property_key)

        }// end foreach ($class_property_array as $property_key => $property_value)

    }// end function __destruct

}// end of class DataModel
?>