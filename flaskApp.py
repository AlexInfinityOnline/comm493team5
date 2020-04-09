from flask import Flask, request, render_template
from COMM493 import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/search-product')
def searchProduct():
    idrequest = request.args['request-id']
    try:
        idsubmit = int(idrequest)
        return """
        <html><body>
            <h1>Hello!</h1>
            The similar products are {0}.
        </body></html>
        """.format(
            str(prodReco(int(idsubmit))))
    except:
        return """
        <html><body>
            <h1>Hello!</h1>
            You inputted an invalid product id.
        </body></html>
        """

@app.route('/search-customer')
def searchCustomer():
    idrequest = request.args['request-id']
    try:
        idsubmit = int(idrequest)
        return """
        <html><body>
            <h1>Hello!</h1>
            The products this customer will like are {0}.
        </body></html>
        """.format(
            str(custReco(int(idsubmit))))
    except:
        return """
        <html><body>
            <h1>Hello!</h1>
            You inputted an invalid customer id.
        </body></html>
        """

# Launch the FlaskPy dev server
app.run(host="localhost", debug=True)