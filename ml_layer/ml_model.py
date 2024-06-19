import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import string
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

#reading our dataset which contains features and labels whether product is genuine or fake
product_data = pd.read_csv("fake_product_dataset.csv")

#dropping all null values of our dataset
product_data.dropna(inplace=True)

label_map = {False: 0, True: 1}
df = product_data['is_authentic'].map(label_map)

plt.scatter(product_data['retail_price'], product_data['discounted_price'], c=df, alpha=0.5)

#defining features and labels of our product
features = product_data[['retail_price', 'discounted_price']]

labels = product_data['is_authentic']

X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2)

model = LogisticRegression()

model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

accuracy = model.score(X_test, y_test)*100
print("Model accuracy:", accuracy)

def productAnalyzer(product_details):
    # Example user input:
    user_input = pd.DataFrame(
    {
        "retail_price": [product_details["retailprice"]],
        "discounted_price": [product_details["discountedprice"]]
    })

    # Make a prediction
    product_genuine = model.predict(user_input)
    print(product_genuine)
    return product_genuine