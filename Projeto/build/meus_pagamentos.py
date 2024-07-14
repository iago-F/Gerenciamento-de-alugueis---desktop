import tkinter as tk
from tkinter import ttk, messagebox
from Pagamento import PaginaPagamento

from Contrato import Contratos
from Projeto.build.models.models import Casa, Base
from sqlalchemy.orm import sessionmaker
from connection import engine
from Pagamento import PaginaPagamento

Session = sessionmaker(bind=engine)
session = Session()
class meus_pagamentos:
    def __init__(self, master):
    # Adicionando a tabela
        self.master = master
        self.tree = ttk.Treeview(master, columns=("ID", "Data do Pagamento", "Valor"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Data do Pagamento", text="Data do Pagamento")
        self.tree.heading("Valor", text="Valor")
        self.tree.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        # Definindo a largura das colunas
        self.tree.column("ID", width=50)
        self.tree.column("Data do Pagamento", width=100)
        self.tree.column("Valor", width=100)

        self.exibir_pagamentos()
    def exibir_pagamentos(self):
        try:
            pagamentos = PaginaPagamento.get_mostrar_pagamentos()

            for pagamento in pagamentos:

                self.tree.insert("", "end", values=(pagamento.id, pagamento.dt_pagamento, pagamento.valor_pagamento))
        except Exception as e:
            print(f"Erro ao mostrar os pagamentos: {str(e)}")
