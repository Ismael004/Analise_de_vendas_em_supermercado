import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from typing import List
import logging

class Analise_Exploratoria_marketplace:
    def __init__(self, arquivo_csv: str):
        try:
            self.df = pd.read_csv(arquivo_csv)
            self.df.columns = self.df.columns.str.strip()  # remove espaços nos nomes
            logging.info("Arquivo CSV carregado com sucesso!")
        except FileNotFoundError:
            print("Arquivo CSV não encontrado.")
            self.df = pd.DataFrame()
            raise

    def exibir_tabela_inicial(self) -> None:
        print("\n🟦 Primeiras linhas do DataFrame:")
        print(self.df.head())
        print("\n📊 Descrição estatística:")
        print(self.df.describe())
        print("\n📁 Colunas disponíveis:")
        print(self.df.columns)

    def criar_coluna_total_produtos(self, nome_nova_coluna: str = "Total_Produtos") -> None:
        if "Quantity" not in self.df.columns or "Unit price" not in self.df.columns:
            raise KeyError("As colunas 'Quantity' e 'Unit price' devem existir.")
        self.df[nome_nova_coluna] = self.df["Quantity"] * self.df["Unit price"]
        print(f"\n✅ Coluna '{nome_nova_coluna}' criada com sucesso!")

    def gerar_painel_multigraficos(self, colunas: List[str], titulo_geral: str, metrica: str = "Quantidade", salvar_html: str = "outputs/painel.html") -> None:
        from plotly.subplots import make_subplots
        total_linhas = len(colunas)

        figura = make_subplots(
            rows=total_linhas,
            cols=2,
            subplot_titles=[
                f"{colunas[i // 2]} - Barras" if i % 2 == 0 else f"{colunas[i // 2]} - Pizza"
                for i in range(2 * total_linhas)
            ],
            specs=[[{"type": "xy"}, {"type": "domain"}] for _ in range(total_linhas)],
            vertical_spacing=0.12
        )

        for idx, coluna in enumerate(colunas, start=1):
            if coluna not in self.df.columns:
                print(f"❌ Coluna '{coluna}' não encontrada no DataFrame.")
                continue

            if metrica not in self.df.columns:
                print(f"❌ Métrica '{metrica}' não existe no DataFrame.")
                continue

            # Agrupamento por soma
            df_agrupado = self.df.groupby(coluna)[metrica].sum().reset_index().sort_values(by=metrica, ascending=False)

            # Gráfico de barras
            fig_barra = px.bar(
                df_agrupado,
                x=coluna,
                y=metrica,
                title=f"{metrica} por {coluna}",
                text_auto=True,
                color_discrete_sequence=["#636EFA"]
            )

            # Gráfico de pizza
            fig_pizza = px.pie(
                df_agrupado,
                values=metrica,
                names=coluna,
                title=f"Distribuição percentual - {coluna}"
            )

            # Adiciona os gráficos no painel
            for trace in fig_barra.data:
                figura.add_trace(trace, row=idx, col=1)
            for trace in fig_pizza.data:
                figura.add_trace(trace, row=idx, col=2)

        figura.update_layout(
            height=450 * total_linhas,
            title_text=titulo_geral,
            showlegend=False
        )

        figura.write_html(salvar_html)
        print(f"\n✅ Painel HTML salvo como '{salvar_html}' com sucesso!")
        figura.show()