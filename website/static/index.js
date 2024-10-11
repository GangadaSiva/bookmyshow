setTimeout(function() {
    let alert = document.querySelector('.alert');
    if (alert) {
        alert.classList.remove('show'); // Fade out
        setTimeout(() => alert.remove(), 200); // Remove from DOM
    }
}, 2000); // Auto dismiss after 3 seconds


//for delete note in home page
function deleteMovie(movieid) {
    if (confirm("Are you sure!")){
        fetch("/admin/movies/delete/", {
            method:'POST',
            body: JSON.stringify({movie_id : movieid}),
            headers : {
                'Content-Type': "application/json"
            }
        }).then((_res)=>{
            window.location.href = "/admin/add"
        })
    }      
}

//delete theater
function deleteTheater(theater_id){
    if(confirm("Are you Sure")){
        fetch("/delete_theater" ,{
            method: 'POST',
            body: JSON.stringify({theater_id: theater_id}),
            headers:{
                'Content-Type': "application/json"
            }
        }).then((_res)=>{
            // window.location.href = "/admin/add"
            location.reload()
        })
    }
}

//delete theater
function deleteShow(show_id){
    if(confirm("Are you sure")){
        fetch("/delete_show",{
            method: "POST",
            body: JSON.stringify({show_id: show_id}),
            headers:{
                'Content-Type':"application/json"
            }
        }).then((_res)=>{
            //window.location.href= "/admin/add"
            location.reload() 
        })
    }
}

//delete seat
function deleteSeat(seat_id){
    if(confirm("Are you sure")){
        fetch("/delete_seat",{
            method: "POST",
            body: JSON.stringify({seat_id : seat_id}),
            headers: {
                'Content-Type': "application/json"
            }
        }).then((_res)=>{
            location.reload()
        })
    }
}





//move focus to next input in vertify otp
function moveFocus(currentInput, nextInputName) {
    if (currentInput.value.length === 1 && nextInputName) {
        document.getElementsByName(nextInputName)[0].focus();
    }
}



function updateMovie(id, title,description, duration, language, release_date, genre) {    
    document.getElementById('movie-id').value = id;
    document.getElementById('new-title').value = title;
    document.getElementById('new-description').value = description;
    document.getElementById('new-duration').value = duration;
    document.getElementById('new-language').value = language;
    document.getElementById('new-release-date').value = release_date;
    document.getElementById('new-genre').value = genre;

    

}

function viewMovie(id, title, description, duration, language, releaseDate, genre) {
    document.getElementById('view-movie-id').value = id;
    document.getElementById('view-new-title').value = title;
    document.getElementById('view-new-description').value = description;
    document.getElementById('view-new-duration').value = duration;
    document.getElementById('view-new-language').value = language;
    document.getElementById('view-new-release-date').value = releaseDate;
    document.getElementById('view-new-genre').value = genre;
}

function updateTheater(movie_id,id, name, location, total_screens) {
    document.getElementById('theater_id').value = movie_id
    document.getElementById('cinema-id').value = id;
    document.getElementById('new-theater-name').value = name;
    document.getElementById('new-location').value = location;
    document.getElementById('new-total-screens').value = total_screens
    
}

function updateShow(movie_id, theater_id,id, screen_number, start_time, end_time, price){
    document.getElementById('movie-id').value = movie_id;
    document.getElementById('theater-id').value = theater_id;
    document.getElementById('screening-id').value = id;
    document.getElementById('new-screen-number').value = screen_number;
    document.getElementById('new-start-time').value = start_time;
    document.getElementById('new-end-time').value = end_time
    document.getElementById('new-price').value = price
}


function updateSeat(id,seat_number){
    document.getElementById('seat-id').value = id;
    document.getElementById('new_seat_number').value = seat_number;
}






function handleScroll(direction){
    gallery = document.getElementById("movieGallery");
    scrollAmount = 500;

    if(direction === "left" ){
        gallery.scrollTo({
            left: gallery.scrollLeft - scrollAmount,
            behavior : 'smooth'
        })
    }else if (direction === "right"){
        gallery.scrollTo({
            left:gallery.scrollLeft +scrollAmount,
            behavior : 'smooth'
        })
    }
} 

function handleiconsScroll(direction){
    image_gallery = document.getElementById('image-gallery');
    scrollAmount = 500;
    if (direction ==='left'){
        image_gallery.scrollTo({
            left: image_gallery.scrollLeft -scrollAmount,
            behavior: 'smooth' 
        })
         
    }else if(direction === 'right'){
        image_gallery.scrollTo({
            left: image_gallery.scrollLeft + scrollAmount,
            behavior : 'smooth'
        })
    }
}




let start1 = document.getElementById("star1")
let start2 = document.getElementById("star2")
let start3 = document.getElementById("star3")
let start4 = document.getElementById("star4")
let start5 = document.getElementById("star5")
let rating = document.getElementById("rating")

rating.addEventListener("input", (e)=>{
    value = e.target.value
    if (value == 1){
        start1.classList.add("text-danger")
        start2.classList.remove("text-danger")
        start3.classList.remove("text-danger")
        start4.classList.remove("text-danger")
        start5.classList.remove("text-danger")
    }
    if(value == 2){
        start1.classList.add("text-danger")
        start2.classList.add("text-danger")
        start3.classList.remove("text-danger")
        start4.classList.remove("text-danger")
        start5.classList.remove("text-danger")
    }
    if(value == 3){
        start1.classList.add("text-danger")
        start2.classList.add("text-danger")
        start3.classList.add("text-danger")
        start4.classList.remove("text-danger")
        start5.classList.remove("text-danger")
    }
    if(value == 4){
        start1.classList.add("text-danger")
        start2.classList.add("text-danger")
        start3.classList.add("text-danger")
        start4.classList.add("text-danger")
        start5.classList.remove("text-danger")
    }
    if(value == 5){
        start1.classList.add("text-danger")
        start2.classList.add("text-danger")
        start3.classList.add("text-danger")
        start4.classList.add("text-danger")
        start5.classList.add("text-danger")
    }

})

start1.addEventListener("click", (e)=>{
    e.preventDefault()
    start1.classList.add("text-danger")
    start2.classList.remove("text-danger")
    start3.classList.remove("text-danger")
    start4.classList.remove("text-danger")
    start5.classList.remove("text-danger")
    rating.value = 1
})
start2.addEventListener("click", (e)=>{
    e.preventDefault()
    start1.classList.add("text-danger")
    start2.classList.add("text-danger")
    start3.classList.remove("text-danger")
    start4.classList.remove("text-danger")
    start5.classList.remove("text-danger")
    rating.value = 2
})
start3.addEventListener("click", (e)=>{
    e.preventDefault()
    start1.classList.add("text-danger")
    start2.classList.add("text-danger")
    start3.classList.add("text-danger")
    start4.classList.remove("text-danger")
    start5.classList.remove("text-danger")
    rating.value = 3
})
start4.addEventListener("click", (e)=>{
    e.preventDefault()
    start1.classList.add("text-danger")
    start2.classList.add("text-danger")
    start3.classList.add("text-danger")
    start4.classList.add("text-danger")
    start5.classList.remove("text-danger")
    rating.value = 4
})
start5.addEventListener("click", (e)=>{
    e.preventDefault()
    start1.classList.add("text-danger")
    start2.classList.add("text-danger")
    start3.classList.add("text-danger")
    start4.classList.add("text-danger")
    start5.classList.add("text-danger")
    rating.value = 5
})






















// const imageGallery = document.getElementById('image-gallery');
// let isDragging = false;
// let startX;
// let scrollLeft;

// imageGallery.addEventListener('mousedown', (e) => {
//   isDragging = true;
//   startX = e.pageX - imageGallery.offsetLeft;
//   scrollLeft = imageGallery.scrollLeft;
//   imageGallery.classList.add('active');
// });

// imageGallery.addEventListener('mouseleave', () => {
//   isDragging = false;
//   imageGallery.classList.remove('active');
// });

// imageGallery.addEventListener('mouseup', () => {
//   isDragging = false;
//   imageGallery.classList.remove('active');
// });

// imageGallery.addEventListener('mousemove', (e) => {
//   if (!isDragging) return;
//   e.preventDefault();
//   const x = e.pageX - imageGallery.offsetLeft;
//   const walk = (x - startX) * 2; // The multiplier controls the scroll speed
//   imageGallery.scrollLeft = scrollLeft - walk;
// });