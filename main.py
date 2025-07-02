import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.graph_objs import Figure
from typing import List
import plotly.io as pio
import logging

class Analise_Exploratoria_marketplace:
    def __init__(self, arquivo_csv: str ):
        try:
            self.df = pd.read_csv(arquivo_csv)
            logging.info("Arquivo csv encontrada com sucesso!")
        except FileNotFoundError:
            print("Arquivo csv não encontrado")
            self.df = pd.DataFrame()
            raise
    
    def exibir_tabela_inicial(self) -> None:
        print(self.df.head())
        print(self.df.describe())
        print(self.df.index)
        print(self.df.columns)
    
    def __contar_dados_coluna(self, coluna_analisada: str, novo_nome_coluna: str) -> pd.DataFrame:
        contagem = self.df[coluna_analisada].value_counts().reset_index()
        contagem.columns = [coluna_analisada, novo_nome_coluna]
        return contagem
    
    def contar_dados_varias_colunas(self, colunas_analisadas: List[str]) -> pd.DataFrame:
        contagem = self.df[colunas_analisadas].value_counts().reset_index()
        return contagem
    
    def __gerar_grafico_barras(self, 
                             coluna_analisada: str, 
                             nome_info_contagem: str, 
                             titulo_grafico: str,
                             nome_exibido_eixo_x: str,
                             intervalo_y: int = 20) -> Figure:
    
        df_agrupado = self.__contar_dados_coluna(coluna_analisada, nome_info_contagem)
        df_agrupado = df_agrupado.sort_values(by=nome_info_contagem, ascending=False)

        fig = px.bar(df_agrupado, 
                     x=coluna_analisada, 
                     y=nome_info_contagem, 
                     title=titulo_grafico, 
                     labels={coluna_analisada: nome_exibido_eixo_x, nome_info_contagem: "Total"},
                     color_discrete_sequence=["#636EFA"])
        
        fig.update_yaxes(dtick=intervalo_y, gridcolor="lightgrey")
        fig.update_layout(xaxis_tickangle=-45)
        return fig
    
    def __gerar_grafico_pizza(self, coluna_analisada: str, nome_info_contagem: str) -> Figure:
        df_agrupado = self.__contar_dados_coluna(coluna_analisada, nome_info_contagem)
        fig = px.pie(df_agrupado, 
                     values=nome_info_contagem,
                     names=coluna_analisada,
                     title="Distribuição percentual")
        return fig
    
    def operacoes_colunas_criar_nova(self, colunas: List[str], operacao: str):
        df_colunas = self.contar_dados_varias_colunas(colunas)

        for col in colunas: 
            if col not in df_colunas.columns:
                raise ValueError(f"A coluna '{col}' não existe no Dataframe")
            
        resultado = df_colunas[colunas[0]]

        for col in colunas[1:]:
            if operacao == "+":
                resultado = resultado + df_colunas[col]
            elif operacao == "-":
                resultado = resultado - df_colunas[col]
            elif operacao == "*":
                resultado = resultado * df_colunas[col]
            elif operacao == "/":
                resultado = resultado / df_colunas[col]
            else:
                raise ValueError("Operação inválida! Use + , - ,* ou /")
            
        nome_nova_coluna = f"resultado_{operacao}_colunas"
        df_colunas[nome_nova_coluna] = resultado

        return resultado
        

    def gerar_painel_multigraficos(self, colunas: List[str], titulo_geral: str) -> None:
        total_linhas = len(colunas)
        figura = make_subplots(
            rows=total_linhas,
            cols=2,
            subplot_titles=[
                f"{colunas[i//2]} - Barras" if i % 2 == 0 else f"{colunas[i//2]} - Pizza"
                for i in range(2 * total_linhas)
            ],
            specs=[[{"type": "xy"}, {"type": "domain"}] for _ in range(total_linhas)],
            vertical_spacing=0.15
        )

        for idx, coluna in enumerate(colunas, start=1):
            if coluna not in self.df.columns:
                print("coluna não encontrada")
                continue

            fig_barra = self.__gerar_grafico_barras(
                coluna_analisada=coluna,
                nome_info_contagem="Quantidade",
                titulo_grafico=f"Distribuição por {coluna}",
                nome_exibido_eixo_x=coluna
            )

            fig_pizza = self.__gerar_grafico_pizza(coluna, nome_info_contagem="Quantidade")

            for trace in fig_barra.data:
                figura.add_trace(trace, row=idx, col=1)
            for trace in fig_pizza.data:
                figura.add_trace(trace, row=idx, col=2)

        figura.update_layout(
            height=400 * total_linhas,
            title_text=titulo_geral,
            showlegend=False
        )

        figura.show()
        figura.write_html("painel_exploratorio.html")
        figura.write_image("painel_exploratotio.pdf", format="pdf")
        print("Painel feito com sucesso")


if __name__ == "__main__":
    analisador = Analise_Exploratoria_marketplace("SuperMarket_Analysis.csv")
    analisador.exibir_tabela_inicial()
    analisador.contar_dados_varias_colunas(["Product line", "Gender", "Quantity"])

    analisador.gerar_painel_multigraficos(
        colunas=["City", "Product line", "Gender", "Payment", "Customer type"],
        titulo_geral="Análise Exploratória"
    )
