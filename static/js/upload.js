const socket = io.connect();
const textUploadButton = document.querySelector("#text-input-btn");
const text = document.querySelector("#text-input");
const urlUploadButton = document.querySelector("#url-upload-btn");
const url = document.querySelector("#url-input");
const fileuploadButton = document.querySelector("#file-upload-btn");
const selectFile = document.getElementById("fileID");

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

fileuploadButton.addEventListener("click", () => {
    selectFile.click();
});

async function uploadFile(file){
    try{
        const formData = new FormData();
        formData.append("file", file);
        const response = await fetch('upload',{
            method: 'POST',
            body: formData
        });
        if (response.ok){
            console.log("File was uploaded succesfully")
        } else{
            throw new Error(`Error uploading the file: ${response.statusText}`);
        }
    } catch(error){
        console.error('Error', error)
    }
}

selectFile.addEventListener("change", (event) =>{
    const file = event.target.files[0]; // Get the selected file

     if (file && file.type === "application/pdf"){//MIME type
        uploadFile(file);
        console.log("File selected:", file.name);
        console.log("File size:", (file.size / 1024).toFixed(1));
    }
    else{
        alert("Please select a PDF file.")
    }
});




