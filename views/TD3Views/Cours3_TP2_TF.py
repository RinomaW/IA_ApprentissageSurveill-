from flask import Flask, request, render_template
from tensorflow import keras

mnist = keras.datasets.mnist
results_list = []  # Liste globale pour stocker les résultats des requêtes

def create_model(num_classes, num_hidden_layers, units_per_layer, activation_function='relu'):
    model = keras.Sequential()
    model.add(keras.Input(shape=(28 * 28,)))  # Couche d'entrée

    # Ajouter des couches cachées avec la fonction d'activation choisie
    for _ in range(num_hidden_layers):
        model.add(keras.layers.Dense(units_per_layer, activation=activation_function))

    # Couche de sortie avec 10 classes
    model.add(keras.layers.Dense(num_classes, activation='softmax'))
    return model
def train_model_view():
    if request.method == 'POST':
        # Récupérer les paramètres du formulaire
        num_hidden_layers = int(request.form.get('num_hidden_layers', 1))
        units_per_layer = int(request.form.get('units_per_layer', 128))
        batch_size = int(request.form.get('batch_size', 128))
        epochs = int(request.form.get('epochs', 20))
        activation_function = request.form.get('activation_function', 'relu')  # Utiliser la fonction d'activation choisie
        loss_function = request.form.get('loss_function', 'categorical_crossentropy')  # Récupérer la fonction de perte choisie
        validation_split = float(request.form.get('validation_split', 0.1))  # Récupérer le pourcentage de validation

        # Charger les données
        (X_train, y_train), (X_test, y_test) = mnist.load_data()
        X_train = X_train.reshape(X_train.shape[0], -1).astype('float32') / 255.0
        X_test = X_test.reshape(X_test.shape[0], -1).astype('float32') / 255.0

        # Si on utilise Sparse Categorical Crossentropy, pas besoin de convertir y_train et y_test
        if loss_function == 'sparse_categorical_crossentropy':
            y_train = y_train
            y_test = y_test
        else:
            y_train = keras.utils.to_categorical(y_train, num_classes=10)
            y_test = keras.utils.to_categorical(y_test, num_classes=10)

        # Créer le modèle
        model = create_model(num_classes=10, num_hidden_layers=num_hidden_layers, 
                             units_per_layer=units_per_layer, activation_function=activation_function)

        # Compiler le modèle avec la fonction de perte choisie
        model.compile(loss=loss_function, optimizer='adam', metrics=['accuracy'])

        # Entraîner le modèle avec le pourcentage de validation spécifié
        model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1, validation_split=validation_split)

        # Tester le modèle
        score = model.evaluate(X_test, y_test, verbose=0)

        # Enregistrer les résultats dans la liste globale
        results_list.insert(0, {  # Insérer à la position 0 pour avoir la dernière requête en premier
            'num_hidden_layers': num_hidden_layers,
            'units_per_layer': units_per_layer,
            'batch_size': batch_size,
            'epochs': epochs,
            'test_loss': score[0],
            'test_accuracy': score[1],
            'activation_function': activation_function
        })

    return render_template('TD3templates/Tp2.html', results=results_list)