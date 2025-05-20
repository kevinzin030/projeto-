import tkinter as tk
from tkinter import messagebox
import json
import os

# Verifica e cria o arquivo de usuários se não existir
if not os.path.exists("usuarios.json"):
    with open("usuarios.json", "w") as f:
        json.dump([], f)

def salvar_usuario(nome, usuario, email, senha, cargo):
    with open("usuarios.json", "r") as f:
        usuarios = json.load(f)

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

    with open("usuarios.json", "w") as f:
        json.dump(usuarios, f, indent=4)

    return True, "Usuário cadastrado com sucesso!"

def tela_cadastro():
    cadastro = tk.Tk()
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

    # Cargo (Administrador ou Funcionário)
    frame_cargo = tk.Frame(cadastro, bg="#f5f5f5")
    frame_cargo.pack(pady=5)
    tk.Label(frame_cargo, text="Cargo:", width=15, anchor="w", bg="#f5f5f5").pack(side="left")
    cargo_var = tk.StringVar(value="Funcionário")
    tk.OptionMenu(frame_cargo, cargo_var, "Funcionário", "Administrador").pack(side="left")

    def registrar():
        nome = nome_entry.get().strip()
        usuario = usuario_entry.get().strip()
        email = email_entry.get().strip()
        senha = senha_entry.get().strip()
        confirmar = confirmar_entry.get().strip()
        cargo = cargo_var.get()

        if not all([nome, usuario, email, senha, confirmar]):
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        if senha != confirmar:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return

        sucesso, mensagem = salvar_usuario(nome, usuario, email, senha, cargo)
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            cadastro.destroy()
        else:
            messagebox.showerror("Erro", mensagem)

    tk.Button(cadastro, text="Cadastrar", font=("Arial", 12), bg="#4a7abc", fg="white", command=registrar).pack(pady=20)

    cadastro.mainloop()

# Executar a tela de cadastro
if __name__ == "__main__":
    tela_cadastro()
