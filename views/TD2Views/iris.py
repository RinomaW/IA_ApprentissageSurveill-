from flask import  render_template, request
from sklearn.datasets import load_iris
import random
import matplotlib.pyplot as plt
from sklearn.datasets import load_diabetes


import os
# Créer une figure et un axe
def create_iris_plot():
    # Charger les données iris
    data = load_iris()
    X = data.data
    y = data.target
    target_names = data.target_names

    # Créer une figure et un axe
    fig, ax = plt.subplots()

    # Définir les couleurs pour chaque espèce
    colors = ['navy', 'darkorange', 'darkgreen']
    markers = ['o', '^', 's']

    # Plotter les données
    for color, i, target_name in zip(colors, range(3), target_names):
        ax.scatter(X[y == i, 2], X[y == i, 3], color=color, label=target_name, marker=markers[i])

    # Ajouter des étiquettes et une légende
    ax.set_xlabel('Longueur du pétale (cm)')
    ax.set_ylabel('Largeur du pétale (cm)')
    ax.legend(loc='best')
    ax.set_title('Iris Dataset')

    # Dynamically calculate the path to save the plot
    base_dir = os.path.dirname(__file__)  # Get the current directory of iris.py
    static_dir = os.path.join(base_dir, '..', '..', 'static')  # Navigate to the static folder

    # Ensure the 'static' directory exists
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # Save the image in the 'static' directory
    plt.savefig(os.path.join(static_dir, 'iris_plot.png'))
    plt.close()

# Appeler la fonction pour créer l'image
create_iris_plot()

# Initialiser l'application Flask
# app = Flask(__name__)

def display_iris():
    # Charger les données iris
    data = load_iris()
    X = data.data
    y = data.target

    # Choisir un échantillon aléatoire
    index = random.randint(0, len(data.data) - 1)
    sepal_length = data.data[index][0]
    sepal_width = data.data[index][1]
    petal_length = data.data[index][2]
    petal_width = data.data[index][3]
    class_label = data.target[index]
    class_name = data.target_names[class_label]
    
    # Filtrer par espèce si spécifié
    selected_species_index = request.args.get('species', default=-1, type=int)
    if selected_species_index >= 0:
        selected_species = data.target_names[selected_species_index]
        filtered_iris = [
            {
                'index': i,
                'sepal_length': X[i, 0],
                'sepal_width': X[i, 1],
                'petal_length': X[i, 2],
                'petal_width': X[i, 3]
            }
            for i in range(len(data.target)) if data.target[i] == selected_species_index
        ]
    else:
        selected_species = None
        filtered_iris = None

    return render_template(
        'TD2templates/iris.html',
        index=index,
        class_name=class_name,
        sepal_length=sepal_length,
        sepal_width=sepal_width,
        petal_length=petal_length,
        petal_width=petal_width,
        species_names=data.target_names,
        selected_species_index=selected_species_index,
        filtered_iris=filtered_iris,
        selected_species=selected_species
    )



def display_diabetes():
   
    
    diabetes = load_diabetes(scaled=False)
    index = random.randint(0, len(diabetes.data) - 1)
    features = diabetes.data[index]
    target_value = diabetes.target[index]

    sample_info = {
        'index': index,
        'target_value': target_value,
        'features': features
    }
    
    # Filtrer par des critères si nécessaire
    filtered_data = None  # Vous pouvez ajouter une logique de filtrage ici

    return render_template(
        'TD2templates/diabetes.html',
        sample_info=sample_info,
        filtered_data=filtered_data
    )

