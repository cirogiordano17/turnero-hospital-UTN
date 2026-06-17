"""
Configuración compartida para los tests.

Agrega el directorio raíz al sys.path para que los imports
funcionen igual que en producción.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
