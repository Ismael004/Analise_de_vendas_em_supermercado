from src.analise_exploratoria import Analise_Exploratoria_marketplace


analisador = Analise_Exploratoria_marketplace("data/SuperMarket_Analysis.csv")
analisador.exibir_tabela_inicial()
analisador.criar_coluna_total_produtos(nome_nova_coluna="Total_Produtos")

analisador.gerar_painel_multigraficos(
    colunas=["City", "Product line", "Gender", "Payment", "Customer type"],
    titulo_geral="Análise Exploratória - Total por Categoria",
    metrica="Total_Produtos",
    salvar_html="outputs/painel_total_produtos.html"
)
