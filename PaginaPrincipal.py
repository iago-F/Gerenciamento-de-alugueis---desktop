import tkinter as tk
from tkinter import ttk


class PaginaPrincipal:
    def __init__(self, master,nome_usuario, email_usuario):
        self.master = master
        self.master.title("Página Principal")

        # # Adicionando a imagem
        # self.imagem = tk.PhotoImage(file=r"Projeto/build/assets/imgs/LOGO_CASA_PRINCIPAL.PNG")
        # self.label_imagem = tk.Label(master, image=self.imagem)
        # self.label_imagem.pack()

        # Adicionando o nome do usuário
        self.label_nome = tk.Label(master, text=f"Nome: {nome_usuario}", anchor="w")
        self.label_nome.pack(fill=tk.X)

        # Adicionando o email do usuário
        self.label_email = tk.Label(master, text=f"Email: {email_usuario}", anchor="w")
        self.label_email.pack(fill=tk.X)

        # Criando a barra superior (Topbar)
        self.topbar = tk.Frame(master)
        self.topbar.pack(fill=tk.X)

        # Adicionando um menu suspenso à barra superior
        self.dropdown_menu = tk.Menu(self.topbar)
        self.master.config(menu=self.dropdown_menu)

        # Adicionando um item de menu com subitens
        self.menu_paginas = tk.Menu(self.dropdown_menu, tearoff=0)
        self.dropdown_menu.add_cascade(label="Menu", menu=self.menu_paginas)

        # Adicionando botões ao menu suspenso
        self.botao_pagamento = ttk.Button(self.menu_paginas, text="Pagamento", command=self.ir_para_pagamento)
        self.menu_paginas.add_command(label="Pagamento", command=self.ir_para_pagamento)

        self.botao_contrato = ttk.Button(self.menu_paginas, text="Contrato", command=self.ir_para_contrato)
        self.menu_paginas.add_command(label="Contrato", command=self.ir_para_contrato)

        self.botao_casa = ttk.Button(self.menu_paginas, text="Casa", command=self.ir_para_casa)
        self.menu_paginas.add_command(label="Casa", command=self.ir_para_casa)

    def ir_para_pagamento(self):
        # Adicione aqui o código para ir para a página de Pagamento
        pass

    def ir_para_contrato(self):
        # Adicione aqui o código para ir para a página de Contrato
        pass

    def ir_para_casa(self):
        # Adicione aqui o código para ir para a página de Casa
        pass

#     # Testando a página principal
#
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = PaginaPrincipal(root, )
#     root.mainloop()