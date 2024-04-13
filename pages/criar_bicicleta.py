import streamlit as st 
import requests

BASE_URL = 'http://localhost:5000/bikes'

def criar_bike(marca, modelo, cidade, status):
    try:
        response = requests.post(BASE_URL, json={
            'marca': marca,
            'modelo': modelo,
            'cidade': cidade,
            'status': status
        })
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
    st.title('Criar Bicicleta')
    marca = st.text_input('Marca')
    modelo = st.text_input('Modelo')
    cidade = st.text_input('Cidade')
    status = st.selectbox('Status', ['Disponível', 'Alugada'], index=0)
    criar = st.button('Criar')

    if criar:
        status = status.lower()
        if marca and marca != '' and modelo and modelo != '' and cidade and cidade != '' and status and status != '':
            response = criar_bike(marca, modelo, cidade, status)
            if response is not None:
                if response.status_code == 201:
                    st.session_state.mensagem = { 'sucesso': 'Bicicleta criada com sucesso' }
                else:
                    data = response.json()
                    st.session_state.mensagem = { 'erro': data.get('mensagem', 'Erro ao criar bicicleta') }
            else:
                st.session_state.mensagem = { 'erro': 'Erro interno ao criar bicicleta' }

    exibir_mensagem()
            

if __name__ == '__main__':
    main()