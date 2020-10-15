from flask_restx import reqparse, inputs


def repository_args():
    """
    Query params para o endpoint de busca de repositório
    """
    parser = reqparse.RequestParser()
    parser.add_argument(
        "save_data",
        type=inputs.boolean,
        required=True,
        help="Armazena no banco de dados os dados coletado do github?",
        location="args",
    )
    return parser.parse_args()


def repository_list_args():
    """
    Query params para o endpoint de listagem de repositórios
    """
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username",
        required=True,
        type=str,
        help="Usuário do github",
        location="args",
    )
    parser.add_argument(
        "from_local",
        type=inputs.boolean,
        default=False,
        help="Pegar dados local ou do github diretamente?",
        location="args",
    )
    return parser.parse_args()
