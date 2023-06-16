const chatInput = document.querySelector("#chat-input");
const sendButton = document.querySelector("#send-btn");
const chatContainer = document.querySelector(".chat-container");
const themeButton = document.querySelector("#theme-btn");
const deleteButton = document.querySelector("#delete-btn");
const uploadButton = document.querySelector("#upload-btn");
const fileInfo = document.querySelector(".file-info");
const newChatButton = document.querySelector("#new-chat-btn");
const history = document.querySelector(".history");
const chatNum = 0;
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

    chatContainer.innerHTML = localStorage.getItem(`chat-history ${chatNum}`) || defaultText;
    //automatic scrolldown
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
}

loadDataFromLocalstorage(); 

const createChatElement = (html, className) => {
    //create new div and apply chat, specified class and set html content of div
    const chatDiv = document.createElement("div");
    chatDiv.classList.add("chat", className)
    chatDiv.innerHTML = html;
    return chatDiv; 
}

const getChatResponse = (aiChatDiv) =>{
    const pElement = document.createElement("p");
    aiChatDiv.querySelector(".chat-details").appendChild(pElement);
    const timeElement = document.createElement("span");
    timeElement.className = "time";
    aiChatDiv.querySelector(".chat-details").appendChild(timeElement);

    const receiveResponse = (msg) => {
        pElement.textContent = msg.trim();
        timeElement.textContent = getCurrentTime();
        aiChatDiv.querySelector(".typing-animation").remove();
        socket.off('backend_message', receiveResponse);
    };

    socket.on('backend_message', receiveResponse);

    socket.on('backend_error', () => {
        pElement.classList.add("error");
        pElement.textContent = "Oops! Something went wrong while retrieving the response. Please try again.";
        aiChatDiv.querySelector(".typing-animation").remove();
        socket.off('backend_message', receiveResponse);
    });
    //saving all chat HTML data as chat-hystory name in local storage
    localStorage.setItem(`chat-history ${chatNum}`, chatContainer.innerHTML)
    //automatic scrolldown
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
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
                    <span onclick="negFeedback" id="thumb-down" class="material-symbols-outlined">thumb_down</span>
                    </div>
                </div>`;
    const aiChatDiv = createChatElement(html, "backend");
    chatContainer.appendChild(aiChatDiv);
    //automatic scrolldown
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    getChatResponse(aiChatDiv);
}

const getCurrentTime = () =>{
    let dateObject = new Date();
    let cDate = dateObject.getDate() + '/' + (dateObject.getMonth() + 1) + '/' + dateObject.getFullYear();
    let cTime = dateObject.getHours() + ":" + dateObject.getMinutes() + ":" + dateObject.getSeconds();
    return cTime + ' ' + cDate;
}

const handleUserMessage = () => {
    if(chatInput.value){
        socket.emit('client_message', chatInput.value);
        const html =`<div class="chat-content">
                        <div class="chat-details">
                            <img src="../static/images/user_logo.png" alt="user-img">
                            <p>${chatInput.value}</p>
                            <span class="time">${getCurrentTime()}</span>
                        </div>
                    </div>`;
        const userChatDiv = createChatElement(html, "client");
        document.querySelector(".default-text")?.remove();
        chatContainer.appendChild(userChatDiv);
        chatInput.value = " " //clear the textarea after sending
        chatInput.style.height = `${initialHeight}px`;
    } 
    showTypingAnimation();
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
}

themeButton.addEventListener("click", () =>{
    document.body.classList.toggle("light-mode");
    localStorage.setItem("theme-color", themeButton.innerText);
    themeButton.innerText = document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";
})

deleteButton.addEventListener("click", () =>{
    //TO-DO: change confirm window to a centered pop-up window
    if(confirm("Are you sure that you want to delete the history of this chat?")){
        localStorage.removeItem(`chat-history ${chatNum}`);
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

newChatButton.addEventListener("click", () => {
    // chatDiv = localStorage.getItem(`chat-history ${chatNum}`);
    // const pElement = document.createElement("p");
    // pElement.textContent = `chat ${chatNum}`
    // history.appendChild(pElement);
    // chatContainer.remove();
    // chatNum++;  
    // console.log(chatNum);
});


// Sidebar Close and Open Button
    /* Set the width of the sidebar to 250px and the left margin of the page content to 250px */
    function openNav() {
        document.getElementById("leftbox").style.width = "250px";
        document.getElementById("chatbox").style.marginLeft = "250px";
    }
    
    /* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
    function closeNav() {
        document.getElementById("leftbox").style.width = "0";
        document.getElementById("chatbox").style.marginLeft = "0";
    }

//TO-DO: New Chat
//Save in Cache -> save in database with id
//Delete old chat
//Move the Chats in the history

const posFeedback = () => {

}

const negFeedback = () => {
    document.getElementById("rightbox").style.width = "250px";
    document.getElementById("chatbox").style.marginRight = "250px";
}

function closeFeedback() {
    document.getElementById("rightbox").style.width = "0";
    document.getElementById("chatbox").style.marginRight = "0";
}