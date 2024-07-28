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
from sqlalchemy import inspect, func
from auth import get_authenticated_user
from Projeto.build.models.models import Contrato
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw, ImageOps
from LoginUser import PaginaLogin

Session = sessionmaker(bind=engine)
session = Session()

class PaginaPrincipal:
    def __init__(self, master, nome_usuario, email_usuario, sobrenome_usuario, user_id, cpf):

        self.master = master
        self.master.title("Página Principal")
        self.master.geometry("1000x600")  # Defina o tamanho da janela aqui

        self.nome_usuario = nome_usuario
        self.email_usuario = email_usuario
        self.sobrenome_usuario = sobrenome_usuario
        self.user_id = user_id
        self.cpf = cpf

        self.master.config(bg="white")
        self.imagem_original = Image.open(
            r"C:\Users\IAGO\Documents\Projeto desktop\Projeto\build\assets\imgs\LOGO_CASA_PRINCIPAL.PNG")
        self.imagem_original = self.imagem_original.resize((50, 50), Image.LANCZOS)
        self.imagem_redonda = self.arredondar_imagem(self.imagem_original)
        # Converter para PhotoImage
        self.imagem_tk = ImageTk.PhotoImage(self.imagem_redonda)
        # Criando a barra superior (Topbar)
        self.topbar = tk.Frame(master, bg="lightblue")
        self.topbar.pack(fill=tk.X)

        # Criando a top navigation bar ao lado do menu suspenso
        self.navbar_frame = tk.Frame(self.topbar, bg="lightblue")
        self.navbar_frame.pack(side=tk.LEFT, padx=0, pady=5)

        # Adicionando a imagem ao navbar_frame
        self.label_imagem = tk.Label(self.navbar_frame, image=self.imagem_tk, bg="lightblue")
        self.label_imagem.pack(side=tk.LEFT, padx=10, pady=5)
        self.label_imagem.bind("<Button-1>", self.mostrar_menu_suspenso)

        # Criar o menu suspenso
        self.menu_suspenso = tk.Menu(master, tearoff=0)
        self.menu_suspenso.add_command(label="Meu perfil", command=self.editar_informacoes)
        self.menu_suspenso.add_command(label="Sair", command=self.logout)

        # Definindo o estilo da fonte para negrito
        button_font = ('Arial', 10, 'bold')

        # Adicionando botões à top navigation bar
        self.botao_minhas_casas_nav = tk.Button(self.navbar_frame, text="Minhas Casas", command=self.ir_para_minha_casa,
                                                bg="orange", fg="white", font=button_font)
        self.botao_minhas_casas_nav.pack(side=tk.LEFT, padx=5, pady=5)

        self.botao_meus_pagamentos_nav = tk.Button(self.navbar_frame, text="Meus Pagamentos", command=self.ir_para_meus_pagamentos, bg="orange", fg="white", font=button_font)
        self.botao_meus_pagamentos_nav.pack(side=tk.LEFT, padx=5, pady=5)

        self.botao_meus_contratos_nav = tk.Button(self.navbar_frame, text="Meus Contratos",
                                                  command=self.ir_para_meus_contratos, bg="orange", fg="white",
                                                  font=button_font)
        self.botao_meus_contratos_nav.pack(side=tk.LEFT, padx=5, pady=5)

        self.botao_casa_nav = tk.Button(self.navbar_frame, text="Cadastrar Casa", command=self.ir_para_casa,
                                        bg="orange", fg="white", font=button_font)
        self.botao_casa_nav.pack(side=tk.LEFT, padx=5, pady=5)

        self.botao_pagamento_nav = tk.Button(self.navbar_frame, text="Cadastrar Pagamento",
                                             command=self.ir_para_pagamento, bg="orange", fg="white", font=button_font)
        self.botao_pagamento_nav.pack(side=tk.LEFT, padx=5, pady=5)

        self.botao_contrato_nav = tk.Button(self.navbar_frame, text="Cadastrar Contrato", command=self.ir_para_contrato,
                                            bg="orange", fg="white", font=button_font)
        self.botao_contrato_nav.pack(side=tk.LEFT, padx=5, pady=5)

        # Remover o botão de logout daqui
        # self.botao_logout_nav = tk.Button(self.topbar, text="Logout", command=self.logout, bg="#ff9999", fg="white",font=button_font)
        # self.botao_logout_nav.pack(side=tk.RIGHT, padx=10, pady=5)

        # Frame para organizar os labels
        self.details_frame = tk.Frame(master, bg="white")
        self.details_frame.pack( anchor="w")

        # Título com o texto de boas-vindas
        self.titulo = tk.Label(self.details_frame,
                               text=f"Bem-vindo",
                               anchor="w",
                               bg="white",
                               font=('Arial', 12, 'bold'),
                               fg="lightblue")
        self.titulo.grid(row=0, column=0, columnspan=2, padx=10, sticky="w")

        # Criando um frame para os detalhes do usuário (nome e email)
        self.details_frame = tk.Frame(master, bg="white")
        self.details_frame.pack(pady=10, anchor="w")

        # Labels para Nome e Sobrenome na primeira linha
        self.label_nome = tk.Label(self.details_frame,
                                   text=f"Nome: {nome_usuario}",
                                   anchor="w", bg="white",
                                   font=('Arial', 10, 'bold'))
        self.label_nome.grid(row=0, column=0, padx=10, pady=2, sticky="w")

        self.label_sobrenome = tk.Label(self.details_frame,
                                        text=f"Sobrenome: {sobrenome_usuario}",
                                        anchor="w",
                                        bg="white",
                                        font=('Arial', 10, 'bold'))
        self.label_sobrenome.grid(row=0, column=1, padx=10, pady=2, sticky="w")

        # Labels para Email e CPF na segunda linha
        self.label_email = tk.Label(self.details_frame,
                                    text=f"Email: {email_usuario}",
                                    anchor="w",
                                    bg="white",
                                    font=('Arial', 10, 'bold'))
        self.label_email.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.label_cpf = tk.Label(self.details_frame, text=f"CPF: {cpf}", anchor="w", bg="white",
                                  font=('Arial', 10, 'bold'))
        self.label_cpf.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.user_frame = tk.Frame(master, bg="white")
        self.user_frame.pack(pady=20, anchor="w")
        # Adicionando o texto "Agenda de Contratos"
        self.label_agenda = tk.Label(self.user_frame, text="Agenda de Contratos", anchor="w", bg="white",
                                     font=('Arial', 14), fg="lightblue")
        self.label_agenda.pack(fill=tk.X, anchor="w", padx=10, )

        # Adicionando o calendário
        self.calendar_frame = tk.Frame(master, bg="white")  # Definindo o tamanho do frame
        self.calendar_frame.pack(anchor="w", padx=10, pady=10)

        self.calendar = Calendar(self.calendar_frame, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendar.pack()

        # Alterando a cor do calendário
        self.calendar.config(
            background='white',
            foreground='black',
            headersbackground='lightblue',
            headersforeground='black'
        )
        self.calendar.pack()

        self.contrato_info_frame = tk.Frame(master, bg="white")
        self.contrato_info_frame.pack(pady=20, anchor="w")

        self.contract_details = {}

        self.mostrar_eventos_calendario(user_id)

        # Bind evento de clique no calendário
        self.calendar.bind("<<CalendarSelected>>", self.mostrar_detalhes_contrato)

        # Criar um frame para o conteúdo
        self.frame = tk.Frame(master, bg="white")
        self.frame.pack(expand=True, fill=tk.BOTH)

        # Adiciona o título com informações do usuário
        self.titulo = tk.Label(self.frame, text=f"Bem-vindo, {nome_usuario} {sobrenome_usuario}", font=('Arial', 16, 'bold'), bg="lightblue")
        self.titulo.pack(pady=10)

        # Adiciona o rótulo para o valor total dos contratos
        self.label_total_contratos = tk.Label(self.frame, text="", font=('Arial', 14), bg="white")
        self.label_total_contratos.pack(pady=10)

        self.label_quantidade_contratos = tk.Label(self.frame, text="", font=('Arial', 14), bg="white")
        self.label_quantidade_contratos.pack(pady=10)

        # Atualiza o valor total dos contratos
        self.atualizar_valor_total_contratos()

    def atualizar_valor_total_contratos(self):
        try:
            authenticated_user = get_authenticated_user()
            if not authenticated_user:
                raise Exception("Usuário não autenticado")

            usuario_id = authenticated_user.id

            # Consulta para calcular o valor total dos contratos do usuário
            total_valor_contratos = (
                session.query(func.sum(Contrato.valor_total))
                .filter(Contrato.usuario_id == usuario_id)
                .scalar()
            )

            quantidade_contratos = (
                session.query(func.count(Contrato.id))
                .filter(Contrato.usuario_id == usuario_id)
                .scalar()
            )

            # Se não houver contratos, total_valor_contratos será None, então definimos como 0
            if total_valor_contratos is None:
                total_valor_contratos = 0

            self.label_total_contratos.config(text=f"Valor total dos contratos: R${total_valor_contratos:,.2f}")
            self.label_quantidade_contratos.config(text=f"Quantidade total de contratos: {quantidade_contratos}")


        except Exception as e:
            print(f"Erro ao calcular o valor total dos contratos: {e}")
        finally:
            session.close()

    def editar_informacoes(self):
        from EditarInfosUser import EditarInformacoes
        EditarInformacoes(self.master, self.nome_usuario, self.email_usuario, self.cpf, self.atualizar_informacoes, self.sobrenome_usuario, self.user_id)

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
                self.calendar.calevent_create(contrato.dt_termino, 'Fim Contrato', 'end')

                # Adiciona detalhes do contrato ao dicionário (usado ao clicar na data)
                self.contract_details[contrato.dt_inicio.strftime('%Y-%m-%d')] = contrato
                self.contract_details[contrato.dt_termino.strftime('%Y-%m-%d')] = contrato
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar contratos: {str(e)}")

    def arredondar_imagem(self, imagem):
        # Criar uma máscara circular
        mask = Image.new('L', imagem.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + imagem.size, fill=255)

        # Aplicar a máscara à imagem
        imagem_arredondada = ImageOps.fit(imagem, mask.size, centering=(0.5, 0.5))
        imagem_arredondada.putalpha(mask)
        return imagem_arredondada

    def mostrar_menu_suspenso(self, event):
        self.menu_suspenso.post(event.x_root, event.y_root)

    def logout(self):
        resposta = messagebox.askquestion("Confirmação", "Tem certeza de que deseja fazer logout?", icon='warning')
        if resposta == 'yes':
            self.master.destroy()  # Fecha a janela principal
            # Inicializa a tela de login
            PaginaLogin()
        else:
            pass


    def ir_para_pagamento(self):
        janela_pagamento = tk.Toplevel(self.master)
        pagina_pagamento = PaginaPagamento(janela_pagamento)

    def ir_para_meus_contratos(self):
        janela_contrato = tk.Toplevel(self.master)
        pagina_contrato = meus_contratos(janela_contrato)

    def ir_para_meus_pagamentos(self):
        janela_pagamento = tk.Toplevel(self.master)
        pagina_pagamento = meus_pagamentos(janela_pagamento)

    def ir_para_minha_casa(self):
        janela_minha_casa = tk.Toplevel(self.master)
        pagina_minha_casa = minhas_casas(janela_minha_casa)

    def ir_para_contrato(self):
        janela_pagamento = tk.Toplevel(self.master)
        pagina_pagamento = Contratos(janela_pagamento)

    def ir_para_casa(self):
        janela_casa = tk.Toplevel(self.master)
        pagina_casa = Cadastro_Casas(janela_casa)


    def atualizar_informacoes(self, novo_nome, novo_email, novo_cpf, novo_sobrenome):
        self.nome_usuario = novo_nome
        self.email_usuario = novo_email
        self.cpf = novo_cpf
        self.sobrenome_usuario = novo_sobrenome

        self.label_nome.config(text=f"Nome: {self.nome_usuario}")
        self.label_email.config(text=f"Email: {self.email_usuario}")
        self.label_sobrenome.config(text=f"Sobrenome: {self.sobrenome_usuario}")
        self.label_cpf.config(text=f"CPF: {self.cpf}")
