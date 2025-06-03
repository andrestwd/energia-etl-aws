# Permisos Configurados en Lake Formation

Este documento describe los permisos configurados en AWS Lake Formation para el proyecto ETL de Energía.

## 1. Administrador del Data Lake
- **Rol**: `LakeFormationAdmin`
- **Permisos**: Control total sobre el Data Lake.
- **Configuración**:
  ```yaml
  LakeFormationSettings:
    Type: AWS::LakeFormation::DataLakeSettings
    Properties:
      Admins:
        - DataLakePrincipalIdentifier: arn:aws:iam::<AccountId>:role/LakeFormationAdmin
  ```

## 2. Permisos de Ubicación de Datos
- **Ubicaciones**:
  - `s3://energy-datalake-raw-<Environment>`
  - `s3://energy-datalake-processed-<Environment>`
- **Permisos**: `DATA_LOCATION_ACCESS` otorgados al rol `LakeFormationAdmin`.
- **Configuración**:
  ```yaml
  DataLocationPermission:
    Type: AWS::LakeFormation::Permissions
    Properties:
      DataLakePrincipal:
        DataLakePrincipalIdentifier: arn:aws:iam::<AccountId>:role/LakeFormationAdmin
      Resource:
        DataLocation:
          S3Resource: arn:aws:s3:::energy-datalake-raw-<Environment>
      Permissions:
        - DATA_LOCATION_ACCESS
  ```

## 3. Permisos sobre la Base de Datos Glue
- **Base de Datos**: `energy_datalake_db_<Environment>`
- **Permisos**: `ALL` otorgados al rol `LakeFormationAdmin`.
- **Configuración**:
  ```yaml
  GlueDatabasePermission:
    Type: AWS::LakeFormation::Permissions
    Properties:
      DataLakePrincipal:
        DataLakePrincipalIdentifier: arn:aws:iam::<AccountId>:role/LakeFormationAdmin
      Resource:
        Database:
          Name: energy_datalake_db_<Environment>
      Permissions:
        - ALL
  ```

## 4. Permisos para Consultas en Athena
- **Rol**: `AthenaQueryRole`
- **Permisos**: `SELECT` y `DESCRIBE` sobre la base de datos Glue.
- **Configuración**:
  ```yaml
  AthenaWorkGroupPermission:
    Type: AWS::LakeFormation::Permissions
    Properties:
      DataLakePrincipal:
        DataLakePrincipalIdentifier: arn:aws:iam::<AccountId>:role/AthenaQueryRole
      Resource:
        Database:
          Name: energy_datalake_db_<Environment>
      Permissions:
        - SELECT
        - DESCRIBE
  ```

## Referencia
Estos permisos están configurados en la plantilla CloudFormation (`datalake.yml`) bajo las secciones:
- `LakeFormationSettings`
- `Lake Formation Permissions`
