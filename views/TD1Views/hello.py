from flask import render_template, request

def calculer_indice_de_chaleur(temp, humidite):
    c1 = -8.785
    c2 = 1.611
    c3 = 2.339
    c4 = -0.146
    c5 = -1.231e-2
    c6 = -1.642e-2
    c7 = 2.212e-3
    c8 = 7.255e-4
    c9 = -3.582e-6
    
    hi = (c1 + (c2 * temp) + (c3 * humidite) + (c4 * temp * humidite) +
          (c5 * (temp**2)) + (c6 * humidite**2) +
          (c7 * (temp**2) * humidite) + (c8 * temp * (humidite**2)) +
          (c9 * (temp**2) * (humidite**2)))
    
    return round(hi, 2)

def hello_tp1():
    indice_de_chaleur = None
    chaleur_f = None
    if request.method == 'POST':
        temp = float(request.form.get('temperature'))
        humidite = float(request.form.get('humidite'))

        indice_de_chaleur = calculer_indice_de_chaleur(temp, humidite)
        chaleur_f = round((indice_de_chaleur * (9/5)) + 32)
    
    return render_template('TD1templates/hello.html', indice_de_chaleur=indice_de_chaleur, chaleur_f=chaleur_f)
