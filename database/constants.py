#   Database
import os

database_host_name = os.getenv("KIH_API_DATABASE_HOST_NAME")
database_host_ip = os.getenv("KIH_API_DATABASE_HOST_IP")
database_user_name = os.getenv("KIH_API_DATABASE_USER_NAME")
database_user_name_password = os.getenv("KIH_API_DATABASE_USER_NAME_PASSWORD")
database_name = "KIH-DB1"

#   Database - Objects
database_application_name = ""
column_Timestamp = "Timestamp"

table_API_Calls =  "API_Calls"
column_API_Calls__Application = "Application"
column_API_Calls__URL = "URL"
column_API_Calls__Parameters = "Parameters"
column_API_Calls__Response_Code = "Response_Code"
column_API_Calls__Response = "Response"
column_API_Calls__Execution_Time = "Execution_Time"


table_Log = "Log"
column_Log__Application = "Application"
column_Log__Logger_Level = "Logger_Level"
column_Log__Log = "Log"

table_Performance = "Performance"
column_Performance__Application = "Application"
column_Performance__Execution_Type = "Execution_Type"
column_Performance__Execution_Subtype = "Execution_Subtype"
column_Performance__Execution_Command = "Execution_Command"
column_Performance__Execution_Time = "Execution_Time"

table_Market_Data = "Market_Data"
column_Market_Data__Instrument_Type = "Instrument_Type"
column_Market_Data__Symbol = "Symbol"
column_Market_Data__Market_Data = "Market_Data"
column_Market_Data__Raw_Data = "Raw_Data"
column_Market_Data__Timestamp = "Timestamp"

column_Market_Data__Instrument_Type_Stock = "Stock"

execution_type__Database = "Database"


table_Website_Views = "Website_Views"
column_Website_Views__IP_Address = "IP_Address"
column_Website_Views__Other_Info = "Other_Info"
