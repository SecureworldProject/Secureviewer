#Date
from datetime import datetime

# RSA python
import cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding

import numpy as np
import os
from tkinter import messagebox

#Path RSA key
key_path = os.environ['SECUREMIRROR_CAPTURES']
key=os.listdir(key_path + "/" + "key_priv_RSA")


#Current date of Internet
def current_date():
    try:
        import time, datetime
        import ntplib
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org')
        a=time.localtime(response.tx_time)
        cdate = datetime.datetime(*a[:6])
        return cdate
            
    except:
        messagebox.showinfo(message="No ha sido posible obtener la fecha de hoy compruebe la conexión a Internet", title="No tiene conexión a Internet")

#Formating date
def form_date(date):
    string = str(date,'utf-8')
    formatting = "%d/%m/%Y"
    form_date=datetime.strptime(string, formatting)
    
    return form_date

#loading private_key
def read_keys_from_files(private_key_filename):
    private_key = None
    
    if private_key_filename:
        try:
            with open(private_key_filename, "rb") as file:
                private_key = serialization.load_pem_private_key(
                    file.read(),
                    password=None,
                )
        except Exception as e:
            messagebox.showinfo(message=f"No se pudo cargar la clave privada RSA, revise el archivo de entrada: '{private_key_filename}'", title="Error en clave privada")
            
    else:
        messagebox.showinfo(message=f"La clave privada RSA no está especificada", title="Error en clave privada")
   
    return (private_key)

#XOR Encryption
def xor_int(key_pdf,stream_pdf,ran):    
    result=[np.bitwise_xor(key_pdf,stream_pdf[0])]
    for i in range(1,ran):
        r=np.bitwise_xor(key_pdf,stream_pdf[i])
        result.append(r)
    return result

#convert np_array to list
def conv (stream_pdf_plaintext):
    return bytes(list(stream_pdf_plaintext))

#Opening document
def open_doc(filepath):
    cdate=current_date()
    
    #private_key = read_keys_from_files(private_key_filename=key_path + "/" + key[0])
    private_key = read_keys_from_files(private_key_filename=key_path + "/" + "key_priv_RSA"+ "/" +key[0])

    original_encrypted_text_file= filepath 

    #opening Uva file
    with open(original_encrypted_text_file, "rb") as file:
        

        #skip zero header
        file.seek(512)
        #reading information header 
        original_encrypted_text = file.read(512)
        #skip headers
        file.seek(1024)
        #reading information stream PDF  
        stream_pdf=file.read()
        
        stream_pdf=list(stream_pdf)
        stream_pdf_a=stream_pdf[:len(stream_pdf)-(len(stream_pdf)%8)]
        stream_pdf_a=[stream_pdf_a[i:i+8] for i in range(0, len(stream_pdf_a), 8)]
             
    
        try:
            # Decrypt text
            new_plaintext = private_key.decrypt(
                original_encrypted_text,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA1()),
                    algorithm=hashes.SHA1(),
                    label=None
                )
            )
                        
            #reading validity date PDF
            d_star=form_date(new_plaintext[9:19])
            d_end=form_date(new_plaintext[20:30])
        
            if((cdate>d_star) and (cdate<d_end)):
        
                #reading decrypt key PDF
                key_pdf=list(new_plaintext[1:9])
               
                ran=int(len(stream_pdf)/8)
                stream_pdf_plain=xor_int(key_pdf,stream_pdf_a,ran)
                
                bytestr=list(map(conv,stream_pdf_plain))
                stream_pdf_plaintext=b''.join(bytestr)
                
                #save bytes unencrypt
                size_str_pdf=len(stream_pdf)
                resto_pdf=bytes(stream_pdf[(size_str_pdf-(size_str_pdf%8)):size_str_pdf])

                #pdf bytes stream in plain text 
                src=bytes(stream_pdf_plaintext)+resto_pdf
                return src
        
            else:
              messagebox.showinfo(message="La fecha de hoy no se encuentra dentro del período de validez del documento", title="Fecha fuera del rango de validez")
        except:
            messagebox.showinfo(message="La clave privada del cifrado RSA no se corresponde con el documento selecionado", title="ClaveRSA incorrecta")
            
    
        

        


       