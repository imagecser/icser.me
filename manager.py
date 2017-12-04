from flask import send_from_directory, render_template, Flask, request, jsonify
from werkzeug.exceptions import HTTPException
import templates.calc.calc as calc
import os
app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template("index.html")


@app.route('/beating-heart/')
def beating_heart_page():
    return render_template('beating-heart/index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@app.route('/calc/<line>')
def calc_line(line='0'):
    return calc.calc_line(line)


@app.errorhandler(404)
@app.errorhandler(405)
def error404(error):
    return render_template('errors/index.html', code=str(error.code)), error.code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
