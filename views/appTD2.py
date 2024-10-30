from flask import render_template
from views.TD2Views.iris import display_iris
from views.TD2Views.iris import display_diabetes
from views.TD2Views.tpKagger import kagger_jeux
from views.TD2Views.tpKagger import Classification
from views.TD2Views.tp2_1Alchemy import db_load
from views.TD2Views.tp2_1Alchemy import db_load_nb_album
from views.TD2Views.tp2_1Alchemy import popular_artists
from views.TD2Views.tp2_1Alchemy import get_top_spending_customers
from views.TD2Views.tp2_1Alchemy import genres_histogram



def index():
    return render_template('indexTD2.html')

def iris():
    return display_iris()

def diabete():
    return display_diabetes()

def Kaggle():
    return kagger_jeux()


def Kaggle_Classification():
    return Classification()

def Alchemy():
    return db_load()  # Call the alchemy function directly


def Alchemy_nb():
    return db_load_nb_album() 


def Alchemy_10mostknown():
    return popular_artists()

def Alchemy_customers():
    return get_top_spending_customers()


def Alchemy_histogramme():
    return genres_histogram()

