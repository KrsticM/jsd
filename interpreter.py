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

def parse_table(data):
    # Za sada ovako, mozda enkapsulirati promenljive u klasu Tabela?
    numRow = None
    title = None
    datasource = None
    col_names = []
    for attr in data.table_attr:
        attr_type = attr.__class__.__name__ 
        if(attr_type == 'DataSource'):
            datasource = attr.name

            if datasource not in all_data or datasource not in all_data_colnames:
                print("[Exception]: datasource " + datasource + " doesn't exists")
                return 
        elif(attr_type == 'NumRow'):
            numRow = attr.num_row
        elif(attr_type == 'Title'):
            title = attr.title
        elif(attr_type == 'Select'):
            for col in attr.columns:        

                if col.name.value not in all_data_colnames[datasource]:
                    print("[Exception]: column " + col.name.value + " doesn't exists")
                    return 

                col_names.append(col.name.value)
        else:
            print('nije nista')

    table_data = all_data[datasource]
    table_data_col_names = all_data_colnames[datasource]
    #print("TABLE DATA:")
    #print(table_data)
    arranged_table = []
    # Treba da preslozimo podatke u table_data da odgovaraju redosledu select kolona
    for row in table_data:
        arranged_row = []
        for select_col_name in col_names:
            #print(table_data_col_names)
            index = table_data_col_names.index(select_col_name)
            arranged_row.append(row[index])

        arranged_table.append(arranged_row)
    
    print('bbb ', len(col_names))
    template = jinja_env.get_template('table.j2')
    output_folder.write(template.render(col_names_num=len(col_names), numRow=numRow, title=title, col_names=col_names, arranged_table=arranged_table))

# main fuction
if __name__ == "__main__":
    output_folder = open('generated/output.html', 'w')

    template = jinja_env.get_template('html_header.j2')
    output_folder.write(template.render())

    for document_statement in model.document_statement:
        if(document_statement.data != None):
            parse_data(document_statement.data)
        elif(document_statement.text != None):
            parse_text(document_statement.text)
        elif(document_statement.image != None):
            parse_image(document_statement.image)
        elif(document_statement.table != None):
            parse_table(document_statement.table)
        else:
            print("Exception")

    template = jinja_env.get_template('html_footer.j2')
    output_folder.write(template.render())

    con.close()
    output_folder.close()
    print(all_data)
    print(all_data_colnames)