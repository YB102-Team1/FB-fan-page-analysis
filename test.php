<?php
include "class/class.inc";
$code = $_POST['code'];
?>
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <form method="post" action="test.php">
        <textarea name="code" rows="10" style=""><?php echo $code; ?></textarea>
        <button type="submit">Run</button>
    </form>
    <div><?php echo eval($code); ?></div>
</body>
</html>