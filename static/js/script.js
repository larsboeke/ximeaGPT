const chatInput = document.querySelector("#chat-input");
const sendButton = document.querySelector("#send-btn");
const chatContainer = document.querySelector(".chat-container");
const themeButton = document.querySelector("#theme-btn");
const deleteButton = document.querySelector("#delete-btn")
const uploadButton = document.querySelector("#upload-btn")
const fileInfo = document.querySelector(".file-info")
const socket = io.connect('http://localhost:5000');

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/service-worker.js')
            .then((registration) => {
                console.log('Service Worker registered:', registration);
            })
            .catch((error) => {
                console.error('Service Worker registration failed:', error);
            });
    });
}


const initialHeight = chatInput.scrollHeight;

const loadDataFromLocalstorage = () => {
    //localstorage for now, mongobd for later
    const themeColor = localStorage.getItem("theme-color");

    document.body.classList.toggle("light-mode", themeColor === "light_mode");
    themeButton.innerText = document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";

    const defaultText =`<div class="default-text">
                            <h1>AI:lean Demo</h1>
                            <p>Start a conversation and explore the power of AI.<br> Your chat history will be displayed here.</p>
                        </div>`

    chatContainer.innerHTML = localStorage.getItem("chat-history") || defaultText;
    //automatic scrolldown
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
}

loadDataFromLocalstorage(); 

const createElement = (html, className) => {
    //create new div and apply chat, specified class and set html content of div
    const chatDiv = document.createElement("div");
    chatDiv.classList.add("chat", className)
    chatDiv.innerHTML = html;
    return chatDiv; 
}

const getChatResponse = async(aiChatDiv) =>{

    const pElement = document.createElement("p");
    //TO-DO: here POST request, define properties 
    try {
        //const response = await(await fetch(API_URL, requestOptions)).json();
        const response1 = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua";
        pElement.textContent = response1.trim();

    } catch(error){
        pElement.classList.add("error");
        pElement.textContent ="Ooops! Something went wtrong while retrievig the response.Please try again.";
    }

    aiChatDiv.querySelector(".typing-animation").remove();
    aiChatDiv.querySelector(".chat-details").appendChild(pElement);
    //automatic scrolldown
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    //saving all chat HTML data as chat-hystory name in local storage
    //TO-DO: saving in MongoDB?
    localStorage.setItem("chat-history", chatContainer.innerHTML)
}

const copyResponse = (copyBtn) => {
    // Copy the ai response to the clipboard
    const responseTextElement = copyBtn.parentElement.previousElementSibling.querySelector("p");
    navigator.clipboard.writeText(responseTextElement.textContent);
    copyBtn.textContent = "done";
    setTimeout(() => copyBtn.textContent = "content_copy", 1000);
}

const showTypingAnimation = () => {
    const html =`<div class="chat-content">
                    <div class="chat-details">
                        <img src="../static/images/gpt_logo.png" alt="chatbot-img">
                        <div class="typing-animation">
                            <div class="typing-dot" style="--delay: 0.2s"></div>
                            <div class="typing-dot" style="--delay: 0.3s"></div>
                            <div class="typing-dot" style="--delay: 0.4s"></div>
                         </div>
                    </div>
                    <div class="chat-controls">
                    <span onclick="copyResponse(this)" class="material-symbols-rounded">content_copy</span>
                    <!--TO-DO:Feedback buttons onclick functionality-->
                    <span id="thumb-up" class="material-symbols-outlined">thumb_up</span>
                    <span id="thumb-down" class="material-symbols-outlined">thumb_down</span>
                    </div>
                </div>`;
    const aiChatDiv = createElement(html, "backend");
    chatContainer.appendChild(aiChatDiv);
    //automatic scrolldown
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    //getChatResponse(aiChatDiv);
}

const handleUserMessage = () => {
    if(chatInput.value){
        socket.emit('client_message', chatInput.value);
        const html =`<div class="chat-content">
                    <div class="chat-details">
                        <img src="../static/images/user_logo.png" alt="user-img">
                        <p>${chatInput.value}</p>
                    </div>
                </div>`;
        const userChatDiv = createElement(html, "client");
        document.querySelector(".default-text")?.remove();
        chatContainer.appendChild(userChatDiv);
        chatInput.value = " " //clear the textarea after sending
        chatInput.style.height = `${initialHeight}px`;
    } 

    socket.on('backend_message', (msg) => {
        const pElement = document.createElement("p");
        pElement.textContent = msg.trim();
        const html =`<div class="chat-content">
                    <div class="chat-details">
                        <img src="../static/images/gpt_logo.png" alt="chatbot-img">
                        <div class="typing-animation">
                            <div class="typing-dot" style="--delay: 0.2s"></div>
                            <div class="typing-dot" style="--delay: 0.3s"></div>
                            <div class="typing-dot" style="--delay: 0.4s"></div>
                         </div>
                    </div>
                    <div class="chat-controls">
                    <span onclick="copyResponse(this)" class="material-symbols-rounded">content_copy</span>
                    <!--TO-DO:Feedback buttons onclick functionality-->
                    <span id="thumb-up" class="material-symbols-outlined">thumb_up</span>
                    <span id="thumb-down" class="material-symbols-outlined">thumb_down</span>
                    </div>
                </div>`;
        const aiChatDiv = createElement(html, "backend");
        chatContainer.appendChild(aiChatDiv);
        aiChatDiv.querySelector(".typing-animation").remove();
        aiChatDiv.querySelector(".chat-details").appendChild(pElement);
        chatContainer.scrollTo(0, chatContainer.scrollHeight);
    });  
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    //setTimeout(showTypingAnimation,500);
}

themeButton.addEventListener("click", () =>{
    document.body.classList.toggle("light-mode");
    localStorage.setItem("theme-color", themeButton.innerText);
    themeButton.innerText = document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";
})

deleteButton.addEventListener("click", () =>{
    //TO-DO: change confirm window to a centered pop-up window
    if(confirm("Are you sure that you want to delete the history of this chat?")){
        localStorage.removeItem("chat-history");
        fileInfo.remove();
        loadDataFromLocalstorage();
    }
});

uploadButton.addEventListener("change", (event)=> {
    const file = event.target.files[0]; // Get the selected file

     if (file && file.type === "application/pdf"){//MIME type  
        const formData = new FormData(); // Create a new FormData instance 
        formData.append("file", file); // Append the file to the form data

        uploadFile(file);

        console.log("File selected:", file.name);
        console.log("File size:", (file.size / 1024).toFixed(1));

        //TO-DO: only one file can be selected.

        const infoElement = document.createElement('p');
        infoElement.textContent = `${file.name}`;
        fileInfo.append(infoElement)
    }
    else{
        alert("Please select a PDF file.")
    }
})

async function uploadFile(file){
    try{
        const response = await fetch('upload',{
            method: 'POST',
            body: formData
        });
        if (response.ok){
            const infoElement = document.createElement('p');
            infoElement.textContent = `${file.name}`;
            fileInfo.append(infoElement)
            console.log("File was uploaded succesfully")
        } else{
            throw new Error(`Error uploading the file: ${response.statusText}`);
        }
    } catch(error){
        console.error('Error', error)
    }
}


//Adjustig the textarea hight to fit the content
chatInput.addEventListener("input", () =>{
    chatInput.style.height = `${initialHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;

});

//send message using Enter key ad Shift+Enter to go to a new line
chatInput.addEventListener("keydown", (e) => {
    if(e.key === "Enter" && !e.shiftKey && window.innerWidth > 800){
        e.preventDefault();
        handleUserMessage();
    }  
})

sendButton.addEventListener("click", handleUserMessage);