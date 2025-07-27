import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib   


df = pd.read_csv("data/dataset.csv")
X = df['text']
y = df['category']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)

pipeline = Pipeline([
    ('cv', CountVectorizer()),
    ('nb', MultinomialNB())
])

pipeline.fit(X_train, y_train)
result= pipeline.predict(X_test)
print(result,y_test)
accuracy = pipeline.score(X_test, y_test)
print("Accuracy:", accuracy)
joblib.dump(pipeline, 'model.pkl')