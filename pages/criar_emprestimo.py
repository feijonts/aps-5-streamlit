import streamlit as st 
import requests

BASE_URL = 'https://aps-5-7418c433bf87.herokuapp.com/emprestimos'

def criar_emprestimo(id_usuario, id_bike, data_inicio):
    try:
        response = requests.post(BASE_URL, json={
            'id_usuario': id_usuario,
            'id_bike': id_bike,
            'data_inicio': data_inicio
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
    st.title('Criar Emprestimo')
    id_usuario = st.text_input('ID Usuário')
    id_bike = st.text_input('ID Bicicleta')
    data_inicio = st.date_input('Data de Início')
    criar = st.button('Criar')

    if criar:
        data_inicio = str(data_inicio)
        if id_usuario != '' and id_bike != '' and data_inicio != '':
            response = criar_emprestimo(id_usuario, id_bike, data_inicio)
            if response is not None:
                if response.status_code == 201:
                    st.session_state.mensagem = { 'sucesso': 'Emprestimo criado com sucesso' }
                else:
                    data = response.json()
                    st.session_state.mensagem = { 'erro': data.get('mensagem', 'Erro ao criar emprestimo') }
            else:
                st.session_state.mensagem = { 'erro': 'Erro interno ao criar emprestimo' }

    exibir_mensagem()
            

if __name__ == '__main__':
    main()