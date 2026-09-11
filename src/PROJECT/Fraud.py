import pandas as pd
from sklearn.model_selection import train_test_split


df = pd.read_csv("creditcard.csv")

# print(df.head())
# print(df.isnull().sum().sum())
X = df.drop("Class", axis=1)
y = df["Class"]
print(X.head())
print(y.head())


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)