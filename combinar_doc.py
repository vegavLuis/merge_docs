import zipfile
import os
import shutil
import sys
from lxml import etree

def extraer_documento(archivo_docx, temp_folder):
    # Descomprimir el archivo .docx
    with zipfile.ZipFile(archivo_docx, 'r') as docx:
        docx.extractall(temp_folder)

def combinar_documentos(archivo1, archivo2, archivo_salida):
    # Crear directorios temporales
    temp_dir1 = 'temp1'
    temp_dir2 = 'temp2'
    
    # Extraer contenido de los documentos
    extraer_documento(archivo1, temp_dir1)
    extraer_documento(archivo2, temp_dir2)

    # Leer el contenido XML de los dos documentos
    doc1_xml = os.path.join(temp_dir1, 'word', 'document.xml')
    doc2_xml = os.path.join(temp_dir2, 'word', 'document.xml')

    # Parsear los archivos XML con lxml
    tree1 = etree.parse(doc1_xml)
    tree2 = etree.parse(doc2_xml)

    # Combinar el contenido de los dos documentos (por ejemplo, insertando el contenido de document.xml del segundo archivo)
    body1 = tree1.xpath('//w:body', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})[0]
    body2 = tree2.xpath('//w:body', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})[0]

    # Fusionar los cuerpos de ambos documentos
    for element in body2:
        body1.append(element)

    # Guardar el nuevo documento XML combinado
    output_doc_xml = os.path.join(temp_dir1, 'word', 'document.xml')
    tree1.write(output_doc_xml, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    # Crear un nuevo archivo .docx para el resultado
    with zipfile.ZipFile(archivo_salida, 'w') as docx_output:
        # Copiar todos los archivos del primer documento
        for foldername, subfolders, filenames in os.walk(temp_dir1):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, temp_dir1)
                docx_output.write(file_path, arcname)

    # Limpiar los directorios temporales
    shutil.rmtree(temp_dir1)
    shutil.rmtree(temp_dir2)

    print(f"Documentos combinados exitosamente en: {archivo_salida}")

if __name__ == "__main__":
    # Obtener los archivos pasados desde Node.js
    archivo1 = sys.argv[1]
    archivo2 = sys.argv[2]
    archivo_salida = sys.argv[3]
    
    combinar_documentos(archivo1, archivo2, archivo_salida)
