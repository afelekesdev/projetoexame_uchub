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