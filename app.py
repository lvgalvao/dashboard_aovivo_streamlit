import io
import pandas as pd
import streamlit as st

def main():
    st.title("Conversor de Arquivos")

    # Escolha da conversão
    opcao = st.selectbox("Escolha a conversão", ["Parquet para CSV", "CSV para Parquet"])
    
    arquivo_carregado = st.file_uploader(f"Carregue seu arquivo {opcao.split()[0]}", type=[opcao.split()[0].lower()])

    if opcao == "CSV para Parquet":
        opcao_2 = st.selectbox("Escolha o delimitador", [";", ","])

    if arquivo_carregado is not None:
        try:
            if opcao == "Parquet para CSV":
                # Ler o arquivo Parquet em um DataFrame do pandas
                df = pd.read_parquet(io.BytesIO(arquivo_carregado.getvalue()))

                # Exibir uma pré-visualização básica
                st.write("Pré-visualização do DataFrame")
                st.dataframe(df.head())  # Exibir as primeiras linhas

                # Converter para CSV
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Baixar CSV",
                    data=csv,
                    file_name="convertido.csv",
                    mime="text/csv"
                )

            elif opcao == "CSV para Parquet":
                # Ler o arquivo CSV em um DataFrame do pandas

                df = pd.read_csv(arquivo_carregado, sep=opcao_2)

                # Exibir uma pré-visualização básica
                st.write("Pré-visualização do DataFrame")
                st.dataframe(df.head())  # Exibir as primeiras linhas

                # Converter para Parquet
                parquet = io.BytesIO()
                df.to_parquet(parquet, index=False)
                st.download_button(
                    label="Baixar Parquet",
                    data=parquet.getvalue(),
                    file_name="convertido.parquet",
                    mime="application/octet-stream"
                )

        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")
    else:
        st.warning(f"Por favor, carregue um arquivo {opcao.split()[0]}.")

if __name__ == "__main__":
    main()