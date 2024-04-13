import streamlit as st 
import requests
from datetime import datetime

BASE_URL = 'http://localhost:5000/emprestimos'

def buscar_emprestimo(id_emprestimo):
    try:
        response = requests.get(f'{BASE_URL}/{id_emprestimo}')
        return response
    except Exception as e:
        print(e)
        return None
    
def remover_emprestimo(id_emprestimo):
    try:
        response = requests.delete(f'{BASE_URL}/{id_emprestimo}')
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
    st.title('Buscar Emprestimo')
    if 'data' not in st.session_state:
        st.session_state.data = None

    id_emprestimo = st.text_input('ID do Emprestimo')
    buscar = st.button('Buscar')

    if buscar and id_emprestimo and id_emprestimo != '':
        response = buscar_emprestimo(id_emprestimo)
        if response:
            if response.status_code == 200:
                st.session_state.data = response.json()
            else:
                st.session_state.mensagem = { 'erro': response.json().get('mensagem', 'Erro ao buscar emprestimo') }
                limpar_estado()
        else:
            st.session_state.mensagem = { 'erro': 'Erro interno ao buscar emprestimo' }
            limpar_estado()

    exibir_mensagem()

    if 'data' in st.session_state and st.session_state.data:
        data = st.session_state.data
        st.text_input('ID', value=data['_id'], disabled=True)
        st.text_input('ID Usuário', value=data['id_usuario'], disabled=True)
        st.text_input('ID Bicicleta', value=data['id_bike'], disabled=True)
        data_emprestimo = datetime.strptime(data['data_emprestimo'], '%d/%m/%Y').date()
        st.date_input('Data de Empréstimo', value=data_emprestimo, format='DD/MM/YYYY', disabled=True)
        remover = st.button('Remover Emprestimo', type='primary')
    
        if remover:
            response = remover_emprestimo(data['_id'])
            if response:
                if response.status_code == 204:
                    st.session_state.mensagem = { 'sucesso': 'Emprestimo removido com sucesso!' }
                else:
                    st.session_state.mensagem = { 'erro': response.json().get('mensagem', 'Erro ao remover Emprestimo') }
            else:
                st.session_state.mensagem = { 'erro': 'Erro interno ao remover Emprestimo' }
            limpar_estado()
            st.rerun()

if __name__ == '__main__':
    main()