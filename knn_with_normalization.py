# -*- coding: utf-8 -*-
"""KNN with Normalization.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yLw_ZYbNb6p9m21G0pUhntMVjtUaDEMC
"""

#you can use your own data set and change the path of dataset
#KNN with Normalization
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error

# Dataset
file_path = '/content/Food_Delivery_Times.csv'
data = pd.read_csv(file_path)

# Check Order_ID 103
row_103 = data[data['Order_ID'] == 103]

# Check Order_ID column is Present or Not and drop delivery Time column
data_cleaned = data.dropna(subset=['Delivery_Time_min']).drop(columns=['Order_ID'])

X = data_cleaned.drop(columns=['Delivery_Time_min'])
y = data_cleaned['Delivery_Time_min']

# Identify numeric and categorical columns
numeric_features = X.select_dtypes(include=['float64', 'int64']).columns.tolist()
categorical_features = X.select_dtypes(include=['object']).columns.tolist()

# Preprocessing steps
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# Training and Testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Applying k-NN for given k values
k_values = [5, 10, 15]
results = {}

for k in k_values:
    # Create a pipeline with preprocessing and k-NN
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('knn', KNeighborsRegressor(n_neighbors=k))
    ])

    # Train the model
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Calculate the MSE
    mse = mean_squared_error(y_test, y_pred)
    results[k] = mse

# Predict delivery time for Order_ID 103
if not row_103.empty:
    X_103 = row_103.drop(columns=['Order_ID', 'Delivery_Time_min'], errors='ignore')

    # Preprocess and predict for each k value
    predictions_103 = {}
    for k in k_values:
        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('knn', KNeighborsRegressor(n_neighbors=k))
        ])
        model.fit(X_train, y_train)
        predictions_103[k] = model.predict(X_103)[0]

    print("Predictions for Order_ID 103:", predictions_103)

print("Mean Squared Errors for k values:", results)