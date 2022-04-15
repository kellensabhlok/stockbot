from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/<stock_name>')
def index(stock_name='AAPL'):
    test = "hi"
    # show the user the index.html page from the template folder
    return render_template('index.html', stock_name=stock_name, test=test)

if __name__ == '__main__':
    app.run(debug=True)