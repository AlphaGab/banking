from flask import Flask,render_template,request,redirect,url_for
from website.auth import auth
import yaml
import pymysql



app = Flask(__name__,template_folder='website/template')
db = yaml.safe_load(open('db.yaml'))


app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_PORT']= db['mysql_port']
app.config['MYSQL_USER'] =db['mysql_user']
app.config['MYSQL_PASSWORD'] =db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['SECRET_KEY'] = 'hello' 
app.config['db_connection']= pymysql.connect(
        host=app.config['MYSQL_HOST'],
        port=app.config['MYSQL_PORT'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
            )



app.register_blueprint(auth,url_prefix='/')

@app.route('/')
def index():
    return redirect(url_for('auth.login'))






if __name__ == '__main__':
    app.run(debug=True)

