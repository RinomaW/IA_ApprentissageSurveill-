from flask import render_template, request
from tensorflow import keras

# Importations de Keras
cifar100 = keras.datasets.cifar100
Sequential = keras.models.Sequential
Dense = keras.layers.Dense
Flatten = keras.layers.Flatten
Conv2D = keras.layers.Conv2D
MaxPooling2D = keras.layers.MaxPooling2D
sparse_categorical_crossentropy = keras.losses.sparse_categorical_crossentropy
Adam = keras.optimizers.Adam
SGD = keras.optimizers.SGD
RMSprop = keras.optimizers.RMSprop

def loadData(n_epoch=50, validation_split=0.2, batch_size=50, optimizer_name='adam'):
    if request.method == 'POST':
        # Récupérer les paramètres du formulaire
        n_epoch = int(request.form.get('n_epoch', 50))  # Augmenté par défaut à 50
        validation_split = float(request.form.get('validation_split', 0.2))
        batch_size = int(request.form.get('batch_size', 50))
        optimizer_name = request.form.get('optimizer', 'adam')

        # Choisir l'optimiseur
        if optimizer_name == 'adam':
            optimizer = Adam(learning_rate=0.001)  # Taux d'apprentissage par défaut
        elif optimizer_name == 'sgd':
            optimizer = SGD(learning_rate=0.01)  # Taux d'apprentissage pour SGD
        elif optimizer_name == 'rmsprop':
            optimizer = RMSprop(learning_rate=0.001)  # Taux d'apprentissage pour RMSprop
        else:
            optimizer = Adam(learning_rate=0.001)  # Par défaut

        # Configuration du modèle
        img_width, img_height, img_num_channels = 32, 32, 3
        no_classes = 100
        verbosity = 1

        # Chargement des données CIFAR-100
        (input_train, target_train), (input_test, target_test) = cifar100.load_data()

        # Déterminer la forme des données
        input_shape = (img_width, img_height, img_num_channels)

        # Normaliser les données
        input_train = input_train.astype('float32') / 255
        input_test = input_test.astype('float32') / 255

        # Création du modèle
        model = Sequential()
        model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(256, activation='relu'))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(no_classes, activation='softmax'))

        # Compiler le modèle
        model.compile(loss=sparse_categorical_crossentropy,
                      optimizer=optimizer,
                      metrics=['accuracy'])

        # Ajuster les données au modèle
        history = model.fit(input_train, target_train,
                            batch_size=batch_size,
                            epochs=n_epoch,
                            verbose=verbosity,
                            validation_split=validation_split)

        # Générer des métriques de généralisation
        score = model.evaluate(input_test, target_test, verbose=0)
        loss = score[0]
        accuracy = score[1]

        listRetour = [[n_epoch,validation_split,score[0],score[1],history.history['loss'][0],history.history['accuracy'][0],history.history['loss'][n_epoch-1],history.history['accuracy'][n_epoch-1]]]


        # Retourner les résultats
        return render_template('TD3templates/Tp3.html', loss=loss, accuracy=accuracy, 
                               n_epoch=n_epoch, validation_split=validation_split, 
                               batch_size=batch_size, optimizer_name=optimizer_name,listRetour=listRetour)

    # Si GET, afficher la page avec des valeurs par défaut
    return render_template('TD3templates/Tp3.html', loss=None, accuracy=None, 
                           n_epoch=n_epoch, validation_split=validation_split, 
                           batch_size=batch_size, optimizer_name=optimizer_name)
