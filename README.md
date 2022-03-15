# SALESFORCE APP

Purpose: Load data from Salesforce with Salesforce API and insert data to SQL Server

Technologies:
- Language : Python
- Encrypt salesforce credentials : encryptoenv https://pypi.org/project/encryptoenv/ 
- Interact with Salesforce : simple-salesforce https://pypi.org/project/simple-salesforce/0.3/
- Interact with SQL Server : sqlalchemy https://pypi.org/project/SQLAlchemy/
- Handle data : Pandas https://pypi.org/project/pandas/
- Log execution data to excel : https://pypi.org/project/XlsxWriter/

## Program features:

#### Connect to Salesfoce with Salesforce API
- Authentication for Salesforce API

#### Connect to SQL Server
- Authentication for SQL Server
- Create SQL engine instance for STG database and for DW database

#### Load data from Salesforce
- Fetch Salesforce object names and labels
- Fetch columns for object (filter out compund type columns : Salesforce column soaptype = urn:xxxx)
- Query Salesforce with object name and column names
- Transform Salesforce data types to corresponding sqlalchemy data types
- Transform datetime values in acceptable format for SQL Server
- Remove Salesforce table attribute column
- Add LOAD_CREATED_DATE for data rows

#### Insert data to SQL Server
- Check if Salesforce table is empty -> do not create table or insert data
- Check if table already exists in SQL Server
- Comnpare schemas between STG table in SQL Server and current salesforce table
- If needed add columns to STG table
- Append salesforce data to existing STG table
- Insert and replace data in existing DW table
- Delete over 7 old records from STG table

#### Execution log
Program finishes succesfully:
- Creates execution log under /salesforce-app/excecution_log/
Program finishes with failure:
- Error message logged under /salesforce-app/excecution_log/

#### Run program as daily or hourly excecution 
With command line arguments daily or hourly execution log can be defined. See more in section 'Program up and running'
Daily excecution:
- Load all salesforce objects and insert into SQL Server
Hourly excecution:
- Load objects specified in .env file from salesforce and insert into SQL Server

#### Error handling
In case of any exception program quits execution and acts per excecution log program finishes with failure

## Program up and running
- Activate virtual environment 
C:\sfloads\salesforce-app\venv\Scripts\activate
- Start program and provide command line argument
python C:\sfloads\salesforce-app\src\sfdumbs\main.py daily
or
python C:\sfloads\salesforce-app\src\sfdumbs\main.py hourly
