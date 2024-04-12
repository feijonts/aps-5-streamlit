import streamlit as st
import requests

BASE_URL = 'http://localhost:5000/usuarios'
dados = {
    'ID': [],
    'Nome': [],
    'CPF': [],
    'Data de Nascimento': []
}

def buscar_usuarios():
    try:
        response = requests.get(f'{BASE_URL}')
        return response
    except Exception as e:
        print(e)
        return None
    
def main():
    st.title('Usuários')
    try:
        response = buscar_usuarios()
        if response is not None:
            if response.status_code == 200:
                data = response.json()['usuarios']
                if len(data) <= 0:
                    st.warning('Nenhum usuário encontrado')
                else:
                    for usuario in data:
                        dados['ID'].append(usuario['_id'])
                        dados['Nome'].append(usuario['nome'])
                        dados['CPF'].append(usuario['cpf'])
                        dados['Data de Nascimento'].append(usuario['data_nascimento'])
                    st.table(dados)
            else:
                st.error('Erro ao buscar usuários')
        else:
            st.error('Erro ao buscar usuários')
    except Exception as e:
        print(e)
        st.error('Erro interno ao buscar usuários')

if __name__ == '__main__':
    main()