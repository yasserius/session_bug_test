from flask import Flask, session, request, jsonify
from flask_session.defaults import Defaults
from flask_session.filesystem import FileSystemSessionInterface
import datetime

class CustomSessionInterface(FileSystemSessionInterface):
    def should_set_cookie(self, app, session):
        return_val = not session.get('lesssecure', False)
        return return_val

# Create the app
app = Flask(__name__)

# Configuring the app
app.config["SESSION_COOKIE_SAMESITE"] = "lax"
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_PATH"] = "/"
app.config["SESSION_TYPE"] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=730)
app.config['SECRET_KEY'] = 'supersecretkey'

# Custom session interface using Defaults from flask_session.defaults
session_interface = CustomSessionInterface(
    app=app,
    cache_dir=Defaults.SESSION_FILE_DIR,  # Use default session file directory
    threshold=Defaults.SESSION_FILE_THRESHOLD,  # Use default session file threshold
    mode=Defaults.SESSION_FILE_MODE,  # Use default session file mode
    key_prefix=Defaults.SESSION_KEY_PREFIX,  # Use default key prefix
    use_signer=Defaults.SESSION_USE_SIGNER,  # Use default signer setting
    permanent=Defaults.SESSION_PERMANENT,  # Use default permanent setting
    sid_length=Defaults.SESSION_ID_LENGTH,  # Use default session ID length
    serialization_format=Defaults.SESSION_SERIALIZATION_FORMAT,  # Use default serialization format
)

app.session_interface = session_interface

# Route to handle login and set the session
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username == 'admin' and password == 'password':  # Simplified authentication check
        session['logged_in'] = True
        session['username'] = username
        return jsonify({"message": "Login successful", "session": dict(session)}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Route to get or set the session
@app.route('/session', methods=['GET', 'POST'])
def manage_session():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({"message": "Unauthorized, please log in first"}), 401

    if request.method == 'POST':
        # Set or modify the session
        session['my_key'] = request.json.get('my_key', 'default_value')
        return jsonify({"message": "Session updated", "session": dict(session)})
    else:
        # Return the current session
        return jsonify({"message": "Current session", "session": dict(session)})

if __name__ == '__main__':
    app.run(debug=True)
