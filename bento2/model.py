import uuid, mlflow, optuna, bentoml
from mlflow import MlflowClient
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime

UNIQUE_PREFIX = str(uuid.uuid4())[:8]
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

X = load_iris().data
y = load_iris().target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

def objective(trial):
    params = {'max_depth': trial.suggest_int('max_depth', 2, 8)
              , 'random_state': trial.suggest_int('random_state', 42, 123)}
    run_name = f'{CURRENT_TIME}-{UNIQUE_PREFIX}-rfc'
    with mlflow.start_run(run_name=run_name):
        mlflow.log_params(params)
        clf = RandomForestClassifier(**params).fit(X_train, y_train)
        score = cross_val_score(clf, X_test, y_test, cv=3, scoring='accuracy').mean()
        mlflow.log_metric('accuracy', score)
    return score

if __name__ == '__main__':
    experiment_name = f'RandomForest'
    mlflow.set_tracking_uri('http://127.0.0.1:8081')
    mlflow.set_experiment(experiment_name)
    
    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: objective(trial), n_trials=5)
    params = study.best_params
    
    run_name = f'{CURRENT_TIME}-Best_rfc_model'
    with mlflow.start_run(run_name=run_name):
        mlflow.log_params(params)
        clf = RandomForestClassifier(**params).fit(X_train, y_train)
        score = cross_val_score(clf, X_test, y_test, cv=3, scoring='accuracy').mean()
        mlflow.log_metric('accuracy', score)
        mlflow.sklearn.log_model(clf, "random_forest_model")


        run_id = mlflow.last_active_run().info.run_id
        artifact_path = "random_forest_model"  # 이 부분을 모델이 저장된 경로로 수정
        model_uri = f"runs:/{run_id}/{artifact_path}"
        bento_model = bentoml.mlflow.import_model('random_forest_model', model_uri)
        print(f"Model imported to BentoML: {bento_model}")
        
    @bentoml.artifacts([bentoml.mlflow.MlflowModelArtifact('random_forest_model')])
    @bentoml.env(pip_dependencies=["scikit-learn"])
    class RandomForestService(bentoml.BentoService):
        
        # API 정의
        @bentoml.api(bentoml.handlers.DataframeHandler)
        def predict(self, df):
            # 모델 예측
            return self.artifacts.random_forest_model.predict(df)

    # BentoML 서비스 인스턴스 생성
    bento_svc = RandomForestService()
    bento_svc.pack('random_forest_model', bento_model)
    bentoml.server.start_bento_server(bento_svc)
