import uuid, mlflow, optuna, bentoml
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier

UNIQUE_PREFIX = str(uuid.uuid4())[:8]

X = load_iris().data
y = load_iris().target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

def objective(trial):
    params = {'max_depth': trial.suggest_int('max_depth', 2, 8)
              ,'random_state': trial.suggest_int('random_state',42, 123)}
    run_name = f'{UNIQUE_PREFIX}rfc'
    with mlflow.start_run(run_name=run_name):
        mlflow.log_params(params)
        clf = RandomForestClassifier(**params).fit(X_train, y_train)
        score = cross_val_score(clf, X_test, y_test, cv=3, scoring='accuracy').mean()
        mlflow.log_metric('accuracy', score)
    return score

def rfc_run():
    experiment_name = 'RandomForestClassifier-hpo'
    mlflow.set_tracking_uri('http://127.0.0.1:8081')
    mlflow.set_experiment(experiment_name)
    study = optuna.create_study(direction='maximize')
    # study.optimize(lambda trial: objective(trial), n_trials=5)
    study.optimize(objective, n_trials=5)
    best_param = study.best_params

    with mlflow.start_run(run_name='Best-rfc'):
        clf = RandomForestClassifier(**best_param).fit(X_train, y_train)
        score = cross_val_score(clf, X_train, y_train, cv=3, scoring='accuracy').mean()
        mlflow.log_metric('accuracy', score)
        mlflow.sklearn.log_model(clf, "RandomForestClassifier_model")

    run_id = mlflow.last_active_run().info.run_id
    artifact_path = "RandomForestClassifier_model"  # 이 부분을 모델이 저장된 경로로 수정
    model_uri = f"runs:/{run_id}/{artifact_path}"
    bento_model = bentoml.mlflow.import_model('RandomForestClassifier_model', model_uri)
    print(f"Model imported to BentoML: {bento_model}")

if __name__ == '__main__':
    rfc_run()