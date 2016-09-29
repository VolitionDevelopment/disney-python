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

    cursor.execute("SELECT header, content, image FROM page_content "
                   "WHERE page = 'home' AND location = 'left-bar' AND status = 1")

    data = cursor.fetchall()
    return render_template('index.html', header=header, data=data)


@app.route('/login', methods=['GET'])
def admin():
    return render_template('login.html', failure=request.args.get('failure'))


@app.route('/login', methods=['POST'])
def login():
    if 'username' in session:
        return redirect('/admin')
    elif request.form['username'] == 'admin' and request.form['password'] == 'password':
        session['username'] = request.form['username']
        return redirect('/admin')
    else:
        return redirect('/login?failure=true')


@app.route('/admin', methods=['GET'])
def admin_cp():
    if 'username' in session:
        home_query = "SELECT id, header, content, image, status FROM page_content WHERE page = 'home'"
        cursor.execute(home_query)
        home_data = cursor.fetchall()

        return render_template('admin.html', success=request.args.get('success'), home_data=home_data)
    else:
        return redirect('/login?failure=true')


@app.route('/admin', methods=['POST'])
def submit():
    if 'username' in session:
        body = request.form['body']
        header = request.form['header']
        image = request.form['image']

        query = "INSERT INTO page_content VALUES (DEFAULT, 'home', %s, 1, 1, 'left_bar', '', %s, %s)"

        cursor.execute(query, (body, header, image))
        connection.commit()

        return redirect('/admin?success=true')

    else:
        return redirect('/login?failure=true')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/edit/<id>', methods=['GET'])
def edit(id):
    query = "SELECT id, header, content, image, status, priority FROM page_content WHERE id = %s"
    cursor.execute(query, id)
    print query
    data = cursor.fetchone()

    return render_template('edit.html', data=data)


@app.route('/edit/<id>', methods=['POST'])
def update(id):
    query = "UPDATE page_content SET header = %s, content = %s, image = %s WHERE id = %s"
    cursor.execute(query, (request.form['header'], request.form['body'], request.form['image'], id))
    connection.commit()
    return redirect('/admin')


@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    query = "DELETE FROM page_content WHERE id = %s"
    cursor.execute(query, id)
    connection.commit()
    return redirect('/admin')


@app.route('/test', methods=['POST'])
def test():
    query = "SELECT * FROM page_content WHERE image = " + request.form['rekt']
    print query
    cursor.execute(query)
    connection.commit()
    return redirect('/admin')


if __name__ == '__main__':
    app.run(debug=True)
