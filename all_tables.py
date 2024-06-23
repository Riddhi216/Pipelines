def copy_all_tables(source_engine, target_engine):
    inspector = inspect(source_engine)
    tables = inspector.get_table_names()
    for table in tables:
        df = pd.read_sql_table(table, source_engine)
        df.to_sql(table, target_engine, if_exists='replace', index=False)

# Usage
source_engine = get_engine('source_user', 'source_password', 'source_host', 'source_port', 'source_db')
target_engine = get_engine('target_user', 'target_password', 'target_host', 'target_port', 'target_db')
copy_all_tables(source_engine, target_engine)
