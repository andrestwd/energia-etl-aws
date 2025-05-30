HEAD
#  Proyecto ETL Comercializadora de Energía - AWS Data Lake
Pipeline de procesamiento de datos en AWS para comercializadora de energía



##  Descripción General

Este proyecto implementa un pipeline de datos para una comercializadora de energía que recopila información desde archivos CSV generados por un sistema transaccional. La solución automatiza el proceso de ingestión, transformación, catalogación, consulta y carga hacia un Data Warehouse en AWS Redshift utilizando una arquitectura moderna basada en servicios administrados y buenas prácticas de gobierno de datos.

##  Objetivo del Proyecto

Automatizar el flujo de datos provenientes de archivos CSV generados por el sistema de la compañía, para:

- Centralizar los datos en un **Data Lake** en Amazon S3.
- Transformarlos y almacenarlos en **formato Parquet**.
- Catalogarlos mediante **AWS Glue Crawlers**.
- Ejecutar consultas con **Amazon Athena**.
- Cargarlos en un **Data Warehouse (Amazon Redshift)**.
- Aplicar control de acceso y permisos mediante **AWS Lake Formation**.
- Orquestar todo el flujo con **AWS Step Functions**.
- Desplegar toda la infraestructura automáticamente con **AWS CloudFormation**.


##  Servicios AWS Utilizados

| Servicio              | Propósito                                                                 |
|-----------------------|--------------------------------------------------------------------------|
| Amazon S3             | Almacenamiento raw y processed (particionado por fecha)                 |
| AWS Glue              | Crawlers para catálogo, Jobs para transformación y carga a Redshift     |
| Amazon Athena         | Consulta de datos transformados mediante SQL desde Python               |
| Amazon Redshift       | Almacenamiento final en Data Warehouse                                  |
| AWS Lake Formation    | Gobierno de datos, control de acceso y permisos                         |
| AWS Step Functions    | Orquestación del pipeline ETL                                           |
| AWS IAM               | Gestión de roles y permisos                                             |
| AWS CloudFormation    | Infraestructura como código (IaC) para desplegar toda la arquitectura   |

##  Estructura del Repositorio

```
energia-etl-aws/
├── cloudformation/
│   └── datalake.yml             # Plantilla IaC completa del proyecto
├── scripts/
│   ├── transformar_clientes_parquet.py
│   ├── transformar_proveedores_parquet.py
│   ├── transformar_transacciones_parquet.py
│   ├── load_clientes_s3_to_redshift.py
│   ├── load_proveedores_s3_to_redshift.py
│   └── load_transacciones_s3_to_redshift.py
├── athena/
│   └── queries.py               # Consultas SQL básicas desde Python con boto3
├── data/
│   ├── raw/clientes/...
│   ├── raw/proveedores/...
│   └── raw/transacciones/...
├── README.md                    # Documentación completa
└── requirements.txt             # Dependencias de Python
```

##  Infraestructura como Código (IaC)

Todo el pipeline es desplegable mediante el archivo [`cloudformation/datalake.yml`](cloudformation/datalake.yml). Esto incluye:

- Bucket S3 para las zonas `raw/`, `processed/`, `scripts/`, `temp/`, `athena-query-results/`
- Bases de datos Glue `energia_raw_cf`, `energia_etl_db`
- Crawlers para raw y processed
- Jobs de Glue (transformación y carga)
- Máquina de estado Step Functions
- Roles IAM (Glue, Redshift, Lambda, Step Functions)
- Lambda para ejecutar DDL en Redshift
- Permisos y registro en Lake Formation

Para desplegar:

```
aws cloudformation deploy   --template-file cloudformation/datalake.yml   --stack-name energia-etl-completo   --capabilities CAPABILITY_NAMED_IAM   --parameter-overrides Environment=dev BucketName=energia-etl-datalake-andrestwd ...
```

## 🔄 Orquestación del Pipeline

- El pipeline está controlado por una **state machine** en AWS Step Functions.
- Define la ejecución secuencial de los Glue Jobs:
  1. Transformación de datos de proveedores, clientes y transacciones.
  2. Carga hacia Redshift.
- Se detiene ante errores y permite reinicios fáciles.

##  Consultas SQL en Athena

Consulta de los datos procesados con Athena vía Python (ejecutadas desde `boto3`):

```sql
-- Total de ventas por tipo de energía
SELECT tipo_energia, SUM(cantidad_comprada * precio) AS total_ventas
FROM transacciones
WHERE tipo_transaccion = 'venta'
GROUP BY tipo_energia;

-- Conteo de clientes por ciudad
SELECT ciudad, COUNT(*) AS total_clientes
FROM clientes
GROUP BY ciudad;
```

Los resultados se almacenan en:
`s3://energia-etl-datalake-andrestwd/athena-query-results/`

##  Permisos, Políticas y Gobierno (Lake Formation)

1. **Registro del recurso**:
   - Bucket registrado como recurso en Lake Formation.
2. **Permisos sobre base de datos y tablas**:
   - `LakeFormationAdmin`: permisos `ALL` sobre S3 y Glue DB.
   - `ReportViewer`: permisos `SELECT` y `DESCRIBE` sobre:
     - `energia_etl_db`: clientes, proveedores.
     - `energia_raw_cf`: transacciones.
3. **IAM Roles utilizados**:
   - `AWSGlueServiceRole-ETL`
   - `LakeFormationAdmin`
   - `ReportViewer`
   - `AthenaQueryExecutionRole`
   - `glue-job-role-dev`
   - `glue-crawler-role-dev`

##  Flujo Periódico / Automatización

Aunque actualmente la ejecución es **manual (on demand)**, este pipeline puede automatizarse con:

- **Eventos de carga en S3**
- **CloudWatch Events o EventBridge**
- **Triggers en Glue**
- **Ejecución programada de Step Functions**

##  Puntos Plus (Bonus)

| Requisito                                 | Implementado |
|------------------------------------------|--------------|
| Infraestructura como código (IaC)        | ✅           |
| Gobierno con Lake Formation              | ✅           |
| Carga final en Amazon Redshift           | ✅           |

##  Requisitos

- AWS CLI configurado
- Python 3.9+
- Boto3
- Zip y herramientas básicas de empaquetado

##  Autores

- Andrés agudelo
- Prueba técnica - Evaluación para ingeniería de datos