import streamlit as streamlit
from azure.storage.blob import BlobServiceClient
import os
import pymssql
import uuid
import json
from dotenv import load_dotenv
load_dotenv()

blobConnectionString = os.getenv('BLOB_CONNECTION_STRING')
blobContainerName = os.getenv('BLOB_CONTAINER_NAME')
blobAccountName = os.getenv('BLOB_ACCOUNT_NAME')

SQL_SERVER = os.getenv('SQL_SERVER')
SQL_DATABASE = os.getenv('SQL_DATABASE')
SQL_USER = os.getenv('SQL_USER')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')

st.title('Cadastro de Produtos')
product_name = st.text_input('Nome do produto')
product_price = st.number_input('Preço do produto', min_value=0.0, format='%.2f')
product_description = st.text_input('Descrição do produto')
product_image = st.file_uploader('Imagem do produto', type=['jpg','png', 'jpeg'])

if st.button('Salvar produto'):
  return_message = 'Produto salvo com sucesso'

st.header('Produtos cadastrados')

if st.button('Listar produtos'):
  return_message = 'Produtos listados com sucesso'