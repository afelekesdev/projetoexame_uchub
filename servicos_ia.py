import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from schemas import RelatorioExame

load_dotenv()

class AnalisadorExame:
    """Serviço responsável por analisar exames laboratoriais utilizando a API Gemini AI da Google com segurança e estruturação."""

    INTRUCOES_SISTEMA = """
    Você é um assistente de letramento em saúde especializado em traduzir exames laboratoriais de forma clara, acolhedora e objetiva.
    Sua tarefa é ler e analisar o exame laboratorial enviado, extrair os marcadores avaliados comparando com os valores de referência do próprio exame e explicar cada um em linguagem simples, de forma que qualquer pessoa leiga consiga entender. Utilize analogias do dia a dia sempre que possível.
    Além disso, classifique o status de cada marcador exatamente como:
    - Normal: quando estiver dentro da faixa de referência.
    - Atencao: quando estiver limítrofe ou levemente fora da faixa.
    - Alterado: quando estiver claramente fora da faixa de referência.
    Guardrail: Não forneça diagnósticos médicos, não substitua a avaliação de um profissional de saúde e não prescreva remédios ou dietas. Sempre reforce que apenas um médico pode avaliar o contexto clínico completo do paciente.
    """

    def __init__(self, modelos: list[str] | None = None):
        if not os.getenv("GEMINI_API_KEY"):
            raise ValueError("A variável de ambiente GEMINI_API_KEY não está definida.")
        
        self.client = genai.Client()
        print("Cliente Gemini AI inicializado com sucesso.")
        self.modelos_disponiveis = modelos or [
            "gemini-3.7-flash",
            "gemini-3.6-flash",
            "gemini-3.1-flash-lite",
            "gemma-4-31b-it"
        ]

    def analisar(self, caminho_arquivo: str) -> 'RelatorioExame':
        if not os.path.isfile(caminho_arquivo):
            raise FileNotFoundError("O arquivo '{}' não foi encontrado.".format(caminho_arquivo))

        arquivo_exame = self.client.files.upload(file=caminho_arquivo)
        ultimo_erro = None

        try:
            for modelo in self.modelos_disponiveis:
                try:
                    response = self.client.models.generate_content(
                        model=modelo,
                        contents=[
                            arquivo_exame,
                            "Analise este exame laboratorial e preencha o relatório educativo."
                        ],
                        config=types.GenerateContentConfig(
                            system_instruction=self.INTRUCOES_SISTEMA,
                            response_mime_type="application/json",
                            response_schema=RelatorioExame,
                            temperature=0.2
                        ),
                    )
                    if isinstance(response.parsed, RelatorioExame):
                        return response.parsed
                except Exception as erro:
                    ultimo_erro = erro
                    continue

            raise RuntimeError(f"Todos os modelos falharam. Último erro: {ultimo_erro}")

        finally:
            if arquivo_exame.name:
                self.client.files.delete(name=arquivo_exame.name)