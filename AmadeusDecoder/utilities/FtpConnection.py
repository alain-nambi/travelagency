import ftplib
import os
from io import BytesIO
from cryptography.fernet import Fernet
import requests

from AmadeusDecoder.utilities.ProductImportParser import ProductParser

key = b'0TWo1KInmeAbdcTf-RaelDAFwGtZfK47tbHOfdgGqRw='

def decrypt_text(text):
    fernet = Fernet(key)
    text_decrypt = fernet.decrypt(text).decode()
    return text_decrypt

def connect():
    username = b'gAAAAABjakVlrbIOLh-YhxnpByNZEUH9AwJD_1goQqxCm5O_YKCAsfGVyenSJZTlRnxJ4EF4CExj-c6oS-Tm7mJ3t8AgpvZwgA=='
    password = 'MGbi@261**'
    hostname = '5.135.136.201'
    port = 22
    ftp_server = ftplib.FTP()
    ftp_server.connect(hostname, 22)
    ftp_server.login(decrypt_text(username), password)

    return ftp_server

def upload_file(file, des_path, des_file):
    session = connect()
    session.cwd(des_path)
    with open(file, 'rb') as f:
        session.storbinary('STOR {}'.format(des_file), f)

    # Call Odoo import
    print("------------------Call Odoo import-----------------------")
    response = requests.get("http://5.135.136.201:8075/web/syncorders")
    print(response.content)

    session.quit()

    

def download_file(ftp_dir):
    session = connect()
    session.encoding = 'utf-8'
    session.cwd(ftp_dir)
    contents = session.nlst()
    for file in contents:
        if file != 'logs' and file != 'imported':
            byte = BytesIO()
            session.retrbinary('RETR {}'.format(file), byte.write)
            byte.seek(0)
            ProductParser.import_product(byte)
            session.rename('{}/{}'.format(ftp_dir, file), '{}/imported/{}'.format(ftp_dir, file))

