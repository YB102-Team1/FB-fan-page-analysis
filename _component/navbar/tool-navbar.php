<?php
$page_array = array(
    "PHP Test" => "/tool/test.php",
    "Create Model" => "/tool/model.php",
    "Export Table" => "/tool/table.php",
    "PHP Info" => "/tool/phpinfo.php"
);
?>
<div class="navbar navbar-inverse navbar-fixed-top">
    <div class="navbar-inner">
        <ul class="nav">
            <?php
            foreach ($page_array as $page_title => $page_url) {

                if ($page_url == $file_path) {
            ?>
            <li class="active"><a><?php echo $page_title; ?></a></li>
            <?php
                } else {
            ?>
            <li><a href="<?php echo $page_url; ?>"><?php echo $page_title; ?></a></li>
            <?php
                }

            }// end foreach ($page_array as $page_title => $page_url)
            ?>
        </ul>
    </div>
</div>