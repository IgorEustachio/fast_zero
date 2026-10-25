from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    # arrange está dentro de conftest, definindo o client
    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá Mundo!'}  # Assert
