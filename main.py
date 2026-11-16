import threading
import time
import random

NUM_FILOSOFOS = 5

class Filosofo(threading.Thread):
    def __init__(self, id_filosofo, garfo_esquerdo, garfo_direito):
        super().__init__()
        self.id = id_filosofo
        self.garfo_esquerdo = garfo_esquerdo
        self.garfo_direito = garfo_direito

    def run(self):
        for ciclo in range(1, 4):
            self.pensar()
            self.comer(ciclo)

    def pensar(self):
        print(f"Filósofo {self.id} está PENSANDO.")
        time.sleep(random.uniform(0.5, 1.5))

    def comer(self, ciclo):
        print(f"Filósofo {self.id} está com FOME (ciclo {ciclo}).")

        if self.id == NUM_FILOSOFOS - 1:
            primeiro_garfo = self.garfo_direito
            segundo_garfo = self.garfo_esquerdo
        else:
            primeiro_garfo = self.garfo_esquerdo
            segundo_garfo = self.garfo_direito

        primeiro_garfo.acquire()
        print(f"-> Filósofo {self.id} pegou o primeiro garfo.")

        segundo_garfo.acquire()
        print(f"--> Filósofo {self.id} pegou o segundo garfo e está COMENDO.")
        
        time.sleep(random.uniform(0.5, 1.0))

        segundo_garfo.release()
        primeiro_garfo.release()
        print(f"<-- Filósofo {self.id} terminou de comer, devolveu os garfos e voltou a pensar.")

def main():
    print(f"--- Iniciando a simulação do Jantar dos Filósofos ({NUM_FILOSOFOS} participantes) ---\n")

    garfos = [threading.Lock() for _ in range(NUM_FILOSOFOS)]

    filosofos = []
    for i in range(NUM_FILOSOFOS):
        filosofo = Filosofo(
            id_filosofo=i,
            garfo_esquerdo=garfos[i],
            garfo_direito=garfos[(i + 1) % NUM_FILOSOFOS]
        )
        filosofos.append(filosofo)
        filosofo.start()

    for filosofo in filosofos:
        filosofo.join()

    print("\n--- Simulação finalizada com sucesso! Todos os filósofos comeram. ---")

if __name__ == "__main__":
    main()