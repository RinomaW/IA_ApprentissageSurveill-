from flask import Flask, render_template, request
from sklearn.datasets import load_digits, load_iris, load_diabetes
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import linear_model

def loadDataDigits():
    test_size = 0.1  # Valeur par défaut
    n_estimators = 10  # Valeur par défaut
    dataset_name = 'digits'  # Valeur par défaut

    if request.method == 'POST':
        # Récupérer les valeurs du formulaire
        test_size = float(request.form.get('test_size', 0.1))
        n_estimators = int(request.form.get('n_estimators', 10))
        dataset_name = request.form.get('dataset', 'digits')  # Nouvelle ligne pour récupérer le nom du dataset

    # Charger les données en fonction de la sélection
    classifications = load_data(dataset_name,n_estimators,test_size)
    # Générer le rapport de classification
    

    return render_template('TD3templates/Tp1.html', n_estimate=n_estimators, test_size=test_size, classifications=classifications, dataset=dataset_name)

def load_data(dataset_name,n_estimators,test_size ):
    if dataset_name == 'digits':
        data = load_digits()
        classifications = load_database(data, test_size, n_estimators)
        return classifications
    elif dataset_name == 'diabetes':
        data =  load_diabetes()
        classifications = load_database_diabete(data, test_size, n_estimators)
        return classifications
    elif dataset_name == 'iris':
        data =  load_iris()
        classifications = load_database(data, test_size, n_estimators)
        return classifications
    else:

        raise ValueError("Dataset non supporté")

def load_database(data, test_size, n_estimators):
    # Diviser les données
    Xtrain, Xtest, ytrain, ytest = train_test_split(
        data.data, 
        data.target,
        test_size=test_size
    )
    # Définir le modèle
    model = RandomForestClassifier(n_estimators)

    # Entraîner le modèle
    model.fit(Xtrain, ytrain)

    # Prédire avec le modèle
    ypred = model.predict(Xtest)

    # Générer le rapport de classification
    classifications = metrics.classification_report(ytest, ypred)  # Retourne sous forme de chaîne
    return classifications


def load_database_diabete(data, test_size, n_estimators):
    # Charger les données
    X = data.data
    y = data.target

    # Convertir la cible continue en classes (par exemple, seuil à 140)
    threshold = 140
    y = (y > threshold).astype(int)  # 1 si diabétique, 0 sinon

    # Diviser les données
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)

    # Créer le modèle de régression logistique
    model = linear_model.LogisticRegression()

    # Ajuster le modèle
    model.fit(X_train, y_train)

    # Faire des prédictions
    y_pred = model.predict(X_test)

    # Générer le rapport de classification
    classifications = metrics.classification_report(y_test, y_pred)
    return classifications
    
