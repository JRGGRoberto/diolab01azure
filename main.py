import streamlit as st
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

# formulário de cadastro de produtos
st.title('Cadastro de Produtos')
product_name = st.text_input('Nome do produto')
product_price = st.number_input('Preço do produto', min_value=0.0, format='%.2f')
product_description = st.text_input('Descrição do produto')
product_image = st.file_uploader('Imagem do produto', type=['jpg','png', 'jpeg'])

#Save image on blob storage
def upload_blob(file):
    blob_service_client = BlobServiceClient.from_connection_string(blobConnectionString)
    container_client = blob_service_client.get_container_client(blobContainerName)
    blob_name = str(uuid.uuid4()) + file.name
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(file.read(), overraite=True)
    image_url = f"https://{blobAccountName}.blob.core.windows.net/{blobContainerName}/{blob_name}"
    return image_url

def insert_product(product_name, product_price, product_description, product_image):
  try:
      image_url = upload_blob(product_image)
      conn = pymssql.connect(SQL_SERVER, SQL_USER, SQL_PASSWORD, SQL_DATABASE)
      cursor = conn.cursor()
      cursor.execute("INSERT INTO Products (nome, descricao,  preco, imagem_url) VALUES (%s, %s, %s, %s)", ('{product_name}', {product_price}, '{product_description}', '{product_image}'))
      conn.commit()
      conn.close()
      return True
  except Exception as e:
      st.error(f"Erro ao inserir produto: {e}")
      return False
  

if st.button('Salvar produto'):
  insert_product(product_name, product_price, product_description, product_image)
  return_message = 'Produto salvo com sucesso'

st.header('Produtos cadastrados')

if st.button('Listar produtos'):
  return_message = 'Produtos listados com sucesso'
