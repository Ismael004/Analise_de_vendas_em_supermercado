from src.analise_exploratoria import Analise_Exploratoria_marketplace

if __name__ == "__main__":
    analisador = Analise_Exploratoria_marketplace("data/SuperMarket_Analysis.csv")
    analisador.exibir_tabela_inicial()
    
    df_produto = analisador.contar_dados_varias_colunas(["Product line", "Quantity"])
    df_produto = df_produto.rename(columns={"Quantity": "Quantidade"})


    analisador.gerar_painel_multigraficos(
        colunas=["City", "Product line", "Gender", "Payment", "Customer type"],
        titulo_geral="Análise Exploratória",
        dataframes={
            "Product line": df_produto  # chave correta
        }
    )
