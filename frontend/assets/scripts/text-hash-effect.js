/**
 * Just a show-off text...
 */

// Get text and wanted value
const showOff = document.querySelector("#show-off");
const finalText = showOff.innerHTML;

// Here's the show-off effect
let index = 0;
let increment = setInterval(() => index++, 300)
let effect = setInterval(() => {
    // End the effect
    if (index == finalText.length) {
        showOff.innerHTML = finalText;
        clearInterval(effect);
        clearInterval(increment);
        return;
    }

    // Generate a noise of random capital letters
    // and add it as remaining letters.
    let noise = String.fromCharCode(
                    ...Array.from({length: finalText.length - index})
                            .map(code => Math.floor(Math.random() * 26) + 65)
                )
    showOff.innerHTML = finalText.slice(0, index) + noise;
}, 70);