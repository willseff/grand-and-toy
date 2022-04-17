from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)
# define our routes
@app.route('/')
# apps can have multiple routes!
# this dcorator sends the name varaiable thru the url, dont need request.args anymore
@app.route('/<name>')
def index(name="Treehouse"):
	#name = request.args.get('name', name)
	#return "Hello from {}".format(name)
	return render_template("index.html", name=name)
#debug = true means that flask auto restarts when we make changes
# host 0.0.0.0 means listen on all addresses

# variables come in as a string by dafault 
@app.route('/add/<int:num1>/<int:num2>')
@app.route('/add/<float:num1>/<float:num2>')
@app.route('/add/<int:num1>/<float:num2>')
@app.route('/add/<float:num1>/<int:num2>')
def add(num1,num2):
	context = {"num1":num1, "num2":num2}
	return render_template("add.html", **context)
	#return f"""
	#<!doctype html>
	#<html>
	#<head><title>Adding!</title></head>
	#<body>
	#<h1> {num1} + {num2} = {num1+num2}</h1>
	#</body>
	#</html>
	#"""
	#return '{} + {} = {}'.format(num1,num2,num1+num2)


app.run(debug=True, port=8000, host='0.0.0.0')

