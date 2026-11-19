# Pipeline MLOps – Iris Dataset | Semana 2 - Actividad 2 Seminario de Grado II

1. Descripción del proyecto

El presente proyecto implementa un pipeline automatizado de Machine Learning utilizando el conjunto de datos Iris obtenido de la librería sklearn, con el propósito de integrar procesos de validación de calidad de datos, preparación de información, entrenamiento, evaluación y seguimiento de experimentos.

Esta solución incorpora un contrato de datos en formato JSON y un sistema de validación realizado en Python, el cual permite verificar la integridad de los registros antes de iniciar el entrenamiento del modelo.

El flujo de trabajo se automatiza implementando un script de orquestación que ejecuta de manera secuencial los procesos de preparación y entrenamiento, interrumpiendo la ejecución cuando se detectan errores que afectan la calidad de los datos.

# Objetivos

Como principales objetivos establecidos para este proyecto se definen los siguientes:

- Implementar controles de calidad de datos mediante reglas definidas en un contrato JSON.
- Automatizar la preparación, validación y división de los datos.
- Entrenar y evaluar un modelo de clasificación Random Forest.
- Registrar parámetros y métricas del modelo utilizando MLflow.
- Implementar un mecanismo de control de errores que impida el entrenamiento del modelo cuando los datos incumplen las reglas establecidas.
- Facilitar la reproducibilidad del proceso mediante una ejecución automatizada.

2. Arquitectura del proyecto

El proyecto se encuentra estructurado de la siguiente forma:

mlops-semana-2/
│
├── contracts/
│   └── data_contract.json
│
├── data/
│   └── processed/
│       ├── train.csv
│       └── test.csv
│
├── src/
│   ├── validate_data.py
│   ├── prepare.py
│   └── train.py
│
├── models/
│   └── iris_model.pkl
│
└── run_pipeline_2.py


# Descripción de los componentes

- **contracts/**: esta carpeta contiene el contrato de datos que define las reglas de validación.
- **data/processed/**: almacena los conjuntos de entrenamiento y prueba generados durante la preparación de los datos.
- **src/validate_data.py**: implementa las funciones para ejecutar la validación de datos.
- **src/prepare.py**: carga el dataset, aplica las funciones de validación y genera los conjuntos de entrenamiento y prueba.
- **src/train.py**: entrena el modelo Random Forest, calcula métricas y registra el experimento en MLflow.
- **models/**: almacena el modelo entrenado en formato '.pkl'.
- **run_pipeline_2.py**: es el módulo o archivo que orquesta la ejecución secuencial de los procesos de preparación y entrenamiento.

3. Tecnologías utilizadas

| Python: Usado para el desarrollo de la lógica del pipeline.
| Pandas: Usado para la manipulación y preparación de datos. 
| Scikit-learn: Se usa para la carga del dataset, división de datos, entrenamiento y evaluación.
| Random Forest: Se implementa el algoritmo de clasificación implementado.
| MLflow: Con él se realiza el registro de experimentos, parámetros y métricas.
| Joblib: Persistencia del modelo entrenado.
| JSON: Se define el contrato de datos. 

4. Contrato de datos

El contrato de datos se encuentra en el archivo 'contracts/data_contract.json' y establece las condiciones que deben cumplir las variables del conjunto de datos antes de permitir el entrenamiento.

# Variables predictoras

| sepal length (cm) | Numérico | 4.3 – 7.9 |
| sepal width (cm) | Numérico | 2.0 – 4.4 |
| petal length (cm) | Numérico | 1.0 – 6.9 |
| petal width (cm) | Numérico | 0.1 – 2.5 |

# Variable objetivo

| species | Entero | 0, 1, 2 |

# Reglas de validación

- Las variables predictoras requeridas deben estar presentes.
- No se permiten valores nulos, de lo contrario no se ejecuta el entrenamiento de los datos.
- Las variables predictoras deben contener valores numéricos válidos.
- Los valores numéricos deben ser finitos.
- Las variables predictoras deben cumplir los rangos establecidos en el contrato.
- La variable objetivo debe ser de tipo entero y pertenecer al conjunto de valores permitidos.

Los rangos definidos corresponden a las restricciones establecidas para el conjunto de datos utilizado en el proyecto y no corresponden por tanto a límites biológicos observables en el mundo real.

5. Validación de datos

La validación se implementa mediante funciones personalizadas en el archivo 'src/validate_data.py', utilizando Python y las herramientas de manipulación de datos del proyecto. Este proceso verifica las condiciones establecidas en el contrato antes de permitir la preparación de los conjuntos de datos; de esta forma, cuando se detectan inconsistencias, el sistema genera mensajes de error que identifican los registros y las condiciones incumplidas.

Si los datos no cumplen las reglas, el proceso de preparación se interrumpe y retorna un código de salida de error, evitando que el pipeline continúe hacia el entrenamiento.

6. Pipeline automatizado

El flujo de trabajo se ejecuta mediante el archivo 'run_pipeline_2.py', con el que se coordinan los siguientes procesos:

1. **Preparación y validación:** carga el contrato y el dataset Iris, verifica el cumplimiento de las reglas y detiene la ejecución cuando se detectan errores.
2. **División de datos:** genera los conjuntos de entrenamiento y prueba mediante 'train_test_split', aquí se utiliza una proporción de 80% y 20%, respectivamente, y estratificación según la variable objetivo.
3. **Entrenamiento:** ajusta un modelo Random Forest Classifier utilizando los datos de entrenamiento.
4. **Evaluación:** calcula la exactitud del modelo sobre los conjuntos de entrenamiento y prueba.
5. **Seguimiento:** registra los parámetros y métricas del experimento en MLflow.
6. **Persistencia:** almacena el modelo entrenado localmente en formato '.pkl'.

# Flujo de ejecución

mermaid
flowchart TD
    A[run_pipeline_2.py] --> B[prepare.py]
    B --> C[Carga dataset y contrato]
    C --> D[Validación de datos]
    D --> E{¿Datos válidos?}
    E -->|Sí| F[División Train/Test]
    F --> G[train.py]
    G --> H[Entrenamiento Random Forest]
    H --> I[Evaluación]
    I --> J[Registro MLflow]
    J --> K[Guardar modelo]
    E -->|No| L[Interrumpir pipeline]

7. Instalación y requisitos

Para poder ejecutar este flujo de trabajo se requiere tener instalado un entorno de Python y las siguientes librerías. Se recomienda utilizar un entorno virtual para aislar las dependencias del proyecto.

- pandas
- scikit-learn
- mlflow
- joblib

Para instalar las librerías puede utilizarse el siguiente comando.

```bash
pip install pandas scikit-learn mlflow joblib
```

8. Ejecución del pipeline

Para ejecutar todo el flujo, debe ubicarse en la carpeta raíz del proyecto y ejecutar:

```bash
python run_pipeline_2.py
```

El orquestador ejecuta automáticamente los procesos de preparación y entrenamiento. 

Si los datos cumplen el contrato, el pipeline continúa hasta finalizar el entrenamiento y registrar el experimento.

Si se detectan errores de validación, el pipeline se interrumpe y no ejecuta el proceso de entrenamiento.

---

9. Resultados obtenidos

En la ejecución de referencia del proyecto se obtuvieron los siguientes resultados:

| Indicador                          Resultado |

| Registros totales                        150 |
| Registros de entrenamiento               120 |
| Registros de prueba                       30 |
| Algoritmo           Random Forest Classifier |
| Número de estimadores                    100 |
| Profundidad máxima                      None |
| Random State                              42 |
| Train Accuracy                          1.00 |
| Test Accuracy                           0.90 |

El modelo obtuvo una exactitud de 100% sobre el conjunto de entrenamiento y 90% sobre el conjunto de prueba.

La diferencia entre ambas métricas puede sugerir cierto sobreajuste. Sin embargo, el tamaño reducido del conjunto de prueba limita la capacidad de establecer conclusiones definitivas sobre la capacidad de generalización del modelo.

# Artefactos generados

- 'data/processed/train.csv': conjunto de entrenamiento.
- 'data/processed/test.csv': conjunto de prueba.
- 'models/iris_model.pkl': modelo entrenado y persistido.
- MLflow: registro de parámetros y métricas del experimento.


10. Prueba de control de calidad

Se realizó una prueba de validación introduciendo temporalmente un valor nulo en la variable 'sepal width (cm)' de uno de los registros del dataset.

La prueba permitió verificar los siguientes comportamientos:

- El sistema detectó la inconsistencia del dato.
- La validación generó un mensaje de error.
- El proceso de preparación se interrumpió.
- El orquestador capturó el código de salida de error.
- El proceso de entrenamiento no se ejecutó.

La prueba evidenció que el pipeline implementa controles de calidad que impiden avanzar hacia el entrenamiento cuando los datos incumplen las reglas del contrato.

Posteriormente, se retiró la modificación temporal y se restauró el flujo normal de ejecución.

11. Reproducibilidad

El proyecto incorpora elementos que facilitan la reproducibilidad de las ejecuciones:

- Dataset Iris utilizado como fuente de datos.
- Contrato de datos definido en JSON.
- Validación automatizada de registros.
- División de datos con 'random_state=42'.
- Estratificación de la variable objetivo.
- Parámetros definidos para el modelo Random Forest.
- Registro de parámetros y métricas en MLflow.
- Persistencia local del modelo.
- Orquestación mediante un único comando.

Para reproducir la ejecución, se requiere contar con las dependencias instaladas, los archivos del proyecto y, muy importante, contar con la configuración de acceso a la base de datos de seguimiento de MLflow utilizada por el módulo de entrenamiento.

12. Limitaciones y mejoras futuras

El proyecto constituye una implementación inicial de un pipeline MLOps y por ende presenta oportunidades de mejora:

- Incorporar pruebas automatizadas mediante pytest.
- Implementar un sistema de versionamiento de datos y modelos.
- Integrar Git y GitHub para el seguimiento de cambios en el código.
- Incorporar mecanismos de seguimiento de métricas adicionales.
- Automatizar pruebas de calidad y evaluación del modelo.
- Implementar mecanismos de monitoreo del modelo y de los datos.
- Ampliar los controles de validación del contrato de datos.
- Mejorar la trazabilidad de los experimentos y artefactos.


13. Conclusión

La implementación permitió integrar controles de calidad de datos, preparación, entrenamiento, evaluación y seguimiento de experimentos en un flujo automatizado de Machine Learning.

El uso de un contrato de datos y de un mecanismo de validación personalizado permitió establecer controles previos al entrenamiento, mientras que la orquestación mediante Python facilitó la ejecución secuencial de los componentes y la interrupción del proceso ante inconsistencias.

El proyecto constituye una base para la implementación progresiva de prácticas MLOps orientadas a la reproducibilidad, trazabilidad y control de calidad de los procesos de Machine Learning.