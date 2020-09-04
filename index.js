'use strict';

// based off of https://stackoverflow.com/a/12712600
function launchPopup({url, name, width, height, left, top})
{
    const options = Object.entries({
        toolbar: 'no',
        scrollbars: 'no',
        menubar: 'no',
        status: 'no',
        directories: 'no',
        location: 'no',
        width,
        height,
        left,
        top
    }).map(([key, value]) => `${key}=${value}`).join(', ');

    return window.open(url, name, options);
}

function launchStatusIndicator() {
    return launchPopup({
        url: 'popup.html',
        name: 'popup',
        width: 240,
        height: 200,
        left: 0,
        top: 0
    });
}
