from flask import render_template


def coucou(name=None):
    return render_template('coucou.html', name=name)
