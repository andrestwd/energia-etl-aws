# Scripts del Proyecto ETL de Energía

Este directorio contiene los scripts necesarios para transformar, cargar y procesar los datos en el pipeline ETL.

## Scripts Disponibles

### Transformaciones
- **transformar_clientes_parquet.py**: Transforma los datos de clientes y los almacena en formato Parquet.
- **transformar_proveedores_parquet.py**: Transforma los datos de proveedores y los almacena en formato Parquet.
- **transformar_transacciones_parquet.py**: Transforma los datos de transacciones y los almacena en formato Parquet.

### Carga a Redshift
- **load_clientes_s3_to_redshift.py**: Carga los datos de clientes desde S3 a Redshift.
- **load_proveedores_s3_to_redshift.py**: Carga los datos de proveedores desde S3 a Redshift.
- **load_transacciones_s3_to_redshift.py**: Carga los datos de transacciones desde S3 a Redshift.

### Consultas en Athena
- **queries.py**: Ejecuta consultas SQL básicas en Athena utilizando `boto3`.

## Uso
Ejecuta cada script de forma independiente o como parte de la orquestación con AWS Step Functions.
