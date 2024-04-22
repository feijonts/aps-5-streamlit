import streamlit as st 
import requests
from datetime import datetime

BASE_URL = 'http://localhost:5000/usuarios'

def buscar_usuario(usuario_id):
    try:
        response = requests.get(f'{BASE_URL}/{usuario_id}')
        return response
    except Exception as e:
        print(e)
        return None
    
def atualizar_usuario(id, nome, cpf, data_nascimento):
    try:
        response = requests.put(f'{BASE_URL}/{id}', json={
            'nome': nome,
            'cpf': cpf,
            'data_nascimento': data_nascimento
        })
        return response
    except Exception as e:
        print(e)
        return None
    
def remover_usuario(id):
    try:
        response = requests.delete(f'{BASE_URL}/{id}')
        return response
    except Exception as e:
        print(e)
        return None
    
def exibir_mensagem():
    if 'mensagem' in st.session_state:
        mensagem = st.session_state.mensagem
        if 'erro' in mensagem:
            st.error(mensagem['erro'])
        elif 'sucesso' in mensagem:
            st.success(mensagem['sucesso'])
        del st.session_state.mensagem

def limpar_estado():
    st.session_state.pop('data', None)
    
def main():
    st.title('Buscar Usuário')
    if 'data' not in st.session_state:
        st.session_state.data = None

    id_usuario = st.text_input('ID do Usuário')
    buscar = st.button('Buscar')

    if buscar and id_usuario and id_usuario != '':
        response = buscar_usuario(id_usuario)
        if response is not None:
            if response.status_code == 200:
                st.session_state.data = response.json()
            else:
                st.session_state.mensagem = { 'erro': response.json().get('mensagem', 'Erro ao buscar usuário') }
                limpar_estado()
        else:
            st.session_state.mensagem = { 'erro': 'Erro interno ao buscar usuário' }
            limpar_estado()

    exibir_mensagem()

    if 'data' in st.session_state and st.session_state.data:
        data = st.session_state.data
        nome = st.text_input('Nome', value=data.get('nome', ''))
        cpf = st.text_input('CPF', value=data.get('cpf', ''))
        data_nascimento = datetime.strptime(data.get('data_nascimento', ''), '%Y-%m-%d')
        min_date = datetime(1900, 1, 1)
        max_date = datetime.now()
        data_nascimento = st.date_input('Data de Nascimento', value=data_nascimento, min_value=min_date, max_value=max_date, format='DD/MM/YYYY')

        atualizar = st.button('Atualizar Usuário')
        remover = st.button('Remover Usuário')

        if atualizar and nome and cpf and data_nascimento:
            if nome != data.get('nome') or cpf != data.get('cpf') or data_nascimento != data.get('data_nascimento'):
                data_nascimento = str(data_nascimento)
                response = atualizar_usuario(data['_id'], nome, cpf, data_nascimento)
                if response is not None:
                    if response.status_code == 200:
                        st.session_state.mensagem = { 'sucesso': 'Usuário atualizado com sucesso!' }
                    else:
                        st.session_state.mensagem = { 'erro': response.json().get('mensagem', 'Erro ao atualizar usuário') }
                else:
                    st.session_state.mensagem = { 'erro': 'Erro interno ao atualizar usuário' }
                limpar_estado()
                st.rerun()
    
        if remover:
            response = remover_usuario(data['_id'])
            if response is not None:
                if response.status_code == 204:
                    st.session_state.mensagem = { 'sucesso': 'Usuário removido com sucesso!' }
                else:
                    st.session_state.mensagem = { 'erro': response.json().get('mensagem', 'Erro ao remover usuário') }
            else:
                st.session_state.mensagem = { 'erro': 'Erro interno ao remover usuário' }
            limpar_estado()
            st.rerun()

if __name__ == '__main__':
    main()