import streamlit as st 
import requests
from datetime import datetime

BASE_URL = 'http://localhost:5000/usuarios'

def criar_usuario(nome, cpf, data_nascimento):
    try:
        response = requests.post(BASE_URL, json={
            'nome': nome,
            'cpf': cpf,
            'data_nascimento': data_nascimento
        })
        return response
    except Exception as e:
        print(e)
        return None

def main():
    st.title('Criar Usuário')
    nome = st.text_input('Nome')
    cpf = st.text_input('CPF')
    min_date = datetime(1900, 1, 1)
    max_date = datetime.now()
    data_nascimento = st.date_input('Data de Nascimento', min_value=min_date, max_value=max_date, format='DD/MM/YYYY')
    criar = st.button('Criar Usuário')

    if criar:
        data_nascimento = str(data_nascimento)
        if nome and nome != '' and cpf and cpf != '' and data_nascimento and data_nascimento != '':
            response = criar_usuario(nome, cpf, data_nascimento)
            if response is not None:
                if response.status_code == 201:
                    st.success('Usuário criado com sucesso!')
                else:
                    data = response.json()
                    st.error(data.get('mensagem', 'Erro ao criar usuário'))
            else:
                st.error('Erro interno ao criar usuário')

if __name__ == '__main__':
    main()