const socket = io.connect();
const textUploadButton = document.querySelector("#text-input-btn");
const text = document.querySelector("#text-input");
const urlUploadButton = document.querySelector("#url-upload-btn");
const url = document.querySelector("#url-input");

textUploadButton.addEventListener("click", () => {
    if (text.value !== ""){
        socket.emit('upload_text', text.value);
        text.value = "";
    }
    else 
    {
        alert("Please type something in");
    }
});

urlUploadButton.addEventListener("click", () => {
    if (url.value !== ""){
        socket.emit('upload_url', url.value);
        url.value = "";
    }
    else 
    {
        alert("Please type something in");
    }
});

// TODO: Anbindung des PDF Uploads ans Frontend implementieren