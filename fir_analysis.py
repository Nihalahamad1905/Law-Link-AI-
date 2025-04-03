import pandas as pd
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download necessary NLTK data (only runs once)
nltk.download("punkt")
nltk.download("stopwords")

# Load IPC dataset (ensure ipc_dataset.csv is in the same folder)
df = pd.read_csv("ipc_ds.csv")
# Normalize column names to lowercase: 'section', 'title', 'description'
df.columns = df.columns.str.lower()

def preprocess_text(text):
    text = text.lower().translate(str.maketrans("", "", string.punctuation))
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words("english")]
    return " ".join(tokens)

# Preprocess the 'description' field for all entries and store in new column
df["processed_description"] = df["description"].apply(preprocess_text)

# Train and cache the TF-IDF model on processed descriptions
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["processed_description"])

def analyze_fir(incident_text):
    processed_text = preprocess_text(incident_text)
    input_vector = vectorizer.transform([processed_text])
    similarities = cosine_similarity(input_vector, tfidf_matrix).flatten()
    threshold = 0.2  # Adjust threshold if needed
    matching_rows = df[similarities > threshold]
    results = []
    for _, row in matching_rows.iterrows():
        # Use lowercase keys: 'section', 'title', 'description'
        result = f"Section: {row['section']} - {row['title']}\nDescription: {row['description']}"
        results.append(result)
    return results
