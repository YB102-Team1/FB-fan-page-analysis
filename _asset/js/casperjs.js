var utils = require('utils');
var fs = require('fs');
var casper = require('casper').create({
    verbose: false,
    logLevel: "debug",
    viewportSize: {width: 800, height: 10000},
    // clientScripts:  [
    //     'includes/jquery.js',      // These two scripts will be injected in remote
    //     'includes/underscore.js'   // DOM on every request
    // ],
    pageSettings: {
        loadImages:  false,         // The WebPage instance used by Casper will
        loadPlugins: false,         // use these settings
        userAgent: 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7 (.NET CLR 3.5.30729)'
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
    // console.log("page loaded");
    // this.test.assertExists('form#login_form', 'form is found');
    this.fill('form#login_form', {
        email: 'samas0120@gmail.com',
        pass:  'xup6u4vu;6'
    }, true);
}).thenOpen('http://www.facebook.com/samas.lin/likes', function() {
    this.scrollToBottom();
    this.wait(20000, function() {

        var html = this.getHTML();
        // utils.dump(html);
        var f = fs.open('result.html', 'w');
        f.write(html);
        f.close();

    });
}).run();