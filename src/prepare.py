import sys
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

# Se importan las funciones del módulo de validación 'validate_data.py'.

from validate_data import (
    load_contract,
    load_iris_dataset,
    validate_dataset
)


def prepare_data():

    """
    Carga, valida y prepara el conjunto Iris
    para el entrenamiento del modelo.
    """

    project_root = Path(__file__).resolve().parent.parent

    processed_path = project_root / "data" / "processed"

    print("CARGANDO CONTRATO DE DATOS")
    contract = load_contract()

    print("\nCARGANDO DATASET IRIS")
    df = load_iris_dataset()
    
    print("Registros cargados:", len(df))
    print("Variables:", len(df.columns))

    print("\nVALIDANDO CALIDAD DE LOS DATOS")

    records = df.to_dict(orient="records")

    errors = validate_dataset(records, contract)

    if errors:

        print("\nSe encontraron errores en los datos:")

        for error in errors[:20]:
            print("-", error)

        print("\nPROCESO DETENIDO: los datos no cumplen el contrato.")

        sys.exit(1)

    print("Todos los registros cumplen con el contrato.")

    print("\nDIVIDIENDO EL DATASET")

    train_df, test_df = train_test_split(
        df,
        test_size=0.20,
        random_state=42,
        stratify=df["species"]
    )

    print("Registros de entrenamiento:", len(train_df))
    print("Registros de prueba:", len(test_df))

    processed_path.mkdir(parents=True, exist_ok=True)

    train_file = processed_path / "train.csv"
    test_file = processed_path / "test.csv"

    train_df.to_csv(train_file, index=False)
    test_df.to_csv(test_file, index=False)

    print("\nARCHIVOS GENERADOS")
    print("Entrenamiento:", train_file)
    print("Prueba:", test_file)

    print("\nPREPARACIÓN COMPLETADA EXITOSAMENTE")


if __name__ == "__main__":
    prepare_data()
