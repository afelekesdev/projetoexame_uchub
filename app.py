import os
import tempfile
import streamlit as st
from servicos_ia import AnalisadorExame
from schemas import RelatorioExame

st.set_page_config(
    page_title="Analisador de Exames | UC HUB", 
    page_icon="⚕️", 
    layout="wide",
    initial_sidebar_state="expanded"
    )

# css para melhorar a aparencia da aplicação
st.markdown(
   """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
        max-width: 1180px;
    }

    /* Cabeçalho moderno, minimalista e adaptativo ao tema */
    .header-box {
        background-color: var(--secondary-background-color);
        padding: 1.75rem 2rem;
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-top: 3px solid #0D9488;
        margin-bottom: 1.75rem;
    }
    .header-kicker {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        color: #0D9488;
        margin-bottom: 0.4rem;
    }
    .header-title {
        color: var(--text-color);
        font-size: 1.7rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin: 0;
    }
    .header-subtitle {
        color: var(--text-color);
        opacity: 0.8;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-top: 0.45rem;
    }
    .header-meta {
        margin-top: 1rem;
        padding-top: 0.75rem;
        border-top: 1px solid rgba(148, 163, 184, 0.18);
        font-size: 0.78rem;
        color: var(--text-color);
        opacity: 0.68;
    }

    /* Cards dos biomarcadores adaptativos e sem bordas grossas */
    .marker-card {
        background-color: var(--secondary-background-color);
        padding: 1.25rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 0.9rem;
        border: 1px solid rgba(148, 163, 184, 0.22);
        transition: border-color 0.2s ease;
    }
    .marker-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--text-color);
    }
    .marker-values {
        margin-top: 0.45rem;
        font-size: 0.88rem;
        color: var(--text-color);
        opacity: 0.82;
    }
    .marker-desc {
        margin-top: 0.75rem;
        margin-bottom: 0;
        color: var(--text-color);
        opacity: 0.92;
        line-height: 1.55;
        font-size: 0.94rem;
    }

    /* Badges translúcidos que funcionam no Claro e no Escuro */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.22rem 0.7rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .badge-normal {
        background-color: rgba(16, 185, 129, 0.14);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .badge-atencao {
        background-color: rgba(245, 158, 11, 0.14);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .badge-alterado {
        background-color: rgba(239, 68, 68, 0.14);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    /* Botão principal em Teal Clínico */
    .stButton > button[kind="primary"] {
        background-color: #0D9488;
        border-color: #0D9488;
        color: #FFFFFF;
        font-weight: 600;
        border-radius: 8px;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #0F766E;
        border-color: #0F766E;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_resource
def obter_analisador() -> AnalisadorExame:
    return AnalisadorExame()

def formatar_relatorio_texto(relatorio: RelatorioExame) -> str:
    linhas = [
        "RELATÓRIO EDUCATIVO DE EXAME LABORATORIAL - UC HUB",
        "=" * 52,
        f"\nRESUMO GERAL:\n{relatorio.resumo_acolhedor}\n",
        "MARCADORES AVALIADOS:",
    ]
    for m in relatorio.marcadores:
        linhas.append(
            f"- {m.nome} [{m.status.upper()}]: {m.valor_encontrado} (Ref: {m.referencia})\n"
            f"  Explicação: {m.explicacao_simples}"
        )
    linhas.append("\nPERGUNTAS SUGERIDAS PARA A CONSULTA MÉDICA:")
    for p in relatorio.perguntas_medico:
        linhas.append(f"- {p}")
    linhas.append(f"\nAVISO LEGAL:\n{relatorio.aviso_legal}")
    return "\n".join(linhas)

# Barra Lateral Institucional
with st.sidebar:
    st.markdown("### ⚕️ UC HUB Saúde")
    st.caption("Plataforma de Apoio ao Letramento Clínico")
    st.divider()
    st.markdown("**Como funciona:**")
    st.markdown(
        "1. Envie o laudo em PDF ou imagem nítida.\n"
        "2. O sistema extrai os biomarcadores e compara com as referências.\n"
        "3. Receba uma tradução acessível para preparar sua consulta."
    )
    st.divider()
    st.markdown("**Privacidade e Ética (LGPD):**")
    st.caption(
        "Os documentos enviados são processados em memória temporária e excluídos "
        "imediatamente após a geração do relatório. Esta ferramenta possui caráter "
        "exclusivamente educativo e não realiza diagnósticos."
    )

    # Cabeçalho Principal
st.markdown(
"""
    <div class="header-box">
        <div class="header-kicker">UC HUB &bull; Módulo de Letramento Clínico e Apoio ao Paciente</div>
        <div class="header-title">Interpretação Estruturada de Exames Laboratoriais</div>
        <div class="header-subtitle">
            Processamento automatizado de biomarcadores para decodificação de termos técnicos, contextualização de faixas de referência e preparo para consulta médica.
        </div>
        <div class="header-meta">
            <strong>Caráter Exclusivamente Educativo</strong> &nbsp;|&nbsp; Sem finalidade diagnóstica &nbsp;|&nbsp; Processamento temporário em conformidade com a LGPD
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Layout Principal em Duas Colunas
col_upload, col_resultado = st.columns([1, 2], gap="large")

with col_upload:
    with st.container(border=True):
        st.subheader("Documento Clínico")
        arquivo_upload = st.file_uploader(
            "Formatos aceitos: PDF, JPG, JPEG ou PNG",
            type=["pdf", "jpg", "jpeg", "png"],
        )

        if arquivo_upload is not None:
            if arquivo_upload.type.startswith("image/"):
                st.image(arquivo_upload, caption="Pré-visualização do laudo", use_container_width=True)
            else:
                st.info(f"Arquivo PDF carregado: **{arquivo_upload.name}**")

            analisar_clicado = st.button("Processar Laudo", type="primary", use_container_width=True)
        else:
            analisar_clicado = False

with col_resultado:
    if arquivo_upload is not None and analisar_clicado:
        extensao = os.path.splitext(arquivo_upload.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=extensao) as temp_file:
            temp_file.write(arquivo_upload.getbuffer())
            caminho_temp = temp_file.name

        try:
            with st.spinner("Processando biomarcadores e estruturando relatório..."):
                analisador = obter_analisador()
                relatorio = analisador.analisar(caminho_temp)
                st.session_state["relatorio_atual"] = relatorio
        except Exception as erro:
            st.error(f"Falha no processamento do documento: {erro}")
        finally:
            if os.path.exists(caminho_temp):
                os.remove(caminho_temp)

    if "relatorio_atual" in st.session_state:
        relatorio: RelatorioExame = st.session_state["relatorio_atual"]

        # Indicadores Numéricos (KPIs do Exame)
        total = len(relatorio.marcadores)
        qtd_normal = sum(1 for m in relatorio.marcadores if m.status == "Normal")
        qtd_atencao = sum(1 for m in relatorio.marcadores if m.status == "Atencao")
        qtd_alterado = sum(1 for m in relatorio.marcadores if m.status == "Alterado")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Avaliado", total)
        m2.metric("Normal", qtd_normal)
        m3.metric("Atenção", qtd_atencao)
        m4.metric("Alterado", qtd_alterado)

        st.markdown("")
        with st.container(border=True):
            st.markdown("**Síntese Clínica ao Paciente**")
            st.write(relatorio.resumo_acolhedor)

        aba_marcadores, aba_consulta, aba_exportar = st.tabs(
            ["Biomarcadores", "Preparação para Consulta", "Exportar Relatório"]
        )

        cores_borda = {
            "Normal": "#16A34A",
            "Atencao": "#D97706",
            "Alterado": "#DC2626",
        }
        classes_badge = {
            "Normal": "badge-normal",
            "Atencao": "badge-atencao",
            "Alterado": "badge-alterado",
        }

        with aba_marcadores:
            for m in relatorio.marcadores:
                badge_cls = classes_badge.get(m.status, "badge-normal")
                st.markdown(
                    f"""
                    <div class="marker-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span class="marker-title">{m.nome}</span>
                            <span class="badge {badge_cls}">{m.status}</span>
                        </div>
                        <div class="marker-values">
                            <strong>Resultado:</strong> <code>{m.valor_encontrado}</code> &nbsp;&bull;&nbsp;
                            <strong>Referência:</strong> {m.referencia}
                        </div>
                        <p class="marker-desc">{m.explicacao_simples}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                with aba_consulta:
                    with st.container(border=True):
                        st.markdown("**Perguntas Sugeridas ao Médico**")
                        for pergunta in relatorio.perguntas_medico:
                            st.markdown(f"- {pergunta}")

                with aba_exportar:
                    texto_exportacao = formatar_relatorio_texto(relatorio)
                    st.download_button(
                        label="Baixar Relatório Completo (.txt)",
                        data=texto_exportacao,
                        file_name="relatorio_exame_uchub.txt",
                        mime="text/plain",
                        use_container_width=True,
                    )
                    st.text_area("Pré-visualização do arquivo de texto:", texto_exportacao, height=250)

                st.caption(relatorio.aviso_legal)
            else:
                with st.container(border=True):
                    st.markdown("#### Aguardando envio do documento")
                    st.write(
                        "Selecione um exame laboratorial no painel ao lado e clique em **Processar Laudo** "
                        "para visualizar os indicadores clínicos e a análise educativa."
                    )