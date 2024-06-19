
from flask import Flask, render_template, request, redirect, url_for, session, flash
from blockchain_layer.blockchain_layer import Blockchain
from ml_layer import ml_model
from qr_code import qrcode
import json

app = Flask(__name__)
app.secret_key = "alkdjfalkdjf"
blockchain = Blockchain()


# Load user information from JSON file
with open("users.json", "r") as file:
    users_data = json.load(file)


# Helper function to authenticate users
def authenticate(username, password, user_type):
    for user in users_data["users"]:
        if user["username"] == username and user["password"] == password and user["role"] == user_type:
            return user
    return None


@app.route("/set_user_type/<user_type>")
def set_user_type(user_type):
    session["user_type"] = user_type

    if user_type in ["manufacturer", "supplier", "admin"]:
        return redirect(url_for("login"))
    elif user_type == "customer":
        return redirect(url_for("search_product"))
    else:
        return redirect(url_for("index"))


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/home", methods=["GET", "POST"])
def home():
    if "user_auth" in session:
        if session["user_type"] == "admin":
            return redirect(url_for('admin'))
        elif session["user_type"] == "manufacturer":
            return redirect(url_for('manufacturer'))
        elif session["user_type"] == "supplier":
            return redirect(url_for('supplier'))
        else:
            session["user_type"] = ""
            session["user_auth"] = {}
            return redirect(url_for('index'))
    else:
        session["user_type"] = ""
        flash("Please login to access the home page.")
        return redirect(url_for('index'))


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pswd = request.form["password"]

        session["user_auth"] = authenticate(user, pswd, session["user_type"])
        
        if session["user_auth"]:
            if session["user_type"] == "admin":
                return redirect(url_for('admin'))
            elif session["user_type"] == "manufacturer":
                return redirect(url_for('manufacturer'))
            elif session["user_type"] == "supplier":
                return redirect(url_for('supplier'))
            else:
                session["user_type"] = ""
                session.pop("user_auth", None)
                return redirect(url_for('index'))
        else:
                flash("Invalid Username or Password")
                return render_template('login.html', error_message="Invalid Username or Password")
    else:
        return render_template('login.html')


@app.route("/add_product", methods=["POST", "GET"])
def add_product():
    if request.method == "POST":
        product_details = {}
        for key in ["productname", "brand", "productid", "retailprice", "discountedprice"]:
            product_details[key] = request.form[key]
        product_details["uniqueid"] = str(blockchain.unique_id)
        session["product_details"] = product_details
        return redirect(url_for('confirm'))
    
    elif session["user_type"] and session["user_auth"]:
        return render_template('add_product.html')
    else:
       return redirect(url_for('index'))

@app.route("/confirm", methods=["GET", "POST"])
def confirm():
    product_details = session.get("product_details")
    if request.method == "POST":
        if product_details:
            blockchain.addproduct(product_details, session["user_auth"])
            path = qrcode.generate_qr_code(product_details)
            session.pop("product_details", None)  # Clear product_details from the session
            flash("The Product has been added in the Blockchain")
            return render_template('confirm.html', product_details=product_details, message="The Product has been added in the Blockchain", path=path)

    elif session["user_type"] and session["user_auth"]:
        return render_template('confirm.html', product_details=product_details)
    else:
       return redirect(url_for('index'))


@app.route("/admin")
def admin():
    if session["user_type"] == "admin":
    	return render_template('add_product.html')
    else:
    	return redirect(url_for('home'))

@app.route("/manufacturer")
def manufacturer():
    if session["user_type"] == "manufacturer":
    	return render_template('manufacturer.html')
    else:
    	return redirect(url_for('home'))

@app.route("/supplier")
def supplier():
    if session["user_type"] == "supplier":
    	return render_template('supplier.html')
    else:
    	return redirect(url_for('home'))

@app.route("/added")
def added():
	return render_template('added.html')


@app.route("/search_product", methods=["GET", "POST"])
def search_product():
    if request.method == "POST":
        qr_code_image = request.files.get('qrCodeImage')
        
        product_details = {}
        for key in ["productname", "brand", "productid", "uniqueid", "retailprice", "discountedprice"]:
            product_details[key] = request.form[key]
        
        if qr_code_image:
            product_details_qr = qrcode.decode_qr_code(qr_code_image)
            product_details_qr = product_details_qr.replace("'", '"')
            product_details = json.loads(product_details_qr)
        
        elif any(field == "" for field in product_details.values()):
            flash("Fill all product details!")
            return render_template('search_product.html', error_message="Please either fill all Product Details or Upload QR Code!")
        
        
        for key in ["productid", "uniqueid", "retailprice", "discountedprice"]:
            product_details[key] = int(product_details[key])
        
        # Verify product with blockchain
        blockchain_product_details = blockchain.getProduct(product_details["uniqueid"])
        is_on_blockchain = blockchain_product_details.get("isAuthentic", False)
        
        # Analyze product with ML
        is_authentic_ml = ml_model.productAnalyzer(product_details)
       
        if is_on_blockchain and is_authentic_ml:
            if all( blockchain_product_details[key] == product_details[key] 
                 for key in ["productname", "brand", "productid", "retailprice", "discountedprice"] ):
                isAuthentic = True
            else:
                flash("Invalid Product Details!")
                return render_template('search_product.html', error_message="Invalid Product Details! Enter Again")
        else:
            isAuthentic = False
        
        session["search_result"] = {
            "product_details": blockchain_product_details,
            "isAuthentic": isAuthentic
        }

        return redirect(url_for('search_result'))

    else:
        return render_template('search_product.html')

@app.route("/search_result")
def search_result():
    if session["search_result"]:
        search_result = session.get("search_result")
        session.pop("search_result", None)
        return render_template('search_result.html', search_result=search_result)
    else:
        return redirect(url_for('search_product'))
    


@app.route("/logout")
def logout():
    session["user_auth"] = {}
    flash("You have been logged out.")
    return render_template('login.html', error_message="You have been logged out")


if __name__ == "__main__":
    app.run(debug=True)
    session["user_type"] = ""
    session["user_auth"] = {}