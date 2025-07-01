import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

class Analise_Exploratoria:
    def __init__(self, caminho_arquivo: str):
        self.df = pd.read_csv(caminho_arquivo)

    def grafico_coluna_padrao(self, coluna_analisada: str, titulo_grafico: str, nome_coluna_contagem: str, nome_exibido_eixo_x: str):
        fig_bar = self.gerar_grafico_barras(coluna_analisada, nome_coluna_contagem, titulo_grafico, nome_exibido_eixo_x)
        fig_pie = self.gerar_grafico_pizza(coluna_analisada, nome_coluna_contagem)

        figura = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Gráfico de Barras", "Gráfico de Pizza"),
            specs=[[{"type": "xy"}, {"type": "domain"}]]
        )

        for trace in fig_bar.data:
            figura.add_trace(trace, row=1, col=1)
        for trace in fig_pie.data:
            figura.add_trace(trace, row=1, col=2)

        figura.update_layout(title_text=titulo_grafico, showlegend=False)
        figura.show()

    def exibir_tabela_inicial(self):
        print(self.df.head())

    def contar_valores_unicos(self, coluna_analisada: str, nome_coluna_contagem: str) -> pd.DataFrame:
        contagem = self.df[coluna_analisada].value_counts().reset_index()
        contagem.columns = [coluna_analisada, nome_coluna_contagem]
        return contagem

    def gerar_grafico_barras(self, coluna_analisada: str, nome_coluna_contagem: str, titulo_grafico: str, nome_exibido_eixo_x: str, intervalo_y: int = 20):
        df_agrupado = self.contar_valores_unicos(coluna_analisada, nome_coluna_contagem)
        fig = px.bar(
            df_agrupado,
            x=coluna_analisada,
            y=nome_coluna_contagem,
            title=titulo_grafico or f"Distribuição por {coluna_analisada}",
            labels={coluna_analisada: nome_exibido_eixo_x, nome_coluna_contagem: nome_coluna_contagem}
        )
        fig.update_yaxes(dtick=intervalo_y, tick0=0, gridcolor="lightgrey")
        return fig

    def gerar_grafico_pizza(self, coluna_analisada, nome_coluna_contagem):
        df_agrupado = self.contar_valores_unicos(coluna_analisada, nome_coluna_contagem)
        fig = px.pie(df_agrupado, values=nome_coluna_contagem, names=coluna_analisada)
        return fig


if __name__ == "__main__":
    analisador = Analise_Exploratoria("SuperMarket_Analysis.csv")
    analisador.grafico_coluna_padrao("City", "Ocorrências por cidade", "Quantidade", "Cidade")
    analisador.exibir_tabela_inicial()
