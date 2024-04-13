import streamlit as st 
import requests
from datetime import datetime

BASE_URL = 'http://localhost:5000/bikes'

def buscar_bike(id_bike):
    try:
        response = requests.get(f'{BASE_URL}/{id_bike}')
        return response
    except Exception as e:
        print(e)
        return None
    
def atualizar_bike(id_bike, marca, modelo, cidade, status):
    try:
        response = requests.put(f'{BASE_URL}/{id_bike}', json={
            'marca': marca,
            'modelo': modelo,
            'cidade': cidade,
            'status': status
        })
        return response
    except Exception as e:
        print(e)
        return None
    
def remover_bike(id_bike):
    try:
        response = requests.delete(f'{BASE_URL}/{id_bike}')
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
    st.title('Buscar Bicicleta')
    if 'data' not in st.session_state:
        st.session_state.data = None

    id_bike = st.text_input('ID da Bicicleta')
    buscar = st.button('Buscar')

    if buscar and id_bike and id_bike != '':
        response = buscar_bike(id_bike)
        if response:
            if response.status_code == 200:
                st.session_state.data = response.json()
            else:
                st.session_state.mensagem = { 'erro': response.json().get('mensagem', 'Erro ao buscar bicicleta') }
                limpar_estado()
        else:
            st.session_state.mensagem = { 'erro': 'Erro interno ao buscar bicicleta' }
            limpar_estado()

    exibir_mensagem()

    if 'data' in st.session_state and st.session_state.data:
        data = st.session_state.data
        marca = st.text_input('Marca', value=data.get('marca', ''))
        modelo = st.text_input('Modelo', value=data.get('modelo', ''))
        cidade = st.text_input('Cidade', value=data.get('cidade', ''))
        status = st.selectbox('Status', ['Disponivel', 'Em uso'], index = 0 if data.get('status') == 'disponivel' else 1)

        atualizar = st.button('Atualizar Bicicleta')
        remover = st.button('Remover Bicicleta')

        if atualizar and marca and modelo and cidade and status:
            if marca != data.get('marca') or modelo != data.get('modelo') or cidade != data.get('cidade') or status != data.get('status'):
                status = status.lower()
                response = atualizar_bike(data['_id'], marca, modelo, cidade, status)
                if response:
                    if response.status_code == 200:
                        st.session_state.mensagem = { 'sucesso': 'Bicicleta atualizada com sucesso!' }
                    else:
                        st.session_state.mensagem = { 'erro': response.json().get('mensagem', 'Erro ao atualizar bicicleta') }
                else:
                    st.session_state.mensagem = { 'erro': 'Erro interno ao atualizar bicicleta' }
                limpar_estado()
                st.rerun()
    
        if remover:
            response = remover_bike(data['_id'])
            if response:
                if response.status_code == 204:
                    st.session_state.mensagem = { 'sucesso': 'Bicicleta removida com sucesso!' }
                else:
                    st.session_state.mensagem = { 'erro': response.json().get('mensagem', 'Erro ao remover bicicleta') }
            else:
                st.session_state.mensagem = { 'erro': 'Erro interno ao remover bicicleta' }
            limpar_estado()
            st.rerun()

if __name__ == '__main__':
    main()