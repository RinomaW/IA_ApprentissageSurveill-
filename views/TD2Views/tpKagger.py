from flask import Flask, render_template,request
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Charger les données Excel
def load_data():
    base_dir = os.path.dirname(__file__)  # Get the current directory of the script
    static_dir = os.path.join(base_dir, '..', '..', 'static')  # Navigate to the static folder
    file_path = os.path.join(static_dir, 'vgsales.csv')  # Full path to the CSV file

    # Check if the file exists before attempting to read it
    if not os.path.exists(file_path):
        print(f"Le fichier {file_path} est introuvable.")
        return pd.DataFrame()  # Return an empty DataFrame if file is not found

    try:
        df = pd.read_csv(file_path)
        return df
    except pd.errors.EmptyDataError:
        print("Le fichier CSV est vide.")
        return pd.DataFrame()  # Return an empty DataFrame in case the file is empty
    except pd.errors.ParserError:
        print("Erreur de format lors de la lecture du fichier CSV.")
        return pd.DataFrame()  # Return an empty DataFrame in case of parsing errors
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV: {e}")
        return pd.DataFrame()

def kagger_jeux():
    df = load_data()
    # Limit to the top 100 games
    data = df.head(100).to_dict(orient='records')
    return render_template('TD2templates/kagger.html', games=data)


def Classification():
    if request.method == 'POST':
        base_dir = os.path.dirname(__file__)  # Get the current directory of the script
        static_dir = os.path.join(base_dir, '..', '..', 'static')  # Navigate to the static folder
        file_path = os.path.join(static_dir, 'vgsales.csv')  # Full path to the CSV file

        # Load and preprocess the data
        data = pd.read_csv(file_path)

        # Preprocessing
        data['Year'] = data['Year'].fillna(data['Year'].mean())
        data['Publisher'] = data['Publisher'].fillna('Unknown')

        # Label encoding for categorical variables
        le = LabelEncoder()
        data['Platform'] = le.fit_transform(data['Platform'])
        data['Genre'] = le.fit_transform(data['Genre'])
        data['Publisher'] = le.fit_transform(data['Publisher'])

        # Classification target variable
        data['target'] = (data['Global_Sales'] > data['Global_Sales'].mean()).astype(int)

        # Define the features and target for classification
        X = data.drop(['Name', 'Rank', 'Global_Sales', 'target'], axis=1)
        y = data['target']

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model = LogisticRegression()
        model.fit(X_train, y_train)

        # Generate predictions and evaluation metrics
        y_pred = model.predict(X_test)
        class_report = classification_report(y_test, y_pred, output_dict=True)
        conf_matrix = confusion_matrix(y_test, y_pred).tolist()  # Convert to list

        return render_template('TD2templates/KaggerClass.html', class_report=class_report, conf_matrix=conf_matrix)

    return render_template('TD2templates/KaggerClass.html')


    
