import os
import logging
import click
from flask import Flask, redirect, request, url_for, render_template
from flask_login import current_user
from dotenv import load_dotenv
from .config import DevelopmentConfig, ProductionConfig
from .models import User, PhishingChallenge
from .extensions import db, login_manager, migrate
from .simulation.views import simulation_blueprint
from logging.handlers import RotatingFileHandler
from flask_wtf.csrf import CSRFProtect
from flask.cli import with_appcontext
from flask_session import Session
from .extensions import db


  
load_dotenv()
print("Database URL:", os.environ.get('DATABASE_URL'))
print("Secret Key:", os.environ.get('SECRET_KEY'))


logging.basicConfig(level=logging.DEBUG)

def configure_logging(app):
    handler = RotatingFileHandler('my_app.log', maxBytes=10000, backupCount=3)
    formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    if not app.debug:
        file_handler = logging.FileHandler('errorlog.txt')
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)
        
@click.command("seed-db")
@with_appcontext
def seed_database():        
            # Create challenges
            challenges = [
            {"sender": "schoolsecurity96389@info_seek.com", "subject": "Reactivate account", "content": "Dear User, we have detected unusual activity on your school account. As a security measure, your account has been temporarily locked.To verify your identity and regain access to your account, please click the link https://www.letmein27834.com/verify. If you did not request this security check, please ignore this email. Best Regards, School Security Team.", "is_phishing": "phishing",},
            {"sender": "noreply@schoollibraryteam.org", "subject": "Overdue book loan", "content": "Dear Student, your book loan has been overdue. Please update your book loan status by clicking the link or you will incur an additional fine. Regards, School Library Team.", "is_phishing": "phishing"},
            {"sender": "noreply@abchighschoolaccountdepartment.edu.com", "subject": "Print Credit Balance", "content": "Dear Student (Account No. 117263894), Please be aware that your avaliable balance for printing credit is now $0 HKD. Please top up your balance using the link below or visiting the General Office to update your funds so that you have printing availability in School. If there is an error on your account please visit the school accounts department. This is a system generaated message and do not reply to this email.", "is_phishing": "genuine",},
            {"sender": "principal@abchighschool.edu.com", "subject": "Outstanding achievement", "content": "I am pleased to inform you that due to your excellent high attainment grades across all your school subjects, you have been awarded a $250 HKD book coupon. Your continued effort and performance has not gone unnoticed by your teachers and to support your learning further please go to the General Office from next Monday onwards to find out more regarding the prize. Well done and keep up the great work! Best regards, Ms. Honey. Principal. ABC High School. Tel: +852 10101010. https://www.abchighschool.com.", "is_phishing": "genuine",},
            {"sender": "principal3897@abc_high_school.com", "subject": "Congratulations you are a winner!", "content": "Dear Student, I am pleased to inform you that due to your excellent high scores in your subjects, you have won a $1000 HKD voucher and a chance to enter the schools lucky draw. In the lucky draw all participants have the chance to win computers, electronic devices and many more... However you only have until Monday to download the attachment pdf form, complete and return the school office. If there are any issues completing the form please contact us using the link below. Regards, Ms. Honey. Principal. ABC High School. Tel:+852 10101010. http://www.abc_highschool.com", "is_phishing": "phishing"},
            {"sender": "Smith, James <jamessmith2023@email.com>", "subject": "Hope for the future", "content": "You were referred to us with other selected students for a financial grant as an asipring academic student to further your studies. students were chosen based on criteria and information off the school. A student will be given $6000 each. all stduents are to send text to the treasurer on +8521029293 for further information and collection. Regards, James.", "is_phishing": "phishing"},
        ]

            for ch in challenges:
                challenge = PhishingChallenge(content=ch['content'], is_phishing=ch['is_phishing'], sender=ch['sender'], subject=ch['subject'])
                db.session.add(challenge)

            db.session.commit()

            print("Challenges seeded successfully!")
              
def create_app(config_name=None):
    app = Flask(__name__)
    csrf = CSRFProtect()
    if config_name == "testing":
        app.config.from_object('my_app.config.TestingConfig')
    elif os.environ.get('FLASK_ENV') == 'production':
        app.config.from_object('my_app.config.ProductionConfig')
    else:
        app.config.from_object('my_app.config.DevelopmentConfig')
    Session(app)
    configure_logging(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    

    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(str(user_id))
  
    from .main import bp as main_bp
    from .auth import bp as auth_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(simulation_blueprint, url_prefix='/simulation')
    app.cli.add_command(seed_database)

  
    @app.before_request
    def restrict_access():
        if request.endpoint == 'simulation.final_page' and not current_user.has_completed_simulation:
            return redirect(url_for('simulation.base'))
    
    
    @app.route('/simulation/final_page')
    def show_final_page():
        return render_template('simulation/final_page.html')
    
    return app



