<?php
include COMPONENT_ROOT.'/navbar/tool-navbar.php';
?>
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
        url: '/action/tool/export-table',
        type: 'post',
        dataType: 'json'

    });

});
</script>