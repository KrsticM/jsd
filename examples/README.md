# Instructions
1. Create database.ini file in your home folder with PostgreSQL credencials.
```
[postgresql]
host=127.0.0.1
database=jsd
user=*user*
password=*password*
```
2. Run students.py script to add data to database
```
$ python students.py
```
3. Install requirements
```
$ pip install .
```
4. Generate your document
```
$ textx generate --target html+pdf <document_path>
```
5. Genereted files are in the same directory as input file

# Examples

## First example (document.docv)
DSL script which contains a header, horizontal line, image, subheader, normal text, table and piechart. 

### Document example
```
data studenti = "SELECT * FROM studenti"
header H1 blue = "Ocene"
line blue
image = "https://i.imgur.com/vHrSBSi.jpg"
header H2 pink = "Jezici specificni za domen"
text = "Zimski semestar 2019/2020"
table 
[
    datasource studenti
    num-row=4
    title="Tabela 1"
    select = ({{Indeks}}, {{Prezime}}, {{Ime}}, {{Bodovi}}, {{Ocena}},)
]
piechart
[
    title="Pie chart 1"
    datasource studenti
    series-select
    [
        label={{Ocena}}
        value=Count({{Ocena}})
    ]
]
```

### Generated document example
![generated example](document.jpeg)

## Second example (document3.docv)
DSL script which contains a header, horizontal line, normal text and table. 

### Document example
```
data studenti = "SELECT * FROM studenti"
header H1 blue = "Ocene"
line blue
text = "Zimski semestar 2019/2020"
table 
[
    datasource studenti
    num-row=4
    title="Tabela 1"
    select = ({{Indeks}}, {{Prezime}}, {{Ime}}, {{Bodovi}}, {{Ocena}},)
]
```
### Generated document example
![generated example](document3.jpeg)

## Third example (document4.docv)
DSL script which contains a header, horizontal line, subheader, normal text, table and linechart. 

### Document example
```
data studenti = "SELECT * FROM studenti"
header H1 purple = "Ocene"
line purple
header H2 = "Jezici specificni za domen"
text = "Zimski semestar 2019/2020"
table 
[
    datasource studenti
    num-row=4
    title="Tabela 1"
    select = ({{Indeks}}, {{Prezime}}, {{Ime}}, {{Bodovi}}, {{Ocena}},)
]
linechart
[
    title="Pie chart 2"
    datasource studenti
    series-select
    [
        label={{Ocena}}
        value=Sum({{Bodovi}})
    ]
]
```
### Generated document example
![generated example](document4.jpeg)
