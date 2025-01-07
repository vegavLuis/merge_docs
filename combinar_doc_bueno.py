import zipfile
import os
import shutil

def copiar_archivos_como_zip(archivo_origen, archivo_destino):
    # Descomprimir el archivo .docx origen
    with zipfile.ZipFile(archivo_origen, 'r') as docx_origen:
        # Extraer todos los contenidos del archivo de origen
        docx_origen.extractall('temp_origen')

    # Crear el archivo de destino
    with zipfile.ZipFile(archivo_destino, 'w') as docx_destino:
        # Copiar todos los archivos del archivo de origen al archivo de destino
        for foldername, subfolders, filenames in os.walk('temp_origen'):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                # Especificar la ruta de archivo dentro del zip
                arcname = os.path.relpath(file_path, 'temp_origen')
                docx_destino.write(file_path, arcname)
        
    # Limpiar el directorio temporal
    shutil.rmtree('temp_origen')

def combinar_documentos(archivo1, archivo2, archivo_salida):
    # Crear un nuevo archivo .docx vacío para la salida
    with open(archivo_salida, 'w') as f:
        pass  # Solo crear el archivo vacío

    # Copiar el contenido del primer archivo
    copiar_archivos_como_zip(archivo1, archivo_salida)
    
    # Copiar el contenido del segundo archivo
    copiar_archivos_como_zip(archivo2, archivo_salida)

    print(f"Documentos combinados exitosamente en: {archivo_salida}")

if __name__ == "__main__":
    archivo1 = "archivo1.docx"
    archivo2 = "archivo2.docx"
    archivo_salida = "documento_combinado.docx"
    
    combinar_documentos(archivo1, archivo2, archivo_salida)
