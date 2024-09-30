setTimeout(function() {
    let alert = document.querySelector('.alert');
    if (alert) {
        alert.classList.remove('show'); // Fade out
        setTimeout(() => alert.remove(), 200); // Remove from DOM
    }
}, 2000); // Auto dismiss after 3 seconds


//for delete note in home page
function deleteNote(noteId) {
    fetch("/delete-note", {
        method:'POST',
        body: JSON.stringify({noteId : noteId}),
        headers : {
            'Content-Type': "application/json"
        }
    }).then((_res)=>{
        window.location.href = "/"
    })    
}

//move focus to next input in vertify otp
function moveFocus(currentInput, nextInputName) {
    if (currentInput.value.length === 1 && nextInputName) {
        document.getElementsByName(nextInputName)[0].focus();
    }
}