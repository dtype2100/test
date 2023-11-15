import bentoml, mlflow, optuna, uuid, os

from sklearn.datasets import load_iris
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split, cross_val_score

mlflow.set_tracking_uri('http://127.0.0.1:8081')
mlflow.set_experiment('ada-hpo')

iris = load_iris()
X = iris.data
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

UNIQUE_PREFIX = str(uuid.uuid4())[:8]
def objective(trial):
    params = {'random_state': trial.suggest_int('random_state', 42, 1024),
              'n_estimators': trial.suggest_int('n_estimators', 10, 100),}
    run_name = f'{UNIQUE_PREFIX}-{trial.number}'
    with mlflow.start_run(run_name=run_name):
        mlflow.log_params(params)
        clf = AdaBoostClassifier(**params).fit(X_train, y_train)
        score = cross_val_score(clf, X_test, y_test, cv=5).mean()
        mlflow.log_metric('score', score)
    return score
study = optuna.create_study(study_name='ada-hpo', direction='maximize', load_if_exists=True)
study.optimize(lambda trial: objective(trial), n_trials=5)
best_param = study.best_params

if __name__ == '__main__':
    with mlflow.start_run(run_name='Best_ada_model'):
        mlflow.log_params(best_param)
        best_model = AdaBoostClassifier(**best_param).fit(X_train, y_train)
        score = cross_val_score(best_model, X_test, y_test, cv=5).mean()
        mlflow.log_metric('score', score)
        
        model_name = f'{UNIQUE_PREFIX}_ada_model'
        save_path = f"./sk_model/{model_name}"
        # if not os.path.exists(save_path):
        mlflow.sklearn.save_model(best_model, save_path)
        # model_uri = mlflow.get_artifact_uri('./sk_model')
        # saved_model = bentoml.sklearn.save_model("Best_ada_model", best_model)
        bento_model = bentoml.mlflow.import_model(model_name, model_uri=save_path)

    # run_id = mlflow.last_active_run().info.run_id
    # artifact_path = "models"
    # model_uri = f"runs:/{run_id}/{artifact_path}"
    # logged_model = mlflow.sklearn.log_model(best_model, "Best_ada_model")
    # bento_model = bentoml.mlflow.import_model('Best_ada_model', logged_model.model_uri)
    # print(f"Model imported to BentoML: {bento_model}")

