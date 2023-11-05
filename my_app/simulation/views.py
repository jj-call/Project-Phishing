from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    redirect,
    url_for,
    session,
    jsonify,
    current_app,
    current_app as app,
)
from flask_login import login_required, current_user


# Model and database imports
from my_app.models import (
    PhishingResponse,
    PreSimulationResponse,
    PostSimulationResponse,
    PhishingChallenge,
    User,
    UserProgressLog,
)
from ..extensions import db
from my_app.forms import (
    PhishingSimulationForm,
    PostSimulationForm,
    PreSimulationResponseForm,
)

# Other standard imports and utilities
from datetime import datetime
import logging, random

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Blueprint
simulation_blueprint = Blueprint("simulation", __name__)


# Utility functions
def generate_challenges(app):
    with current_app.app_context():
        challenges = []
        for i in range(10):
            c = PhishingChallenge()
            c.timestamp = datetime.now()
            challenges.append(c)
        db.session.add_all(challenges)
        db.session.commit()


# Returns the next challenge for the given user
def get_challenge(user=None, new=True):
    if user is None:
        user = current_user  # Get the current user
    challenges = PhishingChallenge.query.all()  # Get all challenges
    current_app.logger.info(f"All challenges fetched: {challenges}")

    if (
        new or user.current_challenge_id is None
    ):  # If the user is starting a new challenge
        last_challenge_id = user.last_challenge_id

        if last_challenge_id is None:
            # Get the first challenge if the user hasn't started any challenges yet
            challenge = PhishingChallenge.query.order_by(PhishingChallenge.id).first()
        else:
            # Get the next challenge that comes after the user's last completed challenge
            challenge = (
                PhishingChallenge.query.filter(PhishingChallenge.id > last_challenge_id)
                .order_by(PhishingChallenge.id)
                .first()
            )


    else:
        # If the user already has an ongoing challenge, get that challenge
        current_app.logger.info("User already has an ongoing challenge")
        challenge = PhishingChallenge.query.get(user.current_challenge_id)

    return challenge


def validate_form(form, validations):  # Function to validate the form data
    errors = []
    for field, options in validations.items():
        # Check if the field is empty
        if not form.get(field):
            errors.append("Please fill in all fields")
            break
        # Check if the field is one of the expected options
        elif not form.get(field) in options:
            errors.append(
                "Invalid option for {} field".format(field)
            )  # Add an error message to the list
            break
    return errors


# Main routes


# Route for the base page
@simulation_blueprint.route("/base", methods=["GET"])
@login_required
def base():
    user_id = current_user.id
    phishing_responses = PhishingResponse.query.filter_by(user_id=user_id).all()
    form = PhishingSimulationForm()
    return render_template(
        "simulation/base.html", form=form, phishing_responses=phishing_responses
    )


# Route for the pre-simulation questionnaire
@simulation_blueprint.route("/pre_simulation", methods=["GET", "POST"])
@login_required
def submit_pre_simulation():
    form = PreSimulationResponseForm()
    # List to store errors
    errors = []


    if request.method == "POST":  # If the form is submitted
        validations = {
            "gender": ["male", "female"],
            "training": ["yes", "no"],
            "knowledge": ["yes", "no"],
            "message": ["yes", "no"],
            "actions": ["option1", "option2", "option3", "option4"],
            "consequences": ["option1", "option2", "option3"],
        }

        # Validate age
        age = request.form.get("age")
        if not (age and age.isdigit() and 1 <= int(age) <= 85):
            errors.append("Invalid age")

        # Validate rating
        rating = request.form.get("rating", type=str)
        if not (rating and rating.isdigit() and 1 <= int(rating) <= 5):
            errors.append("Invalid rating")
        # Validate other fields using the dictionary
        errors.extend(validate_form(request.form, validations))
        # If there are errors, flash each error and re-render the form
        if errors:
            for error in errors:
                flash(error, "error")
            # Pass the form
            return render_template("simulation/Pre-Questionnaire.html", form=form, errors=errors)


        # If no errors, process form
        try:
            response = PreSimulationResponse(
                user_id=current_user.id,
                age=int(age),
                gender=request.form.get("gender"),
                training=request.form.get("training"),
                knowledge=request.form.get("knowledge"),
                message=request.form.get("message"),
                rating=int(rating),
                actions=request.form.get("actions"),
                consequences=request.form.get("consequences"),
            )
            db.session.add(response)
            db.session.commit()
            flash("Form submitted successfully", "success")
            return redirect(url_for("simulation.base"))
        except Exception as e:
            current_app.logger.error(str(e))
            flash(
                "An error occurred while processing your request. Please try again later.",
                "error",
            )
            return render_template("simulation/Pre-Questionnaire.html")

    else:
        # Render the form for GET requests
        form = PreSimulationResponseForm()
        return render_template("simulation/Pre-Questionnaire.html", form=form, errors=errors)



# Route for the phishing simulation
@simulation_blueprint.route("/phishing_simulation", methods=["GET", "POST"])
@login_required
def phishing_simulation():
    try:
        app.logger.info(
            "Entering phishing_simulation view"
        )  # Log the entry to the view
        user_id = current_user.id
        form = PhishingSimulationForm()
        print(f"Form Data: {form.data}")

        if request.method == "GET":
            app.logger.info("Processing GET request")
            session[
                "start_time"
            ] = datetime.now().isoformat()  # Save the start time in the session
            user = User.query.get(user_id)
            challenge = get_challenge(
                user, new=True
            )  # Get the next challenge for the user
            if not challenge:
                last_challenge_id = user.last_challenge_id
                if last_challenge_id is None:
                    flash("No challenges available. Redirecting to base page.", "info")
                else:
                    flash(
                        "You've completed all challenges! Redirecting to base page.",
                        "info",
                    )
                return redirect(
                    url_for("simulation.base")
                )  # Redirect to the base page if there are no more challenges

            return render_template(
                "simulation/Phishing-Simulation.html",
                sender=challenge.sender,
                subject=challenge.subject,
                content=challenge.content,
                form=form,
                challenge=challenge,
            )  # Render the template with the challenge data

        elif request.method == "POST":
            app.logger.info("Processing POST request")

            start_time_str = session.get("start_time")
            start_time = None
            end_time = datetime.now()
            if start_time_str is not None:
                try:
                    start_time = datetime.fromisoformat(
                        start_time_str
                    )  # Convert the start time string to a datetime object
                    duration_seconds = (
                        end_time - start_time
                    ).total_seconds()  # Calculate the duration of the challenge
                except ValueError:
                    app.logger.error("start_time_str is not a valid string")

            if form.validate():
                challenge_id = form.challenge_id.data
                print(f"Current Challenge ID: {challenge_id}")
                user = User.query.get(current_user.id)

                # Pass user to get_challenge
                next_challenge = get_challenge(user, new=True)

                current_challenge_id = request.form.get(
                    "challenge_id"
                )  # Get the current challenge ID from the form

                existing_responses = PhishingResponse.query.filter_by(
                    user_id=current_user.id, challenge_id=current_challenge_id
                ).all()
                print(f"Existing Responses: {existing_responses}")

                # Saving to the database
                pre_response = PreSimulationResponse.query.filter_by(
                    user_id=current_user.id
                ).first()
                if pre_response is None:
                    app.logger.error("pre_response is None")
                    return (
                        jsonify({"success": False, "error": "pre_response is None"}),
                        500,
                    )

                new_response = PhishingResponse(
                    user_id=current_user.id,
                    challenge_id=challenge_id,
                    duration=duration_seconds,
                    challenge_number=PhishingResponse.query.filter_by(
                        user_id=current_user.id
                    ).count()
                    + 1,
                    clicked_link=(form.clicked_link.data == "True"),
                    phishing=form.phishing.data,
                    confidence=form.confidence.data,
                    reason=form.reason.data,
                    age=pre_response.age,
                    gender=pre_response.gender,
                )

                db.session.add(new_response)  # Add the new response to the database
                current_user.last_challenge_id = current_challenge_id
                current_user.current_challenge_id = None

                # Calculate score and grade for the user
                user_score, grade_level = calculate_score_and_grade(current_user.id)

                # Log this data
                progress_log = UserProgressLog(
                    user_id=current_user.id,
                    user_score=round(user_score),
                    grade_level=grade_level,
                )
                db.session.add(progress_log)

                # Update user's overall score and grade
                current_user.overall_score = user_score
                current_user.grade_level = grade_level

                # Commit all changes to the database at once
                db.session.commit()

                return jsonify(
                    {
                        "success": True,
                        "message": "Response saved successfully!",
                        "redirect": url_for("simulation.phishing_simulation"),
                    }
                )

            else:
                app.logger.info(
                    "Form validation failed"
                )  # Log the form validation failure
                return (
                    jsonify({"success": False, "error": "Form validation failed"}),
                    400,
                )

        else:
            return "Method Not Allowed", 405

    except Exception as e:
        app.logger.error(f"An exception occurred: {e}")
        db.session.rollback()
        return "An error occurred", 500


@simulation_blueprint.app_errorhandler(404)
def page_not_found(e):
    current_app.logger.error(f"404 error: {e}")
    return render_template("404.html"), 404


@simulation_blueprint.route("/link_clicked/<challenge_id>")
def link_clicked(challenge_id):
    # Retrieve the user's ongoing PhishingResponse for the challenge
    response = PhishingResponse.query.filter_by(
        user_id=current_user.id, challenge_id=challenge_id
    ).first()
    if response:
        response.clicked_link = True
        db.session.commit()


@simulation_blueprint.route("/submit_response/<challenge_id>", methods=["POST"])
@login_required
def submit_response(challenge_id):
    # User's perception (either "phishing" or "genuine")
    user_perception = request.form.get("perception")
    if not user_perception:
        return jsonify({'error': 'No perception provided.'}), 400

    # Retrieve the user's ongoing PhishingResponse for the challenge
    response = PhishingResponse.query.filter_by(
        user_id=current_user.id, challenge_id=challenge_id
    ).first()

    if not response:
        return jsonify({'error': 'No existing response for this challenge.'}), 404

    response.phishing = user_perception
    db.session.commit()
    return jsonify({'success': 'Response updated successfully.'}), 200



# Route for the post-simulation questionnaire
@simulation_blueprint.route("/post_simulation", methods=["GET", "POST"])
@login_required
def submit_post_simulation():
    form = PostSimulationForm()
    if request.method == "POST":
        # Validate form data
        if not form.validate_on_submit():
            # Print validation errors for each field
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field '{field}': {error}")

            flash("Invalid form data", "error")
            return render_template("simulation/Post-Questionnaire.html", form=form)

        # Fetch form data
        data = form.data

        # Create PostSimulationResponse object
        response = PostSimulationResponse(
            user_id=current_user.id,
            awareness=data["awareness"],
            ratings=data["ratings"],
            helpful=data["helpful"],
            act=data["act"],
            behaviour=data["behaviour"],
            effective=data["effective"],
            life=data["life"],
            recommend=data["recommend"],
        )

        # Save to database
        db.session.add(response)
        db.session.commit()

        # Mark simulation completed
        current_user.has_completed_simulation = True
        db.session.commit()

        # Redirect to final page
        return redirect(url_for("simulation.final_page"))

    else:
        flash("Invalid form data", "error")

    return render_template("simulation/Post-Questionnaire.html", form=form)


@simulation_blueprint.route("/get_email", methods=["GET"])
def get_email():

    challenge = get_challenge(new=True)

    if not challenge:
        return jsonify({"error": "No challenges available"}), 404

    # Save current challenge to session or database
    session["current_challenge_id"] = str(challenge.id)

    # Return the challenge data
    return jsonify(
        {
            "sender": challenge.sender or "",
            "subject": challenge.subject or "",
            "content": challenge.content or "",
            "button_text": "Click this link",
            "is_phishing": challenge.is_phishing,
        }
    )


@simulation_blueprint.route("/final_page")
@login_required
def final_page():
    # Calculate the score and grade using the function
    average_score, grade = calculate_score_and_grade(current_user.id)

    # Round the score
    rounded_score = round(average_score)

    # Pass the calculated score and grade to the HTML template
    return render_template(
        "simulation/final_page.html", user_score=rounded_score, grade_level=grade
    )


@simulation_blueprint.route("/generate_challenges")
@login_required
def generate_challenges_route():
    generate_challenges(current_app)
    return "Challenges Generated!"


def calculate_score(user_id):
    # Fetch all responses for the given user_id
    responses = PhishingResponse.query.filter_by(user_id=user_id).all()

    # Initialize score
    total_score = 0

    # Weights for different aspects
    correctness_weight = 0.5
    confidence_weight = 0.3
    time_weight = 0.2

    for response in responses:
        # Initialize individual_score
        individual_score = 0

        # Fetch the corresponding challenge
        challenge = PhishingChallenge.query.get(response.challenge_id)

        # Correctness
        correct_answer = "phishing" if challenge.is_phishing else "genuine"

        if response.phishing == correct_answer:
            individual_score += correctness_weight * 100
        elif response.phishing == "unsure":
            individual_score += correctness_weight * 50
        else:
            individual_score += 0

        # Confidence
        if response.confidence == "high":
            individual_score += confidence_weight * 100
        elif response.confidence == "medium":
            individual_score += confidence_weight * 60
        else:  # Assuming 'low' is the only other option
            individual_score += confidence_weight * 30

        # Time
        time_score = 100 - (response.duration / 60 * 100)
        time_score = max(0, time_score)
        individual_score += time_weight * time_score

        total_score += individual_score

    if len(responses) > 0:
        average_score = total_score / len(responses)
    else:
        average_score = 0

    return average_score


def calculate_time_score(time_seconds):
    max_time = 60  # Maximum time in seconds after which the score becomes zero

    if time_seconds > max_time:
        return 0
    optimal_time = 30  # Optimal time in seconds to take for the decision 5 seconds and the typing time for the reason.
    time_penalty = (
        0.5  # Score reduction for each second above or below the optimal time
    )

    # The score starts at 10 and decreases by time_penalty for each second above or below the optimal time
    score = 10 - time_penalty * abs(optimal_time - time_seconds)

    # Make sure the score is within the bounds [0, 10]
    return max(0, min(10, score))


def calculate_score_and_grade(user_id):
    average_score = calculate_score(
        user_id
    )  # Assuming calculate_score is defined as before

    # Determine grade
    if average_score >= 90:
        grade = "Excellent"
    elif average_score >= 80:
        grade = "Very Good"
    elif average_score >= 70:
        grade = "Good"
    elif average_score >= 60:
        grade = "Fair"
    elif average_score >= 50:
        grade = "Needs Improvement"
    else:
        grade = "Poor"

    return average_score, grade


# Error handlers
@simulation_blueprint.app_errorhandler(500)
def internal_server_error(e):
    current_app.logger.error(f"Internal Server Error: {e}")
    return render_template("500.html"), 500


@simulation_blueprint.app_errorhandler(404)
def not_found_error(e):
    current_app.logger.error(f"404 Error: {e}")
    return render_template("404.html"), 404


@simulation_blueprint.app_errorhandler(403)
def forbidden_error(e):
    current_app.logger.error(f"403 Error: {e}")
    return render_template("403.html"), 403


@simulation_blueprint.app_errorhandler(400)
def bad_request(e):
    current_app.logger.error(f"400 Error: {e}")
    return render_template("400.html", error=e), 400
