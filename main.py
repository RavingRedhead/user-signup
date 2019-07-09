from flask import Flask, request, redirect, render_template
import cgi
import re

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['POST', 'GET'])
def index():

    username = ''
    email = ''
    username_error = ''
    password_error = ''
    verify_password_error = ''
    verified_password_error = ''
    email_error = ''
    title = 'Signup'

    if request.method == 'POST':

        username = request.form['username']
        escaped_username = cgi.escape(username)
        password = request.form['password']
        escaped_password = cgi.escape(password)
        verify_password = request.form['verify_password']
        escaped_verify_password = cgi.escape(verify_password)
        email = request.form['email']
        escaped_email = cgi.escape(email)


        for i in escaped_username:
            #if there is a blank space in username, it's invalid
            if i.isspace():
                username_error = 'User name cannot contain spaces'
                username = ''
            else:
                #if username has fewer than 3 or greater than 20 characters, it's invalid
                if (len(escaped_username) < 3) or (len(escaped_username) > 20):
                    username_error = 'User name must be 3-20 characters in length'
                    username = ''

        if not escaped_username:
            username_error = 'Not a valid user name'
            username = ''

        for i in escaped_password:
            if i.isspace():
                password_error = 'Password must not contain spaces'
            else:
                if (len(escaped_password) < 3) or (len(escaped_password) > 20):
                    password_error = 'Password must be 3-20 characters in length'
        if not len(escaped_password):
            password_error = 'Not a valid password'

        if not len(verify_password):
            verify_password_error = 'Not a valid password'

        if escaped_verify_password != escaped_verify_password:
            verified_password_error = 'Passwords do not match.'

        if (escaped_email != '') and (not re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)):
            email_error = 'Not a valid email'
            email = ''

        if (not username_error) and (not password_error) and (not verify_password_error) and (not verified_password_error) and (not email_error):
            return redirect('/welcome?username={0}'.format(username))

    return render_template('signup.html', title=title, username=username, email=email,
                           username_error=username_error, password_error=password_error,
                           verify_password_error=verify_password_error, verified_password_error=verified_password_error, email_error=email_error)


@app.route('/welcome')
def welcome():
    title = "Welcome!"
    username = request.args.get('username')
    return render_template('welcome.html', title=title, username=username) 

app.run()