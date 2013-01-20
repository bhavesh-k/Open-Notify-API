import os
from functools import wraps
from flask import Flask, jsonify, request, current_app, render_template, send_from_directory
import iss
app = Flask(__name__)

# json endpoint decorator
def json(func):
    """Returning a object gets JSONified"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        return jsonify(func(*args, **kwargs))
    return decorated_function

# from farazdagi on github
#   https://gist.github.com/1089923
def jsonp(func):
    """Wraps JSONified output for JSONP requests."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs).data)
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)
    return decorated_function

# APIs:
API_DEFS = [  {
                "title": "ISS Location Now",
                "link": "/iss-now.json",
                "desc": "Current ISS location over Earth (latitude/longitude)",
                "doclink": "http://open-notify.org/api-doc#iss-now",
                "docname": "api-doc#iss-now"
              },
           ]

@app.route("/")
def index():
    return render_template('index.html', apis=API_DEFS)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/iss-now.json")
@jsonp
@json
def iss_now():
    loc = iss.get_location()
    return {"message": "success", "data": loc}

@app.route("/astros.json")
@jsonp
@json
def astros():
    Astros  = [
              {'name': "Oleg Novitskiy",    'craft': "ISS"}
            , {'name': "Evgeny Tarelkin",   'craft': "ISS"}
            , {'name': "Kevin A. Ford",     'craft': "ISS"}
            , {'name': "Roman Romanenko",   'craft': "ISS"}
            , {'name': "Thomas Marshburn",  'craft': "ISS"}
            , {'name': "Chris Hadfield",    'craft': "ISS"}
          ] 
    return {'message': "success", 'number': len(Astros), 'people': Astros}

if __name__ == "__main__":
    app.run()
