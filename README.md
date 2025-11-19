# Antipatrones
# 🔧 Refactorización de Antipatrones de Diseño

> **Proyecto Educativo:** Identificación y corrección de antipatrones comunes en Python

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Antipatrones Identificados](#-antipatrones-identificados)
- [Refactorización Detallada](#-refactorización-detallada)

---

## 📖 Descripción

Este proyecto demuestra la identificación y corrección de tres antipatrones clásicos de diseño de software:

1. **Magic Numbers** - Valores literales sin contexto
2. **Copy-Paste Programming** - Código duplicado
3. **God Object** - Clase con demasiadas responsabilidades

### Objetivo

Transformar código con antipatrones en código limpio, mantenible y profesional siguiendo principios SOLID y mejores prácticas de la industria.

---

## 🚫 Antipatrones Identificados

### 1️⃣ Magic Numbers

**Problema:** Valores hardcodeados sin significado claro

```python
# ❌ ANTES
if user.get("tier") == "gold" and total > 100:
    return total * 0.15  # ¿Qué es 100? ¿Qué es 0.15?
```

```python
# ✅ DESPUÉS
if user.tier == "gold" and total > DiscountConfig.GOLD_MIN_TOTAL:
    return total * DiscountConfig.GOLD_DISCOUNT_RATE
```

**Instancias encontradas:** 15+ magic numbers en 60 líneas de código

---

### 2️⃣ Copy-Paste Programming

**Problema:** Lógica duplicada con inconsistencias peligrosas

```python
# ❌ ANTES: Dos funciones casi idénticas
def ship_cost_domestic(self, weight, distance_km):
    base = 5
    variable = weight * 0.25 + (distance_km / 300)
    if weight > 20:  # Operador >
        variable += 3
    return base + variable

def ship_cost_international(self, weight, distance_km):
    base = 7
    variable = weight * 0.25 + (distance_km / 300)  # DUPLICADO
    if weight >= 20:  # Operador >= (¡inconsistencia!)
        variable += 4
    return base + variable
```

```python
# ✅ DESPUÉS: Lógica unificada
def calculate_cost(weight: float, distance_km: float, 
                  shipping_type: ShippingType) -> float:
    # Una sola función parametrizada
    ...
```

**Impacto:** 90% de duplicación eliminada, inconsistencias resueltas

---

### 3️⃣ God Object

**Problema:** `AppManager` hace TODO

```python
# ❌ ANTES: Una clase con 5 responsabilidades
class AppManager:
    def load_users(self):        # Persistencia
    def print_user(self):         # Presentación
    def discount_for_order(self): # Lógica de negocio
    def ship_cost_domestic(self): # Más lógica de negocio
    def run(self):                # Orquestación
```

```python
# ✅ DESPUÉS: 6 clases especializadas
UserRepository      # Persistencia
DiscountService     # Lógica de descuentos
ShippingCalculator  # Lógica de envíos
UserPresenter       # Presentación
ApplicationController # Orquestación
User               # Modelo de datos
```

**Resultado:** Separación de responsabilidades según SRP

---

## 🔄 Refactorización Detallada

### Corrección 1: Eliminación de Magic Numbers

#### Solución: Clases de Configuración

```python
class DiscountConfig:
    """Configuración centralizada de descuentos"""
    GOLD_MIN_TOTAL = 100.0
    GOLD_DISCOUNT_RATE = 0.15
    
    SILVER_MIN_TOTAL = 42.0
    SILVER_DISCOUNT_RATE = 0.07

class ShippingConfig:
    """Configuración centralizada de envíos"""
    DOMESTIC_BASE_COST = 5.0
    INTERNATIONAL_BASE_COST = 7.0
    WEIGHT_RATE = 0.25
    DISTANCE_DIVISOR = 300.0
    HEAVY_WEIGHT_THRESHOLD = 20.0
    DOMESTIC_HEAVY_SURCHARGE = 3.0
    INTERNATIONAL_HEAVY_SURCHARGE = 4.0
```

**Beneficios:**
- ✅ Código autoexplicativo
- ✅ Un solo lugar para cambiar valores
- ✅ Fácil de mantener y documentar

---

### Corrección 2: Eliminación de Copy-Paste

#### Solución: Método Unificado con Strategy Pattern

```python
class ShippingType(Enum):
    DOMESTIC = "domestic"
    INTERNATIONAL = "international"

class ShippingCalculator:
    @staticmethod
    def calculate_cost(weight: float, distance_km: float, 
                      shipping_type: ShippingType) -> float:
        """Calcula costo de envío con lógica unificada"""
        
        # Configuración según tipo
        if shipping_type == ShippingType.DOMESTIC:
            base_cost = ShippingConfig.DOMESTIC_BASE_COST
            heavy_surcharge = ShippingConfig.DOMESTIC_HEAVY_SURCHARGE
            is_heavy = weight > ShippingConfig.HEAVY_WEIGHT_THRESHOLD
        else:
            base_cost = ShippingConfig.INTERNATIONAL_BASE_COST
            heavy_surcharge = ShippingConfig.INTERNATIONAL_HEAVY_SURCHARGE
            is_heavy = weight >= ShippingConfig.HEAVY_WEIGHT_THRESHOLD
        
        # Cálculo común (sin duplicación)
        variable_cost = (
            weight * ShippingConfig.WEIGHT_RATE + 
            distance_km / ShippingConfig.DISTANCE_DIVISOR
        )
        
        if is_heavy:
            variable_cost += heavy_surcharge
        
        return base_cost + variable_cost
```

**Beneficios:**
- ✅ Sin duplicación (DRY)
- ✅ Comportamiento consistente
- ✅ Fácil agregar nuevos tipos de envío

---

### Corrección 3: Descomposición del God Object

#### Solución: Separación en 6 Clases Especializadas

```python
# 1. MODELO DE DATOS
@dataclass
class User:
    id: int
    name: str
    tier: str

# 2. CAPA DE PERSISTENCIA
class UserRepository:
    """Maneja acceso a datos"""
    def load_all(self) -> List[User]:
        ...

# 3. SERVICIOS DE NEGOCIO
class DiscountService:
    """Calcula descuentos"""
    @staticmethod
    def calculate_discount(user: User, total: float) -> float:
        ...

class ShippingCalculator:
    """Calcula costos de envío"""
    @staticmethod
    def calculate_cost(...) -> float:
        ...

# 4. CAPA DE PRESENTACIÓN
class UserPresenter:
    """Maneja output"""
    @staticmethod
    def print_user(user: User) -> None:
        ...

# 5. CONTROLADOR
class ApplicationController:
    """Orquesta el flujo"""
    def __init__(self, user_repository, discount_service, 
                 shipping_calculator, presenter):
        self.user_repo = user_repository
        self.discount_service = discount_service
        self.shipping_calculator = shipping_calculator
        self.presenter = presenter
    
    def run(self) -> None:
        ...
```
