# ANTIEJEMPLO EDUCATIVO: contiene antipatrones a propósito
import json
from pathlib import Path

class AppManager: 
    def __init__(self, db_path="data.json"):
        self.db_path = Path(db_path)
    
    def load_users(self):
        if not self.db_path.exists():
            return []
        return json.loads(self.db_path.read_text(encoding="utf-8"))
    
    def print_user(self, user):
        print(f"[{user.get('id')}] {user.get('name')} - tier={user.get('tier')}")
    
    def discount_for_order(self, user, total):
        # ANTIPATRÓN 1: MAGIC NUMBERS - valores hardcodeados sin constantes nombradas
        if user.get("tier") == "gold" and total > 100:  # 100 sin explicación
            return total * 0.15  # 0.15 sin contexto
        if user.get("tier") == "silver" and total > 42:  # 42 número arbitrario
            return total * 0.07  # 0.07 sin explicación
        return 0.0
      
    def ship_cost_domestic(self, weight, distance_km):
        # ANTIPATRÓN 1: MAGIC NUMBERS - valores sin constantes nombradas
        base = 5  # número mágico
        variable = weight * 0.25 + (distance_km / 300)  # 0.25 y 300 sin contexto
        if weight > 20:  # umbral mágico - 20 sin explicación
            variable += 3  # 3 sin justificación
        return base + variable
    
    # ANTIPATRÓN 2: COPY-PASTE PROGRAMMING - código duplicado con pequeñas variaciones
    def ship_cost_international(self, weight, distance_km):
        base = 7     # <- divergencia sutil (era 5 en domestic)
        variable = weight * 0.25 + (distance_km / 300)  # lógica duplicada
        if weight >= 20:  # >= en vez de > - inconsistencia peligrosa
            variable += 4  # <- otra divergencia sutil (era 3 en domestic)
        return base + variable
    
    # ANTIPATRÓN 3: GOD OBJECT - clase que hace demasiadas cosas
    # Esta clase maneja: persistencia (load_users), presentación (print_user),
    # lógica de negocio (discount_for_order, ship_cost_*), y orquestación (run)
    def run(self):
        users = self.load_users()
        for u in users:
            self.print_user(u)
            total = 123.45  # Magic number total ficticio - ANTIPATRÓN 1
            d = self.discount_for_order(u, total)
            print(f"Descuento calculado: {d:.2f}")
            # Uso de funciones duplicadas - ANTIPATRÓN 2
            print("Envío nacional:", self.ship_cost_domestic(12, 900))  # 12 y 900 magic numbers
            print("Envío internacional:", self.ship_cost_international(12, 900))

if __name__ == "__main__":
    AppManager().run()