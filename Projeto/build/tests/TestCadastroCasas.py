import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from unittest.mock import patch, MagicMock
from Projeto.build.Casa import Cadastro_Casas, Casa, get_authenticated_user

import pytest


@pytest.fixture



@pytest.mark.usefixtures("mock_tkinter_root")
@patch('Projeto.build.Casa.get_authenticated_user')
@patch('Projeto.build.Casa.session')
def test_cadastrar_casa(mock_session, mock_get_authenticated_user, mock_tkinter_root):
    # Mock do usuário autenticado
    mock_usuario = MagicMock()
    mock_usuario.id = 1
    mock_get_authenticated_user.return_value = mock_usuario

    # Mock da sessão do banco de dados
    mock_db_session = MagicMock()
    mock_session.return_value = mock_db_session

    # Criar a instância do aplicativo
    app = Cadastro_Casas(mock_tkinter_root)

    # Preencher os campos de entrada com dados de teste
    app.entry_num_quarto.insert(0, "3")
    app.entry_num_banheiro.insert(0, "2")
    app.entry_metro_quadrado.insert(0, "120.5")
    app.entry_preco_mensal.insert(0, "1500.0")
    app.entry_descricao.insert(0, "Casa de teste")

    # Chamar o método a ser testado
    app.cadastrar_casa()

    # Verificar se a casa foi adicionada à sessão e comitada
    assert mock_db_session.add.called
    assert mock_db_session.commit.called

    # Verificar o objeto Casa criado
    casa_adicionada = mock_db_session.add.call_args[0][0]
    assert casa_adicionada.num_quartos == 3
    assert casa_adicionada.num_banheiros == 2
    assert casa_adicionada.metro_quadrado == 120.5
    assert casa_adicionada.valor_aluguel_mensal == 1500.0
    assert casa_adicionada.descricao == "Casa de teste"
    assert casa_adicionada.usuario_id == 1
