# Secureviwer
Programa para visualizar ficheros .uva
# DESCRIPCION  
Secureviwer es un softweare necesario para compartir información confidencial con empresas colaboradoras. Secureviwer tiene como objetivo descifrar ficheros .uva que se comparten con empresas colaboradoras y visualizar su contenido como fichero .pdf con información confidenncial. 

# FUNCIONAMIENTO
secureviwer.py: Este fichero contiene el programa principal de Secureviwer y su diseño.

funciones.py: Contiene las funciones correspondientes a la obtención de información del pdf, como metadatos y páginas.

opendoc.py: Contiene las funciones necesarias para descifrar el .uva y obtener la binary string del pdf. 


# REQUISITOS:
La variable de entorno SECUREMIRROR_CAPTURES debe existir y apuntar al path donde se encuentre una carpeta nombrada "key_priv_RSA" donde se guarde la clave de cifrado RSA. Esta carpeta debe contener un solo archivo correspondiente a la clave privada RSA con extención .pem.

Importante::: Instalar PyMuPDF (Para importar fitz, necesario para cargar el documento)
pip install pymupdf

Instalar tkPDFViwer (Para visualizar el PDF a visualizar)
pip install tkPDFViwer

Instalar reporlab (Para importar canvas, necesario para crear el documento)
pip install reporlab 

Instalar cryptography (Para el cifrado RSA)
pip install cryptography

# LIBRERÍAS: 
- tkinter: Para el diseño y visualización del Secureviwer. https://docs.python.org/3/library/tkinter.html
- ntplib:  Para obtener la fecha en tiempo real de de un servidor externo. https://pypi.org/project/ntplib/
- datetime: Para el trabajo con fechas. https://docs.python.org/3/library/datetime.html
- cryptography: Para el descifrado con algoritmo RSA y clave privada. https://cryptography.io/en/latest/
- numpy: Para cifrado/descifrado XOR  y operaciones con vectores y matrices. https://numpy.org/doc/stable/
- math: Para operaciones matemáticas. https://docs.python.org/3/library/math.html
- fitz: Para el manejo de PDFs. https://pymupdf.readthedocs.io/en/latest/document.html#Document
- os: para crear directorios y listar archivos. https://docs.python.org/es/3.10/library/os.html

# Ejecutable
Para utilizar el .exe de Secureviewer, descargar la carpeta "secureviewer" en https://drive.google.com/drive/folders/1ZiKQD9I2wkyUtpFhv4B3JGp0JNFbr6mf?hl=es
y ejecutarlo desde el directorio
