from flask import Flask, render_template, request
from views import appTD3
from views import appTD1
from views import appTD2
import os
from views.TD2Views.models import db

app = Flask(__name__)

# Configuration de la base de données
basedir = os.path.abspath(os.path.dirname(__file__))
static_dir = os.path.join(basedir, 'static')
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

db_path = os.path.join(static_dir, "chinook.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser l'instance SQLAlchemy
db.init_app(app)

# Function to initialize the database
def initialize_db():
    """Initialize the database within the application context."""
    with app.app_context():
        db.create_all()  # Create tables if they don't exist




# --------------------------------------------------APP ROUTE------------------------------------------------------------------ #

@app.route('/')
def index():
    return render_template('index.html')

# ---------------------------------------------------TD1----------------------------------------------------------------------- #
@app.route('/td1')
def td1():
    return appTD1.index()

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return appTD1.hello()

@app.route('/image', methods=['GET', 'POST'])
def image():
    return appTD1.image()

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return appTD1.uploaded_file(filename)

# ---------------------------------------------------TD2----------------------------------------------------------------------- #
@app.route('/td2', methods=['GET', 'POST'])
def td2():
    return appTD2.index()

@app.route('/iris', methods=['GET', 'POST'])
def iris():
    return appTD2.iris()

@app.route('/diabete', methods=['GET', 'POST'])
def diabete():
    return appTD2.diabete()

@app.route('/kaggle', methods=['GET', 'POST'])
def kagger():
    return appTD2.Kaggle()

@app.route('/kaggle_class', methods=['GET', 'POST'])
def kaggel_class():
    return appTD2.Kaggle_Classification()



@app.route('/alchemy', methods=['GET', 'POST'])
def Alchemy_Route():
    return appTD2.Alchemy()

@app.route('/alchemy_nb_album', methods=['GET', 'POST'])
def Alchemy_Nb_Album():
    return appTD2.Alchemy_nb()


@app.route('/alchemy_10_artists', methods=['GET', 'POST'])
def Alchemy_Nb_Artist():
    return appTD2.Alchemy_10mostknown()


@app.route('/alchemy_Customers', methods=['GET', 'POST'])
def Alchemy_Customers():
    return appTD2.Alchemy_customers()


@app.route('/alchemy_Histogramme', methods=['GET', 'POST'])
def Alchemy_Histogramme():
    return appTD2.Alchemy_histogramme()

# ---------------------------------------------------TD3----------------------------------------------------------------------- #
@app.route('/td3', methods=['GET', 'POST'])
def td3():
    return appTD3.index()

@app.route('/td3tp1', methods=['GET', 'POST'])
def td3tp1():
    return appTD3.tp1()

@app.route('/td3tp2', methods=['GET', 'POST'])
def td3tp2():
    return appTD3.tp2()

@app.route('/td3tp3', methods=['GET', 'POST'])
def td3tp3():
    return appTD3.tp3()

if __name__ == '__main__':
    initialize_db()  # Initialize the database here
    app.run(host='0.0.0.0', port=5000,debug=True)    
