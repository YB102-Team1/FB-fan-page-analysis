<?php
class FbUserLikesGod extends DataModelGod
{

    /**
     * inherited variables:
     *
     * protected $db_obj;
     * protected $table_name;
     */

    /**
     * inherited functions:
     *
     * public function getAll() {}
     * public function getDataCount() {}
     * public function getMaxId() {}
     * public function check($instance_property, $undeleted_only = false) {}
     * public function create($class_property_array) {}
     */

    function getDistinctFanPageId($start=0, $length=1) 
    {

        $sql = "SELECT DISTINCT fb_fan_page_id FROM $this->table_name LIMIT $start, $length";

        $return_array = array();
        $result = $this->db_obj->select($sql);
        foreach ($result as $data) {
            array_push($return_array, $data['fb_fan_page_id']);
        }

        return $return_array;

    }// end function getDistinctFanPageId

}// end class FbUserLikesGod
?>