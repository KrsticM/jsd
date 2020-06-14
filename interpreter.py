from textx import metamodel_from_file
from os.path import join, dirname
import psycopg2
import jinja2
import datetime

metamodel = metamodel_from_file('grammar.tx')
model = metamodel.model_from_file('document.docv')
con = psycopg2.connect(database="jsd", user="postgres", password="postgres", host="127.0.0.1", port="5432")

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(join(dirname(__file__), 'templates')), trim_blocks=True, lstrip_blocks=True)
now = datetime.datetime.now().strftime("%a, %b %d, %Y %X")

all_data = {}
all_data_colnames = {}



def parse_data(data):
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

def parse_text(data):    
    data_type = data.__class__.__name__ 
    if(data_type == 'Text'):
        template = jinja_env.get_template('text.j2')
        output_folder.write(template.render(text=data.text, datetime=now))
    elif(data_type == 'Header'):
        template = jinja_env.get_template('header.j2')
        output_folder.write(template.render(data=data, datetime=now))
    else:
        print('propao u else')

def parse_image(data):
    template = jinja_env.get_template('image.j2')
    output_folder.write(template.render(image_source=join('../', data.image_source), datetime=now))

# main fuction
if __name__ == "__main__":
    output_folder = open('generated/output.html', 'w')
    for document_statement in model.document_statement:
        if(document_statement.data != None):
            parse_data(document_statement.data)
        elif(document_statement.text != None):
            parse_text(document_statement.text)
        elif(document_statement.image != None):
            parse_image(document_statement.image)
        else:
            print("Exception")

    con.close()
    output_folder.close()
    print(all_data)
    print(all_data_colnames)