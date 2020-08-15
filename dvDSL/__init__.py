from os.path import dirname
from textx import generator as gen
from .interpreter import generate

@gen('VisualiseData', 'html+pdf')
def docv_pdf_generator(metamodel, model, output_path, overwrite, debug):
    """Generating pdf and html from document visualisation text"""
    input_file = model._tx_filename
    outuput_dir = output_path if output_path else dirname(input_file)
    generate(model, outuput_dir)