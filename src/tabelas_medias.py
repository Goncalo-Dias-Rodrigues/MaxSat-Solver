import os
import re
import sys

import pandas as pd
import matplotlib.pyplot as plt

# Uso:
#   python tabelas_medias.py                -> usa o CSV por defeito
#   python tabelas_medias.py ficheiro.csv   -> usa outro CSV
#
# Gera, para cada algoritmo, uma tabela com:
#   Instância | Qualidade média | Avaliações médias | Tempo CPU médio (s)
# Cada "instância" corresponde a um número de cláusulas.
# Guarda cada tabela em CSV e em imagem PNG, e imprime-as no terminal.

CSV_POR_DEFEITO = "C:/Users/Gdrtu/Documents/Projects/MaxSat-Solver/results.csv"

COLUNAS = [
    "algorithm",
    "num_clauses",
    "execution_time_seconds",
    "number_evaluations",
    "best_result",
]
COLUNAS_NUMERICAS = [
    "num_clauses",
    "execution_time_seconds",
    "number_evaluations",
    "best_result",
]

PASTA_TABELAS = "tabelas"

CABECALHO = [
    "Instância",
    "Qualidade média",
    "Avaliações médias",
    "Tempo CPU médio (s)",
]


# ----------------------------------------------------------------------
# Leitura e limpeza dos dados
# ----------------------------------------------------------------------
def carregar_dados(caminho_csv):
    # Tudo lido como texto para não perder valores com vírgula decimal
    df = pd.read_csv(caminho_csv, sep=None, engine="python", dtype=str)
    df.columns = [c.strip() for c in df.columns]

    em_falta = [c for c in COLUNAS if c not in df.columns]
    if em_falta:
        raise ValueError(f"Faltam as seguintes colunas no CSV: {em_falta}")

    df = df[COLUNAS].copy()
    df["algorithm"] = df["algorithm"].str.strip()
    for coluna in COLUNAS_NUMERICAS:
        df[coluna] = pd.to_numeric(
            df[coluna].str.strip().str.replace(",", ".", regex=False),
            errors="coerce",
        )

    total = len(df)
    df = df.dropna(subset=COLUNAS)
    descartadas = total - len(df)
    if descartadas:
        print(f"Aviso: {descartadas} de {total} linhas descartadas "
              f"por terem valores em falta ou inválidos.")

    return df


# ----------------------------------------------------------------------
# Construção da tabela
# ----------------------------------------------------------------------
def construir_tabela(dados):
    """Agrupa por nº de cláusulas e calcula as médias."""
    tabela = (
        dados.groupby("num_clauses")
        .agg(
            qualidade=("best_result", "mean"),
            avaliacoes=("number_evaluations", "mean"),
            tempo=("execution_time_seconds", "mean"),
        )
        .reset_index()
        .sort_values("num_clauses")
    )
    tabela.columns = CABECALHO
    tabela["Instância"] = tabela["Instância"].astype(int)
    return tabela


def formatar(tabela):
    """Devolve uma cópia com os valores formatados como texto."""
    t = tabela.copy()
    t["Instância"] = t["Instância"].map(lambda v: f"{v}")
    t["Qualidade média"] = t["Qualidade média"].map(lambda v: f"{v:.2f}")
    t["Avaliações médias"] = t["Avaliações médias"].map(lambda v: f"{v:.1f}")
    t["Tempo CPU médio (s)"] = t["Tempo CPU médio (s)"].map(lambda v: f"{v:.4f}")
    return t


# ----------------------------------------------------------------------
# Saída
# ----------------------------------------------------------------------
def guardar_imagem(tabela_formatada, titulo, caminho):
    n_linhas = len(tabela_formatada)
    fig, ax = plt.subplots(figsize=(8, 0.6 + 0.45 * (n_linhas + 1)))
    ax.axis("off")
    ax.set_title(titulo, fontsize=13, pad=12)

    tab = ax.table(
        cellText=tabela_formatada.values,
        colLabels=tabela_formatada.columns,
        cellLoc="center",
        loc="center",
    )
    tab.auto_set_font_size(False)
    tab.set_fontsize(12)
    tab.auto_set_column_width(col=list(range(len(tabela_formatada.columns))))
    tab.scale(1, 1.8)

    for (linha, _), celula in tab.get_celld().items():
        # Contornos pretos bem visíveis em todas as células
        celula.set_edgecolor("black")
        celula.set_linewidth(1.5)
        if linha == 0:
            celula.set_text_props(weight="bold", color="black")
            celula.set_facecolor("#d9d9d9")
        else:
            celula.set_facecolor("white")

    fig.tight_layout()
    fig.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close(fig)


def nome_seguro(texto):
    return re.sub(r"[^\w\-]+", "_", str(texto))


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    caminho_csv = sys.argv[1] if len(sys.argv) > 1 else CSV_POR_DEFEITO

    df = carregar_dados(caminho_csv)
    os.makedirs(PASTA_TABELAS, exist_ok=True)

    algoritmos = df["algorithm"].drop_duplicates().tolist()

    for algoritmo in algoritmos:
        dados = df[df["algorithm"] == algoritmo]
        tabela = construir_tabela(dados)
        formatada = formatar(tabela)
        base = nome_seguro(algoritmo)

        print(f"\n=== {algoritmo} ===")
        print(formatada.to_string(index=False))

        tabela.round(4).to_csv(
            os.path.join(PASTA_TABELAS, f"tabela_{base}.csv"), index=False
        )
        guardar_imagem(
            formatada,
            f"{algoritmo}",
            os.path.join(PASTA_TABELAS, f"tabela_{base}.png"),
        )

    print(f"\nConcluído: {len(algoritmos)} tabelas guardadas na pasta '{PASTA_TABELAS}'.")


if __name__ == "__main__":
    main()