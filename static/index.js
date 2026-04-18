document.querySelector("form").addEventListener("submit", function () {
    setTimeout(() => {
        document.getElementById("urlInput").value = "";
    }, 100);
})