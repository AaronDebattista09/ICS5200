import shutil
import xml.etree.ElementTree as ET
import os
import re

from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


class XMLFileObject(object):
    source_folder = None
    originals_folder = None

    def __init__(self, file_xml, source_folder, originals_folder):
        self.source_folder = source_folder
        self.originals_folder = originals_folder

        self.content_hash = file_xml.find('contenthash').text
        self.context_id = file_xml.find('contextid').text
        self.component = file_xml.find('component').text
        self.file_area = file_xml.find('filearea').text
        self.item_id = file_xml.find('itemid').text
        self.file_path = file_xml.find('filepath').text
        self.file_name = file_xml.find('filename').text
        self.user_id = file_xml.find('userid').text
        self.file_size = file_xml.find('filesize').text
        self.mime_type = file_xml.find('mimetype').text
        self.status = file_xml.find('status').text
        self.time_created = file_xml.find('timecreated').text
        self.time_modified = file_xml.find('timemodified').text
        self.source = file_xml.find('source').text
        self.author = file_xml.find('author').text
        self.license = file_xml.find('license').text
        self.sort_order = file_xml.find('sortorder').text
        self.repository_type = file_xml.find('repositorytype').text
        self.repository_id = file_xml.find('repositoryid').text
        self.reference = file_xml.find('reference').text
        self.find_source()

    def find_source(self):

        subfolder = self.content_hash[0:2]

        try:
            path = "{0}/{1}".format(self.source_folder, subfolder)
            print("Processing: {0} - ".format(path), end="")

            for source_file in os.listdir(path):

                if source_file == self.content_hash:
                    self.source_file = "{0}/{1}".format(path, source_file)

            print("Folder discovered... {0}".format("Source file identified." if source_file
                                                    else "Source file not identified."))
        except FileNotFoundError:
            print("Folder not found.")

    def recover_original(self):
        try:
            path = "{0}/{1}".format(self.originals_folder, self.source)
            shutil.copy(self.source_file, path)
            print("Copied {0}.. \n\t..into {1}\n".format(self.source_file, path))
        except AttributeError:
            print("Skipping copy (source file attribute is not populated)")


def generate_originals():
    for xml_list_file in ['../QariTalProvi_Batch_2/Mal1030-sem2/files.xml', '../QariTalProvi_Batch_2/Mal1031-sem1/files.xml']:
        print("Processing File: " + xml_list_file)

        tree = ET.parse(xml_list_file)
        root = tree.getroot()

        for file_xml in root.findall("file"):
            obj_file = XMLFileObject(file_xml, xml_list_file.replace('.xml', ''), '../QariTalProvi_Batch_2/Originals')
            obj_file.recover_original()


def _pdf_to_text(filename):
    output_string = StringIO()
    with open(filename, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    output_list = filter(lambda z: z and re.match('^(?=.*[a-zA-Z])', z),
                         " ".join(filter(lambda y: y,
                                         map(lambda x: re.sub(r'\s+', ' ', x).strip(),
                                             output_string.getvalue().split("\n"))
                                         )
                                  ).split(".")
                         )

    output_list = map(lambda x: x.strip() + ".", output_list)

    return list(output_list)


def convert_pdf_files():
    listdir = glob.glob('../QariTalProvi_Batch_2/Training/Vetted/*.pdf')
    no_of_files = len(listdir)
    counter = 0

    for file in listdir:
        counter += 1
        print('Processing ({0}/{1}): {2}'.format(counter, no_of_files, file))
        lines = _pdf_to_text(file)

        with open(file.replace('Vetted', 'Converted').replace('pdf', 'txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

