var x = 0, h = 0;
function judge() {
    console.log('judge...');
    if (document.body.scrollHeight == h) {
        clearInterval(x);
        console.log('end');
    }
}
function scroll() {
    console.log('scroll');
    h = document.body.scrollHeight;
    window.scrollTo(0,h);
    setTimeout(judge, 3000);
}
x = setInterval(scroll, 3100);