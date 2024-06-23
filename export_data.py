import pandas as pd
from sqlalchemy import create_engine
import pyarrow as pa
import pyarrow.parquet as pq
import fastavro

def get_engine(user, password, host, port, db):
    return create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

def export_table_to_formats(engine, table_name, output_dir):
    df = pd.read_sql_table(table_name, con=engine)
    
    # Export to CSV
    csv_path = f"{output_dir}/{table_name}.csv"
    df.to_csv(csv_path, index=False)
    
    # Export to Parquet
    parquet_path = f"{output_dir}/{table_name}.parquet"
    table = pa.Table.from_pandas(df)
    pq.write_table(table, parquet_path)
    
    # Export to Avro
    avro_path = f"{output_dir}/{table_name}.avro"
    schema = {
        "type": "record",
        "name": table_name,
        "fields": [{"name": col, "type": "string"} for col in df.columns]
    }
    records = df.to_dict(orient='records')
    with open(avro_path, 'wb') as out:
        fastavro.writer(out, schema, records)
    
    return csv_path, parquet_path, avro_path

if __name__ == "__main__":
    # Replace the following variables with your actual database credentials and details
    user = 'riddhi'
    password = 'Rid12345'
    host = 'localhost'
    port = 5432  # Replace with your actual port number (e.g., 5432 for PostgreSQL)
    db = 'csidatabase'
    table_name = 'export_datas'
    output_dir = 'C:/Users/Lenovo/Desktop/Project/outputs'

    engine = get_engine(user, password, host, port, db)
    export_table_to_formats(engine, table_name, output_dir)
