from flask import render_template
from my_app.main import bp

@bp.route('/')
def index():
    return render_template('main/index.html')




