from servicos_ia import AnalisadorExame
def executar_teste():
    analisador = AnalisadorExame()
    print("Analisador de exames incializado com sucesso. Processando exame...")

    relatorio = analisador.analisar("exame_teste.jpg")
    print("Análise concluída. Relatório gerado com sucesso!\n")
    print(relatorio.model_dump_json(indent=2))

    if __name__ == "__main__":
        executar_teste()