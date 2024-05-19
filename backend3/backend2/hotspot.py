from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', message='No file part')
    
    file = request.files['file']
    
    if file.filename == '':
        return render_template('index.html', message='No selected file')
    
    if file:
        df = pd.read_csv(file)

        # Preprocess data and train machine learning model
        X = df.drop(columns=['Crime_Type'])
        y = df['Crime_Type']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        clf = RandomForestClassifier()
        clf.fit(X_train, y_train)

        # Make predictions
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        # Visualize predictions
        feature_importance = pd.Series(clf.feature_importances_, index=X.columns)
        feature_importance = feature_importance.sort_values(ascending=False)
        feature_importance_plot = px.bar(feature_importance, x=feature_importance.index, y=feature_importance.values, title='Feature Importance')

        accuracy_plot = px.bar(x=['Accuracy'], y=[accuracy], title='Model Accuracy')

        feature_importance_div = feature_importance_plot.to_html(full_html=False)
        accuracy_div = accuracy_plot.to_html(full_html=False)

        return render_template('index.html', feature_importance_div=feature_importance_div, accuracy_div=accuracy_div)

if __name__ == '__main__':
    app.run(debug=True)
