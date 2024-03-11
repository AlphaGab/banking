from flask import Blueprint,render_template,current_app,request,redirect,url_for,make_response,session,abort
from website.bankModel import BankUser
from website.auth  import disableCache

view =  Blueprint('view',__name__)

@view.route('/account_dashboard')
def show_dashboard():
    card_number= session.get('cardnumber', None)
    if card_number:
        response = make_response(render_template('dashboard.html',bank_user=show_user_details(card_number)))
        print("here")
        return disableCache(response) 
    else:
        abort(400)

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
    
    except Exception as e:
        print(f"Error executing the query: {str(e)}")
