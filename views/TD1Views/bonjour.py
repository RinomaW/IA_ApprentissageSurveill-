from flask import render_template


def bonjour(prenom =None):
    return render_template('TD1templates/bonjour.html', prenom=prenom)