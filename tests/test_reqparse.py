from flask_restx import inputs
from unittest import mock

from app.reqparse import repository_args, repository_list_args


def test_repository_args_validate_args(mocker):
    RequestParserMocked = mock.MagicMock()
    add_argument_mocked = mock.MagicMock()
    parse_args_mocked = mock.MagicMock()
    RequestParserMocked.add_argument = add_argument_mocked
    RequestParserMocked.parse_args = parse_args_mocked

    mocker.patch("flask_restx.reqparse.RequestParser", return_value=RequestParserMocked)

    repository_args()

    add_argument_mocked.assert_called_with(
        "save_data",
        type=inputs.boolean,
        required=True,
        help="Armazena no banco de dados os dados coletado do github?",
        location="args",
    )
    parse_args_mocked.assert_called()


def test_repository_list_args_validate_args(mocker):
    RequestParserMocked = mock.MagicMock()
    add_argument_mocked = mock.MagicMock()
    parse_args_mocked = mock.MagicMock()
    RequestParserMocked.add_argument = add_argument_mocked
    RequestParserMocked.parse_args = parse_args_mocked

    mocker.patch("flask_restx.reqparse.RequestParser", return_value=RequestParserMocked)

    repository_list_args()

    add_argument_mocked.call_args_with(
        "username",
        required=True,
        type=str,
        help="Usuário do github",
        location="args",
    )

    add_argument_mocked.call_args_with(
        "from_local",
        type=inputs.boolean,
        default=False,
        help="Pegar dados local ou do github diretamente?",
        location="args",
    )

    assert add_argument_mocked.call_count, 2
    parse_args_mocked.assert_called()
