import pandas as pd
import plotly.express as px

class Analise_Exploratoria:
    def __init__(self, caminho_arquivo: str):
        self.dados = pd.read_csv(caminho_arquivo)

    def exibir_tabela_inicial(self):
        print(self.dados.head())

    def contar_valores_unicos(self, coluna_analisada: str, nome_coluna_contagem: str) -> pd.DataFrame:
        contagem = self.dados[coluna_analisada].value_counts().reset_index()
        contagem.columns = [coluna_analisada, nome_coluna_contagem]
        return contagem

    def gerar_grafico_barras(self, coluna_analisada: str, nome_coluna_contagem: str, titulo_grafico: str, nome_exibido_eixo_x: str, intervalo_y: int = 20):
        dados_agrupados = self.contar_valores_unicos(coluna_analisada, nome_coluna_contagem)
        fig = px.bar(
            dados_agrupados,
            x=coluna_analisada,
            y=nome_coluna_contagem,
            title=titulo_grafico or f"Distribuição por {coluna_analisada}",
            labels={coluna_analisada: nome_exibido_eixo_x, nome_coluna_contagem: nome_coluna_contagem}
        )
        fig.update_yaxes(dtick=intervalo_y, tick0=0, gridcolor="lightgrey")
        fig.show()

    def grafico_coluna_padrao(self, coluna_analisada: str, titulo_grafico: str, nome_coluna_contagem: str, nome_exibido_eixo_x: str):
        self.gerar_grafico_barras(coluna_analisada, nome_coluna_contagem, titulo_grafico, nome_exibido_eixo_x)

if __name__ == "__main__":
    analisador = Analise_Exploratoria("SuperMarket_Analysis.csv")
    analisador.grafico_coluna_padrao("City", "Ocorrências por Cidade", "Quantidade", "Cidade")
    analisador.exibir_tabela_inicial()
