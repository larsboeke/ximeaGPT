const socket = io.connect();
const resetAllFeedback = document.querySelector("#reset-all-feedback-btn");
const resetChunkFeedbacks = document.querySelectorAll(".reset-feedback-btn");
const deleteChunks = document.querySelectorAll(".delete-chunk-btn");

/*-- FEEDBACK SECTION -- */

// Remove all Feedback -> no Chunk will be removed from database
resetAllFeedback.addEventListener('click', () => {
    console.log('Reset all feedback');
    socket.emit('reset_all_feedback');
    window.location.href = '/admin/feedback';
});

// Remove single Feedback that represent one chunk -> Chunk wont be removed from database
resetChunkFeedbacks.forEach((resetChunkFeedback) => {
    resetChunkFeedback.addEventListener('click', function() {
        var chunk_id = this.parentElement.id; 
        localStorage.setItem('chunk_id', chunk_id);
        console.log('You reset feedback for chunk with id', chunk_id);
        socket.emit('reset_feedback', chunk_id);
        document.getElementById(chunk_id).parentElement.style.display = "none";
    });
});

// Delete single chunk from database
deleteChunks.forEach((btn) => {
    btn.addEventListener('click', function() {
        var chunk_id = this.parentElement.id; 
        localStorage.setItem('chunk_id', chunk_id);
        console.log('You deleted chunk with id', chunk_id);
        socket.emit('delete_chunk', chunk_id);
    });
});
