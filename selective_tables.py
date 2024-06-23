def copy_selective_tables(source_engine, target_engine, table_columns):
    for table, columns in table_columns.items():
        query = f"SELECT {', '.join(columns)} FROM {table}"
        df = pd.read_sql_query(query, source_engine)
        df.to_sql(table, target_engine, if_exists='replace', index=False)

# Usage
table_columns = {
    'table1': ['column1', 'column2'],
    'table2': ['column3', 'column4']
}
copy_selective_tables(source_engine, target_engine, table_columns)
