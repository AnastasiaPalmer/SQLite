table_name = "Studendts"
data = [
    [ "name", "room"],
    [ "vasia", 10],
    [ "peter", 12]
]
create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({','.join([data[0][i] for i in range(len(data[0]))])})"

print(create_table_query)
# print( data[0] )
# print( ['col'+str(i)+' TEXT' for i in range(len(data[0]))] )
# print( len(data[0]) )
# print( range(len(data[0])) )
insert_query = f"INSERT INTO {table_name} VALUES ({','.join(['?']*len(data[0]))})"
print(insert_query)
