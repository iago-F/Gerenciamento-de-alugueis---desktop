import tkinter as tk
from tkinter import ttk, messagebox
from Pagamento import PaginaPagamento
from Casa import Cadastro_Casas, get_mostrar_casas, excluir_casa
from Contrato import Contratos
from Projeto.build.models.models import Casa, Base, Contrato
from sqlalchemy.orm import sessionmaker
from connection import engine
from auth import get_authenticated_user
from datetime import datetime

from Contrato import Contratos

Session = sessionmaker(bind=engine)
session = Session()
# class meus_contratos():
#     def __init__(self, master):
#     # Adicionando a tabela de casas
#         self.master = master
#         self.tree = ttk.Treeview(master, columns=("ID", "Data de inicio", "Data de termino", "Valor Total"), show="headings")
#         self.tree.heading("ID", text="ID")
#         self.tree.heading("Data de inicio", text="Data de inicio")
#         self.tree.heading("Data de termino", text="Data de termino")
#         self.tree.heading("Valor Total", text="Valor Total")
#         self.tree.pack(fill=tk.BOTH, expand=True)
#
#         style = ttk.Style()
#         style.configure("Treeview", rowheight=25)
#         # Definindo a largura das colunas
#         self.tree.column("ID", width=50)
#         self.tree.column("Data de inicio", width=100)
#         self.tree.column("Data de termino", width=100)
#         self.tree.column("Valor Total", width=100)
#
#
#
#         # Criando um Frame para centralizar os botões
#         self.button_frame = tk.Frame(master)
#         self.button_frame.pack(side=tk.TOP, pady=10)
#
#         self.botao_excluir = tk.Button(self.button_frame, text="Excluir Contrato",
#                                        command=self.excluir_contrato_selecionado, bg="red",
#                                        fg="white")
#         self.botao_excluir.pack(side=tk.LEFT, padx=13)
#
#         self.botao_atualizar = tk.Button(self.button_frame, text="Atualizar Contrato", command=self.atualizar_contrato,
#                                          bg="green",
#                                          fg="white")
#         self.botao_atualizar.pack(side=tk.LEFT, padx=13)
#
#         self.contract_details = {}
#
#         self.exibir_contratos()
#
#
#     def exibir_contratos(self):
#         try:
#             authenticated_user = get_authenticated_user()
#             if not authenticated_user:
#                 raise Exception("Usuário não autenticado")
#
#             usuario_id = authenticated_user.id
#             contratos = session.query(Contrato).filter_by(usuario_id=usuario_id).all()
#
#             for contrato in contratos:
#                 # Adicionando detalhes do contrato ao dicionário self.contract_details
#                 self.contract_details[contrato.dt_inicio] = contrato
#
#                 self.tree.insert("", "end",
#                                  values=(contrato.id, contrato.dt_inicio, contrato.dt_termino, contrato.valor_total))
#
#         except Exception as e:
#             messagebox.showerror("Erro", f"Erro ao mostrar os contratos: {str(e)}")
#         finally:
#             session.close()
#
#
#     def excluir_contrato_selecionado(self):
#         try:
#             selected_item = self.tree.selection()[0]
#             contrato_id = self.tree.item(selected_item, "values")[0]
#             self.excluir_contrato(contrato_id)
#             self.tree.delete(selected_item)
#             messagebox.showinfo("Sucesso", "Contrato excluído com sucesso!")
#         except IndexError:
#             messagebox.showwarning("Seleção inválida", "Por favor, selecione um contrato para excluir.")
#         except Exception as e:
#             messagebox.showerror("Erro", f"Erro ao excluir o contrato: {str(e)}")
#
#     def excluir_contrato(self, contrato_id):
#         try:
#             contrato = session.query(Contrato).filter_by(id=contrato_id).first()
#             if contrato:
#                 session.delete(contrato)
#                 session.commit()
#                 print("Contrato deletado com sucesso!")
#             else:
#                 print("Contrato não encontrado.")
#         except Exception as e:
#             session.rollback()
#             print(f"Erro ao excluir contrato: {str(e)}")
#
#     def atualizar_contrato(self):
#         try:
#             selected_item = self.tree.selection()[0]
#             contrato_id = self.tree.item(selected_item, "values")[0]
#             contrato = session.query(Contrato).filter_by(id=contrato_id).first()
#
#             if contrato:
#                 self.janela_atualizar = tk.Toplevel(self.master)
#                 self.janela_atualizar.title("Atualizar Contrato")
#
#                 tk.Label(self.janela_atualizar, text="Data de Início").grid(row=0, column=0)
#                 self.entry_dt_inicio_atualizar = tk.Entry(self.janela_atualizar)
#                 self.entry_dt_inicio_atualizar.grid(row=0, column=1)
#                 self.entry_dt_inicio_atualizar.insert(0, contrato.dt_inicio.strftime('%Y-%m-%d'))
#
#                 tk.Label(self.janela_atualizar, text="Data de Término").grid(row=1, column=0)
#                 self.entry_dt_termino_atualizar = tk.Entry(self.janela_atualizar)
#                 self.entry_dt_termino_atualizar.grid(row=1, column=1)
#                 self.entry_dt_termino_atualizar.insert(0, contrato.dt_termino.strftime('%Y-%m-%d'))
#
#                 tk.Label(self.janela_atualizar, text="Valor Total").grid(row=2, column=0)
#                 self.entry_valor_total_atualizar = tk.Entry(self.janela_atualizar)
#                 self.entry_valor_total_atualizar.grid(row=2, column=1)
#                 self.entry_valor_total_atualizar.insert(0, str(contrato.valor_total))
#
#                 tk.Button(self.janela_atualizar, text="Salvar",
#                           command=lambda: self.salvar_atualizacao(contrato_id)).grid(
#                     row=3, column=0, columnspan=2)
#             else:
#                 print("Contrato não encontrado.")
#         except IndexError:
#             print("Nenhum contrato selecionado.")
#
#     def salvar_atualizacao(self, contrato_id):
#         try:
#             contrato = session.query(Contrato).filter_by(id=contrato_id).first()
#             if contrato:
#                 contrato.dt_inicio = datetime.strptime(self.entry_dt_inicio_atualizar.get(), '%Y-%m-%d').date()
#                 contrato.dt_termino = datetime.strptime(self.entry_dt_termino_atualizar.get(), '%Y-%m-%d').date()
#                 contrato.valor_total = float(self.entry_valor_total_atualizar.get())
#                 session.commit()
#
#                 self.tree.item(self.tree.selection()[0], values=(
#                     contrato.id, contrato.dt_inicio.strftime('%Y-%m-%d'), contrato.dt_termino.strftime('%Y-%m-%d'),
#                     contrato.valor_total))
#                 print("Contrato atualizado com sucesso!")
#                 self.janela_atualizar.destroy()
#             else:
#                 print("Contrato não encontrado.")
#         except Exception as e:
#             session.rollback()
#             print(f"Erro ao atualizar contrato: {str(e)}")

class meus_contratos():
    def __init__(self, master):
        # Adicionando a tabela de casas
        self.master = master
        self.tree = ttk.Treeview(master, columns=("ID", "Data de inicio", "Data de termino", "Valor Total"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Data de inicio", text="Data de inicio")
        self.tree.heading("Data de termino", text="Data de termino")
        self.tree.heading("Valor Total", text="Valor Total")
        self.tree.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        self.tree.column("ID", width=50)
        self.tree.column("Data de inicio", width=100)
        self.tree.column("Data de termino", width=100)
        self.tree.column("Valor Total", width=100)

        # Criando um Frame para os filtros
        self.filter_frame = tk.Frame(master)
        self.filter_frame.pack(side=tk.TOP, pady=10)

        # Campos de filtro
        tk.Label(self.filter_frame, text="Data Inicial:").grid(row=0, column=0)
        self.entry_data_inicial = tk.Entry(self.filter_frame)
        self.entry_data_inicial.grid(row=0, column=1)

        tk.Label(self.filter_frame, text="Data Final:").grid(row=0, column=2)
        self.entry_data_final = tk.Entry(self.filter_frame)
        self.entry_data_final.grid(row=0, column=3)

        tk.Label(self.filter_frame, text="Valor Total:").grid(row=0, column=4)
        self.entry_valor_total = tk.Entry(self.filter_frame)
        self.entry_valor_total.grid(row=0, column=5)

        # Botão para aplicar o filtro
        self.botao_filtrar = tk.Button(self.filter_frame, text="Aplicar Filtro", command=self.aplicar_filtro)
        self.botao_filtrar.grid(row=0, column=6, padx=10)

        # Criando um Frame para centralizar os botões
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(side=tk.TOP, pady=10)

        self.botao_excluir = tk.Button(self.button_frame, text="Excluir Contrato", command=self.excluir_contrato_selecionado, bg="red", fg="white")
        self.botao_excluir.pack(side=tk.LEFT, padx=13)

        self.botao_atualizar = tk.Button(self.button_frame, text="Atualizar Contrato", command=self.atualizar_contrato, bg="green", fg="white")
        self.botao_atualizar.pack(side=tk.LEFT, padx=13)

        self.contract_details = {}

        # Chamada inicial para exibir todos os contratos sem filtro
        self.exibir_contratos()

    def exibir_contratos(self, filtros=None):
        try:
            authenticated_user = get_authenticated_user()
            if not authenticated_user:
                raise Exception("Usuário não autenticado")

            usuario_id = authenticated_user.id
            query = session.query(Contrato).filter_by(usuario_id=usuario_id)

            # Aplicando filtros, se houver
            if filtros:
                if filtros.get('data_inicial'):
                    query = query.filter(Contrato.dt_inicio >= filtros['data_inicial'])
                if filtros.get('data_final'):
                    query = query.filter(Contrato.dt_termino <= filtros['data_final'])
                if filtros.get('valor_total'):
                    query = query.filter(Contrato.valor_total == filtros['valor_total'])

            contratos = query.all()

            # Limpar a tabela antes de exibir os novos resultados
            self.tree.delete(*self.tree.get_children())

            for contrato in contratos:
                self.contract_details[contrato.dt_inicio] = contrato
                self.tree.insert("", "end", values=(contrato.id, contrato.dt_inicio, contrato.dt_termino, contrato.valor_total))

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao mostrar os contratos: {str(e)}")
        finally:
            session.close()

    def aplicar_filtro(self):
        # Coletando os dados dos filtros
        data_inicial = self.entry_data_inicial.get()
        data_final = self.entry_data_final.get()
        valor_total = self.entry_valor_total.get()

        filtros = {}
        if data_inicial:
            filtros['data_inicial'] = datetime.strptime(data_inicial, '%Y-%m-%d').date()
        if data_final:
            filtros['data_final'] = datetime.strptime(data_final, '%Y-%m-%d').date()
        if valor_total:
            filtros['valor_total'] = float(valor_total)

        # Exibindo os contratos com os filtros aplicados
        self.exibir_contratos(filtros)

    # Definindo o método excluir_contrato_selecionado corretamente
    def excluir_contrato_selecionado(self):
        try:
            selected_item = self.tree.selection()[0]
            contrato_id = self.tree.item(selected_item, "values")[0]
            self.excluir_contrato(contrato_id)
            self.tree.delete(selected_item)
            messagebox.showinfo("Sucesso", "Contrato excluído com sucesso!")
        except IndexError:
            messagebox.showwarning("Seleção inválida", "Por favor, selecione um contrato para excluir.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir o contrato: {str(e)}")

    def excluir_contrato(self, contrato_id):
        try:
            contrato = session.query(Contrato).filter_by(id=contrato_id).first()
            if contrato:
                session.delete(contrato)
                session.commit()
                print("Contrato deletado com sucesso!")
            else:
                print("Contrato não encontrado.")
        except Exception as e:
            session.rollback()
            print(f"Erro ao excluir contrato: {str(e)}")

    def atualizar_contrato(self):
        try:
            selected_item = self.tree.selection()[0]
            contrato_id = self.tree.item(selected_item, "values")[0]
            contrato = session.query(Contrato).filter_by(id=contrato_id).first()

            if contrato:
                # Cria a janela de atualização
                self.janela_atualizar = tk.Toplevel(self.master)
                self.janela_atualizar.title("Atualizar Contrato")

                # Campos para edição de Data de Início
                tk.Label(self.janela_atualizar, text="Data de Início").grid(row=0, column=0)
                self.entry_dt_inicio_atualizar = tk.Entry(self.janela_atualizar)
                self.entry_dt_inicio_atualizar.grid(row=0, column=1)
                self.entry_dt_inicio_atualizar.insert(0, contrato.dt_inicio.strftime('%Y-%m-%d'))

                # Campos para edição de Data de Término
                tk.Label(self.janela_atualizar, text="Data de Término").grid(row=1, column=0)
                self.entry_dt_termino_atualizar = tk.Entry(self.janela_atualizar)
                self.entry_dt_termino_atualizar.grid(row=1, column=1)
                self.entry_dt_termino_atualizar.insert(0, contrato.dt_termino.strftime('%Y-%m-%d'))

                # Campos para edição de Valor Total
                tk.Label(self.janela_atualizar, text="Valor Total").grid(row=2, column=0)
                self.entry_valor_total_atualizar = tk.Entry(self.janela_atualizar)
                self.entry_valor_total_atualizar.grid(row=2, column=1)
                self.entry_valor_total_atualizar.insert(0, str(contrato.valor_total))

                # Botão para salvar as alterações
                tk.Button(self.janela_atualizar, text="Salvar",
                          command=lambda: self.salvar_atualizacao(contrato_id)).grid(
                    row=3, column=0, columnspan=2)
            else:
                messagebox.showwarning("Erro", "Contrato não encontrado.")
        except IndexError:
            messagebox.showwarning("Seleção inválida", "Por favor, selecione um contrato para atualizar.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir a janela de atualização: {str(e)}")

    def salvar_atualizacao(self, contrato_id):
        try:
            # Obtém o contrato do banco de dados
            contrato = session.query(Contrato).filter_by(id=contrato_id).first()
            if contrato:
                # Atualiza os valores do contrato com base nas entradas do usuário
                contrato.dt_inicio = datetime.strptime(self.entry_dt_inicio_atualizar.get(), '%Y-%m-%d').date()
                contrato.dt_termino = datetime.strptime(self.entry_dt_termino_atualizar.get(), '%Y-%m-%d').date()
                contrato.valor_total = float(self.entry_valor_total_atualizar.get())

                # Confirma a atualização no banco de dados
                session.commit()

                # Atualiza a linha correspondente na TreeView
                self.tree.item(self.tree.selection()[0], values=(
                    contrato.id, contrato.dt_inicio.strftime('%Y-%m-%d'), contrato.dt_termino.strftime('%Y-%m-%d'),
                    contrato.valor_total))

                # Exibe mensagem de sucesso e fecha a janela de atualização
                messagebox.showinfo("Sucesso", "Contrato atualizado com sucesso!")
                self.janela_atualizar.destroy()
            else:
                messagebox.showwarning("Erro", "Contrato não encontrado.")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor válido no campo 'Valor Total'.")
        except Exception as e:
            session.rollback()
            messagebox.showerror("Erro", f"Erro ao atualizar contrato: {str(e)}")

    def popup_editar_contrato(self, contrato):
        # Aqui você pode criar um popup ou uma nova janela onde os campos de dados do contrato
        # podem ser editados e depois salvos novamente no banco de dados.
        editar_janela = tk.Toplevel(self.master)
        editar_janela.title("Atualizar Contrato")

        # Exemplos de campos que podem ser editados
        tk.Label(editar_janela, text="Data de Início:").grid(row=0, column=0)
        data_inicio_entry = tk.Entry(editar_janela)
        data_inicio_entry.grid(row=0, column=1)
        data_inicio_entry.insert(0, contrato.dt_inicio)

        tk.Label(editar_janela, text="Data de Término:").grid(row=1, column=0)
        data_termino_entry = tk.Entry(editar_janela)
        data_termino_entry.grid(row=1, column=1)
        data_termino_entry.insert(0, contrato.dt_termino)

        tk.Label(editar_janela, text="Valor Total:").grid(row=2, column=0)
        valor_total_entry = tk.Entry(editar_janela)
        valor_total_entry.grid(row=2, column=1)
        valor_total_entry.insert(0, contrato.valor_total)

        def salvar_atualizacao():
            # Lógica para salvar a atualização no banco de dados
            try:
                contrato.dt_inicio = data_inicio_entry.get()
                contrato.dt_termino = data_termino_entry.get()
                contrato.valor_total = float(valor_total_entry.get())

                session.commit()
                messagebox.showinfo("Sucesso", "Contrato atualizado com sucesso!")
                editar_janela.destroy()
            except Exception as e:
                session.rollback()
                messagebox.showerror("Erro", f"Erro ao atualizar o contrato: {str(e)}")

        # Botão de salvar
        tk.Button(editar_janela, text="Salvar", command=salvar_atualizacao).grid(row=3, column=1)

