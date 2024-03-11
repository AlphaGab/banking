from flask import Blueprint,render_template,current_app,request,redirect,url_for,session,make_response
import random
from website.bankModel import BankUser

auth =  Blueprint('auth',__name__)


@auth.route('/login', methods =['GET','POST'])
def login():
    if request.method == "POST":
      print("Hlloe")      

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        customer_name = request.form['name']
        account_type = request.form['account_type']
        pin_number = request.form['pin']
        balance = request.form['initial_deposit']
        bankuser = BankUser(customer_name, account_type, pin_number, balance)

        if len(bankuser.customer_name) <= 5:
            print("here")
            return render_template('register.html', bankuser=bankuser, error_message="Name too short")
           
        elif len(bankuser.pin_number) != 4:
            print("here")
            return render_template('register.html', bankuser=bankuser, error_message="Pin should be 4 digits long")
        elif len(bankuser.account_type) < 1:
            print("here")
            return render_template('register.html', bankuser=bankuser, error_message="Choose Account type")
        elif account_type not in ["fixed", "credit"]:
            print("here")
            return render_template('register.html', bankuser=bankuser, error_message="Error account type")
        elif int(bankuser.balance) <= 2500:
            print("here")
            return render_template('register.html', bankuser=bankuser, error_message="Minimum Deposit is 2500 Php")
        
        cardnumber = generate_card_number()
        insertUser(cardnumber, bankuser)
        return redirect(url_for('auth.show_card_number', cardnumber=cardnumber))
        
    response = make_response(render_template('register.html'))
    return disableCache(response)


@auth.route('/show_card_number/<cardnumber>')
def show_card_number(cardnumber):
   response = make_response(render_template('cardnumber.html',cardnumber=cardnumber))
   return disableCache(response)


def generate_card_number():
    card_number = ''.join(random.choices('0123456789', k=8))
    return card_number



def insertUser(cardnumber,bankuser:BankUser):
    connection = current_app.config['db_connection']
    try:
        with connection.cursor() as cursor:

            cursor.execute(
                "INSERT INTO users (card_number,customer_name, account_type, pin_number, balance) VALUES (%s,%s, %s, %s, %s)",
                (cardnumber,bankuser.customer_name, bankuser.account_type, bankuser.pin_number,bankuser.balance)
            )
        connection.commit()
    except Exception as e:
        print(f"Error inserting data into the database: {str(e)}")

def disableCache(response):
    response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache" 
    response.headers["Expires"] = "0"
    print("here disabled")
    return response