<?php
include $_SERVER['DOCUMENT_ROOT'].'/_config/system_config.inc';
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

        <title>Export Table Page</title>
    </head>
    <body>
        <h1 id="system-message"></h1>
        <h4>&nbsp;</h4>
        <form id="export-table-form" class="form-horizontal">
            <input type="hidden" id="table-list" name="table_list" value="" />
            <div class="control-group">
                <label class="control-label" for="table-name">Localhost Table</label>
                <div class="controls">
                    <div class="span2" style="margin-left: 0;">
                        <table class="table table-bordered table-condensed">
                            <thead>
                            </thead>
                            <tbody>
                                <tr class="info">
                                    <td><input type="checkbox" id="table-checkbox-all" /></td>
                                    <td class="span2"><strong>Table</strong></td>
                                </tr>
                                <?php
                                $db_obj = new DatabaseAccess();
                                $exist_table_array = $db_obj->getAllTables();

                                foreach ($exist_table_array as $table_name) {
                                ?>
                                <tr>
                                    <td>
                                        <input type="checkbox" class="table-checkbox" value="<?php echo $table_name; ?>" />
                                    </td>
                                    <td class="input-medium">
                                        <?php echo $table_name; ?>
                                    </td>
                                </tr>
                                <?php
                                }
                                ?>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <div class="control-group">
                <div class="controls">
                    <button type="submit" class="btn btn-primary">Export</button>
                </div>
            </div>
        </form>
    </body>
</html>
<script>
$(document).ready(function() {

    $(document.body).off('change', '#table-checkbox-all');
    $(document.body).on('change', '#table-checkbox-all', function() {

        if ($(this).is(':checked')) {

            $('.table-checkbox:not(:checked)').trigger("click");

        } else {

            $('.table-checkbox:checked').trigger("click");

        }

    });

    $(document.body).off('change', '.table-checkbox');
    $(document.body).on('change', '.table-checkbox', function() {

        var table_list = "";
        $.each($('.table-checkbox:checked'), function() {

            if (table_list.length > 0) {

                table_list += ',';

            }
            table_list += $(this).val();

        });
        $('#table-list').val(table_list);

    });

    function exportTableValidate(formData, jqForm, options) {

        var validate = true;

        if ($('.table-checkbox:checked').length == 0) {

            validate = false;

        }

        if (validate) {

            $('#system-message').html('處理中');
            $('#system-message').show();

        }

        return validate;

    }

    function exportTableResponse(response, statusText, xhr, $form) {

        if (response.status.code == 0) {

            $('#system-message').html(response.message);
            $('#system-message').fadeOut(3000);

        } else {

            $('#system-message').html('失敗');
            $('#system-message').fadeOut(3000);
        }

    }

    $('#export-table-form').ajaxForm({

        beforeSubmit: exportTableValidate,
        success:      exportTableResponse,
        url: '/action/model/export-table',
        type: 'post',
        dataType: 'json'

    });

});
</script>