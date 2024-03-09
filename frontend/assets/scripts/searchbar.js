/**
 * Search bar
 */

const searchbar = document.querySelector("#searchbar > input");
const searchicon = document.querySelector("#searchbar > img");

searchicon.addEventListener("click", () => {
    if (searchbar.value == "") {
        return;
    }

    window.location = `http://127.0.0.1:8080/search/${searchbar.value}`;
});

searchbar.addEventListener("keydown", event => {
    if (event.key == "Enter" && searchbar.value != "") {
        window.location = `http://127.0.0.1:8080/search/${searchbar.value}`;
    }
});