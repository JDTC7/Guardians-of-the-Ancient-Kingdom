"""personajes.py - Clases del juego Guardians of the Ancient Kingdom."""

from abc import ABC, abstractmethod


class Personaje(ABC):
    """Clase base (abstracta). Todos los héroes comparten estos datos."""

    def __init__(self, nombre, vida, ataque, defensa):
        self.set_nombre(nombre)
        self.set_vida(vida)
        self.set_ataque(ataque)
        self.set_defensa(defensa)

    def get_nombre(self):
        return self._nombre

    def set_nombre(self, valor):
        if not isinstance(valor, str) or valor.strip() == "":
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor.strip()

    def get_vida(self):
        return self._vida

    def set_vida(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool) or valor < 0 or valor > 100:
            raise ValueError("La vida debe ser un entero entre 0 y 100.")
        self._vida = valor

    def get_ataque(self):
        return self._ataque

    def set_ataque(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
            raise ValueError("El ataque debe ser un entero positivo.")
        self._ataque = valor

    def get_defensa(self):
        return self._defensa

    def set_defensa(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool) or valor < 0:
            raise ValueError("La defensa no puede ser negativa.")
        self._defensa = valor

    def recibir_danio(self, cantidad):
        if cantidad < 0:
            raise ValueError("El daño no puede ser negativo.")
        danio_real = min(cantidad, self._vida)
        self._vida = self._vida - danio_real
        return danio_real

    def esta_vivo(self):
        return self._vida > 0

    def mostrar_estado(self):
        return f"{self.get_nombre()} | Vida: {self.get_vida()} | Ataque: {self.get_ataque()} | Defensa: {self.get_defensa()}"

    def validar_ataque(self, objetivo):
        """Revisa que el ataque sea válido antes de ejecutarlo."""
        if not isinstance(objetivo, Personaje):
            raise ValueError("El objetivo no es un personaje válido.")
        if not self.esta_vivo():
            raise ValueError(f"{self.get_nombre()} está derrotado y no puede atacar.")
        if not objetivo.esta_vivo():
            raise ValueError(f"{objetivo.get_nombre()} ya está derrotado.")

    @abstractmethod
    def atacar(self, objetivo):
        pass

class Guerrero(Personaje):
    """Golpe poderoso: ataque + 20% antes de restar la defensa."""

    def atacar(self, objetivo):
        self.validar_ataque(objetivo)
        ataque_potenciado = (self.get_ataque() * 6) // 5   # ataque x 1.20 redondeado hacia abajo
        danio = max(0, ataque_potenciado - objetivo.get_defensa())
        return objetivo.recibir_danio(danio)


class Mago(Personaje):
    """Hechizo penetrante: ignora la defensa."""

    def atacar(self, objetivo):
        self.validar_ataque(objetivo)
        return objetivo.recibir_danio(self.get_ataque())


class Arquero(Personaje):
    """Disparo crítico: si el ataque supera la defensa, daño doble."""

    def atacar(self, objetivo):
        self.validar_ataque(objetivo)
        if self.get_ataque() > objetivo.get_defensa():
            danio = (self.get_ataque() - objetivo.get_defensa()) * 2
        else:
            danio = 0
        return objetivo.recibir_danio(danio)


class Combate:
    """Controla los turnos y decide el resultado. Recibe dos personajes ya creados."""

    def __init__(self, personaje1, personaje2):
        self.personaje1 = personaje1
        self.personaje2 = personaje2
        self.atacante = personaje1      # quien ataca ahora
        self.defensor = personaje2
        self.rondas = 0
        self.ganador = None
        self.resultado = ""             # "victoria", "empate tecnico" o "empate"

    def cambiar_turno(self):
        self.atacante, self.defensor = self.defensor, self.atacante

    def verificar_ganador(self):
        if not self.personaje1.esta_vivo():
            return self.personaje2
        if not self.personaje2.esta_vivo():
            return self.personaje1
        return None

    def iniciar(self):
        print("=== INICIO DEL COMBATE ===")
        print(self.personaje1.mostrar_estado())
        print(self.personaje2.mostrar_estado())

        while self.resultado == "":
            self.rondas += 1
            danio_ronda = 0

            for _ in range(2):  # cada personaje ataca una vez por ronda
                danio = self.atacante.atacar(self.defensor)  # polimorfismo
                danio_ronda += danio
                print(f"\n{self.atacante.get_nombre()} ataca a {self.defensor.get_nombre()}: {danio} de daño")
                print(self.personaje1.mostrar_estado())
                print(self.personaje2.mostrar_estado())

                self.ganador = self.verificar_ganador()
                if self.ganador is not None:
                    break
                self.cambiar_turno()

            if self.ganador is not None:
                self.resultado = "victoria"
            elif danio_ronda == 0:
                self.resultado = "empate tecnico"
            elif self.rondas == 50:
                self.resultado = "empate"

        self.mostrar_resultado()

    def mostrar_resultado(self):
        print("\n=== RESULTADO ===")
        if self.resultado == "victoria":
            print(f"Ganador: {self.ganador.get_nombre()}")
        elif self.resultado == "empate tecnico":
            print("Empate técnico: una ronda sin daño.")
        else:
            print("Empate: se completaron 50 rondas sin ganador.")