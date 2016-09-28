from flask import Flask, render_template, request, redirect, session
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'x'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Password12!'
app.config['MYSQL_DATABASE_DB'] = 'disney'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

app.secret_key = "ewiurhguirhg222uhrgwoeirug"
connection = mysql.connect()
cursor = connection.cursor()


@app.route('/')
def index():

    cursor.execute("SELECT content FROM page_content WHERE page = 'home' AND location = 'header' AND status = 1")

    header = cursor.fetchone()

    cursor.execute("SELECT header_text, content, image FROM page_content "
                   "WHERE page = 'home' and location = 'left-bar' AND status = 1")

    data = cursor.fetchall()
    return render_template('index.html', header=header, data=data)


@app.route('/login', methods=['GET'])
def admin():
    return render_template('login.html', failure=request.args.get('failure'))


@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        session['username'] = request.form['username']
        return redirect('/admin')
    else:
        return redirect('/login?failure=true')


@app.route('/admin', methods=['GET'])
def admin_cp():
    if 'username' in session:
        return render_template('admin.html', success=request.args.get('success'))
    else:
        return redirect('/login?failure=true')


@app.route('/admin', methods=['POST'])
def submit():
    if 'username' in session:
        body = request.form['body']
        header = request.form['header']
        image = request.form['image']

        query = "INSERT INTO page_content VALUES (DEFAULT, 'home', '%s', 1, 1, 'left_bar', '', '%s', '%s')" \
                % (body, header, image)



        cursor.execute(query)
        connection.commit()

        return redirect('/admin?success=true')

    else:
        return redirect('/login?failure=true')


if __name__ == '__main__':
    app.run(debug=True)
