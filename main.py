from src.analise_exploratoria import Analise_Exploratoria_marketplace

if __name__ == "__main__":
    analisador = Analise_Exploratoria_marketplace("data/SuperMarket_Analysis.csv")
    analisador.exibir_tabela_inicial()
    analisador.contar_dados_varias_colunas(["Product line", "Gender", "Quantity"])

    analisador.gerar_painel_multigraficos(
        colunas=["City", "Product line", "Gender", "Payment", "Customer type"],
        titulo_geral="Análise Exploratória"
    )
