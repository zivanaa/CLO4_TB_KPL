from datetime import datetime
from flask import render_template

def get_landing_content():
    """
    Render landing page content using HTML template
    """
    current_time = datetime.now().strftime("%B %d, %Y")
    return render_template("landing_page.html", current_time=current_time)
