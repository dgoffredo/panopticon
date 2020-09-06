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

function launchStatusIndicator(options) {
    const {
        width = 240,
        height = 200,
        left = 0,
        top = 0
    } = options;

    return launchPopup({
        url: 'popup.html',
        name: 'popup',
        width,
        height,
        left,
        top
    });
}

document.addEventListener('DOMContentLoaded', function () {
    // "Launch Popup" form submission hander
    document.forms['launchPopup'].addEventListener('submit', async function (event) {
        event.preventDefault(); // don't submit -- I'll do it in javascript

        const form = event.target;
        const endpoint = form.action;

        console.log(form);

        // Save the launch-related settings by POSTing to the server, and then
        // use the returned JSON parameters to open the popup (the parameters
        // will be consistent with the values in the submitted form).
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                body: new URLSearchParams(new FormData(form))
            });
            const bodyJson = await response.json();
            console.log('POST /popup response: ', bodyJson);
            launchStatusIndicator(bodyJson); // here's where the popup happens
        }
        catch (error) {
            console.error(error);
            alert('Error submitting form. See log.\n' + error);
        }
    });
});
