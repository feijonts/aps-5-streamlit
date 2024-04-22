import streamlit as st
import requests

BASE_URL = 'http://localhost:5000/bikes'
dados = {
    'ID': [],
    'Marca': [],
    'Modelo': [],
    'Cidade': [],
    'Status': []
}

def buscar_bikes():
    try:
        response = requests.get(f'{BASE_URL}')
        return response
    except Exception as e:
        print(e)
        return None
    
def main():
    st.title('Bicicletas')
    response = buscar_bikes()
    if response is not None:
        if response.status_code == 200:
            data = response.json()
            if len(data) <= 0:
                st.warning('Nenhuma bicicleta encontrada')
            else:
                for bike in data:
                    dados['ID'].append(bike['_id'])
                    dados['Marca'].append(bike['marca'])
                    dados['Modelo'].append(bike['modelo'])
                    dados['Cidade'].append(bike['cidade'])
                    dados['Status'].append(bike['status'])
                st.table(dados)
        else:
            st.error('Erro ao buscar bicicletas')
    else:
        st.error('Erro ao buscar bicicletas')

if __name__ == '__main__':
    main()