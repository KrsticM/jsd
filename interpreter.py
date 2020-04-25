from textx import metamodel_from_file

metamodel = metamodel_from_file('grammar.tx')

model = metamodel.model_from_file('document.docv')