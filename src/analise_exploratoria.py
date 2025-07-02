import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.graph_objs import Figure
from typing import List, Optional
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
        contagem = self.df.groupby(colunas_analisadas[0])[colunas_analisadas[1]].sum().reset_index()
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
    
    
    #Apagar caso a não ser útil
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
        

    def gerar_painel_multigraficos(self, titulo_geral: str, colunas: Optional[List[str]] = None, dataframes: Optional[dict] = None) -> None:
        """
        Gera painel de gráficos multiplos (barras + pizza) para colunas selecionadas.
        Parâmetro `dataframes` espera um dict com { nome_coluna: dataframe_agrupado }
        """
        if colunas is None:
            raise ValueError("O parâmetro 'colunas' não pode ser None.")
        total_linhas = len(colunas)
        figura = make_subplots(
            rows=total_linhas,
            cols=2,
            subplot_titles=[
                f"{colunas[i // 2]} - Barras" if i % 2 == 0 else f"{colunas[i // 2]} - Pizza"
                for i in range(2 * total_linhas)
            ],
            specs=[[{"type": "xy"}, {"type": "domain"}] for _ in range(total_linhas)],
            vertical_spacing=0.15
        )

        for idx, coluna in enumerate(colunas, start=1):
            if dataframes and coluna in dataframes:
                df_agrupado = dataframes[coluna]
            else:
                # Usa método interno se o DataFrame não for fornecido
                df_agrupado = self.__contar_dados_coluna(coluna, "Quantidade")

            # Gráfico de barras
            fig_barra = px.bar(df_agrupado,
                            x=coluna,
                            y="Quantidade",
                            title=f"Distribuição por {coluna}",
                            labels={coluna: coluna, "Quantidade": "Total"},
                            color_discrete_sequence=["#636EFA"])
            fig_barra.update_yaxes(dtick=20, gridcolor="lightgrey")
            fig_barra.update_layout(xaxis_tickangle=-45)

            # Gráfico de pizza
            fig_pizza = px.pie(df_agrupado,
                            values="Quantidade",
                            names=coluna,
                            title="Distribuição percentual")

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
        figura.write_html("outputs/painel_exploratorio.html")
        figura.write_image("outputs/painel_exploratorio.pdf", format="pdf")
        print("Painel feito com sucesso")