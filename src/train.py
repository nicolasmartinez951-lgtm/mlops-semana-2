import pandas as pd
import mlflow
import mlflow.sklearn
import joblib

from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def train_model():

    """
    Entrena y evalúa un modelo Random Forest
    utilizando los datos preparados previamente.
    """

    project_root = Path(__file__).resolve().parent.parent

    train_path = project_root / "data" / "processed" / "train.csv"
    test_path = project_root / "data" / "processed" / "test.csv"

    models_path = project_root / "models"

    tracking_db = (
        project_root.parent / "mlflow.db"
    )

    if not tracking_db.exists():
        raise FileNotFoundError(
            f"No se encontró la base de datos de MLflow: {tracking_db}. "
            "Verifica su ubicación antes de continuar."
        )

    tracking_uri = f"sqlite:///{tracking_db.as_posix()}"

    mlflow.set_tracking_uri(tracking_uri)

    mlflow.set_experiment("Baseline_RF")

    print("CARGANDO DATOS DE ENTRENAMIENTO Y PRUEBA")

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    print("Registros de entrenamiento:", len(train_df))
    print("Registros de prueba:", len(test_df))

    X_train = train_df.drop(columns=["species"])
    y_train = train_df["species"]

    X_test = test_df.drop(columns=["species"])
    y_test = test_df["species"]

    n_estimators = 100
    max_depth = None
    random_state = 42

    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state
    )

    print("\nINICIANDO ENTRENAMIENTO")

    with mlflow.start_run(run_name="Iris_RandomForest_Semana2"):

        model.fit(X_train, y_train)

        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)

        train_accuracy = accuracy_score(
            y_train, y_train_pred
        )

        test_accuracy = accuracy_score(
            y_test, y_test_pred
        )

        print("\nRESULTADOS DEL MODELO")
        print("-----------------------------")
        print("Train Accuracy:", train_accuracy)
        print("Test Accuracy:", test_accuracy)

        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("random_state", random_state)

        mlflow.log_metric("train_accuracy", train_accuracy)
        mlflow.log_metric("test_accuracy", test_accuracy)

        mlflow.sklearn.log_model(
            sk_model=model,
            name="iris_model",
            skops_trusted_types=["sklearn.tree._tree.Tree"]
        )

        models_path.mkdir(parents=True, exist_ok=True)

        model_file = models_path / "iris_model.pkl"

        joblib.dump(model, model_file)

        print("\nMODELO GUARDADO")
        print(model_file)

        print("\nEXPERIMENTO REGISTRADO EN MLFLOW")

    print("\nENTRENAMIENTO COMPLETADO EXITOSAMENTE")


if __name__ == "__main__":
    train_model()
