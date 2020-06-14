from textx import metamodel_from_file
import psycopg2

metamodel = metamodel_from_file('grammar.tx')
model = metamodel.model_from_file('document.docv')
con = psycopg2.connect(database="jsd", user="postgres", password="postgres", host="127.0.0.1", port="5432")

all_data = {}
all_data_colnames = {}



def parse_data(data):
    print(data.name)
    print(data.data_value)
    cur = con.cursor()
    cur.execute(data.data_value)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]

    all_data[data.name] = rows
    all_data_colnames[data.name] = colnames
    # print(type(rows))
    # for row in rows:
    #     print(row[0])
    #     print(row[1])
    #     print(row[2])
    #     print(row[3])
    #     print(row[4])
    #     print(row[5] + "\n")

    

# Main loop
for document_statement in model.document_statement:
    print(document_statement)
    print(document_statement.data)
    if(document_statement.data != None):
        parse_data(document_statement.data)
    else:
        print("Exception")

con.close()
print(all_data)
print(all_data_colnames)