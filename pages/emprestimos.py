import streamlit as st
import requests

BASE_URL = 'http://localhost:5000/emprestimos'
dados = {
    'ID': [],
    'ID Usuário': [],
    'ID Bicicleta': [],
    'Data de Empréstimo': [],
}

def buscar_emprestimos():
    try:
        response = requests.get(f'{BASE_URL}')
        return response
    except Exception as e:
        print(e)
        return None
    
def main():
    st.title('Emprestimos')
    response = buscar_emprestimos()
    if response is not None:
        if response.status_code == 200:
            data = response.json()
            if len(data) <= 0:
                st.warning('Nenhum emprestimo encontrado')
            else:
                for emprestimo in data:
                    dados['ID'].append(emprestimo['_id'])
                    dados['ID Usuário'].append(emprestimo['id_usuario'])
                    dados['ID Bicicleta'].append(emprestimo['id_bike'])
                    dados['Data de Empréstimo'].append(emprestimo['data_emprestimo'])
                st.table(dados)
        else:
            st.error('Erro ao buscar emprestimos')
    else:
        st.error('Erro ao buscar emprestimos')

if __name__ == '__main__':
    main()