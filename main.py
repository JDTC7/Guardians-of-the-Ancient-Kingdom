from personajes import Guerrero, Mago, Arquero, Combate


def debe_fallar(descripcion, funcion):
    """Ejecuta funcion y verifica que lance ValueError."""
    try:
        funcion()
        print(f"ERROR: {descripcion} debió ser rechazado")
    except ValueError as error:
        print(f"Correcto: {descripcion} rechazado -> {error}")


print("1. Creación de personajes")
aragorn = Guerrero("Aragorn", 95, 32, 18)
merlin = Mago("Merlín", 70, 38, 8)
robin = Arquero("Robin", 85, 34, 12)

print(aragorn.mostrar_estado())
print(merlin.mostrar_estado())
print(robin.mostrar_estado())


print("\n2. Vida inválida")
debe_fallar("vida 101", lambda: Guerrero("Test", 101, 30, 10))
debe_fallar("vida -5", lambda: Guerrero("Test", -5, 30, 10))


print("\n3. Nombre vacío")
debe_fallar("nombre vacío", lambda: Mago("   ", 50, 30, 10))


print("\n4. Ataque y defensa inválidos")
debe_fallar("ataque 0", lambda: Arquero("Test", 50, 0, 10))
debe_fallar("defensa -1", lambda: Arquero("Test", 50, 20, -1))


print("\n5. Habilidad del Guerrero")
atacante = Guerrero("Guerrero", 100, 36, 20)
objetivo = Mago("Objetivo", 80, 10, 10)
danio = atacante.atacar(objetivo)
print("Ataque 36 vs defensa 10 -> daño", danio, "(esperado 33)")


print("\n6. Habilidad del Mago")
atacante = Mago("Mago", 80, 45, 10)
objetivo = Guerrero("Objetivo", 100, 10, 25)
danio = atacante.atacar(objetivo)
print("Ataque 45 vs defensa 25 -> daño", danio, "(esperado 45)")


print("\n7. Habilidad del Arquero")
atacante = Arquero("Arquero", 90, 38, 15)
objetivo = Guerrero("Objetivo", 100, 10, 14)
danio = atacante.atacar(objetivo)
print("Ataque 38 vs defensa 14 -> daño", danio, "(esperado 48)")


print("\n8. La vida nunca es negativa")
debil = Guerrero("Debil", 20, 10, 5)
debil.recibir_danio(50)
print("Vida después de recibir 50 de daño:", debil.get_vida(), "(esperado 0)")


print("\n9. Un derrotado no puede atacar ni ser atacado")
sano = Mago("Sano", 80, 40, 10)
debe_fallar("derrotado atacando", lambda: debil.atacar(sano))
debe_fallar("atacar a un derrotado", lambda: sano.atacar(debil))


print("\n10 y 11. Combate completo y ganador")
heroe1 = Guerrero("Aragorn", 95, 32, 18)
heroe2 = Mago("Merlín", 70, 38, 8)
combate = Combate(heroe1, heroe2)
combate.iniciar()


print("\n12. Empate técnico")
tanque1 = Guerrero("Tanque1", 100, 1, 60)
tanque2 = Arquero("Tanque2", 100, 12, 60)
combate2 = Combate(tanque1, tanque2)
combate2.iniciar()
