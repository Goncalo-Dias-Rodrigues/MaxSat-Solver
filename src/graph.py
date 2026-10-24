import os
import re
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Uso:
#   python graficos_pontos.py                -> usa o CSV por defeito
#   python graficos_pontos.py ficheiro.csv   -> usa outro CSV
# O modo de execução é sempre perguntado no terminal.

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

PASTA_GRAFICOS = "graficos"

JITTER = 0.08          # dispersão horizontal dos pontos
OFFSET = 0.18          # deslocamento horizontal de cada métrica em relação ao centro
LARGURA_MEDIA = 0.15   # meia largura da linha da média

COR_RESULTADO = "steelblue"
COR_TEMPO = "darkorange"
COR_MEDIA_RESULTADO = "navy"
COR_MEDIA_TEMPO = "crimson"

# Gerador aleatório com semente fixa para o jitter ser reprodutível
rng = np.random.default_rng(0)


# ----------------------------------------------------------------------
# Escolha do modo via terminal (input)
# ----------------------------------------------------------------------
def escolher_modo():
    caminho_csv = sys.argv[1] if len(sys.argv) > 1 else CSV_POR_DEFEITO

    print("Escolhe o modo de execução:")
    print("  1 - Um gráfico por número de cláusulas (algoritmos no eixo x)")
    print("  2 - Um gráfico por algoritmo (todos os números de cláusulas no eixo x)")
    print("  3 - Linhas de performance (uma linha por algoritmo; "
          "instâncias do menor para o maior nº de cláusulas no eixo x)")

    while True:
        opcao = input("Opção [1/2/3]: ").strip()
        if opcao == "1":
            return caminho_csv, "clausulas"
        if opcao == "2":
            return caminho_csv, "algoritmo"
        if opcao == "3":
            return caminho_csv, "performance"
        print("Opção inválida, escreve 1, 2 ou 3.")


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
# Funções de desenho
# ----------------------------------------------------------------------
def desenhar_pontos(ax, dados, metrica, coluna_x, categorias, centro_offset,
                    cor, cor_media):
    """Desenha os pontos individuais e a linha da média de uma métrica.

    coluna_x   -> coluna que define as posições no eixo x
    categorias -> valores dessa coluna, pela ordem em que aparecem no eixo x
    """
    for i, categoria in enumerate(categorias):
        y = dados.loc[dados[coluna_x] == categoria, metrica].to_numpy()
        if len(y) == 0:
            continue

        x0 = i + centro_offset
        x = x0 + rng.uniform(-JITTER, JITTER, size=len(y))
        ax.scatter(x, y, s=30, alpha=0.6, color=cor, edgecolors="none")

        ax.hlines(y.mean(), x0 - LARGURA_MEDIA, x0 + LARGURA_MEDIA,
                  color=cor_media, linewidth=2.5, zorder=3)


def configurar_eixo_x(ax, categorias, rotulos, xlabel):
    ax.set_xticks(range(len(categorias)))
    ax.set_xticklabels(rotulos)
    ax.set_xlim(-0.6, len(categorias) - 0.4)
    ax.set_xlabel(xlabel)
    plt.setp(ax.get_xticklabels(), rotation=25, ha="right")


def guardar(fig, nome_ficheiro):
    fig.tight_layout()
    caminho = os.path.join(PASTA_GRAFICOS, nome_ficheiro)
    fig.savefig(caminho, dpi=150)
    plt.close(fig)
    print(f"Gráfico criado: {caminho}")


def grafico_resultado_tempo(dados, coluna_x, categorias, rotulos, xlabel,
                            titulo_extra, nome_ficheiro):
    """Melhor resultado (eixo esquerdo) + tempo de execução (eixo direito)."""
    fig, ax1 = plt.subplots(figsize=(11, 7))
    ax2 = ax1.twinx()

    desenhar_pontos(ax1, dados, "best_result", coluna_x, categorias, -OFFSET,
                    COR_RESULTADO, COR_MEDIA_RESULTADO)
    desenhar_pontos(ax2, dados, "execution_time_seconds", coluna_x, categorias,
                    +OFFSET, COR_TEMPO, COR_MEDIA_TEMPO)

    configurar_eixo_x(ax1, categorias, rotulos, xlabel)
    ax1.set_title(f"Melhor resultado e tempo de execução — {titulo_extra}")
    ax1.set_ylabel("Melhor resultado", color=COR_RESULTADO)
    ax2.set_ylabel("Tempo (segundos)", color=COR_TEMPO)
    ax1.tick_params(axis="y", labelcolor=COR_RESULTADO)
    ax2.tick_params(axis="y", labelcolor=COR_TEMPO)
    ax1.grid(axis="y", alpha=0.3)

    ax1.legend(
        handles=[
            Line2D([0], [0], marker="o", linestyle="", color=COR_RESULTADO,
                   alpha=0.6, label="Melhor resultado (execuções)"),
            Line2D([0], [0], color=COR_MEDIA_RESULTADO, linewidth=2.5,
                   label="Melhor resultado (média)"),
            Line2D([0], [0], marker="o", linestyle="", color=COR_TEMPO,
                   alpha=0.6, label="Tempo de execução (execuções)"),
            Line2D([0], [0], color=COR_MEDIA_TEMPO, linewidth=2.5,
                   label="Tempo de execução (média)"),
        ],
        loc="best",
    )

    guardar(fig, nome_ficheiro)


def grafico_avaliacoes(dados, coluna_x, categorias, rotulos, xlabel,
                       titulo_extra, nome_ficheiro):
    """Número de avaliações (escala logarítmica se possível)."""
    fig, ax = plt.subplots(figsize=(11, 7))

    desenhar_pontos(ax, dados, "number_evaluations", coluna_x, categorias, 0,
                    "steelblue", "crimson")

    configurar_eixo_x(ax, categorias, rotulos, xlabel)
    ax.set_title(f"Número de avaliações — {titulo_extra}")
    ax.set_ylabel("Número de avaliações")

    if (dados["number_evaluations"] > 0).all():
        ax.set_yscale("log")

    ax.grid(axis="y", alpha=0.3)
    ax.legend(
        handles=[
            Line2D([0], [0], marker="o", linestyle="", color="steelblue",
                   alpha=0.6, label="Execuções individuais"),
            Line2D([0], [0], color="crimson", linewidth=2.5, label="Média"),
        ],
        loc="best",
    )

    guardar(fig, nome_ficheiro)


def grafico_performance(df, clausulas, rotulos, ordem_algoritmos):
    """Linhas de performance: uma linha por algoritmo (nome na legenda).

    Painel de cima  -> melhor resultado (média por instância)
    Painel de baixo -> velocidade / tempo de execução (média por instância,
                       escala logarítmica)
    Eixo x          -> instâncias ordenadas do menor para o maior nº de cláusulas
    """
    medias = (
        df.groupby(["algorithm", "num_clauses"])
        .agg(melhor=("best_result", "mean"),
             tempo=("execution_time_seconds", "mean"))
        .reset_index()
    )

    fig, (ax_res, ax_tempo) = plt.subplots(
        2, 1, figsize=(11, 9), sharex=True,
        gridspec_kw={"height_ratios": [1, 1]},
    )

    cores = plt.cm.tab10(np.linspace(0, 1, 10))
    marcadores = ["o", "s", "^", "D", "v", "P", "X", "*", "h", "<"]
    posicao = {c: i for i, c in enumerate(clausulas)}

    for k, algoritmo in enumerate(ordem_algoritmos):
        d = medias[medias["algorithm"] == algoritmo].sort_values("num_clauses")
        x = [posicao[c] for c in d["num_clauses"]]
        estilo = dict(color=cores[k % 10], marker=marcadores[k % 10],
                      linewidth=2, markersize=7, label=str(algoritmo))

        ax_res.plot(x, d["melhor"], **estilo)
        ax_tempo.plot(x, d["tempo"], **estilo)

    ax_res.set_title("Performance dos algoritmos por instância")
    ax_res.set_ylabel("Melhor resultado (média)")
    ax_res.grid(alpha=0.3)
    ax_res.legend(title="Algoritmo", loc="best")

    # Escala logarítmica apenas na opção 3
    if (medias["tempo"] > 0).all():
        ax_tempo.set_yscale("log")
    ax_tempo.set_ylabel("Velocidade — tempo de execução (s, média, escala log)")
    ax_tempo.set_xlabel("Instância (nº de cláusulas, do menor para o maior)")
    ax_tempo.grid(alpha=0.3, which="both")

    ax_tempo.set_xticks(range(len(clausulas)))
    ax_tempo.set_xticklabels(rotulos)
    ax_tempo.set_xlim(-0.4, len(clausulas) - 0.6)
    plt.setp(ax_tempo.get_xticklabels(), rotation=25, ha="right")

    guardar(fig, "grafico_performance_algoritmos.png")


# ----------------------------------------------------------------------
# Modos de execução
# ----------------------------------------------------------------------
def modo_clausulas(df):
    """Um conjunto de gráficos por nº de cláusulas; algoritmos no eixo x."""
    ordem_algoritmos = df["algorithm"].drop_duplicates().tolist()
    clausulas = sorted(df["num_clauses"].unique())

    for num_clausulas in clausulas:
        dados = df[df["num_clauses"] == num_clausulas]
        titulo = f"{int(num_clausulas)} cláusulas"
        sufixo = f"clausulas_{int(num_clausulas)}"

        grafico_resultado_tempo(dados, "algorithm", ordem_algoritmos,
                                ordem_algoritmos, "Algoritmo", titulo,
                                f"grafico_resultado_tempo_{sufixo}.png")
        grafico_avaliacoes(dados, "algorithm", ordem_algoritmos,
                           ordem_algoritmos, "Algoritmo", titulo,
                           f"grafico_number_evaluations_{sufixo}.png")

    return len(clausulas) * 2


def modo_algoritmo(df):
    """Um conjunto de gráficos por algoritmo; nº de cláusulas no eixo x."""
    ordem_algoritmos = df["algorithm"].drop_duplicates().tolist()
    clausulas = sorted(df["num_clauses"].unique())
    rotulos = [str(int(c)) for c in clausulas]

    for algoritmo in ordem_algoritmos:
        dados = df[df["algorithm"] == algoritmo]
        titulo = f"{algoritmo}"
        nome_seguro = re.sub(r"[^\w\-]+", "_", str(algoritmo))

        grafico_resultado_tempo(dados, "num_clauses", clausulas, rotulos,
                                "Número de cláusulas", titulo,
                                f"grafico_resultado_tempo_algoritmo_{nome_seguro}.png")
        grafico_avaliacoes(dados, "num_clauses", clausulas, rotulos,
                           "Número de cláusulas", titulo,
                           f"grafico_number_evaluations_algoritmo_{nome_seguro}.png")

    return len(ordem_algoritmos) * 2


def modo_performance(df):
    """Um único gráfico com uma linha por algoritmo."""
    ordem_algoritmos = df["algorithm"].drop_duplicates().tolist()
    clausulas = sorted(df["num_clauses"].unique())
    rotulos = [str(int(c)) for c in clausulas]

    grafico_performance(df, clausulas, rotulos, ordem_algoritmos)
    return 1


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    caminho_csv, modo = escolher_modo()

    df = carregar_dados(caminho_csv)
    os.makedirs(PASTA_GRAFICOS, exist_ok=True)

    if modo == "clausulas":
        total = modo_clausulas(df)
    elif modo == "algoritmo":
        total = modo_algoritmo(df)
    else:
        total = modo_performance(df)

    print(f"\nConcluído: {total} gráficos guardados na pasta '{PASTA_GRAFICOS}'.")


if __name__ == "__main__":
    main()