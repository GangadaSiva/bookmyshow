from flask import Flask , Blueprint, render_template, request, flash, jsonify, current_app,redirect,url_for
from flask_login import login_required, current_user
from .models import Review, Movie, User, Booking, Cinema, Screening, Seat, Payment
from werkzeug.utils import secure_filename
from . import db
import os
from datetime import datetime
from sqlalchemy import func
views = Blueprint('views', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg','jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route("/", methods= ["GET", "POST"])
@login_required
def home(): 
    movies = Movie.query.all()
    movie_data = {}
    for movie in movies:
        reviews_count = Review.query.filter_by(movie_id=movie.id).count()
        average_rating = db.session.query(func.avg(Review.rating)).filter_by(movie_id=movie.id).scalar() or 0
        movie_data[movie.id] = {
            'reviews_count': reviews_count,
            'average_rating': average_rating
            
        }
    return render_template("home.html", user=current_user, movies = movies, movie_data = movie_data)



@views.route('/check_movie', methods=["GET", "POST"])
def check_movie():
    title_data = request.get_json()
    title = title_data['title']

    movie = Movie.query.filter_by(title = title).first()
    if movie:
        return jsonify({"message":"Movie already exists", "exists":True}),200
    else:
        return jsonify({"message":"movie available you can proceed", "exists":False}),200

@views.route('/check_theater', methods = ["GET", "POST"])
def checkTheater():
    theater_data = request.get_json()
    theater_name = theater_data['theater_name']
    location = theater_data['location']

    theater = Cinema.query.filter_by(name = theater_name, location=location).first()

    if theater:
        return jsonify({"message": "Theater already exists in this location ", "exists": True}),200
    else:
        return jsonify({"message":"Theater available to add in this location", "exists":False}),200





@views.route("/admin", methods= ["GET", "POST"])
@login_required
def adminhome(): 
    return render_template("admin.html", user=current_user)



@views.route('/admin/add', methods=['GET', 'POST'])
@login_required
def add_movie():
    if request.method == 'POST':
        title = request.form.get('title').strip()
        description = request.form.get('description')
        duration = request.form.get('duration')
        language = request.form.get('language')
        release_date_str = request.form.get('release_date')
        release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
        genre = request.form.get('genre')
        image = request.files.get('poster')

        fileName = None
        if image and allowed_file(image.filename):
            fileName = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], fileName))
            print(f"Image saved to {os.path.join(current_app.config['UPLOAD_FOLDER'], fileName)}")


        # Check if movie already exists
        new_movie = Movie.query.filter_by(title=title).first()
        if not new_movie:
            new_movie = Movie(
                title=title, description=description, duration=duration, language=language,
                release_date=release_date, genre=genre, image=fileName
            )
            db.session.add(new_movie)
            db.session.commit()
            flash('Movie details added successfully!', category='alert-success')
        else:
            flash('Movie already Exists!', category='alert-danger')
        return redirect(url_for('views.add_movie'))
    movies = Movie.query.all()

    return render_template('admin.html', user=current_user, movies=movies)


# Route to update a movie
@login_required
@views.route('/admin/movies/update/', methods=['GET', 'POST'])
def update_movie():
    if request.method == 'POST':
        id = request.form.get('movie_id')
        title = request.form.get('new_title').strip()
        genre = request.form.get('new_genre')
        description = request.form.get('new_description')
        release_date_str = request.form.get('new_release_date')
        release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
        language = request.form.get('new_language')
        duration = request.form.get('new_duration')     
        image = request.files.get('new_poster')
        

        existing_movie = Movie.query.get(id)


        if existing_movie:
            existing_movie.title = title
            existing_movie.genre = genre
            existing_movie.description = description
            existing_movie.duration = duration
            existing_movie.release_date = release_date
            existing_movie.language = language
            fileName = None
            if image and allowed_file(image.filename):
                fileName = secure_filename(image.filename)
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], fileName))
                print(f"Image saved to {os.path.join(current_app.config['UPLOAD_FOLDER'], fileName)}")
            else:
                fileName = existing_movie.image
            existing_movie.image = fileName
            db.session.commit()
            flash('Movie updated successfully!', category='alert-success')
    return redirect(url_for('views.add_movie'))




@views.route('/add_theater/<int:movie_id>', methods=["GET", "POST"])
@login_required
def add_theater(movie_id):
    if request.method == "POST":
        theaterName = request.form.get('theater_name')
        location = request.form.get('location')
        total_screens = request.form.get('total_screens')

        theater = Cinema.query.filter_by(name = theaterName, location = location).first()
        if not theater:
            theater = Cinema(name = theaterName, location = location, total_screens = total_screens)
            db.session.add(theater)
            db.session.commit()
            flash("Theater added succesfully", category="alert-success")
        else:
            flash("Theater already exists!", category="alert-danger")
        return redirect(url_for('views.add_theater', movie_id=movie_id))

    theaters = Cinema.query.all()
    return render_template("addtheater.html", theaters = theaters ,user = current_user, movie_id = movie_id)        


@views.route('/theater/update', methods=["GET", "POST"])
@login_required
def update_theater():
    if request.method == "POST":
        movie_id = request.form.get('theater_id')
        theater_id = request.form.get('cinema_id')
        name = request.form.get('new_theater_name')
        location = request.form.get('new_location')
        total_screens = request.form.get('new_total_screens')

        existing_theater = Cinema.query.get(theater_id)
        if existing_theater:
            existing_theater.name = name
            existing_theater.location = location
            existing_theater.total_screens = total_screens
            db.session.commit()
            flash("Theater Updated succesfully", category="alert-success")
        else:
            flash("Theater Not found", category="alert-danger")
    return redirect(url_for('views.add_theater', movie_id= movie_id ))


@views.route('/add/shows/<int:movie_id>/<int:theater_id>', methods=["GET", "POST"])
@login_required
def add_show(movie_id, theater_id):
    if request.method == "POST":
        screen_number = request.form.get('screen_number')
        start_time_str = request.form.get('start_time')
        end_time_str = request.form.get('end_time')
        start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')
        price = request.form.get('price')

        print(movie_id)
        print(theater_id)
        theater = Cinema.query.get(theater_id)
        if theater:
            showtime = Screening(movie_id = movie_id, cinema_id = theater_id, screen_number = screen_number,start_time = start_time, end_time = end_time, price =price)
            db.session.add(showtime)
            db.session.commit()
            flash("Show added succesfully", category="alert-success")
        else:
            flash("Theater  Not found ", category="alert-danger")
        return redirect(url_for('views.add_show', movie_id=movie_id, theater_id = theater_id))
    print(movie_id)
    print(theater_id)
    shows = Screening.query.filter_by(cinema_id=theater_id, movie_id=movie_id).order_by(Screening.start_time.asc()).all()
    print(shows) 
    return render_template("shows.html", user=current_user, shows = shows, movie_id=movie_id, theater_id = theater_id)   

@views.route("/show_update", methods= ["GET", "POST"])
def show_update():
    if request.method == "POST":
        movie_id = request.form.get('movie_id')
        theater_id = request.form.get('theater_id')
        screen_id = request.form.get('screening_id')
        screen_number = request.form.get('new_screen_number')
        start_time_str = request.form.get('new_start_time')
        end_time_str = request.form.get('new_end_time')
        start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')
        price = request.form.get('new_price')
        existing_screen = Screening.query.get(screen_id)
        if existing_screen:
            existing_screen.screen_number = screen_number
            existing_screen.start_time = start_time
            existing_screen.end_time = end_time
            existing_screen.price = price
            db.session.commit()
            flash("Show Updated succesfully", category="alert-success")
        else:
            flash("Show Not found", category="alert-danger")
    return redirect(url_for('views.add_show', movie_id=movie_id, theater_id = theater_id))



@views.route("/admin/movies/delete/", methods=["GET","POST"])
@login_required
def deleteMovie():
    movie_id = request.args.get('movie_id')
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('views.add_movie'))
    # movie_data = request.get_json()
    # movie_id = movie_data.get('movie_id')

    # if movie_id:
    #     movie = Movie.query.get(movie_id)
    #     if movie:
    #         # Delete the movie and cascade to delete associated screenings and cinemas
    #         db.session.delete(movie)
    #         db.session.commit()
    #         return jsonify({}), 200
    #     return jsonify({"error": "Movie not found"}), 404
    # return jsonify({"error": "Invalid request"}), 404


@views.route("/delete_theater", methods=["POST"])
@login_required
def delete_theater():
    theater_data = request.get_json()
    theater_id = theater_data.get('theater_id')
    if theater_id:
        theater = Cinema.query.get(theater_id)
        if theater:
            db.session.delete(theater)
            db.session.commit()
            return jsonify({}),200
        return jsonify({"error": "Theater not found"}),404
    return jsonify({"error": "Invalid request"}), 404

@views.route("/delete_show", methods=["GET", "POST"])
def delete_show():
    show_details = request.get_json()
    show_id = show_details['show_id']
    if show_id:
        show = Screening.query.get(show_id)
        if show:
            db.session.delete(show)
            db.session.commit()
            return jsonify({}),200
        return jsonify({"error": "Theater not found"}),404
    return jsonify({"error": "Invalid request"}), 404


@views.route("/delete_seat", methods=["GET", "POST"])
def delete_seat():
    seat_details = request.get_json()
    seat_id = seat_details['seat_id']
    if seat_id:
        seat = Seat.query.get(seat_id)
        if seat:
            db.session.delete(seat)
            db.session.commit()
            return jsonify({}),200
        return jsonify({"error": "Seat not found"}),404
    return jsonify({"error": "Invalid request"})




@views.route("/add/rating", methods=["GET", "POST"])
@login_required
def add_rating():
    if request.method == "POST":
        user_id = request.form.get('user_id')
        movie_id = request.form.get('movie_id')
        rating = request.form.get('star-rating')
        comment = request.form.get('review')
        review = Review.query.filter_by(user_id = user_id, movie_id = movie_id).first()
        if not review:
            review = Review(user_id = user_id, movie_id = movie_id, rating = rating, comment = comment)
            db.session.add(review)
            db.session.commit()
            flash("Rating added succesfully", category="alert-success")
        else:
            flash("USer rating already exists for this movie", category="alert-danger")
        return redirect(url_for('views.movie_details', movie_id= movie_id))


#admin seats
@views.route('/seats')
@login_required
def seats():
    screening_id = request.args.get('screening_id')
    seats = Seat.query.filter_by(screening_id = screening_id).all()
    return render_template("addseats.html", user= current_user, screening_id= screening_id, seats = seats)


@views.route('/add_seats', methods=["GET", "POST"])
@login_required
def add_seats():
    if request.method == "POST":
        screening_id = request.form.get('screening_id')
        row = request.form.get('row')
        seat_number = request.form.get('seat_number')
        is_available = True if request.form.get('is_available') == 'true' else False
        seat = Seat.query.filter_by(row = row, seat_number = seat_number, screening_id= screening_id).first()

        if not seat:
            seat = Seat(screening_id = screening_id, row = row, seat_number = seat_number, is_available= is_available)
            db.session.add(seat)
            db.session.commit()
            flash("Seat added succesfully", category="alert-success")
        else:
            flash("Seat already exists", category="alert-danger")
        return redirect(url_for('views.seats', screening_id = screening_id))


@views.route("/seat/update", methods=["GET", "POST"])
def seat_update():
    if request.method == "POST":
        seat_id = request.form.get('seat_id')
        screening_id = request.form.get('screening_id')
        # row = request.form.get('new_row')
        # seat_number = request.form.get('new_seat_number')
        is_available = True if request.form.get('new_is_available') == 'true' else False
        existing_seat = Seat.query.get(seat_id)

        existing_seat.is_available = True if request.form.get('new_is_available') == 'true' else False
        db.session.commit()
        flash("Seat Updated succesfully", category="alert-success")
    return redirect(url_for('views.seats', screening_id = screening_id))


@views.route("/all_reviews/<int:movie_id>", methods=["GET", "POST"])
def all_reviews(movie_id):
    reviews = Review.query.filter_by(movie_id = movie_id).all()
    for review in reviews:
        review.user = User.query.get(review.user_id)
    return render_template("all_reviews.html", user=current_user, reviews = reviews)


@views.route("/delete_review/<int:movie_id>/<int:review_id>", methods=["GET", "POST"])
def delete_reviews(movie_id, review_id):
    review = Review.query.get(review_id)
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for("views.all_reviews", movie_id= movie_id))















#User interface routes


@views.route('/movie/<int:movie_id>')
@login_required
def movie_details(movie_id):
    movie = Movie.query.get(movie_id)
    reviews = Review.query.filter_by(movie_id = movie_id)
    reviews_data = {}
    for review in reviews:
        user = User.query.get(review.user_id)
        reviews_data[review.id] = {
            'comment': review.comment,
            'rating': review.rating,
            'user_name': user.name if user else "unknown user"
        }
    reviews_count = Review.query.filter_by(movie_id=movie_id).count()
    average_rating = db.session.query(func.avg(Review.rating)).filter_by(movie_id=movie_id).scalar()
    user_review = Review.query.filter_by(movie_id = movie_id, user_id = current_user.id).first()
    return render_template('movie_details.html', user = current_user, movie = movie, average_rating= average_rating, reviews_count = reviews_count, user_review= user_review, reviews_data = reviews_data)

@views.route('/theater/<int:movie_id>')
@login_required
def theater_details(movie_id):
    movie = Movie.query.get(movie_id)
    screenings = Screening.query.filter_by(movie_id = movie.id).order_by(Screening.start_time.asc()).all()
    cinemas = []
    for screening in screenings:
        cinema = Cinema.query.get(screening.cinema_id)
        if  cinema not in cinemas:
            cinemas.append(cinema)
    return render_template('theater_list.html', user= current_user, movie=movie, screenings= screenings, cinemas=cinemas)



@views.route('/show/seats/<int:screening_id>')
def show_seats(screening_id):
    seats = Seat.query.filter_by(screening_id= screening_id, is_available = True).all()
    screening = Screening.query.get(screening_id)
    return render_template("seats.html", user= current_user, seats = seats, screening = screening)



@views.route('/payment', methods= ["GET", "POST"])
@login_required
def payment():
    selected_seats = request.form.getlist('selected_seats')
    screening_id = request.form.get('screening_id')
    price = request.form.get('price')

    if not selected_seats:
        flash("Please select seats to proceed", category="alert-danger")
        return redirect(url_for('views.show_seats', screening_id= screening_id))
    else:
        total_price = len(selected_seats) * float(price)
        string_calculation = str(len(selected_seats)) + " X " + str(price)
        screening = Screening.query.get(screening_id)
        return render_template('payment.html',user=current_user, total_price = total_price, screening=screening, selected_seats=selected_seats, string_calculation = string_calculation)

@views.route('/process_payment', methods=["GET", "POST"])
@login_required
def process_payment():
    selected_seats_str = request.form.get('selected_seats')
    selected_seats = selected_seats_str.strip('[]').replace("'", "").split(',')
    print(selected_seats)
    screening_id = request.form.get('screening_id')
    total_price = request.form.get('total_price')
    payment_method = request.form.get('payment_method')
    user_id = current_user.id

    booking_ids = []
    for seat_id in selected_seats:
        seat_id = int(seat_id.strip())
        new_booking = Booking(user_id = user_id, screening_id = screening_id, seat_id = seat_id,amount= total_price)
        db.session.add(new_booking)
        db.session.flush()
        seat = Seat.query.get(seat_id)
        seat.is_available = False
        booking_ids.append(new_booking.id)
    db.session.commit()

    for booking_id in booking_ids:
        payment = Payment(booking_id= booking_id, amount= total_price, payment_method= payment_method,status="Paid")
        db.session.add(payment)
    db.session.commit()
    flash('Payment Successful! Your seats have been booked.', category='alert-success')
    return render_template("success.html", user=current_user)
    # return redirect(url_for("views.home"))


@views.route('/user/bookings', methods = ["POST", "GET"])
def user_bookings():
    user_id = current_user.id
    if current_user.is_admin:
        bookings = Booking.query.all()
    else:
        bookings = Booking.query.filter_by(user_id = user_id).all()

    for booking in bookings:
        booking.screening = Screening.query.get(booking.screening_id)
        booking.seat = Seat.query.get(booking.seat_id)
        booking.movie = Movie.query.get(booking.screening.movie_id)
        booking.cinema = Cinema.query.get(booking.screening.cinema_id)

    return render_template('bookings.html', user=current_user, bookings= bookings)









@views.route('/api/get_all_data', methods=['GET'])
@login_required
def get_all_data():
    # Query all movies, cinemas, and screenings
    movies = Movie.query.all()
    cinemas = Cinema.query.all()
    screenings = Screening.query.all()
    reviews = Review.query.all()
    

    reviews_data = []
    for review in reviews:
        reviews_data.append({
            'id': review.id,
            'user_id': review.user_id,
            'movie_id': review.movie_id,
            'rating': review.rating,
            'comment': review.comment,
            'review_date': review.created_at.strftime('%Y-%m-%d')
        })



    # Serialize data
    movies_data = []
    for movie in movies:
        movies_data.append({
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'duration': movie.duration,
            'language': movie.language,
            'release_date': movie.release_date.strftime('%Y-%m-%d'),
            'genre': movie.genre,
            'image': movie.image
        })
    
    cinemas_data = []
    for cinema in cinemas:
        cinemas_data.append({
            'id': cinema.id,
            'name': cinema.name,
            'location': cinema.location,
            'total_screens': cinema.total_screens
        })

    screenings_data = []
    for screening in screenings:
        screenings_data.append({
            'id': screening.id,
            'movie_id': screening.movie_id,
            'cinema_id': screening.cinema_id,
            'screen_number': screening.screen_number,
            'start_time': screening.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': screening.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'price': screening.price
        })
    
    # Create a response object with all the data
    response = {
        'movies': movies_data,
        'cinemas': cinemas_data,
        'screenings': screenings_data,
        'reviews': reviews_data
    }

    return jsonify(response)