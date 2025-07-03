import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.graph_objs import Figure
from typing import List, Optional, Dict
import logging

class Analise_Exploratoria_marketplace:
    def __init__(self, arquivo_csv: str):
        try:
            self.df = pd.read_csv(arquivo_csv)
            logging.info("Arquivo CSV carregado com sucesso!")
        except FileNotFoundError:
            print("Arquivo CSV não encontrado")
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
        contagem = self.df.groupby(colunas_analisadas[0])[colunas_analisadas[1]].sum().reset_index()
        return contagem

    def __gerar_grafico_barras(self, df: pd.DataFrame, coluna_categoria: str, coluna_valor: str, titulo: str) -> Figure:
        fig = px.bar(
            df,
            x=coluna_categoria,
            y=coluna_valor,
            title=titulo,
            labels={coluna_categoria: coluna_categoria, coluna_valor: "Total"},
            color_discrete_sequence=["#636EFA"]
        )
        fig.update_yaxes(dtick=20, gridcolor="lightgrey")
        fig.update_layout(xaxis_tickangle=-45)
        return fig

    def __gerar_grafico_pizza(self, df: pd.DataFrame, coluna_categoria: str, coluna_valor: str, titulo: str) -> Figure:
        fig = px.pie(
            df,
            names=coluna_categoria,
            values=coluna_valor,
            title=titulo
        )
        return fig

    def gerar_painel_multigraficos(
        self,
        titulo_geral: str,
        colunas: Optional[List[str]] = None,
        dataframes: Optional[Dict[str, pd.DataFrame]] = None
    ) -> None:
        if not colunas and not dataframes:
            raise ValueError("Você deve fornecer pelo menos 'colunas' ou 'dataframes'.")

        total_colunas = len(colunas) if colunas else 0
        total_dataframes = len(dataframes) if dataframes else 0
        total_linhas = total_colunas + total_dataframes

        figura = make_subplots(
            rows=total_linhas,
            cols=2,
            subplot_titles=[
                f"{titulo} - Barras" if i % 2 == 0 else f"{titulo} - Pizza"
                for titulo in (colunas if colunas else []) + (list(dataframes.keys()) if dataframes else [])
                for i in range(2)
            ],
            specs=[[{"type": "xy"}, {"type": "domain"}] for _ in range(total_linhas)],
            vertical_spacing=0.15
        )

        linha_atual = 1

        if colunas:
            for coluna in colunas:
                df_agrupado = self.__contar_dados_coluna(coluna, "Quantidade")
                fig_barra = self.__gerar_grafico_barras(df_agrupado, coluna, "Quantidade", f"Distribuição por {coluna}")
                fig_pizza = self.__gerar_grafico_pizza(df_agrupado, coluna, "Quantidade", f"{coluna} - Pizza")

                for trace in fig_barra.data:
                    figura.add_trace(trace, row=linha_atual, col=1)
                for trace in fig_pizza.data:
                    figura.add_trace(trace, row=linha_atual, col=2)

                linha_atual += 1

        if dataframes:
            for titulo, df_custom in dataframes.items():
                colunas_df = df_custom.columns.tolist()
                if len(colunas_df) != 2:
                    raise ValueError(f"O DataFrame '{titulo}' deve conter exatamente duas colunas.")
                nome_categoria, nome_valor = colunas_df

                fig_barra = self.__gerar_grafico_barras(df_custom, nome_categoria, nome_valor, f"Distribuição por {titulo}")
                fig_pizza = self.__gerar_grafico_pizza(df_custom, nome_categoria, nome_valor, f"{titulo} - Pizza")

                for trace in fig_barra.data:
                    figura.add_trace(trace, row=linha_atual, col=1)
                for trace in fig_pizza.data:
                    figura.add_trace(trace, row=linha_atual, col=2)

                linha_atual += 1

        figura.update_layout(
            height= 1000 * total_linhas,
            title_text=titulo_geral,
            showlegend=False
        )

        figura.show()
        figura.write_html("outputs/painel_exploratorio.html")
        figura.write_image("outputs/painel_exploratorio.pdf", format="pdf")
        print("Painel gerado com sucesso!")
