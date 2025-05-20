import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter, ImageDraw
import json
import os
import sys

# --- Caminho de arquivos para funcionar no executável ---
def recurso_caminho(relativo):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relativo)
    return os.path.join(os.path.abspath("."), relativo)

USUARIOS_FILE = recurso_caminho("usuarios.json")

# Criar arquivo JSON se não existir
if not os.path.exists(USUARIOS_FILE):
    with open(USUARIOS_FILE, "w") as f:
        json.dump([], f)

def carregar_usuarios():
    with open(USUARIOS_FILE, "r") as f:
        return json.load(f)

def salvar_usuarios(usuarios):
    with open(USUARIOS_FILE, "w") as f:
        json.dump(usuarios, f, indent=4)

def salvar_usuario(nome, usuario, email, senha, cargo="Aluno"):
    usuarios = carregar_usuarios()
    for u in usuarios:
        if u["usuario"] == usuario:
            return False, "Nome de usuário já existe."
        if u["email"] == email:
            return False, "E-mail já cadastrado."

    usuarios.append({
        "nome": nome,
        "usuario": usuario,
        "email": email,
        "senha": senha,
        "cargo": cargo
    })
    salvar_usuarios(usuarios)
    return True, "Usuário cadastrado com sucesso!"

def main_screen(nome, cargo):
    root = tk.Tk()
    root.title("Plataforma Educacional")
    root.state('zoomed')

    try:
        fundo_img = Image.open(recurso_caminho("Imagens/21.png"))
        fundo_img = fundo_img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
        fundo = ImageTk.PhotoImage(fundo_img)
    except Exception:
        fundo = None

    if fundo:
        label_fundo = tk.Label(root, image=fundo)
        label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

    header = tk.Frame(root, bg="#4a7abc", height=80)
    header.pack(fill="x")
    title = tk.Label(header, text="Tsuki Education Sistems", font=("Arial", 20), bg="#4a7abc", fg="white")
    title.pack(pady=20)

    welcome = tk.Label(root, text=f"Bem-vindo(a), {nome} ({cargo})", font=("Arial", 16), bg="#f5f5f5")
    welcome.pack(pady=20)

    btn_frame = tk.Frame(root, bg="#f5f5f5")
    btn_frame.pack(pady=10)

    def ver_aulas():
        messagebox.showinfo("Aulas", "Aqui será exibido o conteúdo das aulas.")

    def ver_desempenho():
        messagebox.showinfo("Desempenho", "Aqui será exibido o desempenho do aluno.")

    def configuracoes():
        messagebox.showinfo("Configurações", "Área de configurações.")

    def sair():
        root.destroy()

    botoes_info = [
        ("📚 Documentos do Aluno", ver_aulas),
        ("📝 Trabalhos Acadêmicos", ver_desempenho),
        ("📆 Calendário", configuracoes),
        ("🎓 Aulas ao Vivo", ver_aulas),
        ("🔧 Configurações", configuracoes),
        ("🚪 Sair", sair)
    ]

    for i, (texto, comando) in enumerate(botoes_info):
        btn = tk.Button(btn_frame, text=texto, width=30, height=2, font=("Arial", 12, "bold"),
                        bg="#4a7abc", fg="white", relief="raised", command=comando)
        btn.grid(row=i//2, column=i%2, padx=15, pady=15)

    root.mainloop()

def tela_cadastro():
    cadastro = tk.Toplevel()
    cadastro.title("Cadastro de Usuário")
    cadastro.geometry("500x500")
    cadastro.configure(bg="#f5f5f5")

    tk.Label(cadastro, text="Cadastro de Novo Usuário", font=("Arial", 18), bg="#f5f5f5").pack(pady=20)

    def criar_label_entry(texto):
        frame = tk.Frame(cadastro, bg="#f5f5f5")
        frame.pack(pady=5)
        label = tk.Label(frame, text=texto, width=15, anchor="w", bg="#f5f5f5")
        label.pack(side="left")
        entry = tk.Entry(frame, width=30)
        entry.pack(side="left")
        return entry

    nome_entry = criar_label_entry("Nome completo:")
    usuario_entry = criar_label_entry("Nome de usuário:")
    email_entry = criar_label_entry("E-mail:")
    senha_entry = criar_label_entry("Senha:")
    senha_entry.config(show="*")
    confirmar_entry = criar_label_entry("Confirmar senha:")
    confirmar_entry.config(show="*")

    def registrar():
        nome = nome_entry.get().strip()
        usuario = usuario_entry.get().strip()
        email = email_entry.get().strip()
        senha = senha_entry.get().strip()
        confirmar = confirmar_entry.get().strip()

        if not all([nome, usuario, email, senha, confirmar]):
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        if senha != confirmar:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return

        sucesso, mensagem = salvar_usuario(nome, usuario, email, senha)
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            cadastro.destroy()
        else:
            messagebox.showerror("Erro", mensagem)

    tk.Button(cadastro, text="Cadastrar", font=("Arial", 12), bg="#4a7abc", fg="white", command=registrar).pack(pady=20)

def tela_login():
    login = tk.Tk()
    login.title("Sistema de Login")
    login.state('zoomed')

    largura = login.winfo_screenwidth()
    altura = login.winfo_screenheight()

    try:
        fundo_img = Image.open(recurso_caminho("Imagens/19.png")).resize((largura, altura), Image.Resampling.LANCZOS)
        fundo = ImageTk.PhotoImage(fundo_img)
    except Exception:
        fundo = None

    canvas = tk.Canvas(login, width=largura, height=altura, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    if fundo:
        canvas.create_image(0, 0, image=fundo, anchor="nw")

    if fundo:
        box_bg_img = Image.open(recurso_caminho("Imagens/19.png")).resize((400, 250), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(15))
        mask = Image.new("L", (400, 250), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, 400, 250), radius=30, fill=255)
        box_bg_img.putalpha(mask)
        box_bg = ImageTk.PhotoImage(box_bg_img)
        canvas.create_image(largura//2, altura//2, image=box_bg, anchor="center")

    canvas.create_text(largura//2, altura//2 - 80, text="Entre com o Login", font=("Arial Black", 28), fill="white")

    def clear_placeholder(event, entry, text):
        if entry.get() == text:
            entry.delete(0, tk.END)
            entry.config(fg="white", show="*" if entry == campo_senha else "")

    def add_placeholder(event, entry, text):
        if entry.get() == "":
            entry.insert(0, text)
            entry.config(fg="gray", show="")

    try:
        img_usuario = Image.open(recurso_caminho('Imagens/16.png')).resize((35, 35))
        img_usuario = ImageTk.PhotoImage(img_usuario)
        canvas.create_image(largura//2 - 140, altura//2 - 30, image=img_usuario, anchor="center")
    except Exception:
        pass

    campo_usuario = tk.Entry(login, font=(14), width=25, bg="#000000", fg="gray", insertbackground="white", relief=tk.FLAT)
    campo_usuario.insert(0, "Nome de usuário ou e-mail")
    canvas.create_window(largura//2 - 10, altura//2 - 30, window=campo_usuario)
    campo_usuario.bind("<FocusIn>", lambda e: clear_placeholder(e, campo_usuario, "Nome de usuário ou e-mail"))
    campo_usuario.bind("<FocusOut>", lambda e: add_placeholder(e, campo_usuario, "Nome de usuário ou e-mail"))

    try:
        img_senha = Image.open(recurso_caminho('Imagens/15.png')).resize((35, 35))
        img_senha = ImageTk.PhotoImage(img_senha)
        canvas.create_image(largura//2 - 140, altura//2 + 20, image=img_senha, anchor="center")
    except Exception:
        pass

    campo_senha = tk.Entry(login, font=(14), width=25, bg="#000000", fg="gray", insertbackground="white", relief=tk.FLAT, show="")
    campo_senha.insert(0, "Digite sua senha")
    canvas.create_window(largura//2 - 10, altura//2 + 20, window=campo_senha)
    campo_senha.bind("<FocusIn>", lambda e: clear_placeholder(e, campo_senha, "Digite sua senha"))
    campo_senha.bind("<FocusOut>", lambda e: add_placeholder(e, campo_senha, "Digite sua senha"))

    def entrar():
        usuario = campo_usuario.get().strip()
        senha = campo_senha.get().strip()

        if usuario == "" or usuario == "Nome de usuário ou e-mail":
            messagebox.showerror("Erro", "Por favor, digite seu nome de usuário ou e-mail.")
            return
        if senha == "" or senha == "Digite sua senha":
            messagebox.showerror("Erro", "Por favor, digite sua senha.")
            return

        usuarios = carregar_usuarios()
        user_found = None
        for u in usuarios:
            if (u["usuario"] == usuario or u["email"] == usuario) and u["senha"] == senha:
                user_found = u
                break

        if user_found:
            login.destroy()
            main_screen(user_found["nome"], user_found["cargo"])
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    botao_entrar = tk.Button(login, text="Entrar", bg="#000000", fg="white", font=("Arial Black", 13), command=entrar)
    canvas.create_window(largura//2, altura//2 + 70, window=botao_entrar)

    botao_cadastrar = tk.Button(login, text="Cadastrar novo usuário", bg="#4a7abc", fg="white", font=("Arial", 11), command=tela_cadastro)
    canvas.create_window(largura//2, altura//2 + 120, window=botao_cadastrar)

    botao_entrar.bind("<Enter>", lambda e: botao_entrar.config(bg="#555555"))
    botao_entrar.bind("<Leave>", lambda e: botao_entrar.config(bg="#000000"))

    login.bind("<Escape>", lambda e: login.destroy())
    login.mainloop()

if __name__ == "__main__":
    tela_login()
