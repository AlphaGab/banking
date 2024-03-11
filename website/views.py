from flask import Blueprint,render_template,current_app,request,redirect,url_for,make_response,session,abort
from website.bankModel import BankUser
from website.auth  import disableCache

view =  Blueprint('view',__name__)

@view.route('/account_dashboard')
def show_dashboard():
    card_number= session.get('cardnumber', None)
    if card_number:
        bank_user=show_user_details(card_number)
        response = make_response(render_template('dashboard.html',bank_user=bank_user))
        session['bankuser'] = bank_user.__dict__
        return disableCache(response) 
    else: abort(400)


@view.route('account_dashboard/deposit',methods=['GET','POST'])
def deposit_route():
    bankuser =session.get('bankuser')
    if request.method == 'POST':
        deposit(request.form['amount'])
        return disableCache(make_response(render_template('success.html', success="Deposit was successful")))
    else:
        if bankuser:
            response = make_response(render_template('deposit.html', balance=bankuser['balance']))
            return disableCache(response)
        else:  abort(400)

@view.route('account_dashboard/withdraw',methods=['GET','POST'])

def withdraw_route():
    bankuser =session.get('bankuser')
    if request.method == 'POST':
        withdraw(request.form['amount'])
        if isAmountValid(float(request.form['amount']),float(bankuser['balance'])):
            return disableCache(make_response(render_template('success.html', success="Withdraw was successful",)))
        return disableCache(make_response(render_template('withdraw.html', balance=bankuser['balance'],error="Invalid Withdrawal")))
    else:
        if bankuser:
            response = make_response(render_template('withdraw.html', balance=bankuser['balance']))
            return disableCache(response)
        else: abort(400)


def show_user_details(card_number):
    connection = current_app.config['db_connection']
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM users WHERE card_number = %s"
            cursor.execute(query, (card_number))
            result = cursor.fetchone()

        if result:
            
            return BankUser(result[2],result[3],balance=result[5],card_number=result[1])
        else: return "Nothing Found"

    except Exception as e: print(f"Error executing the query: {str(e)}")

def deposit(amount):
    connection = current_app.config['db_connection']
    bankuser = session['bankuser']
    new_bal = float(bankuser['balance']) + float(amount)
 
    try:
        with connection.cursor() as cursor:
            # Update the balance for the specific card number
            query = "UPDATE users SET balance = %s WHERE card_number = %s"
            cursor.execute(query, (new_bal, bankuser['card_number']))
            connection.commit()
        
        return bankuser

    except Exception as e: print(f"Error executing the query: {str(e)}")

def withdraw(amount):
    connection = current_app.config['db_connection']
    bankuser = session['bankuser']
    new_bal = float(bankuser['balance']) - float(amount)
    try:
        with connection.cursor() as cursor:
            query = "UPDATE users SET balance = %s WHERE card_number = %s"
            cursor.execute(query, (new_bal, bankuser['card_number']))
            connection.commit()
        
        return bankuser

    except Exception as e: print(f"Error executing the query: {str(e)}")

def isAmountValid(amount,balance):
    if amount <= balance:
        return True
    return False