import tkinter as tk
from tkinter import ttk, messagebox
from Pagamento import PaginaPagamento
from Casa import Cadastro_Casas, get_mostrar_casas, excluir_casa
from Contrato import Contratos
from Projeto.build.models.models import Casa, Base
from sqlalchemy.orm import sessionmaker
from connection import engine

Session = sessionmaker(bind=engine)
session = Session()
class minhas_casas:
    def __init__(self, master):
    # Adicionando a tabela de casas
        self.master = master
        self.tree = ttk.Treeview(master, columns=("ID", "Quartos", "Banheiros", "Área", "Aluguel", "Descrição"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Quartos", text="Quartos")
        self.tree.heading("Banheiros", text="Banheiros")
        self.tree.heading("Área", text="Área")
        self.tree.heading("Aluguel", text="Aluguel")
        self.tree.heading("Descrição", text="Descrição")
        self.tree.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        # Definindo a largura das colunas
        self.tree.column("ID", width=50)
        self.tree.column("Quartos", width=50)
        self.tree.column("Banheiros", width=50)
        self.tree.column("Área", width=50)
        self.tree.column("Aluguel", width=50)
        self.tree.column("Descrição", width=100)

    # Criando os botões de Excluir e Atualizar
        self.frame_botoes = tk.Frame(master)
        self.frame_botoes.pack(pady=10)

        self.botao_excluir = tk.Button(self.frame_botoes, text="Excluir Casa", command=self.excluir_casa_selecionada,
                                       bg="red", fg="white")
        self.botao_excluir.pack(side=tk.LEFT, padx=5)

        self.botao_atualizar = tk.Button(self.frame_botoes, text="Atualizar Casa", command=self.atualizar_casa, bg="green",
                                         fg="white")
        self.botao_atualizar.pack(side=tk.LEFT, padx=5)

        self.mostrar_casas()
    def mostrar_casas(self):
        try:
            casas = get_mostrar_casas()

            # Exibe as informações de cada casa na tabela
            for casa in casas:
                self.tree.insert("", "end", values=(casa.id, casa.num_quartos, casa.num_banheiros,
                                                    casa.metro_quadrado, casa.valor_aluguel_mensal, casa.descricao))
        except Exception as e:
            print(f"Erro ao mostrar as casas: {str(e)}")

    def excluir_casa_selecionada(self):
        try:
            selected_item = self.tree.selection()[0]  # Captura o item selecionado
            casa_id = self.tree.item(selected_item, "values")[0]  # Captura o ID da casa selecionada

            # Excluir a casa do banco de dados
            excluir_casa(casa_id)

            # Remove a casa da tabela
            self.tree.delete(selected_item)

            messagebox.showinfo("Sucesso", "Casa excluída com sucesso!")
        except IndexError:
            messagebox.showwarning("Seleção inválida", "Por favor, selecione uma casa para excluir.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir a casa: {str(e)}")

    def atualizar_casa(self):
        try:
            selected_item = self.tree.selection()[0]  # Captura o item selecionado
            casa_id = self.tree.item(selected_item, "values")[0]

            casa = session.query(Casa).filter_by(id=casa_id).first()

            if casa:
                self.janela_atualizar = tk.Toplevel(self.master)
                self.janela_atualizar.title("Atualizar Casa")

                tk.Label(self.janela_atualizar, text="Quartos").grid(row=0, column=0)
                self.entry_quartos = tk.Entry(self.janela_atualizar)
                self.entry_quartos.grid(row=0, column=1)
                self.entry_quartos.insert(0, str(casa.num_quartos))

                tk.Label(self.janela_atualizar, text="Banheiros").grid(row=1, column=0)
                self.entry_banheiros = tk.Entry(self.janela_atualizar)
                self.entry_banheiros.grid(row=1, column=1)
                self.entry_banheiros.insert(0, str(casa.num_banheiros))

                tk.Label(self.janela_atualizar, text="Área").grid(row=2, column=0)
                self.entry_area = tk.Entry(self.janela_atualizar)
                self.entry_area.grid(row=2, column=1)
                self.entry_area.insert(0, str(casa.metro_quadrado))

                tk.Label(self.janela_atualizar, text="Aluguel").grid(row=3, column=0)
                self.entry_aluguel = tk.Entry(self.janela_atualizar)
                self.entry_aluguel.grid(row=3, column=1)
                self.entry_aluguel.insert(0, str(casa.valor_aluguel_mensal))

                tk.Button(self.janela_atualizar, text="Salvar", command=lambda: self.salvar_atualizacao(casa_id)).grid(
                    row=4, column=0, columnspan=2)

            else:
                print("Casa não encontrada.")
        except IndexError:
            print("Nenhuma casa selecionada.")

    def salvar_atualizacao(self, casa_id):
        try:
            casa = session.query(Casa).filter_by(id=casa_id).first()

            if casa:
                casa.num_quartos = int(self.entry_quartos.get())
                casa.num_banheiros = int(self.entry_banheiros.get())
                casa.metro_quadrado = float(self.entry_area.get())
                casa.valor_aluguel_mensal = float(self.entry_aluguel.get())

                session.commit()

                self.tree.item(self.tree.selection()[0], values=(
                casa.id, casa.num_quartos, casa.num_banheiros, casa.metro_quadrado, casa.valor_aluguel_mensal))
                print("Casa atualizada com sucesso!")

                self.janela_atualizar.destroy()
            else:
                print("Casa não encontrada.")
        except Exception as e:
            session.rollback()
            print(f"Erro ao atualizar casa: {str(e)}")
