'use strict';

// When this popup is closing, POST to the server for the record.
window.addEventListener('unload', function () {
    // `sendBeacon` was invented to solve the problem of "I want to send a
    // one-way request to the server on close and I don't want it to be
    // cancelled even though the page is shutting down."
    navigator.sendBeacon('/close');
});

async function postActivity(activityName) {
    try {
        const response = await fetch('/activity', {
            method: 'POST',
            body: JSON.stringify(activityName)
        });
        if (!response.ok) {
            throw Error('POST /activity returned non-ok status ' + response.status);
        }
    }
    catch (error) {
        console.error(error);
        alert('Error POSTing activity status. See log.\n' + error);
    }
}

const onClick = (function () {
    let selectedButton;

    return function (button) {
        console.log('you clicked on:', button);
        
        // Toggle the style of the selected/unselected button (and the
        // previously selected button, if applicable), and then POST the
        // current activity to the server.
        if (button.className === "") {
            button.className = "selected";
            if (selectedButton !== undefined) {
                selectedButton.className = "";
            }
            selectedButton = button;
            postActivity(button.name);
        }
        else {
            button.className = "";
            selectedButton = undefined;
            postActivity('none');
        }
    };
}());
