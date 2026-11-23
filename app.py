import os
import tempfile
import streamlit as st
from servicos_ia import AnalisadorExame
from schemas import RelatorioExame

st.set_page_config(page_title="Analisador de Exames | UC HUB", page_icon="🩺", layout="centered")

@st.cache_resource
def obter_analisador() -> AnalisadorExame:
    return AnalisadorExame()

st.title("🩺 Analisador Inteligente de Exames Laboratoriais")
st.write("Envie seu exame laboratorial em formato de imagem (JPEG, PNG) ou PDF, e receba uma análise detalhada e educativa dos resultados.")

arquivo_upload = st.file_uploader(
    "Selecione o arquivo do seu exame (PDF, JPG ou PNG)",
    type=["pdf", "jpg", "jpeg", "png"]
)

if arquivo_upload is not None:
    if st.button("Analisar Exame"):
        extensao = os.path.splitext(arquivo_upload.name)[1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=extensao) as temp_file:
            temp_file.write(arquivo_upload.getbuffer())
            caminho_temp = temp_file.name

        try:
            with st.spinner("Lendo e traduzindo os seus resultados com segurança..."):
                analisador = obter_analisador()
                relatorio: RelatorioExame = analisador.analisar(caminho_temp)

                #exibir resultados na tela
                st.subheader("Resumo Geral")
                st.info(relatorio.resumo_acolhedor)

                st.subheader("Detalhes dos Marcadores")
                exibidores_status = {
                    "Normal": st.success,
                    "Atencao": st.warning,
                    "Alterado": st.error
                }

                for marcador in relatorio.marcadores:
                    exibir = exibidores_status.get(marcador.status, st.info)
                    exibir(
                       f"**{marcador.nome}** ({marcador.status})  \n"
                    f"**Resultado:** `{marcador.valor_encontrado}` | **Referência:** {marcador.referencia}  \n\n"
                    f"{marcador.explicacao_simples}"
                    )

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Recomendações Gerais")
                    for rec in relatorio.perguntas_medico:
                        st.markdown(f"- {rec}")

                with col2:
                    st.subheader("Perguntas para seu Médico")
                    for pergunta in relatorio.perguntas_medico:
                        st.markdown(f"- {pergunta}")

                st.divider()
                st.subheader(relatorio.aviso_legal)


        except Exception as erro:
            st.error(f"Ocorreu um erro ao processar o exame: {erro}")

        finally:
            if os.path.exists(caminho_temp):
                os.remove(caminho_temp)
                  