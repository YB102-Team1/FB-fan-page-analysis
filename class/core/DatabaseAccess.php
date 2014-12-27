<?php
class DatabaseAccess {

   private $link;

   public function __construct()
   {

      $this->link = new mysqli('127.0.0.1', 'samas', 'xup6u4vu;6');
      $this->link->query("SET time_zone='+8:00'");
      $this->link->query("SET NAMES UTF8");
      $this->link->select_db('YB102_Team1');

   } // end function __construct

   public function insert($sql)
   {

      $query = $this->link->query($sql);
      if (!$query) {

         return array("error" => "insert error");

      } else { // end if (!$query)

         return $query->insert_id;

      } // end if (!$query) else

   } // end function insert

   public function select($sql)
   {

      $query = $this->link->query($sql);
      if (!$query) {

         return array("error" => "select error");

      } else { // end if (!$query)

         return $query->fetch_all();

      } // end if (!$query) else

   } // end function select

   public function update($sql)
   {

      $query = $this->link->query($sql);
      if (!$query) {

         return array("error" => "update error");

      } else { // end if (!$query)

         return $query->affected_rows;

      } // end if (!$query) else

   } // end function update

   public function delete($sql)
   {

      $query = $this->link->query($sql);
      if (!$query) {

         return array("error" => "delete error");

      } else { // end if (!$query)

         return $query->affected_rows;

      } // end if (!$query) else

   } // end function delete

   public function __destruct()
   {

      $this->link->close();

   } // end function __destruct

} // end of class DatabaseAccess
?>