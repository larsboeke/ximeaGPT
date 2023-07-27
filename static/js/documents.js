const searchButton = document.querySelector("#search-btn");
const searchId = document.querySelector("#searchbar-id");
const searchType = document.querySelector("#searchbar-type");
const searchSource = document.querySelector("#searchbar-source");
const searchContent = document.querySelector("#searchbar-content");
const setLimit = document.querySelector("#searchbar-limit");
const searchOutput = document.querySelector(".search-output");
const deleteChunkButton = document.querySelector(".delete-chunk-btn");
const socket = io.connect();

searchButton.addEventListener("click", () => {
    searchOutput.hasChildNodes() ? searchOutput.innerHTML = "": null;
    console.log("You are searching for ....", searchId.value, searchType.value, searchSource.value, searchContent.value, setLimit.value);
    socket.emit('search_doc', searchId.value, searchType.value, searchSource.value, searchContent.value, setLimit.value);
    const searchOptions = [searchId, searchType, searchSource, searchContent, setLimit];
    searchOptions.forEach(input => {input.value = '';
                                    input.disabled = false;});
});

socket.on('searched_doc', (docs) =>{
    console.log("Your searched docs", docs);
    if (docs.length !== 0){
        for (let i = 0; i < docs.length; i++){
            console.log("Your doc", docs[i]);
            const liElement = document.createElement("li");
            liElement.innerHTML = `<div id = "${docs[i]._id}" class="title-with-buttons">
                                        <h2>Chunk ID: ${docs[i]._id}</h2>
                                        <button class="delete-chunk-btn" onclick=deleteChunk(this)>Delete chunk</button>
                                    </div>
                                    <details>
                                        <summary>View details</summary>
                                        <p>Content:  ${docs[i].content}</p>
                                        <p>Type: ${docs[i].metadata.type}</p>
                                        <p>Source ID: ${docs[i].metadata.source_id}</p>
                                        <p>Order ID: ${docs[i].metadata.order_id}</p>
                                    </details>
                                    </div>`;
            searchOutput.appendChild(liElement);
        }           
    }
    else {
        searchOutput.textContent = "Nothing is found..."
    }
});


document.addEventListener("input", () => {
    //the search is either by id alone or other properties of a document
    const extendedSearch = [searchType, searchSource, searchContent, setLimit];
    searchId.value.trim()?extendedSearch.forEach(input => input.disabled = true):extendedSearch.forEach(input => input.disabled = false);
    extendedSearch.some(input => input.value.trim())?searchId.disabled = true:searchId.disabled = false;
});


const deleteChunk = (deleteChunkButton) =>{
    var chunk_id = deleteChunkButton.parentElement.id; 
    console.log('You deleted chunk with id', chunk_id);
    const deletedChunk = document.getElementById(chunk_id);
    deletedChunk.parentElement.remove();
    socket.emit('delete_chunk', chunk_id);
}
