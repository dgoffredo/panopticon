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

// Launch the status indicator UI (a popup window) having the specified options.
function launchStatusIndicator(options) {
    const {
        width,
        height,
        left,
        top
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

// Fill the specified <form> DOM element's inputs with the specific object of
// settings, where the properties of the object correspond to the names of
// <input>s within the form.
function fillPopupSettingsForm(popupSettingsForm, popupSettings) {
    const elements = popupSettingsForm.elements;
    ['width', 'height', 'left', 'top'].forEach(function (property) {
        if (property in popupSettings) {
            elements[property].value = popupSettings[property];
        }
    });
    elements['openAutomatically'].checked = popupSettings.openAutomatically || false;
}

// event handler for when the user submits the form of popup launch settings,
// to launch the status indicator popup UI
async function onPopupSettingsFormSubmit (event) {
    event.preventDefault(); // don't submit -- I'll do it in javascript

    const form = event.target;
    const endpoint = form.action;

    console.log(form);

    // Save the launch-related settings by POSTing to the server, and then use
    // the returned JSON parameters to open the popup (the parameters will be
    // consistent with the values in the submitted form).
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            body: new URLSearchParams(new FormData(form))
        });
        const bodyJson = await response.json();
        console.log('POST /launch response: ', bodyJson);
        // here's where the popup happens
        launchStatusIndicator(bodyJson);
        // fill blank <input>s with defaults from the server
        fillPopupSettingsForm(form, bodyJson);
    }
    catch (error) {
        console.error(error);
        alert('Error submitting form. See log.\n' + error);
    }
}

// When the DOM is loaded enough for us to play with <form>s, fetch configured
// <input> values from the server and set up submission handlers.
document.addEventListener('DOMContentLoaded', async function () {
    const popupSettingsForm = document.forms['launchPopup'];

    // Populate the "launch popup" settings form with the current settings
    // from the server.
    // It would be cleaner to have this pre-populated from the initial GET,
    // but then the server would have to do more than serve a static file.
    // Instead, this.
    const response = await fetch('/launch');
    const popupSettings = await response.json();
    console.log('GET /popup response: ', popupSettings);
    fillPopupSettingsForm(popupSettingsForm, popupSettings);
    if (popupSettings.openAutomatically) {
        launchStatusIndicator(popupSettings);
    }

    // Set a handler for the "Launch Popup" form's submission.
    popupSettingsForm.addEventListener('submit', onPopupSettingsFormSubmit);
});
