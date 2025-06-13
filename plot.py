import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

linux_df = pd.read_csv("resultados_benchmark_linux.csv")
windows_df = pd.read_csv("resultados_benchmark_windows.csv")

linux_df["SO"] = "Linux"
windows_df["SO"] = "Windows"

# combinar os dados
df = pd.concat([linux_df, windows_df], ignore_index=True)

df_forte = df[df["tipo"] == "forte_threads"]

plt.figure(figsize=(9, 6))

sns.lineplot(
    data=df_forte,
    x="threads",
    y="tempo_execucao",
    hue="SO",
    style="SO",
    markers=True,
    dashes=False
)

plt.title("WINDOWS vs LINUX - Escalabilidade Forte (32 min)")
plt.xlabel("Número de Threads")
plt.ylabel("Tempo de Execução (s)")
plt.grid(True)
plt.tight_layout()
plt.show()

df = pd.read_csv("resultados_benchmark.csv") # benchmark do linux
tipos = df["tipo"].unique()

for tipo in tipos:
    titulo = ""
    x = None
    x_label = None
    xticks = None
    show_tempo_em_tela = False

    subset = df[df["tipo"] == tipo]

    if tipo == "forte_threads":
        titulo = "Escalabilidade Forte - Variando Threads (48 min)"
        x = "threads"
        x_label = "Número de Threads"

    if tipo == "forte_frame_skip":
        titulo = "Escalabilidade Forte - Variando Frame Skip (48 min)"
        x = "frame_skip"
        x_label = "Frame Skip"
        show_tempo_em_tela = True

    if tipo == "fraca":
        titulo = "Escalabilidade Fraca - Variando Threads e Duração"
        x_label = "Número de Threads / Duração do Filme"
        subset["threads_duracao"] = subset.apply(lambda row: f"{row['threads']} ({round(row['duracao_total']/60)} min)", axis=1)
        x = "threads_duracao"

    # plotar gráfico
    plt.figure(figsize=(9, 6))
    ax = sns.lineplot(
        data=subset,
        x=x,
        y="tempo_execucao",
        markers=1,
    )

    ax.plot(subset[x], subset["tempo_execucao"], marker='o', linestyle='', color='blue')

    if show_tempo_em_tela:
        for i, row in subset.iterrows():
            ax.text(
                row[x], 
                row["tempo_execucao"] + 10,  # deslocamento vertical para não sobrepor
                f"{round(row['tempo_em_tela'], 1)}s",
                ha='left',
                fontsize=12,
                color='black')

    plt.title(titulo)
    plt.xlabel(x_label)
    plt.ylabel("Tempo de Execução (s)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
