import subprocess
import sys
from pathlib import Path


def run_step(script_path, step_name):
    print("\n" + "=" * 55, flush=True)
    print(f"INICIANDO: {step_name}", flush=True)
    print("=" * 55, flush=True)

    subprocess.run(
        [sys.executable, str(script_path)],
        check=True
    )

    print(f"\nPASO COMPLETADO: {step_name}", flush=True)


def main():

    project_root = Path(__file__).resolve().parent
    src_path = project_root / "src"

    prepare_script = src_path / "prepare.py"
    train_script = src_path / "train.py"

    print("\nINICIANDO PIPELINE DE MLOPS - DATASET IRIS", flush=True)

    try:
        run_step(
            prepare_script,
            "PREPARACIÓN Y VALIDACIÓN DE DATOS"
        )

        run_step(
            train_script,
            "ENTRENAMIENTO Y EVALUACIÓN DEL MODELO"
        )

    except subprocess.CalledProcessError as error:
        print("\n" + "=" * 55)
        print("PIPELINE DETENIDO")
        print("=" * 55)
        print("Uno de los procesos terminó con un error.")
        print("Código de salida:", error.returncode)
        sys.exit(error.returncode)

    print("\n" + "=" * 55)
    print("PIPELINE COMPLETADO EXITOSAMENTE")
    print("=" * 55)


if __name__ == "__main__":
    main()
