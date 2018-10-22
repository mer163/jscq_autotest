from flask import Flask, request,current_app,g,session,make_response,redirect,abort,render_template

app = Flask(__name__)

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    cookie = request.headers.get('Cookie')
    response = make_response('<h1> Test <h1>')
    response.set_cookie("token","11111111111111")
    return response
    # return '<h1>Hello World! </h1>  <p> Your cookie is %s </p>'  %cookie

@app.route('/user/<name>')
def user(name):
    cookie = request.headers.get('Cookie').split(';')
    for i in cookie:
        print(i)
        if 'token' in i:
            token = i


    return '<h1>Hello, %s!<h1>' %token


@app.route('/testdirect')
def direct():

    return redirect('http://app.zhhqice.com.cn')


@app.route('/testabort')
def testabort():
    abort(404)

@app.route('/test')
def test():
    return render_template('index.html')

@app.route('/test/<name>')
def testuser(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,threaded=True,port=9999)