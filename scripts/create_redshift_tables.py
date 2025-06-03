"""
Permisos configurados en Lake Formation:

1. Administrador del Data Lake:
   - Rol: LakeFormationAdmin
   - Permisos: Control total sobre el Data Lake.

2. Permisos de ubicación de datos:
   - Ubicación: S3://energy-datalake-raw-<Environment>
   - Ubicación: S3://energy-datalake-processed-<Environment>
   - Permisos: DATA_LOCATION_ACCESS otorgados al rol LakeFormationAdmin.

3. Permisos sobre la base de datos Glue:
   - Base de datos: energy_datalake_db_<Environment>
   - Permisos: ALL otorgados al rol LakeFormationAdmin.

4. Permisos para consultas en Athena:
   - Rol: AthenaQueryRole
   - Permisos: SELECT y DESCRIBE sobre la base de datos Glue.

Estos permisos están configurados en la plantilla CloudFormation (datalake.yml) bajo las secciones:
- LakeFormationSettings
- Lake Formation Permissions
"""

import redshift_connector

def handler(event, context):
    cluster_id = event['ResourceProperties']['ClusterIdentifier']
    database = event['ResourceProperties']['DatabaseName']
    db_user = event['ResourceProperties']['DbUser']
    tables = event['ResourceProperties']['Tables']

    conn = redshift_connector.connect(
        host=f"{cluster_id}.redshift.amazonaws.com",
        database=database,
        user=db_user,
        password="MasterPass123!"
    )
    cursor = conn.cursor()

    for table in tables:
        print(f"Creando tabla: {table['Name']}")
        cursor.execute(table['Schema'])

    conn.commit()
    cursor.close()
    conn.close()

    return {
        'Status': 'SUCCESS',
        'PhysicalResourceId': 'RedshiftTableSetup',
        'Data': {}
    }
