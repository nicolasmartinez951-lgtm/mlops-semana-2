
import json
import math
from pathlib import Path
import json
import math
import pandas as pd
from pathlib import Path
from sklearn.datasets import load_iris


# Aquí se carga el contrato de datos del archivo generado 'data_contract.json'.

def load_contract(contract_path=None):
    """
    Lee el contrato de datos desde un archivo JSON.
    """

    if contract_path is None:
        project_root = Path(__file__).resolve().parent.parent
        contract_path = project_root / "contracts" / "data_contract.json"

    with open(contract_path, "r", encoding="utf-8") as file:
        contract = json.load(file)

    return contract

# Se valida un registro individual.

def validate_record(record, contract, validate_target=True):
    """
    Valida un registro individual de acuerdo con el contrato.

    Para esto se comprueba:
    
    - Existencia de las variables definidas en el contrato.
    - Tipos de datos.
    - Ausencia de valores nulos.
    - Rangos mínimos y máximos.
    - Valores permitidos para la variable objetivo.
    """

    errors = []

    for feature, rules in contract["features"].items():

        if feature not in record:
            errors.append(
                f"Falta la variable obligatoria: {feature}"
            )
            continue

        value = record[feature]

        if value is None:
            if not rules["nullable"]:
                errors.append(
                    f"{feature}: no se permiten valores nulos."
                )
            continue

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            errors.append(
                f"{feature}: se esperaba un valor numérico."
            )
            continue

        if not math.isfinite(value):
            errors.append(
                f"{feature}: el valor debe ser finito."
            )
            continue

        if value < rules["minimum"]:
            errors.append(
                f"{feature}: el valor {value} está por debajo "
                f"del mínimo permitido ({rules['minimum']})."
            )

        if value > rules["maximum"]:
            errors.append(
                f"{feature}: el valor {value} supera "
                f"el máximo permitido ({rules['maximum']})."
            )

    if validate_target:

        target_rules = contract["target"]
        target_name = target_rules["name"]

        if target_name not in record:
            errors.append(
                f"Falta la variable objetivo: {target_name}"
            )

        else:
            target_value = record[target_name]

            if target_value is None:
                errors.append(
                    f"{target_name}: no se permiten valores nulos."
                )

            elif isinstance(target_value, bool) or not isinstance(target_value, int):
                errors.append(
                    f"{target_name}: se esperaba un valor entero."
                )

            elif target_value not in target_rules["allowed_values"]:
                errors.append(
                    f"{target_name}: valor no permitido. "
                    f"Valores válidos: {target_rules['allowed_values']}."
                )

    return errors

# Se valida un conjunto de datos completo.

def validate_dataset(records, contract, validate_target=True):
    """
    Con esta función se validan todos los registros de un conjunto de datos.

    Recibe una lista de diccionarios y devuelve los errores
    encontrados, indicando el número de fila.
    """

    all_errors = []

    if not records:
        return ["El conjunto de datos está vacío."]

    for index, record in enumerate(records):

        record_errors = validate_record(
            record,
            contract,
            validate_target=validate_target
        )

        for error in record_errors:
            all_errors.append(
                f"Fila {index + 1}: {error}"
            )

    return all_errors


# Se carga el dataset 'iris' completo.

def load_iris_dataset():
    """
    Carga el conjunto Iris y lo organiza en un DataFrame.
    """

    iris = load_iris()

    # Se crea el dataframe teniendo en cuenta las variables predictoras.
    
    df = pd.DataFrame(
        iris.data,
        columns=iris.feature_names
    )

    # Se incorpora la variable objetivo.
    
    df["species"] = iris.target

    return df


# Se ejecuta una prueba con los ejemplos del contrato.

if __name__ == "__main__":

    print("INICIANDO VALIDACIÓN DEL DATASET IRIS")

    contract = load_contract()

    df = load_iris_dataset()

    print("\nInformación del dataset:")
    print("Número de registros:", len(df))
    print("Número de variables:", len(df.columns))

    records = df.to_dict(orient="records")

    errors = validate_dataset(records, contract)

    total_records = len(records)

    invalid_rows = len({
        error.split(":", 1)[0]
        for error in errors
    })

    valid_rows = total_records - invalid_rows

    print("\nRESULTADOS DE LA VALIDACIÓN")
    print("--------------------------------")

    print("Total de registros:", total_records)
    print("Registros válidos:", valid_rows)
    print("Registros inválidos:", invalid_rows)

    if errors:

        print("\nSe encontraron incumplimientos:")

        for error in errors[:20]:
            print("-", error)

        if len(errors) > 20:
            print("Se omitieron", len(errors) - 20, "errores adicionales.")

        print("\nVALIDACIÓN FALLIDA")

        import sys
        sys.exit(1)

    else:

        print("\nTodos los registros cumplen con el contrato.")
        print("VALIDACIÓN EXITOSA")