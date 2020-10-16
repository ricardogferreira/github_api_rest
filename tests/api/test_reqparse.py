from unittest import mock

from flask_restx import inputs

from app.api.reqparse import repository_args, repository_list_args


def test_repository_args_validate_args(mocker):
    RequestParserMock = mock.MagicMock()
    add_argument_mock = mock.MagicMock()
    parse_args_mock = mock.MagicMock()
    RequestParserMock.add_argument = add_argument_mock
    RequestParserMock.parse_args = parse_args_mock

    mocker.patch("flask_restx.reqparse.RequestParser", return_value=RequestParserMock)

    repository_args()

    add_argument_mock.assert_called_with(
        "save_data",
        type=inputs.boolean,
        required=True,
        help="Armazena no banco de dados os dados coletado do github?",
        location="args",
    )
    parse_args_mock.assert_called()


def test_repository_list_args_validate_args(mocker):
    RequestParserMock = mock.MagicMock()
    add_argument_mock = mock.MagicMock()
    parse_args_mock = mock.MagicMock()
    RequestParserMock.add_argument = add_argument_mock
    RequestParserMock.parse_args = parse_args_mock

    mocker.patch("flask_restx.reqparse.RequestParser", return_value=RequestParserMock)

    repository_list_args()

    add_argument_mock.call_args_with(
        "username",
        required=True,
        type=str,
        help="Usuário do github",
        location="args",
    )

    add_argument_mock.call_args_with(
        "from_local",
        type=inputs.boolean,
        default=False,
        help="Pegar dados local ou do github diretamente?",
        location="args",
    )

    assert add_argument_mock.call_count, 2
    parse_args_mock.assert_called()
