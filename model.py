import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

from preprocess import clean_text


MODEL_FILE = "model.joblib"
VECTORIZER_FILE = "vectorizer.joblib"


def train_model():
    #read the CSV file
    data = pd.read_csv("dataset.csv")

    #clean all email texts
    data["clean_text"] = data["email_text"].apply(clean_text)

    #these are the emails
    x = data["clean_text"]

    #these are the answers: phishing or legitimate
    y = data["label"]

    # Split the data into training data and testing data
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=1
    )

    #turn words into numbers
    vectorizer = TfidfVectorizer(max_features=2000)

    x_train_numbers = vectorizer.fit_transform(x_train)
    x_test_numbers = vectorizer.transform(x_test)

    #create the model
    model = LogisticRegression(max_iter=1000)

    #train the model
    model.fit(x_train_numbers, y_train)

    #test the model
    predictions = model.predict(x_test_numbers)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, pos_label="phishing")
    recall = recall_score(y_test, predictions, pos_label="phishing")

    #save the model and vectorizer
    joblib.dump(model, MODEL_FILE)
    joblib.dump(vectorizer, VECTORIZER_FILE)

    return accuracy, precision, recall


def load_model():
    #load the saved model
    model = joblib.load(MODEL_FILE)

    #looading saved vectorizer
    vectorizer = joblib.load(VECTORIZER_FILE)

    return model, vectorizer


def predict_email(email_text, model, vectorizer):
    #clean new email
    cleaned_email = clean_text(email_text)

    #turn  email to numbers
    email_numbers = vectorizer.transform([cleaned_email])

    #predict  result
    prediction = model.predict(email_numbers)[0]

    #get confidence score
    probabilities = model.predict_proba(email_numbers)[0]

    class_names = list(model.classes_)
    prediction_index = class_names.index(prediction)

    confidence = probabilities[prediction_index]

    return prediction, confidence
