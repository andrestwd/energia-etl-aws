# Proyecto ETL de Energía

## Objetivo del Proyecto
Automatizar el flujo de datos provenientes de archivos CSV generados por el sistema de la compañía, para:

- **Centralizar los datos** en un Data Lake en Amazon S3.
- **Transformarlos y almacenarlos** en formato Parquet.
- **Catalogarlos** mediante AWS Glue Crawlers.
- **Ejecutar consultas** con Amazon Athena.
- **Cargarlos** en un Data Warehouse (Amazon Redshift).
- **Aplicar control de acceso y permisos** mediante AWS Lake Formation.
- **Orquestar todo el flujo** con AWS Step Functions.
- **Desplegar toda la infraestructura automáticamente** con AWS CloudFormation.

---

## Infraestructura como Código (IaC)
Todo el pipeline es desplegable mediante el archivo `cloudformation/datalake.yml`. Esto incluye:

1. **Buckets S3**:
   - Zonas `raw/`, `processed/`, `scripts/`, `temp/`, `athena-query-results/`.

2. **Bases de Datos Glue**:
   - `energia_raw_cf`: Base de datos para datos crudos.
   - `energia_etl_db`: Base de datos para datos procesados.

3. **Crawlers de Glue**:
   - Crawler para la zona `raw/`.
   - Crawler para la zona `processed/`.

4. **Jobs de Glue**:
   - Transformación de datos crudos a procesados en formato Parquet.

5. **Máquina de Estados Step Functions**:
   - Orquesta todo el pipeline ETL, desde la transformación hasta la carga en Redshift.

6. **Roles IAM**:
   - Roles para Glue, Redshift, Lambda, Step Functions y Athena.

7. **Lambda para Ejecutar DDL en Redshift**:
   - Función Lambda que crea automáticamente las tablas en Redshift.

8. **Permisos y Registro en Lake Formation**:
   - Configuración de permisos para acceso a datos y consultas en Athena.

### Para desplegar:
Ejecuta el siguiente comando para desplegar toda la infraestructura:
```bash
aws cloudformation deploy \
  --template-file cloudformation/datalake.yml \
  --stack-name energia-etl-completo \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides Environment=dev
```

---

## Estructura del Proyecto
```
energia-etl-aws/
├── cloudformation/
│   └── datalake.yml # Plantilla IaC completa del proyecto
├── scripts/
│   ├── transformar_clientes_parquet.py
│   ├── transformar_proveedores_parquet.py
│   ├── transformar_transacciones_parquet.py
│   ├── load_clientes_s3_to_redshift.py
│   ├── load_proveedores_s3_to_redshift.py
│   ├── load_transacciones_s3_to_redshift.py
│   ├── create_redshift_tables.py # Script para crear tablas en Redshift
│   └── simulate_pipeline.py # Script para simular el pipeline localmente
├── athena/
│   └── queries.py # Consultas SQL básicas desde Python con boto3
├── data/
│   ├── raw/clientes/clientes.csv
│   ├── raw/proveedores/proveedores.csv
│   ├── raw/transacciones/transacciones.csv
├── lakeformation/
│   └── permisos_lakeformation.md # Documentación de permisos configurados en Lake Formation
├── README.md # Documentación completa
└── requirements.txt # Dependencias de Python
```

---

## Servicios Utilizados
### 1. **Amazon S3**
- Almacena los datos crudos (`RawBucket`) y los datos procesados (`ProcessedBucket`).
- Los datos procesados se almacenan en formato Parquet y se particionan por fecha de carga.

### 2. **AWS Glue**
- **Glue Crawlers**: Detectan y catalogan automáticamente los esquemas de los datos en S3.
- **Glue Jobs**: Transforman los datos crudos en datos procesados en formato Parquet.

### 3. **Amazon Redshift**
- Almacena los datos procesados en un Data Warehouse para análisis avanzado.
- Las tablas (`clientes`, `proveedores`, `transacciones`) se crean automáticamente mediante una función Lambda.

### 4. **AWS Lake Formation**
- Centraliza el gobierno y la seguridad del Data Lake.
- Controla el acceso a los datos en S3 y Glue mediante permisos granulares.

### 5. **Amazon Athena**
- Permite ejecutar consultas SQL sobre los datos procesados almacenados en S3.

### 6. **AWS Step Functions**
- Orquesta todo el pipeline ETL, desde la transformación de datos hasta la carga en Redshift.

### 7. **AWS CloudFormation**
- Despliega toda la infraestructura automáticamente, incluyendo S3, Glue, Redshift, Step Functions y Lake Formation.

---

## Permisos y Roles Utilizados en el Proyecto

### 1. **AWS Glue**
#### **Rol: `AWSGlueServiceRole`**
- **Propósito**: Permitir que AWS Glue acceda a los datos en S3 y ejecute trabajos de transformación.
- **Permisos**:
  - `service-role/AWSGlueServiceRole`: Permiso administrado por AWS para Glue.
  - Política personalizada para acceso a S3:
    ```json
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::energy-datalake-raw-*",
        "arn:aws:s3:::energy-datalake-raw-*/*",
        "arn:aws:s3:::energy-datalake-processed-*",
        "arn:aws:s3:::energy-datalake-processed-*/*"
      ]
    }
    ```

### 2. **AWS Redshift**
#### **Rol: `RedshiftS3Access`**
- **Propósito**: Permitir que Redshift acceda a los datos procesados en S3 para cargar datos en las tablas.
- **Permisos**:
  - Política personalizada para acceso a S3:
    ```json
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": [
        "arn:aws:s3:::energy-datalake-processed-*",
        "arn:aws:s3:::energy-datalake-processed-*/*"
      ]
    }
    ```

### 3. **AWS Lake Formation**
#### **Rol: `LakeFormationAdmin`**
- **Propósito**: Administrar el Data Lake y controlar el acceso a los datos.
- **Permisos**:
  - Control total sobre el Data Lake:
    ```yaml
    LakeFormationSettings:
      Admins:
        - DataLakePrincipalIdentifier: arn:aws:iam::<AccountId>:role/LakeFormationAdmin
    ```
  - Permisos de ubicación de datos:
    ```yaml
    DataLocationPermission:
      DataLakePrincipal:
        DataLakePrincipalIdentifier: arn:aws:iam::<AccountId>:role/LakeFormationAdmin
      Resource:
        DataLocation:
          S3Resource: arn:aws:s3:::energy-datalake-raw-<Environment>
      Permissions:
        - DATA_LOCATION_ACCESS
    ```

### 4. **AWS Step Functions**
#### **Rol: `StepFunctionExecutionRole`**
- **Propósito**: Permitir que Step Functions orqueste Glue Jobs y funciones Lambda.
- **Permisos**:
  - Permisos para Glue y Lambda:
    ```json
    {
      "Effect": "Allow",
      "Action": [
        "glue:StartJobRun",
        "lambda:InvokeFunction"
      ],
      "Resource": "*"
    }
    ```

### 5. **Amazon Athena**
#### **Rol: `AthenaQueryRole`**
- **Propósito**: Permitir que Athena consulte los datos procesados catalogados en Glue.
- **Permisos**:
  - Permisos para consultar la base de datos Glue:
    ```yaml
    AthenaWorkGroupPermission:
      DataLakePrincipal:
        DataLakePrincipalIdentifier: arn:aws:iam::<AccountId>:role/AthenaQueryRole
      Resource:
        Database:
          Name: energy_datalake_db_<Environment>
      Permissions:
        - SELECT
        - DESCRIBE
    ```

---

## Pasos del Pipeline ETL
### 1. **Carga de Datos Crudos**
- Los datos crudos (`clientes.csv`, `proveedores.csv`, `transacciones.csv`) se cargan en el bucket S3 (`RawBucket`).

### 2. **Catalogación de Datos Crudos**
- Los Glue Crawlers detectan automáticamente los esquemas de los datos crudos y los catalogan en el Glue Data Catalog.

### 3. **Transformación de Datos**
- Los Glue Jobs transforman los datos crudos en datos procesados:
  - **Clientes**: Renombra columnas y agrega la fecha de carga.
  - **Proveedores**: Normaliza el texto y agrega la fecha de carga.
  - **Transacciones**: Calcula un campo adicional (`total`) y agrega la fecha de carga.
- Los datos procesados se almacenan en el bucket S3 (`ProcessedBucket`) en formato Parquet.

### 4. **Catalogación de Datos Procesados**
- Los Glue Crawlers detectan los datos procesados y actualizan el Glue Data Catalog.

### 5. **Creación de Tablas en Redshift**
- Una función Lambda (`create_redshift_tables.py`) crea automáticamente las tablas en Redshift:
  - `clientes`
  - `proveedores`
  - `transacciones`

### 6. **Carga de Datos a Redshift**
- Los datos procesados se cargan desde S3 a Redshift utilizando scripts de carga (`load_clientes_s3_to_redshift.py`, etc.) que ejecutan consultas `COPY`.

### 7. **Consultas en Athena**
- Se ejecutan consultas SQL en Athena para analizar los datos procesados.

---

## Cómo Ejecutar el Pipeline
### 1. **Despliegue de la Infraestructura**
Ejecuta el siguiente comando para desplegar toda la infraestructura utilizando CloudFormation:
```bash
aws cloudformation deploy \
  --template-file c:\Users\Administrador\energia-etl-aws\cloudformation\datalake.yml \
  --stack-name energia-etl-completo \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides Environment=dev
```

### 2. **Carga de Scripts y Datos a S3**
Sube los scripts de transformación y carga al bucket S3:
```bash
aws s3 cp c:\Users\Administrador\energia-etl-aws\scripts\transformar_clientes_parquet.py s3://energy-datalake-raw-dev/scripts/
aws s3 cp c:\Users\Administrador\energia-etl-aws\scripts\transformar_proveedores_parquet.py s3://energy-datalake-raw-dev/scripts/
aws s3 cp c:\Users\Administrador\energia-etl-aws\scripts\transformar_transacciones_parquet.py s3://energy-datalake-raw-dev/scripts/
aws s3 cp c:\Users\Administrador\energia-etl-aws\scripts\create_redshift_tables.py s3://energy-datalake-raw-dev/scripts/
```

Sube los datos crudos al bucket S3:
```bash
aws s3 cp c:\Users\Administrador\energia-etl-aws\data\raw\clientes\clientes.csv s3://energy-datalake-raw-dev/clientes/
aws s3 cp c:\Users\Administrador\energia-etl-aws\data\raw\proveedores\proveedores.csv s3://energy-datalake-raw-dev/proveedores/
aws s3 cp c:\Users\Administrador\energia-etl-aws\data\raw\transacciones\transacciones.csv s3://energy-datalake-raw-dev/transacciones/
```

### 3. **Ejecutar Crawlers de Glue**
Ejecuta los Glue Crawlers para catalogar los datos:
```bash
aws glue start-crawler --name raw-data-crawler-dev
aws glue start-crawler --name processed-data-crawler-dev
```

### 4. **Ejecutar la State Machine en Step Functions**
Inicia la ejecución de la State Machine para orquestar el pipeline:
```bash
aws stepfunctions start-execution --state-machine-arn <StepFunctionStateMachineArn>
```
Reemplaza `<StepFunctionStateMachineArn>` con el ARN de la State Machine generado por CloudFormation.

### 5. **Validar los Datos Procesados**
Ejecuta consultas en Athena para validar los datos procesados:
```bash
python c:\Users\Administrador\energia-etl-aws\athena\queries.py
```

### 6. **Verificar los Datos en Redshift**
Conéctate al clúster de Redshift y verifica que las tablas contengan los datos cargados:
```sql
SELECT * FROM clientes LIMIT 10;
SELECT * FROM proveedores LIMIT 10;
SELECT * FROM transacciones LIMIT 10;
```

---

## Dependencias
Instala las dependencias necesarias con:
```bash
pip install -r requirements.txt
```

---

## Monitoreo
- **CloudWatch Logs**: Monitorea los Glue Jobs, funciones Lambda y Step Functions.
- **Errores**: Revisa los logs en CloudWatch para identificar posibles errores.

---

## Notas Finales
Este pipeline está diseñado para ser completamente automatizado y escalable. Se debe realizar pruebas en un entorno de desarrollo antes de desplegarlo en producción.