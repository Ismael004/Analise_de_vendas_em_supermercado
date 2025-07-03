from src.analise_exploratoria import Analise_Exploratoria_marketplace

if __name__ == "__main__":
    analisador = Analise_Exploratoria_marketplace("data/SuperMarket_Analysis.csv")
    analisador.exibir_tabela_inicial()

    # Agregações por linha de produto
    df_quantidade = analisador.contar_dados_varias_colunas(["Product line", "Quantity"])
    df_quantidade.rename(columns={"Quantity": "Quantidade"}, inplace=True)

    df_cidades = analisador.contar_dados_varias_colunas

    df_vendas = analisador.contar_dados_varias_colunas(["Product line", "Sales"])
    df_vendas.rename(columns={"Sales": "Quantidade"}, inplace=True)

    # Chaves únicas para o painel
    dataframes_personalizados = {
        "Product line - Quantidade": df_quantidade,
        "Product line - Vendas": df_vendas
    }

    analisador.gerar_painel_multigraficos(
        titulo_geral="Análise Exploratória - Supermercado",
        colunas=["City", "Gender", "Payment", "Customer type"],
        dataframes=dataframes_personalizados
    )
