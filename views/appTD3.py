from flask import Flask, render_template,request  
from views.TD3Views import Cours3_TP1_RF
from views.TD3Views.Cours3_TP2_TF import train_model_view  # Assurez-vous d'importer la bonne fonction
from views.TD3Views import Cours3_TP3_TF_CNN 

app = Flask(__name__)

def index():
    return render_template('indexTD3.html')

def tp1():
    return Cours3_TP1_RF.loadDataDigits()

def tp2():
    return train_model_view()  # Assurez-vous d'appeler la bonne fonction

def tp3():
    return Cours3_TP3_TF_CNN.loadData()  # Default call for GET requests


if __name__ == '__main__':
    app.run(debug=True)
