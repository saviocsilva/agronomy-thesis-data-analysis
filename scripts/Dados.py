import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scikit_posthocs as sp
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from matplotlib.backends.backend_pdf import PdfPages
import os

# 1. Estilo visual e leitura dos dados
sns.set(style="darkgrid")
df = pd.read_csv("dados_tcc_limpo_sem_extras.csv", sep=";")
variaveis_parametricas = ["PH_AGUA", "PH_CACL", "PH_KCL", "ACIDEZ", "ALUMINIO"]
variaveis_nparametricas = ["SODIO", "POTASSIO"]
grupo = "PONTOS"
subgrupo = "PROFUNDIDADE"
saida_png = "graficos_tcc"
os.makedirs(saida_png, exist_ok=True)

# 2. Funções de pós-hoc
def letras_tukey(df, var, fator):
    tukey = pairwise_tukeyhsd(endog=df[var], groups=df[fator], alpha=0.05)
    res = pd.DataFrame(tukey.summary().data[1:], columns=tukey.summary().data[0])
    letras = {g: 'a' for g in df[fator].unique()}
    atual = ord('a')
    grupos = sorted(df[fator].unique())
    grupo_letras = {g: set() for g in grupos}
    for g in grupos:
        grupo_letras[g].add(chr(atual))
        for linha in res.itertuples():
            if linha.reject and g in (linha.group1, linha.group2):
                atual += 1
                grupo_letras[g].add(chr(atual))
    return {g: sorted(grupo_letras[g])[0] for g in grupos}

def letras_dunn(df, var, fator):
    res = sp.posthoc_dunn(df, val_col=var, group_col=fator, p_adjust='bonferroni')
    letras = {g: 'a' for g in res.columns}
    atual = ord('a')
    for g in res.columns:
        for k in res.columns:
            if g != k and res.loc[g, k] < 0.05:
                atual += 1
                letras[g] = chr(atual)
    return letras

# 3. Função para gráfico
def gerar_boxplot(df, var, fator, pdf):
    plt.figure(figsize=(8, 5))
    sns.boxplot(x=fator, y=var, data=df, hue=fator, palette="Set2", dodge=False, legend=False)
    plt.title(f"{var} por {fator} — ANOVA/Kruskal + pós-hoc", fontsize=13)
    plt.xlabel(fator)
    plt.ylabel(var)
    plt.grid(True, linestyle="--", alpha=0.4)

    letras = letras_tukey(df, var, fator) if var in variaveis_parametricas else letras_dunn(df, var, fator)
    for i, g in enumerate(sorted(df[fator].unique())):
        y_max = df[df[fator] == g][var].max()
        plt.text(i, y_max + 0.3, letras[g], ha='center', fontsize=12, fontweight='bold',
                 bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    plt.tight_layout()
    plt.savefig(f"{saida_png}/{var}_{fator}_boxplot.png", dpi=300)
    pdf.savefig()
    plt.close()

# 4. Tabela como figura
def exportar_tabela_pdf(df, titulo, pdf):
    fig, ax = plt.subplots(figsize=(10, len(df)*0.5))
    ax.axis('off')
    ax.set_title(titulo, fontsize=14, weight='bold')
    tabela = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(10)
    tabela.scale(1, 1.5)
    pdf.savefig(fig)
    plt.close()

# 5. Capa do relatório
def capa_pdf(pdf, titulo):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis("off")
    ax.text(0.5, 0.6, titulo, fontsize=20, weight='bold', ha='center')
    ax.text(0.5, 0.45, "Relatório gráfico e estatístico — TCC", fontsize=14, ha='center')
    ax.text(0.5, 0.3, "Gerado automaticamente com Python", fontsize=10, ha='center', style='italic')
    pdf.savefig(fig)
    plt.close()

# 6. Tabelas estatísticas e descritivas
estatisticas = []
descritiva = []
for var in variaveis_parametricas + variaveis_nparametricas:
    for fator in [grupo, subgrupo]:
        resumo = df.groupby(fator)[var].agg(['mean', 'std', 'count']).reset_index()
        letras = letras_tukey(df, var, fator) if var in variaveis_parametricas else letras_dunn(df, var, fator)
        resumo["Letra"] = resumo[fator].map(letras)
        resumo["Variável"] = var
        estatisticas.append(resumo)

        descri = df.groupby(fator)[var].agg(['mean', 'median', 'min', 'max', 'std', 'count']).reset_index()
        descri["Variável"] = var
        descritiva.append(descri)

df_resumo = pd.concat(estatisticas, ignore_index=True)[["Variável", fator, "mean", "std", "count", "Letra"]]
df_descritiva = pd.concat(descritiva, ignore_index=True)[["Variável", fator, "mean", "median", "min", "max", "std", "count"]]

df_resumo[["mean", "std"]] = df_resumo[["mean", "std"]].round(2)
df_descritiva[["mean", "median", "min", "max", "std"]] = df_descritiva[["mean", "median", "min", "max", "std"]].round(2)

# Salva tabelas
df_resumo.to_csv("resumo_estatistico_tcc.csv", sep=";", index=False)
df_resumo.to_excel("resumo_estatistico_tcc.xlsx", index=False)
df_descritiva.to_csv("tabela_descritiva_tcc.csv", sep=";", index=False)
df_descritiva.to_excel("tabela_descritiva_tcc.xlsx", index=False)

# 7. Monta o PDF final com tudo
with PdfPages("tcc_relatorio_completo.pdf") as pdf:
    capa_pdf(pdf, "Análise estatística e gráfica — TCC")
    for fator in [grupo, subgrupo]:
        for var in variaveis_parametricas + variaveis_nparametricas:
            gerar_boxplot(df, var, fator, pdf)
    exportar_tabela_pdf(df_resumo, "Resumo estatístico por grupo e profundidade", pdf)
    exportar_tabela_pdf(df_descritiva, "Tabela descritiva completa", pdf)
