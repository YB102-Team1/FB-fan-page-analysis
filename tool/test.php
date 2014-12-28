<?php
include $_SERVER['DOCUMENT_ROOT'].'/_config/system_config.inc';

if (!empty($_POST['code'])) {
    $code = $_POST['code'];
}
?>
<!DOCTYPE html>
<html>
    <head>
        <title>PHP Test Page</title>
    </head>
    <body>
        <form method="post" action="test.php">
            &lt;?php<br>
            <textarea name="code" rows="30" style="width: 95%; resize: none; overflow: scroll;"><?php echo $code; ?></textarea><br>
            ?&gt;<br>
            <button type="submit">Run</button>
        </form>
        <hr>
        <div><?php eval($code); ?></div>
    </body>
</html>