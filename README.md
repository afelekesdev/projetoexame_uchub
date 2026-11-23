# ⚕️ UC HUB | Portal de Letramento em Saúde e Análise Educativa de Exames

Plataforma baseada em Inteligência Artificial Generativa e Multimodal desenvolvida para traduzir laudos laboratoriais (PDFs e imagens) em explicações claras, acolhedoras e em linguagem acessível, fortalecendo a autonomia do paciente e o diálogo durante a consulta médica.

---

## 🎯 Problema e Proposta de Valor

Laudos laboratoriais frequentemente utilizam terminologias técnicas e faixas de referência complexas que geram ansiedade ou dificultam a compreensão do paciente antes da consulta médica.

Esta aplicação atua como uma **ferramenta de apoio ao letramento em saúde**, extraindo automaticamente os biomarcadores do documento enviado, comparando-os com os valores de referência do próprio laudo e apresentando analogias do dia a dia, orientações gerais de bem-estar e sugestões de perguntas para o médico.

> **Aviso Ético (Guardrail Clínico):** Esta ferramenta possui caráter exclusivamente educativo e informativo. Ela **não realiza diagnósticos médicos**, não prescreve medicamentos ou tratamentos e não substitui a avaliação de um profissional de saúde qualificado.

---

## 🏗️ Arquitetura do Projeto

O sistema foi projetado seguindo o princípio de **Separação de Responsabilidades** e **Programação Orientada a Objetos (POO)**:

```text
projetoexame_uchub/
├── schemas.py         # Contratos de dados e validação estrita via Pydantic
├── servico_ia.py      # Camada de serviço (POO) com integração Google GenAI e fallback de modelos
├── app.py             # Interface web interativa desenvolvida em Streamlit
├── main.py            # Script de entrada para testes rápidos via linha de comando (CLI)
├── requirements.txt   # Dependências do ambiente Python
└── .gitignore         # Proteção contra versionamento de chaves, venv e exames locais
```

### Destaques Técnicos

* **Saída Estruturada Garantida (`schemas.py`):** Utilização do Pydantic (`BaseModel`, `Field` e `Literal`) para forçar a resposta da IA a seguir um contrato JSON rígido, categorizando cada marcador exatamente em `Normal`, `Atencao` ou `Alterado`.
* **Resiliência e Disponibilidade (`servico_ia.py`):** A classe `AnalisadorExames` implementa um mecanismo de *fallback* dinâmico entre modelos da família Gemini/Gemma, contornando instabilidades ou picos de tráfego (`503 UNAVAILABLE`) de forma transparente.
* **Privacidade e Conformidade com a LGPD:** Os arquivos enviados pelo usuário são armazenados apenas em memória temporária durante o processamento e removidos imediatamente (tanto do disco local quanto dos servidores da API via `client.files.delete`) dentro de blocos `finally:`.
* **Interface Clínica Formal (`app.py`):** Desenvolvida em Streamlit com estilização CSS customizada, exibição de KPIs clínicos, cards de status por severidade, pré-visualização do documento e exportação do relatório em `.txt` para levar à consulta.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Inteligência Artificial:** Google GenAI SDK (`google-genai`)
* **Validação de Dados:** Pydantic
* **Interface Web:** Streamlit
* **Gerenciamento de Ambiente:** `python-dotenv`

---

## 🚀 Como Executar Localmente

### 1. Clonar o repositório
```bash
git clone [https://github.com/afelekesdev/projetoexame_uchub.git](https://github.com/afelekesdev/projetoexame_uchub.git)
cd projetoexame_uchub
```

### 2. Criar e ativar o ambiente virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar a chave da API
Crie um arquivo `.env` na raiz do projeto e adicione sua chave da Google AI Studio:

```env
GEMINI_API_KEY=sua_chave_api_aqui
```

### 5. Executar a aplicação web
```bash
streamlit run app.py
```

A interface será aberta automaticamente no navegador em `http://localhost:8501`.

---

## 👤 Autor

Desenvolvido por **Alan de Lima Félix** ([@afelekesdev](https://github.com/afelekesdev)) como parte do projeto **UC HUB**.