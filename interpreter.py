from textx import metamodel_from_file
from os.path import join, dirname
import psycopg2
import jinja2
import pdfkit
import sys

from models.chart import Chart

metamodel = metamodel_from_file('grammar/grammar.tx')
con = psycopg2.connect(database="jsd", user="postgres", password="postgres", host="127.0.0.1", port="5432")

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(join(dirname(__file__), 'templates')), trim_blocks=True, lstrip_blocks=True)

all_data = {}
all_data_colnames = {}
charts = []


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
        output_folder.write(template.render(text=data.text))
    elif(data_type == 'Header'):
        print('header color ', data.header_color)
        template = jinja_env.get_template('header.j2')
        output_folder.write(template.render(data=data))
    else:
        print('propao u else')

def parse_image(data):
    template = jinja_env.get_template('image.j2')
    output_folder.write(template.render(image_source=join(data.image_source)))

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
    arranged_table = []
    # Treba da preslozimo podatke u table_data da odgovaraju redosledu select kolona
    for row in table_data:
        arranged_row = []
        for select_col_name in col_names:
            index = table_data_col_names.index(select_col_name)
            arranged_row.append(row[index])

        arranged_table.append(arranged_row)
    
    template = jinja_env.get_template('table.j2')
    output_folder.write(template.render(col_names_num=len(col_names), numRow=numRow, title=title, col_names=col_names, arranged_table=arranged_table))


def parse_chart(data):
    chart_type = data.__class__.__name__
    print(chart_type)
    if(chart_type == 'PieChart'):
        chart = Chart('pie', 'chart' + str(len(charts)))
        format_chart(chart, data)
        # Render template
        template = jinja_env.get_template('chart.j2')
        output_folder.write(template.render(chart_id=chart.name))

        charts.append(chart)        
    elif(chart_type == 'LineChart'):
        chart = Chart('line', 'chart' + str(len(charts)))
        format_chart(chart, data)

        # Render template
        template = jinja_env.get_template('chart.j2')
        output_folder.write(template.render(chart_id=chart.name))

        charts.append(chart)
    elif(chart_type == 'BarChart'):
        chart = Chart('bar', 'chart' + str(len(charts)))
        format_chart(chart, data)

        # Render template
        template = jinja_env.get_template('chart.j2')
        output_folder.write(template.render(chart_id=chart.name))

        charts.append(chart)

def format_chart(chart, data):
    for chart_attr in data.chart_attr:
        chart_attr_type = chart_attr.__class__.__name__ 
        if(chart_attr_type == 'DataSource'):
            # TODO: Provera da li datasource postoji
            chart.datasource = chart_attr.name
        elif(chart_attr_type == 'SeriesSelect'):
            for series_attr in chart_attr.series_attr:
                series_attr_type = series_attr.__class__.__name__

                # Formiranje vrednosti labela
                if(series_attr_type == 'Label'): 
                    chart_label_type = series_attr.label_value.__class__.__name__

                    if(chart_label_type == 'StringValues'):
                        label_values = []
                        for string_value in series_attr.label_value.string_values:
                            label_values.append(string_value.value)
                        chart.label_values = label_values

                    elif(chart_label_type == 'DataValue'):
                        chart.label = series_attr.label_value.value # Koja je kolona koriscena pri labeliranju
                        chart.label_values = create_chart_label_values(series_attr.label_value.value, chart.datasource)

                elif(series_attr_type == 'Value'):
                    datafield_type = series_attr.datafield.__class__.__name__
                    datafield = series_attr.datafield
                    if(datafield_type == 'AggregateField'):
                        data_values = []
                        if(datafield.type == 'Count'):
                            column = datafield.data_value.value
                            data_values = count(column, chart.datasource)
                        elif(datafield.type == 'Sum'):
                            column = datafield.data_value.value
                            data_values = suma(column, chart)

                        chart.data_values = data_values
                    elif(datafield_type == 'DataValue'):
                        chart_data = all_data[chart.datasource]
                        chart_data_col_names = all_data_colnames[chart.datasource]
                        index = chart_data_col_names.index(datafield.value)
                        
                        data_values = []
                        for data in chart_data:
                            col_value = data[index]
                            data_values.append(col_value)

                        chart.data_values = data_values
                    elif(datafield_type == 'StringValues'):
                        data_values = []
                        for string_value in datafield.string_values:
                            data_values.append(string_value.value)
                        
                        chart.data_values = data_values
        elif(chart_attr_type == 'Title'):
            chart.title = chart_attr.title

def create_chart_label_values(label, datasource):
    # Kreiranje distinct vrednosti
    chart_data = all_data[datasource]
    chart_data_col_names = all_data_colnames[datasource]
    index = chart_data_col_names.index(label)

    label_values = []
    for data in chart_data:
        col_value = data[index]

        if col_value not in label_values:
            label_values.append(col_value)

    return label_values

def count(column, datasource):
    chart_data = all_data[datasource]
    chart_data_col_names = all_data_colnames[datasource]
    index = chart_data_col_names.index(column)

    count_map = {}
    for data in chart_data:
        col_value = data[index] 

        if col_value not in count_map:
            count_map[col_value] = 1
        else:
            count_map[col_value] = count_map[col_value] + 1

    data_values = []
    for key in count_map.keys():
        data_values.append(count_map[key])

    return data_values

def suma(column, chart):
    datasource = chart.datasource

    chart_data = all_data[datasource]
    chart_data_col_names = all_data_colnames[datasource]

    label_index = chart_data_col_names.index(chart.label)
    index = chart_data_col_names.index(column)

    sum_map = {}
    for data in chart_data:
        col_value = data[index]
        label_col_value = data[label_index]

        if label_col_value not in sum_map:
            sum_map[label_col_value] = int(col_value)
        else:
            sum_map[label_col_value] = sum_map[label_col_value] + int(col_value)

    data_values = []
    for key in sum_map.keys():
        data_values.append(sum_map[key])

    return data_values

def parse_line(data):
    template = jinja_env.get_template('horizontal_line.j2')
    output_folder.write(template.render(color=data.color))

def generate_pdf():
    utils_folder = join(dirname(__file__), 'utils')
    config = pdfkit.configuration(wkhtmltopdf=join(utils_folder, 'wkhtmltopdf.exe'))
    options = { 'javascript-delay':'1000' }
    pdfkit.from_file('generated/output.html', 'generated/output.pdf', options=options, configuration=config)

# main fuction
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Error: Document file is missing.')
    else:
        document_file = sys.argv[1]

    model = metamodel.model_from_file(document_file)

    output_folder = open('generated/output.html', 'w', encoding="utf-8")

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
        elif(document_statement.chart != None):
            parse_chart(document_statement.chart)
        elif(document_statement.line != None):
            parse_line(document_statement.line)
        else:
            print("Exception")

    template = jinja_env.get_template('html_footer.j2')
    output_folder.write(template.render(charts=charts))

    con.close()
    output_folder.close()

    generate_pdf()