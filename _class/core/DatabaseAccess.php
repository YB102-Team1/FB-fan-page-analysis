<?php
class DatabaseAccess {

   private $link;

   public function __construct() {

      include DB_CONFIG_FILE;

      $this->link = new mysqli($database_host , $database_user, $database_password, $database_name);
      $this->link->query("SET time_zone='+8:00'");
      $this->link->query("SET NAMES UTF8");

   }// end function __construct

   public function getAllTables() {

      include DB_CONFIG_FILE;

      $sql = "SHOW TABLES FROM $database_name";
      $query_instance = $this->link->query($sql);
      $table_array = array();

      foreach ($query_instance as $instance_data) {

         array_push($table_array, $instance_data['Tables_in_'.strtolower($database_name)]);

      }// end foreach ($query_instance as $instance_data)

      return $table_array;

   }// end function getAllTables

   public function insert($sql) {

      $query = $this->link->query($sql);
      if (!$query) {

         return array("error" => $this->link->error);

      } else { // end if (!$query)

         return $this->link->insert_id;

      }// end if (!$query) else

   }// end function insert

   public function select($sql) {

      $query = $this->link->query($sql);
      if (!$query) {

         return array("error" => $this->link->error);

      } else {// end if (!$query)

         return $query;

      }// end if (!$query) else

   }// end function select

   public function update($sql) {

      $query = $this->link->query($sql);
      if (!$query) {

         return array("error" => $this->link->error);

      } else { // end if (!$query)

         return $this->link->affected_rows;

      }// end if (!$query) else

   }// end function update

   public function delete($sql) {

      $query = $this->link->query($sql);
      if (!$query) {

         return array("error" => $this->link->error);

      } else { // end if (!$query)

         return $this->link->affected_rows;

      }// end if (!$query) else

   }// end function delete

   public function query($sql) {

      $query = $this->link->query($sql);
      if (!$query) {

         return array("error" => $this->link->error);

      } else { // end if (!$query)

         return true;

      }// end if (!$query) else

   }// end function query

   public function __destruct() {

      $this->link->close();

   }// end function __destruct

}// end of class DatabaseAccess
?>