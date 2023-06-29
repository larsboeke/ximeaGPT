const chatInput = document.querySelector("#chat-input");
const sendButton = document.querySelector("#send-btn");
const chatContainer = document.querySelector(".chat-container");
const themeButton = document.querySelector("#theme-btn");
const deleteButton = document.querySelector("#delete-btn");
const uploadButton = document.querySelector("#upload-btn");
const fileInfo = document.querySelector(".file-info");
const newChatButton = document.querySelector("#new-chat-btn");
const history = document.querySelector(".history");
const socket = io.connect('http://localhost:5000');
const thumbUp = document.querySelector("#thumb-up");
const thumbDown = document.querySelector("#thumb-down");
const chatList = document.getElementById("chat-list");
const sourcesHeaders = document.getElementsByClassName("header");
const sourcesContents = document.getElementsByClassName("content");
const icons = document.getElementsByClassName("icon");
var positiveFeedback = new Boolean(false);
var negativeFeedback = new Boolean(false);



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

const loadDefaultWindow = () => {
    //localstorage for now, mongobd for later
    const themeColor = localStorage.getItem("theme-color");

    document.body.classList.toggle("light-mode", themeColor === "light_mode");
    themeButton.innerText = document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";

    const defaultText =`<div class="default-text">
                            <h1>AI:lean Demo</h1>
                            <p>Start a conversation and explore the power of AI.<br> Your chat history will be displayed here.</p>
                        </div>`
    
    chatContainer.innerHTML = defaultText;
    //automatic scrolldown
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
}

loadDefaultWindow();


const createChatElement = (html, className) => {
    //create new div and apply chat, specified class and set html content of div
    const chatDiv = document.createElement("div");
    chatDiv.classList.add("chat", className)
    chatDiv.innerHTML = html;
    return chatDiv;
}

const showSources = (sources) => {
    const html_sources = `<section id="accordion">
                                    <div class="menu">
                                        <div class="header">
                                            <div class="title"> &#128161 Source 1</div>
                                            <span class="icon">&#x2228</span>
                                        </div>
                                        <div class="content">Content 1</div>
                                    </div>
                                    <div class="menu">
                                    <div class="header">
                                        <div class="title"> &#128161 Source 2</div>
                                        <span class="icon">&#x2228</span>
                                    </div>
                                    <div class="content">Content 2</div>
                                </div>
                                <div class="menu">
                                    <div class="header">
                                        <div class="title"> &#128161 Source 3</div>
                                        <span class="icon">&#x2228</span>
                                    </div>
                                    <div class="content">Content 3</div>
                                </div>
                                   
                             </section>`
    const sourceChatDiv = createChatElement(html_sources, "backend");
    chatContainer.appendChild(sourceChatDiv);
    for (let i = 0; i < sourcesHeaders.length; i++) {
        sourcesHeaders[i].addEventListener("click", () => {
            sourcesContents[i].style.display = sourcesContents[i].style.display == "block" ? "none" : "block";
            icons[i].innerHTML = sourcesContents[i].style.display == "block" ? "&#x2227" : "&#x2228";
        });
    }
}


const getChatResponse = (aiChatDiv) =>{
    const pElement = document.createElement("p");
    aiChatDiv.querySelector(".chat-details").appendChild(pElement);
    const timeElement = document.createElement("span");
    timeElement.className = "time";
    aiChatDiv.querySelector(".chat-details").appendChild(timeElement);

    const receiveResponse = (backend_msg, sources) => {
        pElement.textContent = backend_msg.trim();
        if (sources.length !== 0){
            console.log('You have following sources:', sources);
            showSources(sources);            
        }
        else{
            console.log('There are no additionsl sources');            
        }
        timeElement.textContent = getCurrentTime();
        aiChatDiv.querySelector(".typing-animation").remove();
        socket.off('receive_response', receiveResponse);
    };
    socket.on('receive_response', receiveResponse);
    // TO-DO add a socket.emit('error') on the server side
    socket.on('backend_error', () => {
        pElement.classList.add("error");
        pElement.textContent = "Oops! Something went wrong while retrieving the response. Please try again.";
        aiChatDiv.querySelector(".typing-animation").remove();
        socket.off('receive_response', receiveResponse);
    });
    //saving all chat HTML data(only last chat) as chat-hystory name in local storage
    localStorage.setItem('chat-history', chatContainer.innerHTML)
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
                        <span onclick="copyResponse(this)" id="copy" class="material-symbols-rounded">content_copy</span>
                        <!--TO-DO:Feedback buttons onclick functionality-->
                        <!--<span onclick="posFeedback(this)" id="thumb-up" class="material-symbols-outlined">thumb_up</span>-->
                        <!--<span onclick="openFeedbackBar()" id="thumb-down" class="material-symbols-outlined">thumb_down</span>-->
                    </div>
                </div>`;
    const aiChatDiv = createChatElement(html, "backend");
    chatContainer.appendChild(aiChatDiv);
    showSources(html);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    //automatic scrolldown
    getChatResponse(aiChatDiv);
    
}

socket.on('chat_deleted', (data) =>{
    var deletedChatId = data.chat_id;
    console.log('Chat deleted with ID:', deletedChatId);
})


const getCurrentTime = () =>{
    let dateObject = new Date();
    let months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    let cDate = '[' + dateObject.getDate() + ' ' + months[dateObject.getMonth() + 1] + ' ' + dateObject.getFullYear() + ']';
    let cTime =  dateObject.getHours() + ":" + dateObject.getMinutes().toString().padStart(2,'0') + ":" + dateObject.getSeconds().toString().padStart(2,'0');
    return cTime + ' ' + cDate;
}

const startNewChat = () => {
    chatContainer.innerHTML = "";
    var userId = document.cookie.replace(/(?:(?:^|.*;\s*)ailean_user_id\s*=\s*([^;]*).*$)|^.*$/, "$1");
    var newChat = document.createElement('li');
    newChat.textContent = 'New Chat';
    // chatList.appendChild(newChat);
    chatList.prepend(newChat);
    socket.emit('start_chat', userId);
    socket.on('chat_started', (chat_id) =>{
        localStorage.setItem('chat_id', chat_id);
        console.log('New chat started with ID:', chat_id);
        newChat.textContent = chat_id;
    });
}

const handleUserMessage = () => {
    userMessage = chatInput.value.trim();
    if (userMessage !==""){
        //document.querySelector(".default-text")?.startNewChat();
        if (document.querySelector(".default-text")){
            console.log('It you first message! We start new chat');
            startNewChat();            
        }
        var data = {
            'chat_id': localStorage.getItem('chat_id'),
            'text': userMessage
        }
        socket.emit('send_message', data);
        const html =`<div class="chat-content">
                        <div class="chat-details">
                            <img src="../static/images/user_logo.png" alt="user-img">
                            <p>${userMessage}</p>
                            <span class="time">${getCurrentTime()}</span>
                        </div>
                    </div>`;
        const userChatDiv = createChatElement(html, "client");
        //document.querySelector(".default-text")?.remove();
        chatContainer.appendChild(userChatDiv);
        chatInput.value = "";
        chatInput.style.height = `${initialHeight}px`;
        showTypingAnimation();
        chatContainer.scrollTo(0, chatContainer.scrollHeight);
    } 
    else {
        alert("Please type something in...");
    }   
};
// Add an event listener to the button
// document.getElementById('new-chat-btn').addEventListener('click', function() {
//     // Retrieve the user ID from the stored cookies
//     var userId = document.cookie.replace(/(?:(?:^|.*;\s*)ailean_user_id\s*=\s*([^;]*).*$)|^.*$/, "$1");

//     // Emit the 'start_chat' event to the server with the user ID
//     socket.emit('user_id', userId);
//   });
  
  // Listen for the 'chat_started' event from the server
//   socket.on('chat_started', function(data) {
//     var chatId = data.chat_id;
//     // Handle the newly generated chat ID
//     console.log('New chat started with ID:', chatId);
//   });

themeButton.addEventListener("click", () =>{
    document.body.classList.toggle("light-mode");
    localStorage.setItem("theme-color", themeButton.innerText);
    themeButton.innerText = document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";
})

deleteButton.addEventListener("click", () =>{
    //TO-DO: change confirm window to a centered pop-up window
    if(confirm("Are you sure that you want to delete the history of this chat?")){
        socket.emit('delete_chat', localStorage.getItem('chat_id'));
        localStorage.removeItem('chat-history');
        localStorage.removeItem('chat_id');
        fileInfo.remove();
        loadDefaultWindow(); 
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
});

sendButton.addEventListener("click", handleUserMessage);

const loadChat = (messages) => {
    for (let i = 0; i < messages.length; i++){
        //const message = messages[i]; than doesnt use an index
        if (messages.role[i] == 'user'){
            const html =`<div class="chat-content">
                        <div class="chat-details">
                            <img src="../static/images/user_logo.png" alt="user-img">
                            <p>${messages.content[i]}</p>
                            <span class="time">${messages.time[i]}</span>
                        </div>
                    </div>`;
            const userChatDiv = createChatElement(html, "client");
            chatContainer.appendChild(userChatDiv);
        }
        else if(messages.role[i] == 'assistant'){
            const html =`<div class="chat-content">
                        <div class="chat-details">
                            <img src="../static/images/user_logo.png" alt="chatbot-img">
                            <p>${messages.content[i]}</p>
                            <span class="time">${messages.time[i]}</span>
                        </div>
                    </div>`;
            const aiChatDiv = createChatElement(html, "backend");
            chatContainer.appendChild(aiChatDiv);
            //sourses?
        }
    }
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
};

chatList.addEventListener("click", (event) =>{
    var clickedElement = event.target;
    var chatId = clickedElement.id;
    if (clickedElement.tagName === 'LI') {
        console.log('You clicked on chat:', chatId);
        socket.emit('open_chat', chatId);
        socket.on('chat_opened', (messages) =>{
            chatContainer.innerHTML = '';
            console.log(messages);
            loadChat(messages);
        });
      }
    localStorage.setItem('chat_id', chatId);
    // socket.emit('open_chat', chatId);
    // socket.on('chat_opened', (messages) =>{
    //     console.log(messages);
    // });
});

newChatButton.addEventListener("click", startNewChat);
    
    //chatContainer.innerHTML = '';
//     const historyControlsDiv = document.createElement("div");
//     historyControlsDiv.classList.add("history-controls");
//     history.appendChild(historyControlsDiv);

//     const pElement = document.createElement("p");
//     pElement.textContent = "New Chat Started";
//     historyControlsDiv.appendChild(pElement);
//     console.log('New Chat Started');
//     var userId = document.cookie.replace(/(?:(?:^|.*;\s*)ailean_user_id\s*=\s*([^;]*).*$)|^.*$/, "$1");
//     socket.emit('start_chat', userId);
//     socket.on('chat_started', function(chat_id) {
//     pElement.p = chat_id;
//     console.log('New chat started with ID:', chat_id);
//   });








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

const posFeedback = (thumbUpBtn) => {
    changeColorThumb('up', thumbUpBtn);
}

const negFeedback = (sendFeedbackBtn) => {
    const thumbDownBtn = sendFeedbackBtn.parentElement.parentElement.parentElement.parentElement.previousElementSibling.previousElementSibling.lastElementChild.firstElementChild.lastElementChild.lastElementChild;
    changeColorThumb('downSend', thumbDownBtn);
    //thumbDownBtn.parentElement.parentElement.parentElement.parentElement.previousElementSibling.previousElementSibling.lastElementChildren.firstElementChildren.lastElementChildren.lastElementChildren.);

}

const deleteFeedback = (deleteFeedbackBtn) => {
    const thumbDeleteBtn = deleteFeedbackBtn.parentElement.parentElement.parentElement.parentElement.previousElementSibling.previousElementSibling.lastElementChild.firstElementChild.lastElementChild.lastElementChild;
    changeColorThumb('downDelete', thumbDeleteBtn);
}

function changeColorThumb(thumb, thumbBtn) {

    if(thumb == 'up') {
        if (positiveFeedback == false) {
            thumbBtn.style.color = "#249724";
            positiveFeedback = true;
            if (negativeFeedback == true) {
                thumbBtn.nextElementSibling.style.color = "#ACACBE";
                negativeFeedback = false;
            }
        } else {
            thumbBtn.style.color = "#ACACBE";
            positiveFeedback = false;
        }
    } else if (thumb == 'downSend') {
        thumbBtn.style.color = "#b12727";
        negativeFeedback = true;
        if (positiveFeedback == true) {
            thumbBtn.previousElementSibling.style.color = "#ACACBE";
            positiveFeedback = false;
        }
    } else if (thumb == 'downDelete') {
        thumbBtn.style.color = "#ACACBE";
        thumbBtn.previousElementSibling.style.color = "#ACACBE";
        positiveFeedback = false;
        negativeFeedback = false;
    } else {

    }

}

const openFeedbackBar = () => {
    document.getElementById("rightbox").style.width = "250px";
    document.getElementById("chatbox").style.marginRight = "250px";
}

function closeFeedback() {
    document.getElementById("rightbox").style.width = "0";
    document.getElementById("chatbox").style.marginRight = "0";
}