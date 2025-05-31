import pandas as pd
import numpy as np
import sys
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score


# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------


# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the project root
project_root = os.path.dirname(script_dir)
# Construct the path to the dataset
dataset_path = os.path.join(project_root, 'data', 'processed', 'dataset.xlsx')

df = pd.read_excel(dataset_path)


# --------------------------------------------------------------
# Data Cleaning
# --------------------------------------------------------------

# Clean the data to ensure all text is string type
print("Cleaning data...")
print(f"Original dataset shape: {df.shape}")

# Remove any rows with missing values
df = df.dropna()

# Convert text column to string type and handle any datetime objects
df['ujumbe'] = df['ujumbe'].astype(str)

# Remove any rows where ujumbe is empty or just whitespace
df = df[df['ujumbe'].str.strip() != '']

# Remove any rows where ujumbe is 'nan' or similar
df = df[~df['ujumbe'].str.lower().isin(['nan', 'none', 'null'])]

print(f"Cleaned dataset shape: {df.shape}")
print(f"Sample of cleaned data:")
print(df.head())


# --------------------------------------------------------------
# Train test split
# --------------------------------------------------------------


X = df['ujumbe']  # Message text 
y = df['aina']    # Spam/ham labels

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    stratify=y, 
    random_state=42
)

# --------------------------------------------------------------
# Initialize CountVectorizer
# --------------------------------------------------------------

vectorizer = CountVectorizer()

# --------------------------------------------------------------
# Fit and transform the training data (using 'ujumbe' column)
# --------------------------------------------------------------

X_train = vectorizer.fit_transform(X_train  )
X_test = vectorizer.transform(X_test)


# --------------------------------------------------------------
# Initialize MultinomialNB
# --------------------------------------------------------------

model = MultinomialNB()

# --------------------------------------------------------------
# Train the model
# --------------------------------------------------------------

model.fit(X_train, y_train)


# --------------------------------------------------------------
# Evaluate the model
# --------------------------------------------------------------    

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)   

# Print the accuracy
print(f"Accuracy: {accuracy:.2f}")          

# --------------------------------------------------------------
# Additional Evaluation
# --------------------------------------------------------------

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClass Distribution in Dataset:")
print(df['aina'].value_counts())
print(f"Spam percentage: {(df['aina'].value_counts()['spam'] / len(df)) * 100:.1f}%")
print(f"Ham percentage: {(df['aina'].value_counts()['ham'] / len(df)) * 100:.1f}%")



new_messages = ["Mimi mwenye nyumba wako nitumie 300000", "mimi sijambo"]
new_messages_vector = vectorizer.transform(new_messages)
predictions = model.predict(new_messages_vector)
print("\nPredictions for new messages:", predictions)

# --------------------------------------------------------------
# Comprehensive Generalization Testing
# --------------------------------------------------------------

print("\n" + "="*60)
print("COMPREHENSIVE GENERALIZATION TESTING")
print("="*60)

# Test messages covering different scenarios
test_messages = [
    # Legitimate messages (ham)
    "Habari ya asubuhi, je umepata kitabu?",
    "Nitakuja nyumbani mapema leo",
    "Asante kwa msaada wako wa jana",
    "Tutaonana shuleni kesho",
    "Mama amesema tukutane dukani",
    
    # Spam messages with money/financial themes
    "Umeshinda milioni 50, tuma taarifa zako sasa",
    "Malipo yako yamezuiwa, bonyeza link hii",
    "Tuma tsh 10000 ili ushinde bahati nasibu",
    "Pokea mkopo wa tsh 5000000 haraka",
    "Jiunge na freemason upate utajiri",
    
    # Edge cases and variations
    "Hello, how are you today?",  # English
    "Pesa nyingi hapa, tuma namba yako",  # Mixed content
    "Meeting at 3pm tomorrow",  # Short message
    "UMESHINDA TSH 1000000 TUMA TAARIFA ZAKO",  # All caps
    "mimi ni mwanafunzi wa chuo",  # Student message
]

# Labels for evaluation (what we expect)
expected_labels = [
    'ham', 'ham', 'ham', 'ham', 'ham',  # Legitimate messages
    'spam', 'spam', 'spam', 'spam', 'spam',  # Spam messages  
    'ham', 'spam', 'ham', 'spam', 'ham'  # Edge cases
]

print(f"Testing {len(test_messages)} diverse messages:")
print("-" * 60)

# Vectorize test messages
test_vectors = vectorizer.transform(test_messages)
test_predictions = model.predict(test_vectors)
test_probabilities = model.predict_proba(test_vectors)

# Analyze results
correct_predictions = 0
for i, (message, expected, predicted) in enumerate(zip(test_messages, expected_labels, test_predictions)):
    # Get probabilities
    ham_prob = test_probabilities[i][0] if model.classes_[0] == 'ham' else test_probabilities[i][1]
    spam_prob = test_probabilities[i][1] if model.classes_[1] == 'spam' else test_probabilities[i][0]
    
    # Check if prediction is correct
    is_correct = predicted == expected
    if is_correct:
        correct_predictions += 1
    
    # Display result
    status = "CORRECT" if is_correct else "WRONG"
    print(f"{i+1:2d}. {status}")
    print(f"    Message: {message[:50]}...")
    print(f"    Expected: {expected}, Predicted: {predicted}")
    print(f"    Confidence: Ham={ham_prob:.3f}, Spam={spam_prob:.3f}")
    print()

# Summary
print("=" * 60)
print("GENERALIZATION SUMMARY:")
print(f"Correct predictions: {correct_predictions}/{len(test_messages)} ({correct_predictions/len(test_messages)*100:.1f}%)")

# Analyze types of errors
ham_errors = sum(1 for i, (exp, pred) in enumerate(zip(expected_labels, test_predictions)) 
                 if exp == 'ham' and pred == 'spam')
spam_errors = sum(1 for i, (exp, pred) in enumerate(zip(expected_labels, test_predictions)) 
                  if exp == 'spam' and pred == 'ham')

print(f"False positives (ham predicted as spam): {ham_errors}")
print(f"False negatives (spam predicted as ham): {spam_errors}")

if correct_predictions/len(test_messages) >= 0.8:
    print(" Model shows GOOD generalization!")
elif correct_predictions/len(test_messages) >= 0.6:
    print("Model shows MODERATE generalization")
else:
    print("Model shows POOR generalization - needs improvement")

# --------------------------------------------------------------
# Export/Save the Model
# --------------------------------------------------------------

print("\n" + "="*50)
print("EXPORTING MODEL")
print("="*50)

# Create directory for saved models if it doesn't exist
import os
model_dir = "saved_models"
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

# Save the trained model
model_path = os.path.join(model_dir, "spam_classifier_model.pkl")
joblib.dump(model, model_path)
print(f"Model saved to: {model_path}")

# Save the vectorizer
vectorizer_path = os.path.join(model_dir, "vectorizer.pkl")
joblib.dump(vectorizer, vectorizer_path)
print(f"Vectorizer saved to: {vectorizer_path}")

# Save model metadata
metadata = {
    'model_type': 'MultinomialNB',
    'accuracy': accuracy,
    'training_samples': X_train.shape[0],
    'test_samples': X_test.shape[0],
    'features': X_train.shape[1],
    'classes': model.classes_.tolist(),
    'generalization_accuracy': correct_predictions/len(test_messages),
    'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
}

metadata_path = os.path.join(model_dir, "model_metadata.json")
import json
with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2)
print(f"Metadata saved to: {metadata_path}")

print(f"All files saved in: {os.path.abspath(model_dir)}")
print("\nTo use the model later:")
print("1. Load model: model = joblib.load('saved_models/spam_classifier_model.pkl')")
print("2. Load vectorizer: vectorizer = joblib.load('saved_models/vectorizer.pkl')")
print("3. Predict: predictions = model.predict(vectorizer.transform(['new message']))")

# --------------------------------------------------------------
# Demonstration: Load and Test Saved Model
# --------------------------------------------------------------

print("\n" + "="*50)
print("TESTING SAVED MODEL")
print("="*50)

# Load the saved model and vectorizer
loaded_model = joblib.load(model_path)
loaded_vectorizer = joblib.load(vectorizer_path)



