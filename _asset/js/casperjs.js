var utils = require('utils');
var fs = require('fs');
var casper = require('casper').create({
    verbose: false,
    logLevel: "debug",
    // clientScripts: [ "js/jquery-1.10.2.min.js", "js/jquery-ui.min.js"],
    pageSettings: {
        loadImages:  false,         // The WebPage instance used by Casper will
        loadPlugins: false,         // use these settings
        userAgent: 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36'
    }
});

// print out all the messages in the headless browser context
casper.on('remote.message', function(msg) {
    this.echo('remote message caught: ' + msg);
});

// print out all the messages in the headless browser context
casper.on("page.error", function(msg, trace) {
    this.echo("Page Error: " + msg, "ERROR");
});

casper.start("http://www.facebook.com/login.php", function() {
    console.log("page loaded");
    // this.test.assertExists('form#login_form', 'form is found');
    this.fill('form#login_form', {
        email: 'samas0120@gmail.com',
        pass:  'xup6u4vu;6'
    }, true);
});

// casper.thenEvaluate(function(){
//    console.log("Page Title " + document.title);
//    console.log("Your name is " + document.querySelector('.headerTinymanName').textContent );
// });

casper.thenOpen('http://www.facebook.com/samas.lin/likes').then(function() {

    var html = this.getHTML();
    utils.dump(html);
    var f = fs.open('result.html', 'w');
    f.write(html);
    f.close();

    // window.setTimeout(function() {

    //     window.setTimeout(function() {
    //         var x = 0, h = 0;
    //         function judge() {
    //             console.log('judge...');
    //             console.log(document.body.scrollHeight);
    //             if (document.body.scrollHeight == h) {
    //                 clearInterval(x);
    //                 console.logÆ('end');
    //                 phantom.exit();
    //             }
    //         }
    //         function scroll() {
    //             console.log('scroll');
    //             h = document.body.scrollHeight;
    //             window.scrollTo(0,h);
    //             setTimeout(judge, 3000);
    //         }
    //         x = setInterval(scroll, 3100);
    //     }, 3000);

    // }, 3000);

});

casper.run();