const chatInput = document.querySelector("#chat-input");
const sendButton = document.querySelector("#send-btn");
const chatContainer = document.querySelector(".chat-container");
const themeButton = document.querySelector("#theme-btn");
const deleteButton = document.querySelector("#delete-btn");
const newChatButton = document.querySelector("#new-chat-btn");
const history = document.querySelector(".history");
const socket = io.connect();
const thumbDown = document.querySelector("#thumb-down");
const chatList = document.getElementById("chat-list");
const sourcesHeaders = document.getElementsByClassName("header");
const sourcesContents = document.getElementsByClassName("content");
const icons = document.getElementsByClassName("icon");
const logoutButton = document.querySelector("#logout-btn");



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
    newChatButton.disabled = true;
    chatInput.disabled = false;
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

const rateChunk = (thumbDown) =>{
    thumbDown.style.color = "#b12727";
    var chunk_id = thumbDown.parentElement.id;
    localStorage.setItem('chunk_id', chunk_id);
    console.log('You rated chunk with id', chunk_id);
    socket.emit('rate_chunk', chunk_id);
}

const showSources = (sources) => {
    let html_sources = `<section id="accordion">`;
    for (let i = 0; i < sources.length; i++){
        html_sources += `<div class="menu">
                                <div class="header">
                                    <div class="title"> &#128161 Source ${i+1}</div>
                                     <span class="icon">&#x2228</span>
                                </div>`;
        if (sources[i].metadata.type == "manuals"){
            html_sources += `<div id="${sources[i].id}" class="content">
                                <b>From ${sources[i].metadata.type}</b><br>
                                <a href="${sources[i].metadata.source_id}">${sources[i].metadata.source_id}</a>
                                <br><br>${sources[i].content}
                                <span onclick="rateChunk(this)" id="thumb-down" class="material-symbols-outlined">thumb_down</span>
                            </div>`;
        }
        else if (sources[i].metadata.type == "ticket"){
            html_sources += `<div id="${sources[i].id}" class="content">
                                <b>From ${sources[i].metadata.type} with TicketID ${sources[i].metadata.source_id}</b><br>
                                <br><br>${sources[i].content}
                                <span onclick="rateChunk(this)" id="thumb-down" class="material-symbols-outlined">thumb_down</span>
                            </div>`;
        }
        else if (sources[i].metadata.type == "email"){
            html_sources += `<div id="${sources[i].id}" class="content">
                                <b>From ${sources[i].metadata.type} with CaseID ${sources[i].metadata.source_id}</b><br>
                                <br><br>${sources[i].content}
                                <span onclick="rateChunk(this)" id="thumb-down" class="material-symbols-outlined">thumb_down</span>
                            </div>`;
        }      
    }
    html_sources += `</div></section>`;
    const sourceChatDiv = createChatElement(html_sources, "backend");
    chatContainer.appendChild(sourceChatDiv);
    for (let i = 0; i < sourcesHeaders.length; i++) {
        sourcesHeaders[i].addEventListener("click", () => {
            sourcesContents[i].style.display = sourcesContents[i].style.display == "block" ? "none" : "block";
            icons[i].innerHTML = sourcesContents[i].style.display == "block" ? "&#x2227" : "&#x2228";
            sourcesContentsContainer.scrollTo(0, sourcesContents.scrollHeight);
        });
    }
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
}


const getChatResponse = (aiChatDiv) =>{
    const pElement = document.createElement("p");
    aiChatDiv.querySelector(".chat-details").appendChild(pElement);
    const timeElement = document.createElement("span");
    timeElement.className = "time";
    aiChatDiv.querySelector(".chat-details").appendChild(timeElement);

    const receiveResponse = (data) => {
        console.log("getChatResponse: receiveResponse: received!")
        backend_msg = data['assistant_message'];
        sources = data['sources'];
        pElement.textContent = backend_msg.trim();
        if (sources.length !== 0){
            console.log('getChatResponse: receiveResponse: You have following sources:', sources);
            showSources(sources);            
        }
        else{
            console.log('There are no additional sources');            
        }
        let timestamp = new Date();
        timeElement.textContent = parseTime(timestamp);
        aiChatDiv.querySelector(".typing-animation").remove();
        chatInput.disabled = false;
        socket.off('receive_response', receiveResponse);
    };
    socket.on('receive_response', receiveResponse);
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
    chatInput.disabled = true;
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
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    //automatic scrolldown
    getChatResponse(aiChatDiv);
    
}

const parseTime = (timestamp) =>{
    //2023-07-04T11:19:16.115000 in 12:12:42 [4 Aug 2023]
    let dateObject = new Date(timestamp);
    let months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    let cDate = '[' + dateObject.getDate() + ' ' + months[dateObject.getMonth() + 1] + ' ' + dateObject.getFullYear() + ']';
    let cTime =  dateObject.getHours() + ":" + dateObject.getMinutes().toString().padStart(2,'0') + ":" + dateObject.getSeconds().toString().padStart(2,'0');
    return cTime + ' ' + cDate;
};

const startNewChat = (userMessage) => {
    chatContainer.innerHTML = "";
    var userId = localStorage.getItem("username");
    socket.emit('start_chat', userId, userMessage);
    socket.on('chat_started', (data) =>{
        chat_id = data['chat_id']
        title = data['title']
        localStorage.setItem('chat_id', chat_id);
        var newChat = document.createElement('li');
        chatList.prepend(newChat);
        newChat.id = chat_id;
        newChat.textContent = title;
        console.log('New chat started with ID:', chat_id); 
        console.log('New chat started with title:', title);
        handleUserMessage();  
    });
    
}


const handleUserMessage = () => {
    userMessage = chatInput.value.trim();
    if (userMessage !==""){
        if (document.querySelector(".default-text")){
            console.log('It you first message! We start new chat');
            startNewChat(userMessage);         
        }
        else{
            var data = {
                'chat_id': localStorage.getItem('chat_id'),
                'text': userMessage
            }
            socket.emit('send_message', data);
            let timestamp = new Date();
            const html =`<div class="chat-content">
                            <div class="chat-details">
                                <img src="../static/images/user_logo.png" alt="user-img">
                                <p>${userMessage}</p>
                                <span class="time">${parseTime(timestamp)}</span>
                            </div>
                        </div>`;
            const userChatDiv = createChatElement(html, "client");
            //document.querySelector(".default-text")?.remove();
            chatContainer.appendChild(userChatDiv);
            chatInput.value = "";
            chatInput.style.height = `${initialHeight}px`;
            showTypingAnimation();
            chatContainer.scrollTo(0, chatContainer.scrollHeight);
            newChatButton.disabled = false;
        }
    }         
    else {
        alert("Please type something in...");
    }   
};

themeButton.addEventListener("click", () =>{
    document.body.classList.toggle("light-mode");
    localStorage.setItem("theme-color", themeButton.innerText);
    themeButton.innerText = document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";
})

deleteButton.addEventListener("click", () =>{
    if(confirm("Are you sure that you want to delete the history of this chat?")){
        var userId = localStorage.getItem('username');
        var chatId = localStorage.getItem('chat_id');
        socket.emit('delete_chat', userId, chatId);
        chatList.removeChild(document.getElementById(chatId));
        localStorage.removeItem('chat-history');
        localStorage.removeItem('chat_id');
        window.location.href = '/';
    }
});

logoutButton.addEventListener("click", () =>{
    if(confirm("Are you sure that you want to logout?")){
        socket.emit('logout');
        localStorage.removeItem('username');
        window.location.href = '/logout'; 
    }
});

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
        const message = messages[i];
        if (message.role == 'user'){
            const html =`<div class="chat-content">
                        <div class="chat-details">
                            <img src="../static/images/user_logo.png" alt="user-img">
                            <p>${message.content}</p>
                            <span class="time">${parseTime(message.timestamp)}</span>
                        </div>
                    </div>`;
            const userChatDiv = createChatElement(html, "client");
            chatContainer.appendChild(userChatDiv);
        }
        else if(message.role == 'assistant'){
            const html =`<div class="chat-content">
                        <div class="chat-details">
                            <img src="../static/images/user_logo.png" alt="chatbot-img">
                            <p>${message.content}</p>
                            <span class="time">${parseTime(message.timestamp)}</span>
                        </div>
                        <div class="chat-controls">
                        <span onclick="copyResponse(this)" id="copy" class="material-symbols-rounded">content_copy</span>
                        </div>
                    </div>`;
            const aiChatDiv = createChatElement(html, "backend");
            chatContainer.appendChild(aiChatDiv);
            if (message.sources.length !== 0){
                showSources(message.sources);
            }
        }
    }
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    newChatButton.disabled = false;
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
});

newChatButton.addEventListener("click", () => {
    window.location.href = '/';
});
    
function openNav() {
    document.getElementById("leftbox").style.width = "250px";
    document.getElementById("chatbox").style.marginLeft = "250px";
}

function closeNav() {
    document.getElementById("leftbox").style.width = "0";
    document.getElementById("chatbox").style.marginLeft = "0";
}
