#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de demostración para probar ctiRespaldo.py
Crea una estructura de carpetas de prueba y archivos de configuración.
"""

import os
import sys
from datetime import datetime
from pathlib import Path


def crear_estructura_prueba():
    """Crea una estructura de directorios y archivos para prueba."""
    
    print("=" * 70)
    print("CREADOR DE ESTRUCTURA DE PRUEBA PARA ctiRespaldo.py")
    print("=" * 70 + "\n")
    
    # Crear directorios principales
    origen_dir = "datos_prueba_origen"
    destino_dir = "datos_prueba_destino"
    
    print(f"Creando directorio de origen: {origen_dir}")
    os.makedirs(origen_dir, exist_ok=True)
    
    print(f"Creando directorio de destino: {destino_dir}")
    os.makedirs(destino_dir, exist_ok=True)
    
    # Crear estructura de carpetas de prueba en origen
    print("\nCreando estructura de carpetas de prueba...")
    
    # Carpeta 1 - Proyecto Python
    carpeta1 = os.path.join(origen_dir, "proyecto_python")
    os.makedirs(carpeta1, exist_ok=True)
    
    with open(os.path.join(carpeta1, "main.py"), 'w', encoding='utf-8') as f:
        f.write("#!/usr/bin/env python3\n")
        f.write("# Archivo principal\n")
        f.write(f"# Creado: {datetime.now().isoformat()}\n")
        f.write("print('Hola Mundo')\n")
    
    with open(os.path.join(carpeta1, "config.ini"), 'w', encoding='utf-8') as f:
        f.write("[settings]\n")
        f.write("debug = true\n")
        f.write(f"created = {datetime.now().isoformat()}\n")
    
    print(f"✓ Carpeta 1 creada: {os.path.abspath(carpeta1)}")
    print(f"  - main.py")
    print(f"  - config.ini")
    
    # Carpeta 2 - Documentos
    carpeta2 = os.path.join(origen_dir, "documentos")
    os.makedirs(carpeta2, exist_ok=True)
    
    with open(os.path.join(carpeta2, "readme.txt"), 'w', encoding='utf-8') as f:
        f.write("Documentación del proyecto\n")
        f.write(f"Creado: {datetime.now().isoformat()}\n")
    
    with open(os.path.join(carpeta2, "datos.csv"), 'w', encoding='utf-8') as f:
        f.write("id,nombre,descripcion\n")
        f.write("1,item1,Primer item\n")
        f.write("2,item2,Segundo item\n")
    
    # Subcarpeta dentro de documentos
    subcarpeta2 = os.path.join(carpeta2, "subfolder")
    os.makedirs(subcarpeta2, exist_ok=True)
    
    with open(os.path.join(subcarpeta2, "notes.txt"), 'w', encoding='utf-8') as f:
        f.write("Notas adicionales\n")
        f.write(f"Creado: {datetime.now().isoformat()}\n")
    
    print(f"✓ Carpeta 2 creada: {os.path.abspath(carpeta2)}")
    print(f"  - readme.txt")
    print(f"  - datos.csv")
    print(f"  - subfolder/")
    print(f"    - notes.txt")
    
    # Carpeta 3 - Datos
    carpeta3 = os.path.join(origen_dir, "datos_aplicacion")
    os.makedirs(carpeta3, exist_ok=True)
    
    with open(os.path.join(carpeta3, "database.db"), 'w', encoding='utf-8') as f:
        f.write("Simulated database file\n")
        f.write(f"Created: {datetime.now().isoformat()}\n")
    
    with open(os.path.join(carpeta3, "schema.sql"), 'w', encoding='utf-8') as f:
        f.write("CREATE TABLE usuarios (id INT, nombre VARCHAR(255));\n")
        f.write(f"-- Created: {datetime.now().isoformat()}\n")
    
    print(f"✓ Carpeta 3 creada: {os.path.abspath(carpeta3)}")
    print(f"  - database.db")
    print(f"  - schema.sql")
    
    # Crear configuración de origen
    print("\nCreando archivos de configuración...")
    
    carpeta1_destino = os.path.join(destino_dir, "proyecto_python")
    carpeta2_destino = os.path.join(destino_dir, "documentos")
    carpeta3_destino = os.path.join(destino_dir, "datos_aplicacion")
    
    with open("origen_prueba.txt", 'w', encoding='utf-8') as f:
        f.write(f"# Archivo de configuración ORIGEN para pruebas\n")
        f.write(f"# Generado: {datetime.now().isoformat()}\n")
        f.write(f"# Carpetas origen a respaldar\n\n")
        f.write(f"{os.path.abspath(carpeta1)}\n")
        f.write(f"{os.path.abspath(carpeta2)}\n")
        f.write(f"{os.path.abspath(carpeta3)}\n")
    print(f"✓ Creado: origen_prueba.txt")
    
    with open("destino_prueba.txt", 'w', encoding='utf-8') as f:
        f.write(f"# Archivo de configuración DESTINO para pruebas\n")
        f.write(f"# Generado: {datetime.now().isoformat()}\n")
        f.write(f"# Carpetas destino para respaldar\n\n")
        f.write(f"{os.path.abspath(carpeta1_destino)}\n")
        f.write(f"{os.path.abspath(carpeta2_destino)}\n")
        f.write(f"{os.path.abspath(carpeta3_destino)}\n")
    print(f"✓ Creado: destino_prueba.txt")
    
    print("\n" + "=" * 70)
    print("ESTRUCTURA DE PRUEBA CREADA")
    print("=" * 70)
    print(f"\nCarpetas de origen en: {os.path.abspath(origen_dir)}")
    print(f"Carpetas de destino en: {os.path.abspath(destino_dir)}")
    print(f"\nArchivos de configuración creados:")
    print(f"  • {os.path.abspath('origen_prueba.txt')}")
    print(f"  • {os.path.abspath('destino_prueba.txt')}")
    
    print("\n" + "-" * 70)
    print("PRÓXIMOS PASOS - Prueba el script con:")
    print("-" * 70)
    print(f"\n1. Respaldo completo de carpetas:")
    print(f"   python ctiRespaldo.py origen_prueba.txt destino_prueba.txt")
    print(f"\n2. Respaldo solo cambios (modo incremental):")
    print(f"   python ctiRespaldo.py origen_prueba.txt destino_prueba.txt --recent")
    print(f"\n3. Con log personalizado:")
    print(f"   python ctiRespaldo.py origen_prueba.txt destino_prueba.txt --log prueba.log --recent")
    print("\n" + "=" * 70 + "\n")


if __name__ == '__main__':
    try:
        crear_estructura_prueba()
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

