---
name: ml-engineer
description: Machine learning pipelines and integrations. Use for ML/AI development tasks.
triggers:
  - "machine learning"
  - "ML pipeline"
  - "model training"
  - "AI model"
---

# ML Engineer Skill

## Identity

You are a machine learning engineer focused on building ML pipelines, model training, and deployment.

## When to Use

- Building ML pipelines
- Training models
- Feature engineering
- Model deployment

## ML Pipeline Architecture

```
Data Ingestion → Preprocessing → Feature Engineering →
Model Training → Evaluation → Deployment → Monitoring
```

## Project Structure

```
ml-project/
├── data/
│   ├── raw/
│   ├── processed/
│   └── features/
├── models/
│   ├── trained/
│   └── experiments/
├── notebooks/
│   └── exploration.ipynb
├── src/
│   ├── data/
│   │   ├── ingestion.py
│   │   └── preprocessing.py
│   ├── features/
│   │   └── feature_engineering.py
│   ├── models/
│   │   ├── train.py
│   │   └── predict.py
│   └── evaluation/
│       └── metrics.py
├── config/
│   └── config.yaml
├── tests/
├── requirements.txt
└── Dockerfile
```

## Training Pipeline

```python
# src/models/train.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import mlflow

class ModelTrainer:
    def __init__(self, config):
        self.config = config
        self.model = None

    def load_data(self):
        """Load and split data"""
        df = pd.read_csv(self.config['data_path'])
        X = df.drop('target', axis=1)
        y = df['target']

        return train_test_split(
            X, y,
            test_size=self.config['test_size'],
            random_state=self.config['random_state']
        )

    def train(self, X_train, y_train):
        """Train the model"""
        mlflow.start_run()

        self.model = RandomForestClassifier(
            n_estimators=self.config['n_estimators'],
            max_depth=self.config['max_depth'],
            random_state=self.config['random_state']
        )

        self.model.fit(X_train, y_train)

        # Log parameters
        mlflow.log_params(self.config)

        return self.model

    def evaluate(self, X_test, y_test):
        """Evaluate the model"""
        predictions = self.model.predict(X_test)
        report = classification_report(y_test, predictions, output_dict=True)

        # Log metrics
        mlflow.log_metric('accuracy', report['accuracy'])
        mlflow.log_metric('f1_score', report['weighted avg']['f1-score'])

        return report

    def save_model(self, path):
        """Save the trained model"""
        joblib.dump(self.model, path)
        mlflow.sklearn.log_model(self.model, 'model')

# Usage
config = {
    'data_path': 'data/processed/features.csv',
    'test_size': 0.2,
    'random_state': 42,
    'n_estimators': 100,
    'max_depth': 10
}

trainer = ModelTrainer(config)
X_train, X_test, y_train, y_test = trainer.load_data()
trainer.train(X_train, y_train)
metrics = trainer.evaluate(X_test, y_test)
trainer.save_model('models/trained/model.joblib')
```

## Feature Engineering

```python
# src/features/feature_engineering.py
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np

class FeatureEngineer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()

        # Date features
        if 'date' in X.columns:
            X['year'] = pd.to_datetime(X['date']).dt.year
            X['month'] = pd.to_datetime(X['date']).dt.month
            X['day_of_week'] = pd.to_datetime(X['date']).dt.dayofweek

        # Numerical features
        if 'amount' in X.columns:
            X['amount_log'] = np.log1p(X['amount'])
            X['amount_bins'] = pd.qcut(X['amount'], q=5, labels=False)

        # Text features
        if 'description' in X.columns:
            X['text_length'] = X['description'].str.len()
            X['word_count'] = X['description'].str.split().str.len()

        return X

# Pipeline
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

pipeline = Pipeline([
    ('feature_engineer', FeatureEngineer()),
    ('scaler', StandardScaler()),
])
```

## Model Serving

```python
# FastAPI inference server
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()
model = joblib.load('models/trained/model.joblib')

class PredictionRequest(BaseModel):
    features: list[float]

class PredictionResponse(BaseModel):
    prediction: int
    probability: float

@app.post('/predict', response_model=PredictionResponse)
def predict(request: PredictionRequest):
    features = np.array(request.features).reshape(1, -1)
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    return PredictionResponse(
        prediction=int(prediction),
        probability=float(probability)
    )
```

## Tips

- Version your data and models
- Use experiment tracking (MLflow)
- Monitor model performance in production
- Implement A/B testing for new models
- Set up automated retraining
