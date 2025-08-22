import customtkinter as ctk
import tkinter.filedialog as fd
import os
from tkinter import messagebox
from bobinagem import executar_bobinagem
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("orange.json")

labels_variaveis = []

def ler_float(entry, nome_campo="Este campo"):
    try:
        return float(entry.get().replace(",", "."))
    except ValueError:
        messagebox.showerror("Erro", f"O valor digitado em \"{nome_campo}\" é inválido.\nUse apenas números com ponto ou vírgula.")
        raise  # Levanta a exceção para interromper a execução

def limpar_campos():
    for entry in [
        entry_R_c, entry_Comprimento, entry_betac,
        entry_distancia, entry_b, entry_altura_pino,
        entry_lado_maior, entry_lado_menor, entry_altura_peca, entry_velocidade
    ]:
        entry.delete(0, "end")

    # Limpar gráfico, se existir
    for widget in frame_grafico.winfo_children():
        widget.destroy()

    # Limpar variáveis mostradas
    for lbl in labels_variaveis:
        lbl.destroy()
    labels_variaveis.clear()

    # Limpa o conteúdo do textbox do GCODE
    textbox.delete("0.0", "end")

def gerar():
    global labels_variaveis
    estrutura = estrutura_var.get()

    try:
        # Leitura e validação de cada campo — se der erro, raise para parar
        if estrutura == "Cilíndrica":
            Comprimento = float(entry_Comprimento.get().replace(",", "."))
            betac = float(entry_betac.get().replace(",", "."))
            if not (1 <= betac <= 89):
                raise ValueError("Ângulo deve estar entre 1° e 89°.")
            distancia = float(entry_distancia.get().replace(",", "."))
            b = float(entry_b.get().replace(",", "."))
            R_c = float(entry_R_c.get().replace(",", "."))
            altura_pino = float(entry_altura_pino.get().replace(",", "."))
            ladoMaior = ladoMenor = 0
            alturapeca = 0
            velocidade = float(entry_velocidade.get().replace(",", "."))
            if not (9000 >= velocidade):
                 raise ValueError("Velocidade muito alta para a máquina, reduzir para um valor menor")
        elif estrutura == "Retangular":
            Comprimento = float(entry_Comprimento.get().replace(",", "."))
            betac = float(entry_betac.get().replace(",", "."))
            if not (1 <= betac <= 89):
                raise ValueError("Ângulo deve estar entre 1° e 89°.")
            distancia = float(entry_distancia.get().replace(",", "."))
            b = float(entry_b.get().replace(",", "."))
            ladoMaior = float(entry_lado_maior.get().replace(",", "."))
            ladoMenor = float(entry_lado_menor.get().replace(",", "."))
            alturapeca = float(entry_altura_peca.get().replace(",", "."))
            R_c = 0
            altura_pino = 0
            velocidade = float(entry_velocidade.get().replace(",", "."))
            if not (9000 >= velocidade):
                 raise ValueError("Velocidade muito alta para a máquina, reduzir para um valor menor")
        elif estrutura == "Quadrada":
            Comprimento = float(entry_Comprimento.get().replace(",", "."))
            betac = float(entry_betac.get().replace(",", "."))
            if not (1 <= betac <= 89):
                raise ValueError("Ângulo deve estar entre 1° e 89°.")
            distancia = float(entry_distancia.get().replace(",", "."))
            b = float(entry_b.get().replace(",", "."))
            ladoMaior = float(entry_lado_maior.get().replace(",", "."))
            ladoMenor = float(entry_lado_menor.get().replace(",", "."))
            alturapeca = float(entry_altura_peca.get().replace(",", "."))
            R_c = 0
            altura_pino = 0
            velocidade = float(entry_velocidade.get().replace(",", "."))
            if not (9000 >= velocidade):
                 raise ValueError("Velocidade muito alta para a máquina, reduzir para um valor menor")
        else:
            raise ValueError("Tipo de estrutura desconhecido.")

        # Se chegou aqui, todas as leituras estão OK, pode executar
        fig, variaveis_calculadas = executar_bobinagem(
            estrutura, R_c, Comprimento, betac, distancia, b,
            altura_pino, ladoMaior, ladoMenor, alturapeca, velocidade
        )

        # Limpa gráficos anteriores
        for widget in frame_grafico.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        mostrar_arquivo_csv()

        # Limpa labels antigas
        for lbl in labels_variaveis:
            lbl.destroy()
        labels_variaveis.clear()

        # Mostra variáveis calculadas
        for nome, valor in variaveis_calculadas.items():
            lbl = ctk.CTkLabel(frame_variaveis, text=f"{nome}: {valor}", anchor="w")
            lbl.pack(fill="x", padx=10, pady=2)
            labels_variaveis.append(lbl)

        messagebox.showinfo("Sucesso", "Bobinagem executada com sucesso!")

    except ValueError as e:
        messagebox.showerror("Erro", str(e))
        return


janela = ctk.CTk()
janela.title("Bobinagem Filamentar")
janela.geometry("1000x800")

frame_lateral = ctk.CTkFrame(janela, width=300)
frame_lateral.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
frame_lateral.grid_propagate(False)

ctk.CTkLabel(frame_lateral, text="Parâmetros de Entrada", font=("Arial", 16, "bold")).pack(pady=(5, 15))

estrutura_var = ctk.StringVar(value="Cilíndrica")
ctk.CTkLabel(frame_lateral, text="Tipo de estrutura:").pack(pady=(0, 5))
for tipo in ["Cilíndrica", "Retangular", "Quadrada"]:
    ctk.CTkRadioButton(frame_lateral, text=tipo, variable=estrutura_var, value=tipo).pack(anchor="w", padx=20)

def criar_entrada(label_text):
    label = ctk.CTkLabel(frame_lateral, text=label_text)
    entry = ctk.CTkEntry(frame_lateral)
    return label, entry

label_R_c, entry_R_c = criar_entrada("Raio do tubo (mm):")
label_lado_maior, entry_lado_maior = criar_entrada("Lado maior da seção (mm):")
label_lado_menor, entry_lado_menor = criar_entrada("Lado menor da seção (mm):")
label_Comprimento, entry_Comprimento = criar_entrada("Comprimento do tubo (mm):")
label_betac, entry_betac = criar_entrada("Ângulo (1° a 89°):")
label_distancia, entry_distancia = criar_entrada("Distância até o olhau (mm):")
label_b, entry_b = criar_entrada("Largura da fibra (mm):")
label_altura_pino, entry_altura_pino = criar_entrada("Altura do pino (mm):")
label_altura_peca, entry_altura_peca = criar_entrada("Altura da peça (mm):")
label_velocidade, entry_velocidade = criar_entrada("Velocidade da máquina:")

botao_calcular = ctk.CTkButton(frame_lateral, text="Calcular", command=gerar)
botao_limpar = ctk.CTkButton(frame_lateral, text="Limpar", command=limpar_campos)

def atualizar_campos_visiveis(*args):
    for w in [label_R_c, entry_R_c,
              label_Comprimento, entry_Comprimento,
              label_betac, entry_betac,
              label_distancia, entry_distancia,
              label_b, entry_b,
              label_altura_pino, entry_altura_pino,
              label_lado_maior, entry_lado_maior,
              label_lado_menor, entry_lado_menor,
              label_altura_peca, entry_altura_peca,
              label_velocidade, entry_velocidade,
              botao_calcular, botao_limpar]:
        w.pack_forget()

    tipo = estrutura_var.get()

    if tipo == "Cilíndrica":
        label_R_c.pack(pady=(3, 2))
        entry_R_c.pack()
        label_Comprimento.pack(pady=(3, 2))
        entry_Comprimento.pack()
        label_betac.pack(pady=(3, 2))
        entry_betac.pack()
        label_distancia.pack(pady=(3, 2))
        entry_distancia.pack()
        label_b.pack(pady=(3, 2))
        entry_b.pack()
        label_altura_pino.pack(pady=(3, 2))
        entry_altura_pino.pack()
        label_velocidade.pack(pady=(3, 2))
        entry_velocidade.pack()
        botao_calcular.pack(pady=10)
        botao_limpar.pack(pady=5)

    elif tipo == "Retangular":
        label_lado_maior.pack(pady=(3, 2))
        entry_lado_maior.pack()
        label_lado_menor.pack(pady=(3, 2))
        entry_lado_menor.pack()
        label_Comprimento.pack(pady=(3, 2))
        entry_Comprimento.pack()
        label_betac.pack(pady=(3, 2))
        entry_betac.pack()
        label_distancia.pack(pady=(3, 2))
        entry_distancia.pack()
        label_b.pack(pady=(3, 2))
        entry_b.pack()
        label_altura_peca.pack(pady=(3, 2))
        entry_altura_peca.pack()
        label_velocidade.pack(pady=(3, 2))
        entry_velocidade.pack()
        botao_calcular.pack(pady=10)
        botao_limpar.pack(pady=5)

    elif tipo == "Quadrada":
        label_lado_maior.pack(pady=(3, 2))
        entry_lado_maior.pack()
        label_Comprimento.pack(pady=(3, 2))
        entry_Comprimento.pack()
        label_betac.pack(pady=(3, 2))
        entry_betac.pack()
        label_distancia.pack(pady=(3, 2))
        entry_distancia.pack()
        label_b.pack(pady=(3, 2))
        entry_b.pack()
        label_velocidade.pack(pady=(3, 2))
        entry_velocidade.pack()
        label_altura_peca.pack(pady=(3, 2))
        entry_altura_peca.pack()
        botao_calcular.pack(pady=10)
        botao_limpar.pack(pady=5)


estrutura_var.trace_add("write", atualizar_campos_visiveis)
atualizar_campos_visiveis()

# Frame do meio
frame_meio = ctk.CTkFrame(janela)
frame_meio.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
janela.grid_rowconfigure(0, weight=1)
janela.grid_columnconfigure(1, weight=1)
frame_meio.grid_rowconfigure((0,1), weight=1)
frame_meio.grid_columnconfigure(0, weight=1)

frame_meio.grid_rowconfigure(0, minsize=300)
frame_meio.grid_rowconfigure(1, minsize=200)

frame_grafico = ctk.CTkFrame(frame_meio, height=300)
frame_grafico.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
frame_grafico.grid_propagate(False)

frame_csv = ctk.CTkFrame(frame_meio, height=200)
frame_csv.grid(row=1, column=0, sticky="nsew")
frame_csv.grid_propagate(False)

ctk.CTkLabel(frame_csv, text="G-code para Bobinagem", font=("Arial", 14, "bold")).pack(pady=(5, 0))
textbox = ctk.CTkTextbox(frame_csv, wrap="none")
textbox.pack(fill="both", expand=True)

def mostrar_arquivo_csv():
    caminho_csv = "testeG91.csv"
    if os.path.exists(caminho_csv):
        with open(caminho_csv, "r", encoding="utf-8") as f:
            conteudo = f.read()
        textbox.delete("0.0", "end")
        textbox.insert("0.0", conteudo)
    else:
        textbox.delete("0.0", "end")
        textbox.insert("0.0", "Arquivo testeG91.csv não encontrado.")

# Direita
frame_lateral_direita = ctk.CTkFrame(janela)
frame_lateral_direita.grid(row=0, column=2, sticky="ns", padx=10, pady=10)

frame_dica = ctk.CTkFrame(frame_lateral_direita)
frame_dica.pack(pady=(0, 10), padx=10, fill="x")

ctk.CTkLabel(frame_dica, text="IMPORTANTE", font=("Arial", 24, "bold"),
             text_color="#FF6803", anchor="w").pack(fill="x", padx=10, pady=(5, 0))

ctk.CTkLabel(
    frame_dica,
    text="• Ângulos abaixo de 30° precisam de pinos\n\n• Usar o comprimento antes dos pinos\n\n• Usar velocidade 2500 caso não tenha experiência \ncom a máquina (máx 9000"
    ") \n\n•Altura da peça é a distância do eixo até o último\nponto da peça, que pode ser o topo de um pino caso \nexista\n\n•Se a estrutura não tiver pinos, usar valor 0\n\n" \
    "•Veja se a máquina não vai colidir no retorno, ela\nvolta mais no retorno devido à distância do olhau.\nO valor gerado em 'INFORMAÇÕES' apresenta \nesse 'Deslocamento de Colisão' dado em mm",
    font=("Arial", 13),
    justify="left",
    anchor="w"
).pack(fill="x", padx=10, pady=(2, 5))

frame_variaveis = ctk.CTkFrame(frame_lateral_direita)
frame_variaveis.pack(pady=10, padx=10, fill="both")

ctk.CTkLabel(frame_variaveis, text="Informações", font=("Arial", 14, "bold")).pack(pady=(10, 5))

def salvar_como():
    origem = "testeG91_2.csv"
    if not os.path.exists(origem):
        messagebox.showerror("Erro", "Arquivo testeG91.csv não encontrado.")
        return

    destino = fd.asksaveasfilename(defaultextension=".csv",
                                   filetypes=[("CSV files", "*.csv")],
                                   title="Salvar como...")
    if destino:
        with open(origem, "r", encoding="utf-8") as f_src:
            conteudo = f_src.read()
        with open(destino, "w", encoding="utf-8") as f_dst:
            f_dst.write(conteudo)
        messagebox.showinfo("Sucesso", f"Arquivo salvo em:\n{destino}")

ctk.CTkButton(frame_lateral_direita, text="Baixar arquivo CSV", command=salvar_como).pack(pady=20)

janela.mainloop()
