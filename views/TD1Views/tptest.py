from flask import Flask, render_template, request
from views.TD1Views.view import coucou  # Import de la fonction coucou depuis view.py
from views.TD1Views import bonjour


def layout_tp():
    return render_template("TD1templates/layout.html")

# Route pour /coucou avec gestion des méthodes POST et GET
def coucou_route():
    if request.method == 'POST':
        # Récupère le nom envoyé via le formulaire
        name = request.form.get('name')
        return coucou(name)
    else:
        return coucou()
    
def bonjour_route():
    if request.method == 'POST':
        # Récupère le nom envoyé via le formulaire
        prenom = request.form.get('prenom')
        return bonjour(prenom)
    else:
        return bonjour()

