import bentoml, mlflow, optuna, uuid
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.ensemble import AdaBoostClassifier

UNIQUE_PREFIX = str(uuid.uuid4())[:8]
def objective(trial, X, y):
    param = {
        'n_estimators': trial.suggest_int('n_estimators', 10, 100),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 1.0),
    }
    mlflow.log_params(param)
    model = AdaBoostClassifier(**param)
    scores = cross_validate(model, X, y, cv=5)
    mlflow.log_metrics({'scores', scores})
    return scores['train_score'].mean()



def ada_clf_run(X, y):
    mlflow.set_tracking_uri('http://127.0.0.1:8081')
    study = optuna.create_study(study_name='ada-hpo', direction='maximize', load_if_exists=True)
    study.optimize(lambda trial: objective(trial), n_trials=5)
    best_param = study.best_params
    with mlflow.start_run(run_name='Best_model'):
        mlflow.log_params(best_param)
        best_model = AdaBoostClassifier(**best_param).fit(X, y)
        scores = cross_validate(best_model, X, y, cv=5)
        mlflow.log_metrics({'scores', scores})
        model_name = f'ada_clf_model_{UNIQUE_PREFIX}'

        mlflow.sklearn.log_model(best_model, model_name)
        bentoml.mlflow.import_model(
                                    'Best_model',
                                    model_uri="runs:/<mlflow_run_id>/run-relative/path/to/model",
                                    signatures={
                                                "predict": {"batchable": True},
                                                }
                                    )
        run_id = mlflow.active_run().info.run_id

        # Construct the model URI
        model_uri = f"runs:/{run_id}/run-relative/path/to/model"

        # BentoML import_model
        bentoml.mlflow.import_model(
            'Best_model',
            model_uri=model_uri,
            signatures={"predict": {"batchable": True}}
        )
