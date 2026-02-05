import pyodbc

# Vi skriver strängen direkt här för att testa
conn_str = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:weather-db-v2-amir.database.windows.net,1433;"
    "Database=weather-db-v2;"
    "Uid=clouduser;"
    "Pwd=Maryam420?;"  # Här ska lösenordet sitta, innanför citattecknen och semikolonet
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

try:
    print("Försöker ansluta direkt...")
    conn = pyodbc.connect(conn_str)
    print("✅ SUCCESS! Nu fungerar det!")
    conn.close()
except Exception as e:
    print(f"❌ Fel igen: {e}")
