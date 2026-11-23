from typing import Literal
from pydantic import BaseModel, Field

class MarcadorExame(BaseModel):
    nome: str = Field(description="Nome do biomarcador do exame")
    valor_encontrado: str = Field(description="Valor encontrado no exame para o biomarcador")
    referencia: str = Field(description="Valor de referência do biomarcador")
    status: Literal["Normal", "Atencao", "Alterado"] = Field(description="Classificação clínica: Normal, Atenção ou Alterado")
    explicacao_simples: str = Field(description="Explicação em linguagem simples sobre o biomarcador e seu significado. Com analogias do dia a dia sempre que possível.")

class RelatorioExame(BaseModel):
    resumo_acolhedor: str = Field(description="Resumo acolhedor do exame, explicando de forma clara e objetiva o que foi encontrado.")
    marcadores: list[MarcadorExame] = Field(description="Lista de marcadores do exame com suas respectivas análises.")
    perguntas_medico: list[str] = Field(description="Sugestões de perguntas que o paciente pode fazer ao médico sobre os resultados do exame.")
    aviso_legal: str = Field(description="Aviso legal reforçando que o relatório não substitui a avaliação médica.")