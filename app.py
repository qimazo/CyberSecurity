

# os is used to check if a file exists.
import os

#sys is used to read the command from the terminal.
import sys

# These functions come from preprocess.py.
# They help us find links and warning signs in the email.
from preprocess import count_links, find_warning_signs

# db.py is used for the database.
# It saves and reads old email results.
import db

# model.py is used for the machine learning model.
# It trains the model and predicts if an email is phishing.
import model


def main():
    """
    This is the main function.

    It checks what command the user typed.
    Then it calls the correct function.
    """

    # sys.argv is a list of words from the terminal.
   #we need at least 2 items in sys.argv.
    if len(sys.argv) < 2:
        print("Please give a command: train, analyze, history, or report")
        return

    # This gets the command word
    command = sys.argv[1]

    # If the user types "report" we show the summary
    if command == "report":
        report()
        return

    #if the user types "history" we show old checked emails.
    if command == "history":
        history()
        return

    #if the user types "train", we train the model.
    if command == "train":
        train()
        return

    #if the user types "analyze", we check one email.
    if command == "analyze":

        # Sometimes the user gives a file name too.
  
        # In that case, sys.argv[2] is the file name.
        file_path = None

        if len(sys.argv) > 2:
            file_path = sys.argv[2]

        # Now we send the file path to the analyze function.
        # If there is no file path, it will ask the user to paste the email.
        analyze(file_path)
        return

    # If the command is not known, we show this message.
    print("Unknown command. Use: train, analyze, history, or report")


def report():


    #make sure the database table exists before using it.
    db.create_table()

    #get summary numbers from the database.
    stats = db.get_summary()

    #the confidence is saved like 0.92
    #we change it to 92.0% because it is easier to read
    average_confidence = round(stats["avg_confidence"] * 100, 1)

    print("=== Report ===")
    print("Total emails checked: " + str(stats["total"]))
    print("Phishing found:       " + str(stats["phishing_count"]))
    print("Legitimate emails:    " + str(stats["legit_count"]))
    print("Average confidence:   " + str(average_confidence) + "%")


def history():
    """
    This function shows the last email results from the database.

    It does not show the full email text.
    It only shows a short part, so the screen stays clean.
    """

    #make sure the database table exists
    db.create_table()

    #get old results from the database
    rows = db.get_history()
  
    #if the database is empty, show a helpful message
    if not rows:
        print("No history yet. Try 'python app.py analyze' first.")
        return

    #go through each saved result
    for row in rows:

        #each row has these values
        row_id, prediction, confidence, email_text, date_checked = row

        #Only show the first 50 characters of the email
        #This makes the history easier to read
        short_text = email_text[:50]

        #replace new lines with spaces.
        # This keeps each result on one line.
        short_text = short_text.replace("\n", " ")

        #change confidence from 0.92 to 92.
        confidence_percent = round(confidence * 100)

        #print one history result
        print(
            str(row_id) + ". " +
            prediction.upper() +
            " (" + str(confidence_percent) + "%) - " +
            short_text + "... - " +
            date_checked
        )


def train():
    """
    This function trains the model.

    It also prints accuracy, precision, and recall.
    These numbers help us understand how good the model is.
    """

    print("Training model, please wait...")

    #train the model using the train_model function from model.py.
    # the function gives back 3 numbers
    accuracy, precision, recall = model.train_model()

    #change numbers like 0.91 to 91.0%.
    accuracy_percent = round(accuracy * 100, 1)
    precision_percent = round(precision * 100, 1)
    recall_percent = round(recall * 100, 1)

    #print  result for the user
    print("Model trained successfully!")
    print("Accuracy:  " + str(accuracy_percent) + "%")
    print("Precision: " + str(precision_percent) + "%")
    print("Recall:    " + str(recall_percent) + "%")


def analyze(file_path=None):
   

    #before we analyze an email, we need a trained model
    #if the model file does not exist, we tell the user to train first
    if not os.path.exists(model.MODEL_FILE):
        print("No trained model found. Please run: python app.py train")
        return

    #if the user gave a file path, read the email from that file
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            email_text = file.read()

    # If there is no file path ask the user to paste the email
    else:
        print("Paste the email text below, then press Enter:")
        email_text = input("> ")

    # If the email is empty, stop the function.
    if email_text.strip() == "":
        print("No email text was given.")
        return

    # Find warning signs in the email
    warning_signs = find_warning_signs(email_text)

    # Count how many links are in the email
    links = count_links(email_text)

    # Load the trained model and the vectorizer
    # The vectorizer changes text into numbers for the model
    trained_model, vectorizer = model.load_model()

    #predict if the email is phishing or legitimate
    #confidence shows how sure the model is
    prediction, confidence = model.predict_email(
        email_text,
        trained_model,
        vectorizer
    )

    #Change confidence from 0.91 to 91.0%.
    confidence_percent = round(confidence * 100, 1)

    #pint an empty line to make the output clener
    print("")

    #show the main result
    print("Result: " + prediction.upper())
    print("Confidence: " + str(confidence_percent) + "%")

    #if there are warning signs, print them one by one.
    if warning_signs:
        print("Warning signs:")

        for sign in warning_signs:
            print(" - " + sign)

    #if there are no warning signs, say that.
    else:
        print("Warning signs: none found")

    #make sure the database table exists.
    db.create_table()

    #Save the result in the database.
    db.save_result(
        email_text,
        prediction,
        confidence,
        links,
        warning_signs
    )

    print("Saved to database.")


# If another file imports app.py, main() will not run automatically.
if __name__ == "__main__":
    main()
