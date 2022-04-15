from flask import Flask, render_template, request, redirect, url_for
# import module.py in the modules folder
from modules.module import get_name


app = Flask(__name__)


@app.route('/')
@app.route('/<stock_name>')
def index(stock_name='AAPL'):
    # from the query string of the url, get the stock name
    stock_name = request.args.get('ticker')


    test = "hi"
    # show the user the index.html page from the template folder
    return render_template('index.html', stock_name=stock_name, test=test)




if __name__ == '__main__':
    app.run(debug=True)