'use strict';

const onClick = (function () {
    let selectedButton;

    return function (button) {
        console.log(button);
        
        // TODO: This just toggles the style. Also do stuff.
        if (button.className === "") {
            button.className = "selected";
            if (selectedButton !== undefined) {
                selectedButton.className = "";
            }
            selectedButton = button;
        }
        else {
            button.className = "";
            selectedButton = undefined;
        }
    };
}());
