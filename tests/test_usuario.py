import pytest

from dominio.usuario import Usuario



def test_nombre_vacio_lanza_error():
    with pytest.raises(ValueError) as error:
        Usuario("TEST@gmail.com", "Password123!", "")
    assert str(error.value) == "El nombre no debe estar vacio"


def test_email_sin_arroba_tira_error():
    with pytest.raises(ValueError) as error:
        Usuario("TESTgmail.com", "Password123!", "Tets")
    assert str(error.value) == "El correo debe contener un @"

def test_email_sin_dominio_lanza_error():
    with pytest.raises(ValueError) as error:
        Usuario("TEST@", "Password123!", "Test")
    assert str(error.value) == "El email no es válido"
 
 
def test_email_sin_punto_en_dominio_lanza_error():
    with pytest.raises(ValueError) as error:
        Usuario("test@gmailcom", "Password123!", "Test")
    assert str(error.value) == "El email debe tener un dominio válido como '.com' "
 

def test_password_menos_8_caracteres_lanza_error():
    with pytest.raises(ValueError) as error:
        Usuario("test@gmail.com", "Abc1!", "Test")
    assert str(error.value) == "La contraseña debe tener al menos 8 caracteres"
 
 
def test_password_sin_una_mayuscula_lanza_error():
    with pytest.raises(ValueError) as error:
        Usuario("test@gmail.com", "password123!", "Test")
    assert str(error.value) == "La contraseña debe tener al menos una mayúscula"