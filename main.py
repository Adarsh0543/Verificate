from flask import Flask, render_template, request, jsonify, redirect, url_for,session,flash,make_response,send_file
from flask_mail import Mail, Message
from reportlab.pdfgen import canvas
from web3 import Web3
from web3.exceptions import ContractLogicError
from datetime import datetime
import sqlite3
import uuid
import traceback
import random
import pdfkit
import os

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
app.secret_key = "abcd123" 

# Otp mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True 
app.config['MAIL_USERNAME'] = 'certi0chain@gmail.com'
app.config['MAIL_PASSWORD'] = 'omqf iuzg qiac nbsz '  

mail = Mail(app)

# Connect to Blockchain
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))  
contract_address = "0x83EE15DFDDD8b8AD56A73001Ca7A1627c7fe6716"
contract_abi = [
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "string",
          "name": "certID",
          "type": "string"
        },
        {
          "indexed": False,
          "internalType": "string",
          "name": "issuingAuthorityName",
          "type": "string"
        }
      ],
      "name": "CertificateIssued",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "string",
          "name": "certID",
          "type": "string"
        }
      ],
      "name": "CertificateRevoked",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "string",
          "name": "institutionID",
          "type": "string"
        }
      ],
      "name": "InstitutionRegistered",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "string",
          "name": "userId",
          "type": "string"
        }
      ],
      "name": "UserRegistered",
      "type": "event"
    },
    {
      "constant": False,
      "inputs": [
        {
          "internalType": "string",
          "name": "_institutionID",
          "type": "string"
        },
        {
          "components": [
            {
              "internalType": "string",
              "name": "institutionName",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "affiliation",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "regNumber",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "dateOfEstablishment",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "institutionType",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "streetAddress",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "city",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "state",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "postalCode",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "country",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "officialEmail",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "phoneNumber",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "adminName",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "adminDesignation",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "adminEmail",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "adminPhone",
              "type": "string"
            },
            {
              "internalType": "bool",
              "name": "exists",
              "type": "bool"
            }
          ],
          "internalType": "struct CertiChain.Institution",
          "name": "_institution",
          "type": "tuple"
        }
      ],
      "name": "registerInstitution",
      "outputs": [],
      "payable": False,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": True,
      "inputs": [
        {
          "internalType": "string",
          "name": "_institutionID",
          "type": "string"
        }
      ],
      "name": "getInstitution",
      "outputs": [
        {
          "components": [
            {
              "internalType": "string",
              "name": "institutionName",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "affiliation",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "regNumber",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "dateOfEstablishment",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "institutionType",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "streetAddress",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "city",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "state",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "postalCode",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "country",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "officialEmail",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "phoneNumber",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "adminName",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "adminDesignation",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "adminEmail",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "adminPhone",
              "type": "string"
            },
            {
              "internalType": "bool",
              "name": "exists",
              "type": "bool"
            }
          ],
          "internalType": "struct CertiChain.Institution",
          "name": "",
          "type": "tuple"
        }
      ],
      "payable": False,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": False,
      "inputs": [
        {
          "internalType": "string",
          "name": "_certID",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_studentName",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_course",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_issueDate",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_dob",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_courseDuration",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_issuingAuthorityName",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_userEmail",
          "type": "string"
        }
      ],
      "name": "issueCertificate",
      "outputs": [],
      "payable": False,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": True,
      "inputs": [
        {
          "internalType": "string",
          "name": "_certID",
          "type": "string"
        }
      ],
      "name": "getCertificate",
      "outputs": [
        {
          "components": [
            {
              "internalType": "string",
              "name": "certID",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "studentName",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "course",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "issueDate",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "dob",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "courseDuration",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "issuingAuthorityName",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "userEmail",
              "type": "string"
            },
            {
              "internalType": "bool",
              "name": "exists",
              "type": "bool"
            }
          ],
          "internalType": "struct CertiChain.Certificate",
          "name": "",
          "type": "tuple"
        }
      ],
      "payable": False,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": False,
      "inputs": [
        {
          "internalType": "string",
          "name": "_certID",
          "type": "string"
        }
      ],
      "name": "revokeCertificate",
      "outputs": [],
      "payable": False,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": False,
      "inputs": [
        {
          "internalType": "string",
          "name": "_userId",
          "type": "string"
        },
        {
          "components": [
            {
              "internalType": "string",
              "name": "userId",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "name",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "dob",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "phoneNumber",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "country",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "pincode",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "streetAddress",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "city",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "state",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "email",
              "type": "string"
            },
            {
              "internalType": "bool",
              "name": "exists",
              "type": "bool"
            }
          ],
          "internalType": "struct CertiChain.UserProfile",
          "name": "_profile",
          "type": "tuple"
        }
      ],
      "name": "registerUser",
      "outputs": [],
      "payable": False,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": True,
      "inputs": [
        {
          "internalType": "string",
          "name": "_userId",
          "type": "string"
        }
      ],
      "name": "getUser",
      "outputs": [
        {
          "components": [
            {
              "internalType": "string",
              "name": "userId",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "name",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "dob",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "phoneNumber",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "country",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "pincode",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "streetAddress",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "city",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "state",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "email",
              "type": "string"
            },
            {
              "internalType": "bool",
              "name": "exists",
              "type": "bool"
            }
          ],
          "internalType": "struct CertiChain.UserProfile",
          "name": "",
          "type": "tuple"
        }
      ],
      "payable": False,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": True,
      "inputs": [
        {
          "internalType": "string",
          "name": "_userId",
          "type": "string"
        }
      ],
      "name": "isUserRegistered",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "payable": False,
      "stateMutability": "view",
      "type": "function"
    }
  ]

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def connect_db():
    return sqlite3.connect("database.db", timeout=10)

    
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_counts")
def get_counts():
    counts = {
        "institutions": 20,
        "certificates": 13,
        "validations": 125,
        "users": 470
    }
    return jsonify(counts)

@app.route("/login", methods=["GET"])
def login():
    return render_template("Login.html")

@app.route("/login", methods=["POST"])
def login_submit():
    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM institutions WHERE email = ? AND password = ? AND verified = 1", (email, password))
    institution = cursor.fetchone()
    conn.close()

    if institution:
        session["user"] = institution[1]
        session["institution_id"] = institution[0]  # Save institution name in session
        session["login_email"] = email              # Email used for login

        # Generate a 6-digit OTP
        otp = random.randint(100000, 999999)
        session["login_otp"] = str(otp)

        # Send OTP via email
        msg = Message("Your OTP for Login", 
                      sender=app.config["MAIL_USERNAME"],
                      recipients=[email])
        msg.body = f"A new login request has been received.Your OTP for login  is: {otp}"
        try:
            mail.send(msg)
        except Exception as e:
            return render_template("Login.html", error="Failed to send OTP: " + str(e))
        
        # Redirect to OTP verification page
        return redirect(url_for("verify_login_otp"))
    else:
        return render_template("Login.html", error="Invalid email or password")
    
@app.route("/user_login", methods=["POST"])
def user_login_submit():
    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, name FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        user_id, full_name = user  # Extract user_id and name

        # Save user_id, login email, and full_name in the session
        session["user_id"] = user_id
        session["login_email"] = email
        session["user_name"] = full_name  # Store full name for display

        # Generate a 6-digit OTP
        otp = random.randint(100000, 999999)
        session["login_otp"] = str(otp)

        # Send OTP via email
        msg = Message("Your OTP for Login", 
                      sender=app.config["MAIL_USERNAME"],
                      recipients=[email])
        msg.body = f"A new new login request has been received.Your OTP for login  is: {otp}"
        try:
            mail.send(msg)
        except Exception as e:
            return render_template("Login.html", error="Failed to send OTP: " + str(e))
        
        # Redirect to OTP verification page for user login
        return redirect(url_for("verify_user_login_otp"))
    else:
        return render_template("Login.html", error="Invalid email or password")



@app.route("/verify_login_otp", methods=["GET", "POST"])
def verify_login_otp():
    if request.method == "POST":
        user_otp = request.form.get("otp", "").strip()
        if "login_otp" in session and session["login_otp"] == user_otp:
            session.pop("login_otp", None)  # Remove OTP from session
            return redirect(url_for("homepage"))
        else:
            return render_template("verify_login_otp.html", error="Invalid OTP")
    return render_template("verify_login_otp.html")
    
@app.route("/verify_user_login_otp", methods=["GET", "POST"])
def verify_user_login_otp():
    if request.method == "POST":
        user_otp = request.form.get("otp", "").strip()

        if "login_otp" in session and session["login_otp"] == user_otp:
            session.pop("login_otp", None)  # Remove OTP from session

            # Ensure the user's session is updated correctly
            session["user"] = session.get("pending_user")  # Retrieve pending user
            session.pop("pending_user", None)  # Remove temporary storage

            return redirect(url_for("user_homepage"))
        else:
            flash("Invalid OTP. Please try again.", "danger")
            return render_template("verify_user_otp.html", error="Invalid OTP")

    return render_template("verify_user_otp.html")

#Forgot password institution section begins
@app.route("/forgot_password_institution", methods=["GET", "POST"])
def forgot_password_institution():
    if request.method == "POST":
        action = request.form.get("action")
        email = request.form.get("email", "").strip()
        
        if action == "send_otp":
            # Verify if the official email is registered in the institutions table
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT institution_id FROM institutions WHERE email = ?", (email,))
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                flash("Official Email is not registered.", "danger")
                return redirect(url_for("forgot_password_institution"))
            
            # Generate OTP and store in session
            otp = str(random.randint(100000, 999999))
            session["reset_otp_institution"] = otp
            session["reset_email_institution"] = email
            try:
                msg = Message("Your OTP for Password Reset - Institution",
                              sender=app.config["MAIL_USERNAME"],
                              recipients=[email])
                msg.body = f"A password reset request has been received for your institution account. Your OTP is: {otp}"
                mail.send(msg)
                flash("OTP sent to your official email.", "success")
            except Exception as e:
                flash("Failed to send OTP: " + str(e), "danger")
            # Redirect with query parameter to retain email in the session
            return redirect(url_for("forgot_password_institution", retain_email="1"))
        
        elif action == "submit_otp":
            submitted_otp = request.form.get("otp", "").strip()
            if submitted_otp == session.get("reset_otp_institution"):
                # Proceed to the final password reset step without flashing a success message
                return redirect(url_for("forgot_password_institution_final"))
            else:
                flash("Incorrect OTP. Please try again.", "danger")
                return redirect(url_for("forgot_password_institution"))
    
    else:
        # If 'retain_email' is not set, clear the stored email from session
        if request.args.get("retain_email") != "1":
            session.pop("reset_email_institution", None)
        return render_template("forgot_password_institution.html")

# Route for institution final reset step
@app.route("/forgot_password_institution_final", methods=["GET", "POST"])
def forgot_password_institution_final():
    if request.method == "POST":
        new_password = request.form.get("new_password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()
        if new_password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("forgot_password_institution_final"))
        
        email = session.get("reset_email_institution")
        if not email:
            flash("Official Email not found in session.", "danger")
            return redirect(url_for("forgot_password_institution"))
        
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE institutions SET password = ? WHERE official_email = ?", (new_password, email))
            conn.commit()
            reset_success = True
            flash("Password reset successfully!", "success")
        except Exception as e:
            flash("Error updating password: " + str(e), "danger")
            reset_success = False
        finally:
            conn.close()
        
        # Clear the reset-related session variables
        session.pop("reset_otp_institution", None)
        session.pop("reset_email_institution", None)
        
        # Render the final page with a flag to trigger a popup (if needed)
        return render_template("forgot_password_institution_final.html", reset_success=reset_success)
    
    return render_template("forgot_password_institution_final.html")
#Forgot password institution section ends

#Forgot password user section begins
@app.route("/forgot_password_user", methods=["GET", "POST"])
def forgot_password_user():
    if request.method == "POST":
        action = request.form.get("action")
        email = request.form.get("email", "").strip()
        
        if action == "send_otp":
            # Verify if the email is registered in the database
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                flash("Email is not registered.", "danger")
                return redirect(url_for("forgot_password_user"))
            
            # Generate OTP and store in session
            otp = str(random.randint(100000, 999999))
            session["reset_otp_user"] = otp
            session["reset_email_user"] = email
            try:
                msg = Message("Your OTP for Password Reset - User",
                              sender=app.config["MAIL_USERNAME"],
                              recipients=[email])
                msg.body = f"A password request has been received for your account. Your OTP for password reset is: {otp}"
                mail.send(msg)
                flash("OTP sent to your email.", "success")
            except Exception as e:
                flash("Failed to send OTP: " + str(e), "danger")
            # Redirect with a query parameter to retain the email in the session
            return redirect(url_for("forgot_password_user", retain_email="1"))
        
        elif action == "submit_otp":
            submitted_otp = request.form.get("otp", "").strip()
            if submitted_otp == session.get("reset_otp_user"):
                #flash("OTP verified.", "success")
                return redirect(url_for("forgot_password_user_final"))
            else:
                flash("Incorrect OTP. Please try again.", "danger")
                return redirect(url_for("forgot_password_user"))
    
    else:
        # In the GET branch: if the query parameter 'retain_email' is not set, clear the stored email.
        if request.args.get("retain_email") != "1":
            session.pop("reset_email_user", None)
        return render_template("forgot_password_user.html")

@app.route("/forgot_password_user_final", methods=["GET", "POST"])
def forgot_password_user_final():
    if request.method == "POST":
        new_password = request.form.get("new_password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()
        if new_password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("forgot_password_user_final"))
        
        email = session.get("reset_email_user")
        if not email:
            flash("Email not found in session.", "danger")
            return redirect(url_for("forgot_password_user"))
        
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE users SET password = ? WHERE email = ?", (new_password, email))
            conn.commit()
            # Set a flag to indicate success so that the template shows the popup
            reset_success = True
            flash("Password reset successfully!", "success")
        except Exception as e:
            flash("Error updating password: " + str(e), "danger")
            reset_success = False
        finally:
            conn.close()
        
        # Clear the reset-related session variables
        session.pop("reset_otp_user", None)
        session.pop("reset_email_user", None)
        
        # Render the final page with a flag to trigger the popup
        return render_template("forgot_password_user_final.html", reset_success=reset_success)
    
    # GET request simply renders the template without the flag
    return render_template("forgot_password_user_final.html")
#Forgot password user section ends

@app.route('/register_selection')
def register_selection():
    return render_template('register_selection.html')

@app.route("/user_register", methods=["GET", "POST"])
def user_register():
    if request.method == "POST":
        # Retrieve form data
        full_name = request.form.get("full_name")
        date_of_birth = request.form.get("date_of_birth")
        street_address = request.form.get("street_address")
        city = request.form.get("city")
        state = request.form.get("state")
        postal_code = request.form.get("postal_code")
        official_email = request.form.get("official_email")
        phone_number = request.form.get("phone_number")
        country = request.form.get("country")
        # For login, we use the official email
        email = request.form.get("official_email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("user_register"))

        # Check if email is already registered in the users table
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            flash("Email already registered!", "danger")
            return redirect(url_for("user_register"))
        conn.close()

        # Generate a unique user_id
        user_id = str(uuid.uuid4())

        # Store the registration data temporarily in session
        session["register_data"] = {
            "user_id": user_id,
            "full_name": full_name,
            "date_of_birth": date_of_birth,
            "street_address": street_address,
            "city": city,
            "state": state,
            "postal_code": postal_code,
            "official_email": official_email,
            "phone_number": phone_number,
            "country": country,
            "email": email,
            "password": password
        }

        # Generate an OTP and store it in session
        otp = str(random.randint(100000, 999999))
        session["register_otp"] = otp
        session["register_email"] = email

        # Send OTP via email
        try:
            msg = Message("Your OTP for Registration - CertiChain",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email])
            msg.body = f"Your OTP for registration is: {otp}"
            mail.send(msg)
            flash("OTP sent to your email.", "success")
        except Exception as e:
            flash("Failed to send OTP: " + str(e), "danger")
            return redirect(url_for("user_register"))

        # Redirect to OTP verification page
        return redirect(url_for("verify_user_register_otp"))
    
    return render_template("user_register.html")

@app.route("/verify_user_register_otp", methods=["GET", "POST"])
def verify_user_register_otp():
    if request.method == "POST":
        submitted_otp = request.form.get("otp", "").strip()
        
        if submitted_otp == session.get("register_otp"):
            # Retrieve registration data from session
            register_data = session.get("register_data")
            if register_data:
                # Insert data into the database
                try:
                    conn = sqlite3.connect("database.db")
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO users (user_id, name, email, password)
                        VALUES (?, ?, ?, ?)
                    """, (
                        register_data["user_id"],
                        register_data["full_name"],
                        register_data["email"],
                        register_data["password"]
                    ))
                    conn.commit()
                    conn.close()
                except Exception as e:
                    flash("Error saving registration in database: " + str(e), "danger")
                    return redirect(url_for("user_register"))
                
                # Prepare user data for blockchain registration
                user_data = (
                    register_data["user_id"],          # userId
                    register_data["full_name"],        # name
                    register_data["date_of_birth"],    # dob
                    register_data["phone_number"],     # phoneNumber
                    register_data["country"],          # country
                    register_data["postal_code"],      # pincode
                    register_data["street_address"],   # streetAddress
                    register_data["city"],             # city
                    register_data["state"],            # state
                    register_data["official_email"],   # email
                    True                               # exists flag
                )
                try:
                    account = web3.eth.accounts[0]
                    tx_hash = contract.functions.registerUser(
                        register_data["user_id"],
                        user_data
                    ).transact({'from': account})
                    web3.eth.wait_for_transaction_receipt(tx_hash)
                except Exception as e:
                    flash("Error registering on blockchain: " + str(e), "danger")
                    return redirect(url_for("user_register"))
                
                # Send confirmation email to the user
                try:
                    msg = Message("Registration Successful - CertiChain",
                                  sender=app.config["MAIL_USERNAME"],
                                  recipients=[register_data["email"]])
                    msg.body = f"Your registration has been completed successfully.You can now log in using your credentials.Your user id is: {user_data[0]}"
                    mail.send(msg)
                except Exception as e:
                    flash("Registration successful, but error sending confirmation email: " + str(e), "warning")
                
                # Clear registration OTP and data from session
                session.pop("register_otp", None)
                session.pop("register_email", None)
                session.pop("register_data", None)
                
                flash("Registration successful! Please check your email for confirmation.", "success")
                return redirect(url_for("login"))
            else:
                flash("Session expired. Please register again.", "danger")
                return redirect(url_for("user_register"))
        else:
            flash("Incorrect OTP. Please try again.", "danger")
            return redirect(url_for("verify_user_register_otp"))
    
    return render_template("verify_user_register_otp.html")
  
@app.route("/register", methods=["GET", "POST"])
def register_institution():
    if request.method == "POST":
        # Retrieve form data into local variables
        institution_name = request.form["institution_name"]
        affiliation = request.form["affiliation"]
        reg_number = request.form["reg_number"]
        date_of_establishment = request.form["date_of_establishment"]
        institution_type = request.form["institution_type"]
        street_address = request.form["street_address"]
        city = request.form["city"]
        state = request.form["state"]
        postal_code = request.form["postal_code"]
        country = request.form["country"]
        official_email = request.form["official_email"]
        phone_number = request.form["phone_number"]
        admin_name = request.form["admin_name"]
        admin_designation = request.form["admin_designation"]
        admin_email = request.form["admin_email"]
        admin_phone = request.form["admin_phone"]
        login_email = request.form["email"]
        password = request.form["password"]

        # Connect to the database and check if any unique field already exists
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT institution_id FROM institutions 
                WHERE name=? OR reg_number=? OR official_email=? OR phone_number=? OR admin_email=? OR admin_phone=? OR email=?
            """, (institution_name, reg_number, official_email, phone_number, admin_email, admin_phone, login_email))
            result = cursor.fetchone()
        
        if result:
            flash("An institution with one or more of the provided details already exists.", "danger")
            return redirect(url_for("register_institution"))
        
        # If no duplicates found, store registration details in session for OTP verification
        session["register_data"] = {
            "institution_id": str(uuid.uuid4()),
            "name": institution_name,
            "affiliation": affiliation,
            "reg_number": reg_number,
            "date_of_establishment": date_of_establishment,
            "institution_type": institution_type,
            "street_address": street_address,
            "city": city,
            "state": state,
            "postal_code": postal_code,
            "country": country,
            "official_email": official_email,
            "phone_number": phone_number,
            "admin_name": admin_name,
            "admin_designation": admin_designation,
            "admin_email": admin_email,
            "admin_phone": admin_phone,
            "email": login_email,
            "password": password
        }

        # Generate OTP and store it in session along with the registration email
        otp = str(random.randint(100000, 999999))
        session["register_otp"] = otp
        session["register_email"] = login_email

        # Send OTP via email
        try:
            msg = Message("Your OTP for Registration - CertiChain",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[session["register_email"]])
            msg.body = f"Your OTP for registration is: {otp}"
            mail.send(msg)
            flash("OTP sent to your email.", "success")
        except Exception as e:
            flash("Failed to send OTP: " + str(e), "danger")
            return redirect(url_for("register_institution"))
        
        # Redirect to the OTP verification page
        return redirect(url_for("verify_register_otp"))

    return render_template("Register.html")

@app.route("/verify_register_otp", methods=["GET", "POST"])
def verify_register_otp():
    if request.method == "POST":
        submitted_otp = request.form.get("otp", "").strip()
        
        if submitted_otp == session.get("register_otp"):
            # Retrieve registration data from session
            register_data = session.get("register_data")
            if register_data:
                # Insert registration data into the database (verified remains 0 until admin approval)
                with sqlite3.connect("database.db", timeout=10) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO institutions (
                            institution_id, name, affiliation, reg_number, date_of_establishment,
                            institution_type, street_address, city, state, postal_code, country,
                            official_email, phone_number, admin_name, admin_designation,
                            admin_email, admin_phone, email, password, verified
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
                    """, (
                        register_data["institution_id"],
                        register_data["name"],
                        register_data["affiliation"],
                        register_data["reg_number"],
                        register_data["date_of_establishment"],
                        register_data["institution_type"],
                        register_data["street_address"],
                        register_data["city"],
                        register_data["state"],
                        register_data["postal_code"],
                        register_data["country"],
                        register_data["official_email"],
                        register_data["phone_number"],
                        register_data["admin_name"],
                        register_data["admin_designation"],
                        register_data["admin_email"],
                        register_data["admin_phone"],
                        register_data["email"],
                        register_data["password"]
                    ))
                    conn.commit()

                # Send confirmation email to the institution
                try:
                    msg = Message("Registration Request Received - CertiChain",
                                  sender=app.config["MAIL_USERNAME"],
                                  recipients=[session["register_email"]])
                    msg.body = ("Your registration request is under review. "
                                "Please wait for a confirmation message from the admin.")
                    mail.send(msg)
                except Exception as e:
                    flash("Failed to send confirmation email: " + str(e), "warning")
                
                # Clear registration-related session variables
                session.pop("register_otp", None)
                session.pop("register_email", None)
                session.pop("register_data", None)

                # Instead of redirecting immediately, render the same OTP page with a flag to trigger the popup
                return render_template("verify_register_otp.html", reset_success=True)
            else:
                flash("Session expired. Please register again.", "danger")
                return redirect(url_for("register_institution"))
        else:
            flash("Incorrect OTP. Please try again.", "danger")
            return redirect(url_for("verify_register_otp"))
    
    return render_template("verify_register_otp.html")

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        # Connect to the database and check admin credentials
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT admin_id FROM admin WHERE username = ? AND password = ?", (username, password))
        admin = cursor.fetchone()
        conn.close()

        if admin:
            session["admin_id"] = admin[0]
            session["admin_username"] = username
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid admin credentials.", "danger")
            return redirect(url_for("admin_login"))
    else:
        # For GET requests, disable caching
        response = make_response(render_template("admin_login.html"))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

@app.route("/admin_logout")
def admin_logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("admin_login"))

@app.route("/admin_dashboard")
def admin_dashboard():
    # Check if an admin is logged in
    if "admin_id" not in session:
        flash("Login using admin credentials.", "danger")
        return redirect(url_for("admin_login"))
    
    # Build response with cache-control headers to prevent caching
    response = make_response(render_template("admin_dashboard.html"))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/admin_complaints")
def admin_complaints():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT complaint_id, user_email, complaint_text, submission_date FROM complaints")
    rows = cursor.fetchall()
    conn.close()
    
    complaints = [
        {"complaint_id": row[0], "user_email": row[1], "complaint_text": row[2], "submission_date": row[3]}
        for row in rows
    ]
    return render_template("admin_complaints.html", complaints=complaints)

@app.route("/application_details/<institution_id>")
def application_details(institution_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM institutions WHERE institution_id = ?", (institution_id,))
    inst_data = cursor.fetchone()
    conn.close()
    
    if not inst_data:
        return "Institution not found", 404
    
    institution = {
        "institution_id": inst_data[0],
        "name": inst_data[1],
        "affiliation": inst_data[2],
        "reg_number": inst_data[3],
        "date_of_establishment": inst_data[4],
        "institution_type": inst_data[5],
        "street_address": inst_data[6],
        "city": inst_data[7],
        "state": inst_data[8],
        "postal_code": inst_data[9],
        "country": inst_data[10],
        "official_email": inst_data[11],
        "phone_number": inst_data[12],
        "admin_name": inst_data[13],
        "admin_designation": inst_data[14],
        "admin_email": inst_data[15],
        "admin_phone": inst_data[16],
        "email": inst_data[17] 
    }
    
    return render_template("application_details.html", institution=institution)

@app.route("/verify_institution/<institution_id>", methods=["POST"])
def verify_institution(institution_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Fetch the full institution record from the database
    cursor.execute("SELECT * FROM institutions WHERE institution_id = ?", (institution_id,))
    institution = cursor.fetchone()
    
    if institution:
        try:
            # Construct the Institution struct data as expected by your smart contract.
            institution_data = (
                institution[1],  # institutionName
                institution[2],  # affiliation
                institution[3],  # regNumber
                institution[4],  # dateOfEstablishment
                institution[5],  # institutionType
                institution[6],  # streetAddress
                institution[7],  # city
                institution[8],  # state
                institution[9],  # postalCode
                institution[10], # country
                institution[11], # officialEmail
                institution[12], # phoneNumber
                institution[13], # adminName
                institution[14], # adminDesignation
                institution[15], # adminEmail
                institution[16], # adminPhone
                True             # exists flag
            )
            
            # Use the first account from Ganache as the sender
            account = web3.eth.accounts[0]
            
            # Call the smart contract function to store the institution on the blockchain.
            tx_hash = contract.functions.registerInstitution(
                institution[0],    # _institutionID from the database
                institution_data   # The Institution struct data
            ).transact({'from': account})
            web3.eth.wait_for_transaction_receipt(tx_hash)
            
            # After a successful blockchain transaction, update the database record to set verified to 1
            cursor.execute("UPDATE institutions SET verified = 1 WHERE institution_id = ?", (institution_id,))
            conn.commit()
            
            # Send email confirmation to the institution's login email (assumed at index 17)
            try:
                msg = Message("Registration Approved - CertiChain",
                              sender=app.config["MAIL_USERNAME"],
                              recipients=[institution[17]])
                msg.body = ("Your institution registration request has been accepted. "
                            "Login to the portal using your login credentials.")
                mail.send(msg)
            except Exception as e:
                # Log the email sending error if needed
                print("Failed to send approval email:", e)
            
            conn.close()
            return jsonify({"success": True})
        except Exception as e:
            # Check if the error indicates that the institution is already registered on the blockchain.
            if "Institution with this Registration Number already exists" in str(e):
                cursor.execute("UPDATE institutions SET verified = 1 WHERE institution_id = ?", (institution_id,))
                conn.commit()
                # Send email confirmation even if already registered on blockchain
                try:
                    msg = Message("Registration Approved - CertiChain",
                                  sender=app.config["MAIL_USERNAME"],
                                  recipients=[institution[17]])
                    msg.body = ("Your institution registration request has been accepted. "
                                "Login to the portal using your login credentials.")
                    mail.send(msg)
                except Exception as e:
                    print("Failed to send approval email:", e)
                conn.close()
                return jsonify({"success": True, "message": "Institution already registered on blockchain, updated locally."})
            else:
                traceback.print_exc()  # For debugging: prints full traceback to the console.
                conn.close()
                return jsonify({"success": False, "error": str(e)})
    else:
        conn.close()
        return jsonify({"success": False, "error": "Institution not found"})

@app.route("/reject_institution/<institution_id>", methods=["GET", "POST"])
def reject_institution(institution_id):
    if request.method == "POST":
        reason = request.form.get("reason", "").strip()
        if not reason:
            return jsonify({"success": False, "error": "Please provide a reason for rejection."})
        
        # Connect to database and get institution's login email (used for login)
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM institutions WHERE institution_id = ?", (institution_id,))
        row = cursor.fetchone()
        if row:
            login_email = row[0]
        else:
            conn.close()
            return jsonify({"success": False, "error": "Institution not found."})
        
        # Send rejection email to the institution
        try:
            msg = Message("Registration Request Rejected - CertiChain",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[login_email])
            msg.body = f"Your institution registration request has been rejected.\nReason: {reason}"
            mail.send(msg)
        except Exception as e:
            conn.close()
            return jsonify({"success": False, "error": "Failed to send rejection email: " + str(e)})
        
        # Remove the institution from the database
        cursor.execute("DELETE FROM institutions WHERE institution_id = ?", (institution_id,))
        conn.commit()
        conn.close()
        
        return jsonify({"success": True, "message": "Institution rejected successfully."})
    else:
        return render_template("reject_institution.html", institution_id=institution_id)

@app.route("/pending_institutions", methods=["GET"])
def pending_institutions():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT institution_id, name FROM institutions WHERE verified = 0
    """)
    pending = cursor.fetchall()
    conn.close()
    # Convert to a list of dicts
    pending_list = [{"institution_id": row[0], "name": row[1]} for row in pending]
    return jsonify(pending_list)

@app.route("/accepted_institutions", methods=["GET"])
def accepted_institutions():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT institution_id, name FROM institutions WHERE verified = 1
    """)
    accepted = cursor.fetchall()
    conn.close()
    accepted_list = [{"institution_id": row[0], "name": row[1]} for row in accepted]
    return jsonify(accepted_list)

@app.route("/institution_details/<institution_id>")
def institution_details(institution_id):
    try:
        institution = contract.functions.getInstitution(institution_id).call()
        institution_data = {
            "institutionName": institution[0],
            "affiliation": institution[1],
            "regNumber": institution[2],
            "dateOfEstablishment": institution[3],
            "institutionType": institution[4],
            "streetAddress": institution[5],
            "city": institution[6],
            "state": institution[7],
            "postalCode": institution[8],
            "country": institution[9],
            "officialEmail": institution[10],
            "phoneNumber": institution[11],
            "adminName": institution[12],
            "adminDesignation": institution[13],
            "adminEmail": institution[14],
            "adminPhone": institution[15]
        }
    except Exception as e:
        # In case of error
        institution_data = None

    return render_template("institution_details.html", institution=institution_data, institution_id=institution_id)

@app.route("/homepage")
def homepage():
    if "user" not in session:
        return redirect(url_for("login"))
    institution_id = session.get("institution_id")
    response = make_response(render_template("home.html", user=session["user"], institution_id=institution_id))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/user_homepage")
def user_homepage():
    if "user_id" not in session:  # Check if the user is logged in
        return redirect(url_for("login"))

    response = make_response(render_template("home_user.html", user=session.get("user_name")))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/logout")
def logout():
    session.clear()  # Clears user session
    return redirect(url_for("login"))

@app.route("/inst_logout")
def inst_logout():
    session.clear()  # Clears all session data
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

from flask import request, render_template, redirect, url_for, flash, session
import uuid
from datetime import datetime

# Route for reporting an issue/complaint
@app.route("/report_issue", methods=["GET", "POST"])
def report_issue():
    if request.method == "POST":
        # Retrieve the complaint text from the form
        complaint_text = request.form.get("complaint", "").strip()
        if not complaint_text:
            flash("Complaint cannot be empty.", "danger")
            return redirect(url_for("report_issue"))
        
        # Get the logged-in user's email from the session
        user_email = session.get("login_email")
        if not user_email:
            flash("Please log in to submit a complaint.", "danger")
            return redirect(url_for("login"))
        
        # Generate a unique complaint ID and get the submission date
        complaint_id = str(uuid.uuid4())
        submission_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Insert the complaint into the database
        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO complaints (complaint_id, user_email, complaint_text, submission_date)
                VALUES (?, ?, ?, ?)
            """, (complaint_id, user_email, complaint_text, submission_date))
            conn.commit()
            flash("Your complaint has been submitted.", "success")
        except Exception as e:
            flash("Error submitting complaint: " + str(e), "danger")
        finally:
            conn.close()
        
        # After submission, redirect back to the user homepage (or another page)
        return redirect(url_for("user_homepage"))
    
    # For GET requests, display the complaint form
    return render_template("complaints.html")

# @app.route("/issue_certificate", methods=["GET", "POST"])
# def issue_certificate():
#     if request.method == "POST":
#         # Generate a unique certificate ID and set the issue date
#         cert_id = str(uuid.uuid4())
#         issue_date = datetime.now().strftime("%Y-%m-%d")

#         # Retrieve institution name from session (fallback to 'user' if 'institution_name' is not set)
#         issuing_authority = session.get("institution_name") or session.get("user")
#         if not issuing_authority:
#             flash("Institution name not found in session. Please log in again.", "danger")
#             return redirect(url_for("login"))

#         # Check if a User ID is provided
#         user_id = request.form.get("user_id", "").strip()
#         student_name, dob, user_email = None, None, None

#         if user_id:
#             try:
#                 user = contract.functions.getUser(user_id).call()
#                 if user and user[10]:  # Ensure the user exists in the blockchain
#                     student_name = user[1]  # Name
#                     dob = user[2]           # Date of Birth
#                     user_email = user[9]    # Email
#                 else:
#                     flash("User not found on blockchain. Please enter details manually.", "warning")
#             except Exception as e:
#                 flash("Error fetching user details from blockchain: " + str(e), "danger")

#         # If user details weren't found, get data from form
#         if not student_name:
#             student_name = request.form.get("student_name", "").strip()
#             dob = request.form.get("dob", "").strip()
#             user_email = request.form.get("user_email", "").strip()

#         # Retrieve course details from the form
#         course = request.form.get("course", "").strip()
#         course_duration = request.form.get("course_duration", "").strip()

#         # Validate required fields
#         if not all([student_name, dob, user_email, course, course_duration]):
#             flash("All fields are required.", "danger")
#             return redirect(url_for("issue_certificate"))

#         # Issue certificate on the blockchain
#         account = web3.eth.accounts[0]
#         try:
#             tx_hash = contract.functions.issueCertificate(
#                 cert_id,
#                 student_name,
#                 course,
#                 issue_date,
#                 dob,
#                 course_duration,
#                 issuing_authority,
#                 user_email
#             ).transact({'from': account})
#             web3.eth.wait_for_transaction_receipt(tx_hash)
#         except Exception as e:
#             flash("Error issuing certificate on blockchain: " + str(e), "danger")
#             return redirect(url_for("issue_certificate"))

#         # Store only cert_id, email, and course in the database
#         conn = sqlite3.connect("database.db")
#         cursor = conn.cursor()
#         try:
#             cursor.execute("""
#                 INSERT INTO certificates (cert_id, email, course) 
#                 VALUES (?, ?, ?)
#             """, (cert_id, user_email, course))
#             conn.commit()
#         except Exception as e:
#             traceback.print_exc()
#             flash("Error saving certificate in the database: " + str(e), "danger")
#         finally:
#             conn.close()
        
#         # Send an email to the user with the certificate ID
#         try:
#             msg = Message("Your Certificate has been Issued - CertiChain",
#                           sender=app.config["MAIL_USERNAME"],
#                           recipients=[user_email])
#             msg.body = (f"Dear {student_name},\n\n"
#                         f"Your certificate has been successfully issued on CertiChain.\n"
#                         f"Certificate ID: {cert_id}\n\n"
#                         "Thank you for using CertiChain.\n"
#                         "Best regards,\n"
#                         "CertiChain Team")
#             mail.send(msg)
#         except Exception as e:
#             flash("Certificate issued but error sending email: " + str(e), "warning")
        
#         # Instead of redirecting immediately, render a new template that shows the success popup.
#         return render_template("certificate_success.html", cert_id=cert_id)
    
#     else:
#         # For GET requests, provide the issue date and institution name
#         issue_date = datetime.now().strftime("%Y-%m-%d")
#         institution_name = session.get("institution_name") or session.get("user")
#         return render_template("issue_certificate.html", issue_date=issue_date, institution_name=institution_name)



@app.route("/issue_certificate", methods=["GET", "POST"])
def issue_certificate():
    if request.method == "POST":
        # Generate a unique certificate ID and set the issue date
        cert_id = str(uuid.uuid4())
        issue_date = datetime.now().strftime("%Y-%m-%d")

        # Retrieve institution name from session (fallback to 'user' if 'institution_name' is not set)
        issuing_authority = session.get("institution_name") or session.get("user")
        if not issuing_authority:
            flash("Institution name not found in session. Please log in again.", "danger")
            return redirect(url_for("login"))

        # Check if a User ID is provided and try fetching user details from blockchain
        user_id = request.form.get("user_id", "").strip()
        student_name, dob, user_email = None, None, None
        if user_id:
            try:
                user = contract.functions.getUser(user_id).call()
                if user and user[10]:  # Ensure the user exists in the blockchain
                    student_name = user[1]  # Name
                    dob = user[2]           # Date of Birth
                    user_email = user[9]    # Email
                else:
                    flash("User not found on blockchain. Please enter details manually.", "warning")
            except Exception as e:
                flash("Error fetching user details from blockchain: " + str(e), "danger")
        if not student_name:
            student_name = request.form.get("student_name", "").strip()
            dob = request.form.get("dob", "").strip()
            user_email = request.form.get("user_email", "").strip()

        # Retrieve course details from the form
        course = request.form.get("course", "").strip()
        course_duration = request.form.get("course_duration", "").strip()

        # Validate required fields
        if not all([student_name, dob, user_email, course, course_duration]):
            flash("All fields are required.", "danger")
            return redirect(url_for("issue_certificate"))

        # Issue certificate on the blockchain
        account = web3.eth.accounts[0]
        try:
            tx_hash = contract.functions.issueCertificate(
                cert_id,
                student_name,
                course,
                issue_date,
                dob,
                course_duration,
                issuing_authority,
                user_email
            ).transact({'from': account})
            web3.eth.wait_for_transaction_receipt(tx_hash)
        except Exception as e:
            flash("Error issuing certificate on blockchain: " + str(e), "danger")
            return redirect(url_for("issue_certificate"))

        # Store only cert_id, email, and course in the database
        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO certificates (cert_id, email, course) 
                VALUES (?, ?, ?)
            """, (cert_id, user_email, course))
            conn.commit()
        except Exception as e:
            traceback.print_exc()
            flash("Error saving certificate in the database: " + str(e), "danger")
        finally:
            conn.close()

        # Prepare certificate data for PDF generation
        cert_data = {
            "cert_id": cert_id,
            "student_name": student_name,
            "course": course,
            "issue_date": issue_date,
            "dob": dob,
            "course_duration": course_duration,
            "issuing_authority": issuing_authority,
            "user_email": user_email
        }
        # Render certificate HTML from template
        html = render_template("certificate_template.html", **cert_data)
        pdf_dir = "static/certificates"
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)
        pdf_path = os.path.join(pdf_dir, f"{cert_id}.pdf")
        options = {
            'page-width': '816px',
            'page-height': '1056px',
            'margin-top': '0px',
            'margin-bottom': '0px',
            'margin-left': '0px',
            'margin-right': '0px',
            'enable-local-file-access': None
        }
        pdfkit.from_string(html, pdf_path, options=options)

        # Send an email to the user with the certificate attached
        try:
            msg = Message("Your Certificate has been Issued - CertiChain",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[user_email])
            msg.body = (f"Dear {student_name},\n\n"
                        f"Your certificate for {course} has been successfully issued on Verificate by {issuing_authority}.\n"
                        f"Certificate ID: {cert_id}\n\n"
                        "Please find your certificate attached.\n\n"
                        "Best regards,\n"
                        "Verificate Team")
            with app.open_resource(pdf_path) as fp:
                msg.attach(f"{cert_id}.pdf", "application/pdf", fp.read())
            mail.send(msg)
        except Exception as e:
            flash("Certificate issued but error sending email: " + str(e), "warning")
        
        # Instead of redirecting immediately, render a success page that shows a popup message.
        return render_template("certificate_success.html", cert_id=cert_id)
    else:
        issue_date = datetime.now().strftime("%Y-%m-%d")
        institution_name = session.get("institution_name") or session.get("user")
        return render_template("issue_certificate.html", issue_date=issue_date, institution_name=institution_name)


#Revoke certificate section for institution
@app.route("/revoke_certificate_institution/<cert_id>", methods=["POST"])
def revoke_certificate_institution(cert_id):
    # Ensure an institution is logged in
    if "institution_id" not in session:
        return jsonify({"success": False, "error": "Please log in as an institution to revoke a certificate."}), 401

    try:
        account = web3.eth.accounts[0]
        tx_hash = contract.functions.revokeCertificate(cert_id).transact({'from': account})
        web3.eth.wait_for_transaction_receipt(tx_hash)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

#Revoke certificate section for admin
@app.route("/revoke_certificate_admin/<cert_id>", methods=["POST"])
def revoke_certificate_admin(cert_id):
    # Ensure an admin is logged in
    if "admin_id" not in session:
        flash("Please log in as admin to revoke a certificate.", "danger")
        return redirect(url_for("admin_login"))
    
    try:
        account = web3.eth.accounts[0]
        tx_hash = contract.functions.revokeCertificate(cert_id).transact({'from': account})
        web3.eth.wait_for_transaction_receipt(tx_hash)
        flash("Certificate revoked successfully.", "success")
    except Exception as e:
        flash("Error revoking certificate: " + str(e), "danger")
    
    # Redirect to the admin dashboard or a relevant page
    return redirect(url_for("admin_dashboard"))

@app.route("/issued_certificates")
def issued_certificates():
    # Connect to the database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT cert_id, email, course FROM certificates")
    rows = cursor.fetchall()
    conn.close()

    cert_list = []
    for row in rows:
        cert_id, email, course = row
        try:
            # Fetch certificate details from the blockchain
            cert_details = contract.functions.getCertificate(cert_id).call()
            # Check if the certificate exists (assuming the exists 
            if cert_details[8]:
                cert_list.append({
                    "cert_id": cert_id,
                    "email": email,
                    "course": course,
                    "student_name": cert_details[1]
                })
        except Exception as e:
            # Certificate not found or revoked; skip it.
            continue

    return render_template("issuedcert.html", certificates=cert_list)

@app.route("/revoked_certificates")
def revoked_certificates():
    # Connect to the database and fetch all certificate records
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT cert_id, email, course FROM certificates")
    rows = cursor.fetchall()
    conn.close()
    
    revoked_list = []
    for row in rows:
        cert_id, email, course = row
        try:
            # Attempt to fetch certificate details from the blockchain
            cert_details = contract.functions.getCertificate(cert_id).call()
            # In our contract, if a certificate is revoked, its exists flag is false (index 8)
            if not cert_details[8]:
                revoked_list.append({
                    "cert_id": cert_id,
                    "email": cert_details[7],  # Using blockchain value for user email
                    "course": course
                })
        except Exception as e:
            # Fallback: if the blockchain call fails, use the email from the database
            revoked_list.append({
                "cert_id": cert_id,
                "email": email,  # Using fallback email from database
                "course": course
            })
    
    return render_template("revokedcert.html", certificates=revoked_list)


@app.route("/certificate_details/<cert_id>")
def certificate_details(cert_id):
    try:
        # Fetch certificate details from the blockchain
        cert_details = contract.functions.getCertificate(cert_id).call()

        # Structure the certificate data
        cert_data = {
            "cert_id": cert_details[0],
            "student_name": cert_details[1],
            "course": cert_details[2],
            "issue_date": cert_details[3],
            "dob": cert_details[4],
            "course_duration": cert_details[5],
            "issuing_authority": cert_details[6],
            "user_email": cert_details[7]
        }
    except Exception as e:
        return f"Error fetching certificate details: {str(e)}", 500

    return render_template("certdetails.html", certificate=cert_data)

@app.route('/download_certificate/<cert_id>')
def download_certificate(cert_id):
    try:
        # Fetch certificate details directly from blockchain
        cert_details = contract.functions.getCertificate(cert_id).call()
        # Check if certificate exists (assuming 'exists' is at index 8)
        if not cert_details[8]:
            return "Certificate not found", 404

        # Structure the certificate data based on your contract's Certificate struct
        cert_data = {
            "cert_id": cert_details[0],
            "student_name": cert_details[1],
            "course": cert_details[2],
            "issue_date": cert_details[3],
            "dob": cert_details[4],
            "course_duration": cert_details[5],
            "issuing_authority": cert_details[6],
            "user_email": cert_details[7]
        }
    except Exception as e:
        return f"Error fetching certificate details: {str(e)}", 500

    # Render the certificate HTML template with the certificate data
    html = render_template("certificate_template.html", **cert_data)

    # Ensure the directory exists
    pdf_dir = "static/certificates"
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    
    # Path to save the PDF
    pdf_path = os.path.join(pdf_dir, f"{cert_id}.pdf")
    
    # Set pdfkit options to ensure proper page sizing and no extra space
    options = {
        'page-width': '816px',
        'page-height': '1056px',
        'margin-top': '0px',
        'margin-bottom': '0px',
        'margin-left': '0px',
        'margin-right': '0px',
        'enable-local-file-access': None
    }
    
    # Convert HTML to PDF using pdfkit with custom page size and margins
    pdfkit.from_string(html, pdf_path, options=options)
    
    # Serve the PDF file for download (or view inline by setting as_attachment=False)
    return send_file(pdf_path, as_attachment=True)

@app.route("/verify_certificate", methods=["GET", "POST"])
def verify_certificate():
    if request.method == "POST":
        cert_id = request.form.get("cert_id").strip()
        try:
            # Fetch certificate details from blockchain
            cert_details = contract.functions.getCertificate(cert_id).call()
            # Check if certificate exists (assuming the 'exists' flag is at index 8)
            if not cert_details[8]:
                flash("Certificate not found!", "danger")
                return redirect(url_for("verify_certificate"))
            # If exists, redirect to the certificate details page
            return redirect(url_for("certificate_details", cert_id=cert_id))
        except Exception as e:
            error_message = str(e)
            if "Certificate not found" in error_message:
                flash("Certificate not found!", "danger")
            else:
                flash("Error verifying certificate. Please try again.", "danger")
            return redirect(url_for("verify_certificate"))
    
    return render_template("verify_certificate.html")

@app.route("/view_certificates")
def view_certificates():
    # Get the logged-in user's email from the session
    user_email = session.get("login_email")
    if not user_email:
        flash("Please log in to view your certificates.", "danger")
        return redirect(url_for("login"))
    
    # Connect to the database and fetch certificates linked to the user's email
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT cert_id, email, course FROM certificates WHERE email = ?", (user_email,))
    rows = cursor.fetchall()
    conn.close()
    
    certificates = []
    for row in rows:
        cert_id, email, course = row
        try:
            # Fetch certificate details from the blockchain
            cert_details = contract.functions.getCertificate(cert_id).call()
            # Check that the certificate exists (active). Assuming index 8 is the exists flag.
            if cert_details[8]:
                certificates.append({
                    "cert_id": cert_id,
                    "email": email,
                    "course": course
                })
        except Exception as e:
            # If the blockchain call fails (e.g. revoked certificate reverts), skip this certificate.
            continue
    
    return render_template("view_certificates.html", certificates=certificates)

@app.route("/user_profile")
def user_profile():
    #  Get the logged-in user's email from the session.
    login_email = session.get("login_email")
    if not login_email:
        flash("Please log in to view your profile.", "danger")
        return redirect(url_for("login"))

    #  Look up the user_id (and full name) from the database using the login email.
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, name FROM users WHERE email = ?", (login_email,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        flash("User not found in the database.", "danger")
        return redirect(url_for("login"))

    user_id, full_name = row[0], row[1]

    #  Fetch additional user details from the blockchain using the user_id.
    try:
        user_details = contract.functions.getUser(user_id).call()
       
        if user_details and user_details[10]:
            user_data = {
                "full_name": user_details[1],
                "date_of_birth": user_details[2],
                "phone_number": user_details[3],
                "country": user_details[4],
                "postal_code": user_details[5],
                "street_address": user_details[6],
                "city": user_details[7],
                "state": user_details[8],
                "official_email": user_details[9]
            }
        else:
            flash("User details not found on blockchain.", "warning")
            user_data = {}
    except Exception as e:
        flash("Error fetching user details from blockchain: " + str(e), "danger")
        user_data = {}

    #  Fetch the certificate ID from the database using the login email.
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT cert_id FROM certificates WHERE email = ?", (login_email,))
    cert_row = cursor.fetchone()
    conn.close()
    certificate_id = cert_row[0] if cert_row else ""

    #  Prepare login credential info (from session or database)
    login_data = {"login_email": login_email}

    return render_template("user_profile.html",
                           certificate_id=certificate_id,
                           user_id=user_id,
                           user_data=user_data,
                           login_data=login_data)


@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        otp = request.form.get("otp")
        
        # Validate OTP against the one stored in session
        if otp != session.get("reset_otp"):
            flash("Invalid OTP. Please try again.", "danger")
            return redirect(url_for("reset_password"))
        
        # Retrieve the logged-in user's email from session
        login_email = session.get("login_email")
        if not login_email:
            flash("You must be logged in to reset your password.", "danger")
            return redirect(url_for("login"))
        
        # Connect to the database and fetch the current password
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE email = ?", (login_email,))
        row = cursor.fetchone()
        if not row or row[0] != old_password:
            conn.close()
            flash("Old password is incorrect.", "danger")
            return redirect(url_for("reset_password"))
        
        # Update the password in the database
        cursor.execute("UPDATE users SET password = ? WHERE email = ?", (new_password, login_email))
        conn.commit()
        conn.close()
        
        flash("Password updated successfully!", "success")
        # Redirect to user home page after successful reset
        return redirect(url_for("user_homepage"))
    
    else:
        # For GET requests: generate a new OTP for password reset and send it via email.
        login_email = session.get("login_email")
        if not login_email:
            flash("Please log in to reset your password.", "danger")
            return redirect(url_for("login"))
        
        otp = random.randint(100000, 999999)
        session["reset_otp"] = str(otp)
        
        msg = Message("Your OTP for Password Reset",
                      sender=app.config["MAIL_USERNAME"],
                      recipients=[login_email])
        msg.body = f"Your OTP for password reset is: {otp}"
        try:
            mail.send(msg)
        except Exception as e:
            flash("Failed to send OTP: " + str(e), "danger")
        
        # Render the reset password form with no-cache headers so it won't be cached
        response = make_response(render_template("reset_password.html"))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response


@app.route("/fetch_user/<user_id>")
def fetch_user(user_id):
    try:
        user = contract.functions.getUser(user_id).call()
        if user and user[10]:  
            user_data = {
                "userId": user[0],
                "name": user[1],
                "dob": user[2],
                "phoneNumber": user[3],
                "country": user[4],
                "pincode": user[5],
                "streetAddress": user[6],
                "city": user[7],
                "state": user[8],
                "email": user[9]
            }
        else:
            user_data = None
    except Exception as e:
        print("Error fetching user details:", e)
        user_data = None
    return render_template("issue_certificate.html", 
                           user_data=user_data, 
                           institution_name=session.get("institution_name"), 
                           issue_date=datetime.now().strftime("%Y-%m-%d"))


if __name__ == "__main__":
    app.run(debug=True)
