<div class="navbar navbar-inverse navbar-fixed-top">
    <div class="navbar-inner">
        <ul class="nav">
            <?php
            foreach ($nav_array as $page_title => $page_url) {

                if (is_array($page_url)) {

                    if (in_array($url, $page_url)) {
            ?>
            <li class="dropdown active">
                <a class="dropdown-toggle" data-toggle="dropdown"><?php echo $page_title; ?> <b class="caret"></b></a>
                <ul class="dropdown-menu">
                    <?php
                        foreach ($page_url as $sub_page_title => $sub_page_url) {

                            if ($sub_page_url == $url) {
                    ?>
                    <li class="active"><a><?php echo $sub_page_title; ?></a></li>
                    <?php
                            } else {// end if ($sub_page_url == $url)
                    ?>
                    <li><a href="<?php echo $sub_page_url; ?>"><?php echo $sub_page_title; ?></a></li>
                    <?php
                            }// end if ($sub_page_url == $url) else

                        }// end foreach ($page_url as $sub_page_title => $sub_page_url)
                    ?>
                </ul>
            </li>
            <?php
                    } else {// end if (in_array($page_url, $page_url))
            ?>
            <li class="dropdown">
                <a class="dropdown-toggle" data-toggle="dropdown"><?php echo $page_title; ?> <b class="caret"></b></a>
                <ul class="dropdown-menu">
                    <?php
                        foreach ($page_url as $sub_page_title => $sub_page_url) {
                    ?>
                    <li><a href="<?php echo $sub_page_url; ?>"><?php echo $sub_page_title; ?></a></li>
                    <?php
                        }// end foreach ($page_url as $sub_page_title => $sub_page_url)
                    ?>
                </ul>
            </li>
            <?php
                    }// end if (in_array($url, $page_url)) else

                } else if ($page_url == $url) {// end if (is_array($page_url))
            ?>
            <li class="active"><a><?php echo $page_title; ?></a></li>
            <?php
                } else {// end if (...) else if ($page_url == $url)
            ?>
            <li><a href="<?php echo $page_url; ?>"><?php echo $page_title; ?></a></li>
            <?php
                }// end if (...) else if ($page_url == $url) else

            }// end foreach ($nav_array as $page_title => $page_url)
            ?>
        </ul>
    </div>
</div>