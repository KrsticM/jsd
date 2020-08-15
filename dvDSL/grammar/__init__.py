from os.path import dirname, join
from textx import language, metamodel_from_file

@language("VisualiseData", "*.docv")
def visualiseDataLanguage():
    "Domain Specific Language for data visualisation."
    return metamodel_from_file(join(dirname(__file__), "grammar.tx"))