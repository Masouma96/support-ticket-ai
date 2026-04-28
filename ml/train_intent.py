import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

#load data
df = pd.read_csv("dataset/intent_data.csv")

x_train, x_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size=0.2 )

#vectorize text
vectorizer = TfidfVectorizer()
x_train_vec = vectorizer.fit_transform(x_train)

# model training
model= LogisticRegression()
model.fit(x_train_vec, y_train)

# save model and vectorizer
joblib.dump(model, "../backend/app/models/intent_model.pkl")
joblib.dump(vectorizer, "../backend/app/models/intent_vectorizer.pkl")

print("Intent model trained successfully!")

