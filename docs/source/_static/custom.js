document.addEventListener("DOMContentLoaded", function () {
    var searchBox = document.querySelector("input[type='text'][name='q']");
    if (searchBox) {
        searchBox.setAttribute("placeholder", "Search ToxiChemPy");
    }
});
