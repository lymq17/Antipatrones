# CÓDIGO REFACTORIZADO: corrige los antipatrones identificados
import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

# ========================================
# CORRECCIÓN 1: MAGIC NUMBERS -> Constantes nombradas
# ========================================
class DiscountConfig:
    """Configuración de descuentos por tier"""
    GOLD_MIN_TOTAL = 100.0
    GOLD_DISCOUNT_RATE = 0.15
    
    SILVER_MIN_TOTAL = 42.0
    SILVER_DISCOUNT_RATE = 0.07

class ShippingConfig:
    """Configuración de costos de envío"""
    DOMESTIC_BASE_COST = 5.0
    INTERNATIONAL_BASE_COST = 7.0
    
    WEIGHT_RATE = 0.25
    DISTANCE_DIVISOR = 300.0
    
    HEAVY_WEIGHT_THRESHOLD = 20.0
    DOMESTIC_HEAVY_SURCHARGE = 3.0
    INTERNATIONAL_HEAVY_SURCHARGE = 4.0

# ========================================
# CORRECCIÓN 2: COPY-PASTE PROGRAMMING -> DRY (Don't Repeat Yourself)
# ========================================
class ShippingType(Enum):
    DOMESTIC = "domestic"
    INTERNATIONAL = "international"

class ShippingCalculator:
    """Calculadora unificada de costos de envío"""
    
    @staticmethod
    def calculate_cost(weight: float, distance_km: float, 
                      shipping_type: ShippingType) -> float:
        """
        Calcula el costo de envío usando una lógica unificada.
        Evita duplicación de código con parámetros configurables.
        """
        if shipping_type == ShippingType.DOMESTIC:
            base_cost = ShippingConfig.DOMESTIC_BASE_COST
            heavy_surcharge = ShippingConfig.DOMESTIC_HEAVY_SURCHARGE
            # Consistencia: usar > para peso doméstico
            is_heavy = weight > ShippingConfig.HEAVY_WEIGHT_THRESHOLD
        else:  # INTERNATIONAL
            base_cost = ShippingConfig.INTERNATIONAL_BASE_COST
            heavy_surcharge = ShippingConfig.INTERNATIONAL_HEAVY_SURCHARGE
            # Consistencia: usar >= para peso internacional
            is_heavy = weight >= ShippingConfig.HEAVY_WEIGHT_THRESHOLD
        
        variable_cost = (
            weight * ShippingConfig.WEIGHT_RATE + 
            distance_km / ShippingConfig.DISTANCE_DIVISOR
        )
        
        if is_heavy:
            variable_cost += heavy_surcharge
        
        return base_cost + variable_cost

# ========================================
# CORRECCIÓN 3: GOD OBJECT -> Separación de Responsabilidades
# ========================================

@dataclass
class User:
    """Modelo de datos de usuario"""
    id: int
    name: str
    tier: str

class UserRepository:
    """Responsabilidad: Persistencia de datos"""
    
    def __init__(self, db_path: str = "data.json"):
        self.db_path = Path(db_path)
    
    def load_all(self) -> List[User]:
        """Carga usuarios desde el archivo JSON"""
        if not self.db_path.exists():
            return []
        
        data = json.loads(self.db_path.read_text(encoding="utf-8"))
        return [User(**user_data) for user_data in data]

class DiscountService:
    """Responsabilidad: Lógica de negocio de descuentos"""
    
    @staticmethod
    def calculate_discount(user: User, total: float) -> float:
        """Calcula el descuento aplicable según el tier del usuario"""
        if user.tier == "gold" and total > DiscountConfig.GOLD_MIN_TOTAL:
            return total * DiscountConfig.GOLD_DISCOUNT_RATE
        
        if user.tier == "silver" and total > DiscountConfig.SILVER_MIN_TOTAL:
            return total * DiscountConfig.SILVER_DISCOUNT_RATE
        
        return 0.0

class UserPresenter:
    """Responsabilidad: Presentación de datos"""
    
    @staticmethod
    def print_user(user: User) -> None:
        """Imprime información del usuario"""
        print(f"[{user.id}] {user.name} - tier={user.tier}")
    
    @staticmethod
    def print_discount(discount: float) -> None:
        """Imprime el descuento calculado"""
        print(f"Descuento calculado: {discount:.2f}")
    
    @staticmethod
    def print_shipping(label: str, cost: float) -> None:
        """Imprime el costo de envío"""
        print(f"{label}: {cost:.2f}")

class ApplicationController:
    """Responsabilidad: Orquestación y control de flujo"""
    
    def __init__(self, user_repository: UserRepository,
                 discount_service: DiscountService,
                 shipping_calculator: ShippingCalculator,
                 presenter: UserPresenter):
        self.user_repo = user_repository
        self.discount_service = discount_service
        self.shipping_calculator = shipping_calculator
        self.presenter = presenter
    
    def run(self) -> None:
        """Ejecuta el flujo principal de la aplicación"""
        # Constantes para el ejemplo
        SAMPLE_ORDER_TOTAL = 123.45
        SAMPLE_WEIGHT = 12.0
        SAMPLE_DISTANCE = 900.0
        
        users = self.user_repo.load_all()
        
        for user in users:
            self.presenter.print_user(user)
            
            # Calcular descuento
            discount = self.discount_service.calculate_discount(
                user, SAMPLE_ORDER_TOTAL
            )
            self.presenter.print_discount(discount)
            
            # Calcular costos de envío
            domestic_cost = self.shipping_calculator.calculate_cost(
                SAMPLE_WEIGHT, SAMPLE_DISTANCE, ShippingType.DOMESTIC
            )
            self.presenter.print_shipping("Envío nacional", domestic_cost)
            
            international_cost = self.shipping_calculator.calculate_cost(
                SAMPLE_WEIGHT, SAMPLE_DISTANCE, ShippingType.INTERNATIONAL
            )
            self.presenter.print_shipping("Envío internacional", international_cost)
            
            print()  # Separador visual

# ========================================
# PUNTO DE ENTRADA
# ========================================
if __name__ == "__main__":
    # Inyección de dependencias manual (podría usar un DI container)
    user_repo = UserRepository()
    discount_service = DiscountService()
    shipping_calculator = ShippingCalculator()
    presenter = UserPresenter()
    
    app = ApplicationController(
        user_repo,
        discount_service,
        shipping_calculator,
        presenter
    )
    
    app.run()