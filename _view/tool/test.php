<?php
include COMPONENT_ROOT.'/navbar/tool-navbar.php';
?>
<form id="eval-code-form" style="margin: 0 3%;">
    &lt;?php<br>
    <textarea name="code" rows="15" style="width: 99%; resize: none; overflow: scroll; margin-bottom: 0;"></textarea><br>
    ?&gt;<br>
    <button type="submit" class="btn btn-primary">Run</button>
</form>
<hr>
<pre id="eval-block" style="margin: 0 3%;"></pre>
<script>
$(document).ready(function() {

    function evalCodeValidate(formData, jqForm, options) {

        var validate = true;

        if (validate) {

            $('#system-message').html('處理中');
            $('#system-message').show();

        }

        return validate;

    }

    function evalCodeResponse(response, statusText, xhr, $form) {

        $('#eval-block').html(response);

        $('#system-message').html('成功');
        $('#system-message').fadeOut(3000);

    }

    $('#eval-code-form').ajaxForm({

        beforeSubmit: evalCodeValidate,
        success:      evalCodeResponse,
        url: '/action/tool/eval-code',
        type: 'post',
        dataType: 'html'

    });

});
</script>