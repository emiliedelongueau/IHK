from __future__ import print_function
import os
import re

#http://stackoverflow.com/questions/3964681/find-all-files-in-directory-with-extension-txt-with-python
create_table_file = open('create_table.sql', 'r')
output_file = open('import_data.sql', 'w')
print('drop table districts;', file=output_file)
for line in create_table_file:
    print(line, file=output_file)
print('.mode csv', file=output_file)
print('create table if not exists districts (name TEXT, state TEXT, classification TEXT, household_total INTEGER, population_total INTEGER);', file=output_file)

def import_from_file(filename):
    print('.import "data/'+filename+'" raw_data', file=output_file)

for filename in os.listdir("data/"):
    if filename.endswith('.CSV'):
        import_from_file(filename)
        state_name = re.sub(r'.CSV', '', filename)
        state_name = re.sub(r'[()\d]', '', state_name)
        state_name = state_name.strip()
        print('insert or replace into districts select Name, "'+state_name+'", TRU, "No of households", "Total Population Person" from raw_data where Level=\'DISTRICT\';', file=output_file)
        print('drop table raw_data;', file=output_file)
        
        