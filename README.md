# CyberSecurity


How to run

Step 1 — Train the model. Do this first, and only once:

python app.py train

This reads dataset.csv, trains the model, and prints its accuracy.

Step 2 — Analyze an email. Paste the text directly:

python app.py analyze

Then paste the email and press Enter. Or point it at a saved file:

python app.py analyze sample_email.txt

Example result:

Result: PHISHING
Confidence: 90.1%
Warning signs:
 - Contains a link
 - Uses urgent language
Saved to database.

Step 3 — Review past results:

python app.py history

Step 4 — Pull a summary report:

python app.py report

This shows how many emails were checke how many came back as phishing,
and the average confidence.

How it works

preprocess.py cleans the email text first — lowercasing it, stripping
punctuation, and removing common words — so the model has an easier time
finding patterns. model.py then converts that cleaned text into numbers
with TF-IDF and runs it through a logistic regression model to classify it
as phishing or legitimate.

Separately, preprocess.py checks for a few plain warning signs: links,
urgent language, requests for passwords. These don't drive the prediction,
but they make the result easier to explain. db.py writes every result to
phishing.db, so you can check the history later.

Note on the dataset

dataset.csv is a set of example phishing and legitimate emails built from
common patterns. That keeps the program fully offline — nothing to download,
nothing to fetch at runtime.
