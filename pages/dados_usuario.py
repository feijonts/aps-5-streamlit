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
    
def main():
    st.title('Dados do Usuário')
    id_usuario = st.text_input('ID do Usuário')
    buscar = st.button('Buscar Usuário')

    if buscar:
        if id_usuario and id_usuario != '':
            if 'data' in st.session_state:
                del st.session_state.data

            try:
                response = buscar_usuario(id_usuario)
                if not response is None:
                    data = response.json()
                    if response.status_code == 200:
                        data = data['usuario']
                        st.session_state.data = data
                    else:
                        st.session_state.mensagem = { 'erro': data.get('mensagem', 'Erro ao buscar usuário') }
                else:
                    st.session_state.mensagem = { 'erro': 'Erro interno ao buscar usuário' }
            except Exception as e:
                print(e)
                st.session_state.mensagem = { 'erro': 'Erro interno ao buscar usuário' }

    if 'data' in st.session_state:
        data = st.session_state.data
        nome = st.text_input('Nome', value=data.get('nome', ''))
        cpf = st.text_input('CPF', value=data.get('cpf', ''))
        data_nascimento = datetime.strptime(data.get('data_nascimento', ''), '%Y-%m-%d')
        min_date = datetime(1900, 1, 1)
        max_date = datetime.now()
        data_nascimento = st.date_input('Data de Nascimento', value=data_nascimento, min_value=min_date, max_value=max_date, format='DD/MM/YYYY')
        atualizar = st.button('Atualizar Usuário')
        remover = st.button('Remover Usuário')

        if atualizar:
            data_nascimento = str(data_nascimento)
            if nome and nome != '' and cpf and cpf != '' and data_nascimento and data_nascimento != '':
                try:
                    response = atualizar_usuario(id_usuario, nome, cpf, data_nascimento)
                    if response is not None:
                        if response.status_code == 200:
                            st.session_state.mensagem = { 'sucesso': 'Usuário atualizado com sucesso!' }
                        else:
                            data = response.json()
                            st.session_state.mensagem = { 'erro': data.get('mensagem', 'Erro ao atualizar usuário') }
                    else:
                        st.session_state.mensagem = { 'erro': 'Erro interno ao atualizar usuário' }
                except Exception as e:
                    print(e)
                    st.session_state.mensagem = { 'erro': 'Erro interno ao atualizar usuário' }

        if remover:
            try:
                response = remover_usuario(id_usuario)
                if response is not None:
                    if response.status_code == 204:
                        st.session_state.mensagem = { 'sucesso': 'Usuário removido com sucesso!' }
                    else:
                        data = response.json()
                        st.session_state.mensagem = { 'erro': data.get('mensagem', 'Erro ao remover usuário') }
                else:
                    st.session_state.mensagem = { 'erro': 'Erro interno ao remover usuário' }
            except Exception as e:
                print(e)
                st.session_state.mensagem = { 'erro': 'Erro interno ao remover usuário' }

    exibir_mensagem()

if __name__ == '__main__':
    main()