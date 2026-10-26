import pytest
from personajes import Guerrero, Mago, Arquero, Combate


# Creación de personajes válidos

def test_creacion_personajes_validos():
    g = Guerrero("Aragorn", 95, 32, 18)
    m = Mago("Merlín", 70, 38, 8)
    a = Arquero("Robin", 85, 34, 12)
    assert g.get_nombre() == "Aragorn" and g.get_vida() == 95
    assert m.get_ataque() == 38 and m.get_defensa() == 8
    assert a.get_vida() == 85 and a.esta_vivo()


# Rechazo de valores incorrectos

@pytest.mark.parametrize("vida", [101, -5])
def test_vida_invalida(vida):
    with pytest.raises(ValueError):
        Guerrero("Test", vida, 30, 10)


def test_nombre_vacio():
    with pytest.raises(ValueError):
        Mago("   ", 50, 30, 10)


def test_ataque_invalido():
    with pytest.raises(ValueError):
        Arquero("Test", 50, 0, 10)


def test_defensa_invalida():
    with pytest.raises(ValueError):
        Arquero("Test", 50, 20, -1)


# Daño de cada clase

def test_dano_guerrero():
    atacante = Guerrero("G", 100, 36, 20)
    objetivo = Mago("O", 80, 10, 10)
    assert atacante.atacar(objetivo) == 33


def test_dano_mago_ignora_defensa():
    atacante = Mago("M", 80, 45, 10)
    objetivo = Guerrero("O", 100, 10, 25)
    assert atacante.atacar(objetivo) == 45


def test_dano_arquero_critico():
    atacante = Arquero("A", 90, 38, 15)
    objetivo = Guerrero("O", 100, 10, 14)
    assert atacante.atacar(objetivo) == 48


def test_arquero_sin_dano_si_ataque_no_supera_defensa():
    atacante = Arquero("A", 90, 10, 15)
    objetivo = Guerrero("O", 100, 10, 20)
    assert atacante.atacar(objetivo) == 0


# Vida nunca negativa

def test_vida_nunca_negativa():
    p = Guerrero("Debil", 20, 10, 5)
    recibido = p.recibir_danio(50)
    assert p.get_vida() == 0
    assert recibido == 20
    assert not p.esta_vivo()


def test_danio_negativo_rechazado():
    p = Guerrero("P", 50, 10, 5)
    with pytest.raises(ValueError):
        p.recibir_danio(-1)


# Derrotado no puede atacar

def test_derrotado_no_puede_atacar():
    debil = Guerrero("Debil", 20, 10, 5)
    sano = Mago("Sano", 80, 40, 10)
    debil.recibir_danio(50)
    with pytest.raises(ValueError):
        debil.atacar(sano)


def test_no_se_puede_atacar_a_un_derrotado():
    debil = Guerrero("Debil", 20, 10, 5)
    sano = Mago("Sano", 80, 40, 10)
    debil.recibir_danio(50)
    with pytest.raises(ValueError):
        sano.atacar(debil)


# Resultado de los combates

def test_combate_con_ganador():
    aragorn = Guerrero("Aragorn", 95, 32, 18)
    merlin = Mago("Merlín", 70, 38, 8)
    combate = Combate(aragorn, merlin)
    combate.iniciar()
    assert combate.resultado == "victoria"
    assert combate.ganador is aragorn
    assert aragorn.get_vida() == 19


def test_combate_ejemplo_del_enunciado_gana_gandalf():
    arthas = Guerrero("Arthas", 100, 30, 20)
    gandalf = Mago("Gandalf", 80, 40, 10)
    combate = Combate(arthas, gandalf)
    combate.iniciar()
    assert combate.ganador is gandalf
    assert gandalf.get_vida() == 2


def test_empate_tecnico():
    t1 = Guerrero("Tanque1", 100, 1, 60)
    t2 = Arquero("Tanque2", 100, 12, 60)
    combate = Combate(t1, t2)
    combate.iniciar()
    assert combate.resultado == "empate tecnico"
    assert combate.ganador is None
