<?php
include $_SERVER['DOCUMENT_ROOT'].'/_config/system_config.inc';

if (!empty($_POST['code'])) {
    $code = $_POST['code'];
}
?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />

        <script src="/_asset/js/jquery-ui/js/jquery-1.9.1.min.js"></script>
        <script src="/_asset/js/jquery-ui/js/jquery-ui-1.10.2.custom.min.js"></script>
        <script src="/_asset/js/jquery-form/jquery.form.js"></script>
        <script src="/_asset/js/pjax/pjax.js"></script>
        <script src="/_asset/js/konami/jquery.konami.js"></script>
        <script src="/_asset/js/main.js.php"></script>

        <link href="/_asset/css/bootstrap/css/bootstrap.min.css" type="text/css" rel="stylesheet">
        <link href="/_asset/css/main.css" type="text/css" rel="stylesheet">

        <title>PHP Test Page</title>
    </head>
    <body>
        <form method="post" action="test.php" style="margin-left: 3%;">
            &lt;?php<br>
            <textarea name="code" rows="15" style="width: 94%; resize: none; overflow: scroll;"><?php echo $code; ?></textarea><br>
            ?&gt;<br>
            <button type="submit" class="btn btn-primary">Run</button>
        </form>
        <hr>
        <div><?php eval($code); ?></div>
    </body>
</html>