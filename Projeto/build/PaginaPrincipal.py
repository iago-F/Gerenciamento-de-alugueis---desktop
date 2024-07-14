import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Pagamento import PaginaPagamento
from Casa import Cadastro_Casas, get_mostrar_casas, cont_casas
from Contrato import Contratos
from Projeto.build.meus_pagamentos import meus_pagamentos
from minhas_casas import minhas_casas
import matplotlib.pyplot as plt
from meus_contratos import meus_contratos
from connection import engine
from sqlalchemy.orm import sessionmaker
from auth import get_authenticated_user
from Projeto.build.models.models import Contrato
from datetime import datetime

Session = sessionmaker(bind=engine)
session = Session()

class PaginaPrincipal:
    def __init__(self, master,nome_usuario, email_usuario,user_id):
        self.master = master
        self.master.title("Página Principal")
        self.master.geometry("1000x600")  # Defina o tamanho da janela aqui

        self.master.config(bg="lightblue")
        self.imagem_original = tk.PhotoImage(file=r"C:\Users\IAGO\Documents\Projeto desktop\Projeto\build\assets\imgs\LOGO_CASA_PRINCIPAL.PNG")
        self.imagem_redimensionada = self.imagem_original.subsample(2)  # Redimensionando pela metade

        # Criando a barra superior (Topbar)
        self.topbar = tk.Frame(master, bg="lightblue")
        self.topbar.pack(fill=tk.X)


    # Criando a top navigation bar ao lado do menu suspenso
        self.navbar_frame = tk.Frame(self.topbar, bg="lightblue")
        self.navbar_frame.pack(side=tk.LEFT, padx=0, pady=5)

        # Adicionando botões à top navigation bar
        self.botao_minhas_casas_nav = ttk.Button(self.navbar_frame, text="Minhas Casas",command=self.ir_para_minha_casa)
        self.botao_minhas_casas_nav.pack(side=tk.LEFT, padx=5, pady=5)

        self.botao_meus_pagamentos_nav = ttk.Button(self.navbar_frame, text="Meus Pagamentos",
                                                    command=self.ir_para_meus_pagamentos)
        self.botao_meus_pagamentos_nav.pack(side=tk.LEFT, padx=5, pady=5)

        self.botao_meus_contratos_nav = ttk.Button(self.navbar_frame, text="Meus Contratos",
                                                   command=self.ir_para_meus_contratos)
        self.botao_meus_contratos_nav.pack(side=tk.LEFT, padx=5, pady=5)

        self.botao_casa_nav = ttk.Button(self.navbar_frame, text="Cadastrar Casa", command=self.ir_para_casa)
        self.botao_casa_nav.pack(side=tk.LEFT, padx=5, pady=5)

        self.botao_pagamento_nav = ttk.Button(self.navbar_frame, text="Cadastrar Pagamento",
                                              command=self.ir_para_pagamento)
        self.botao_pagamento_nav.pack(side=tk.LEFT, padx=5, pady=5)

        self.botao_contrato_nav = ttk.Button(self.navbar_frame, text="Cadastrar Contrato",
                                             command=self.ir_para_contrato)
        self.botao_contrato_nav.pack(side=tk.LEFT, padx=5, pady=5)

        # Adicionando a imagem em uma label
        self.label_imagem = tk.Label(master, image=self.imagem_redimensionada)
        self.label_imagem.pack(pady=20)

        # Adicionando o nome do usuário
        self.label_nome = tk.Label(master, text=f"Nome: {nome_usuario}", anchor="w")
        self.label_nome.pack(fill=tk.X)

        # Adicionando o email do usuário
        self.label_email = tk.Label(master, text=f"Email: {email_usuario}", anchor="w")
        self.label_email.pack(fill=tk.X)

        # Adicionando o calendário
        self.calendar_frame = tk.Frame(master)
        self.calendar_frame.pack(pady=20)
        self.calendar = Calendar(self.calendar_frame, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendar.pack(pady=20)
        self.mostrar_eventos_calendario(user_id)

        # Dicionário para armazenar detalhes dos contratos
        self.contract_details = {}

        self.mostrar_eventos_calendario(user_id)

        # Bind evento de clique no calendário
        self.calendar.bind("<<CalendarSelected>>", self.mostrar_detalhes_contrato)

    def mostrar_detalhes_contrato(self, event):
        selected_date = self.calendar.get_date()
        contrato = self.contract_details.get(selected_date)

        if contrato:
            detalhes = (
                f"ID: {contrato.id}\n"
                f"Data de Início: {contrato.dt_inicio}\n"
                f"Data de Término: {contrato.dt_termino}\n"
                f"Valor Total: {contrato.valor_total}"
            )
            messagebox.showinfo("Detalhes do Contrato", detalhes)
        else:
            messagebox.showinfo("Detalhes do Contrato", "Nenhum contrato encontrado para esta data.")


    def mostrar_eventos_calendario(self, user_id):
        try:
            authenticated_user = get_authenticated_user()
            if not authenticated_user:
                raise Exception("Usuário não autenticado")

            contratos = session.query(Contrato).filter_by(usuario_id=user_id).all()

            for contrato in contratos:
                # Adiciona eventos ao calendário (cor de fundo para marcar as datas)
                self.calendar.calevent_create(contrato.dt_inicio, 'Início Contrato', 'start')
                self.calendar.calevent_create(contrato.dt_termino, 'Término Contrato', 'end')

            # Define a cor dos eventos
            self.calendar.tag_config('start', background='green', foreground='white')
            self.calendar.tag_config('end', background='red', foreground='white')

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao mostrar os eventos no calendário: {str(e)}")
        finally:
            session.close()


    def ir_para_pagamento(self):
        janela_pagamento = tk.Toplevel(self.master)
        pagina_pagamento = PaginaPagamento(janela_pagamento)

        pass

    def ir_para_meus_contratos(self):
        janela_contrato = tk.Toplevel(self.master)
        pagina_contrato = meus_contratos(janela_contrato)

    def ir_para_meus_pagamentos(self):
        janela_pagamento = tk.Toplevel(self.master)
        pagina_pagamento = meus_pagamentos(janela_pagamento)

    def ir_para_minha_casa(self):
        janela_minha_casa = tk.Toplevel(self.master)
        pagina_minha_casa = minhas_casas(janela_minha_casa)

        pass


    def ir_para_contrato(self):
        janela_pagamento = tk.Toplevel(self.master)
        pagina_pagamento = Contratos(janela_pagamento)
        pass

    def ir_para_casa(self):
      janela_casa = tk.Toplevel(self.master)
      pagina_casa = Cadastro_Casas(janela_casa)
    pass

#     # Testando a página principal
#
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = PaginaPrincipal(root, )
#     root.mainloop()