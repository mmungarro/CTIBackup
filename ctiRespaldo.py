#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de respaldo de carpetas con validación y log.
Copia carpetas origen a destino recursivamente con soporte para deltas.
"""

import os
import sys
import shutil
import hashlib
from datetime import datetime
from pathlib import Path
import argparse


class BackupManager:
    """Gestor de respaldo de carpetas con validación y registro."""

    def __init__(self, origen_file, destino_file, log_file=None, recent_only=False):
        """
        Inicializa el gestor de respaldo.

        Args:
            origen_file: Archivo con las rutas de carpetas origen
            destino_file: Archivo con las rutas de carpetas destino
            log_file: Archivo para guardar el log (default: backup_log.txt)
            recent_only: Si True, solo copia archivos modificados recientemente
        """
        self.origen_file = origen_file
        self.destino_file = destino_file
        self.log_file = log_file or "backup_log.txt"
        self.recent_only = recent_only
        self.archivos_copiados = []
        self.archivos_skipped = []
        self.errores = []
        self.tamaño_total = 0

    def leer_rutas(self, archivo):
        """Lee las rutas desde un archivo de configuración."""
        rutas = []
        try:
            if not os.path.exists(archivo):
                self.errores.append(f"ERROR: Archivo no encontrado: {archivo}")
                return rutas

            with open(archivo, 'r', encoding='utf-8') as f:
                for linea in f:
                    ruta = linea.strip()
                    if ruta and not ruta.startswith('#'):
                        rutas.append(ruta)
            return rutas
        except Exception as e:
            self.errores.append(f"ERROR al leer {archivo}: {e}")
            return rutas

    def validar_rutas(self):
        """Valida la existencia de archivos de configuración y rutas de carpetas."""
        valido = True

        # Validar archivos de configuración
        if not os.path.exists(self.origen_file):
            self.errores.append(f"ERROR: Archivo de configuración origen no existe: {self.origen_file}")
            valido = False

        if not os.path.exists(self.destino_file):
            self.errores.append(f"ERROR: Archivo de configuración destino no existe: {self.destino_file}")
            valido = False

        if not valido:
            return False

        # Validar rutas de origen y destino
        rutas_origen = self.leer_rutas(self.origen_file)
        rutas_destino = self.leer_rutas(self.destino_file)

        if len(rutas_origen) != len(rutas_destino):
            self.errores.append(
                f"ERROR: El número de rutas origen ({len(rutas_origen)}) "
                f"no coincide con destino ({len(rutas_destino)})"
            )
            valido = False

        for i, (ruta_origen, ruta_destino) in enumerate(zip(rutas_origen, rutas_destino)):
            # Validar que ruta origen es un directorio que existe
            if not os.path.exists(ruta_origen):
                self.errores.append(f"ERROR: Carpeta origen no existe (línea {i+1}): {ruta_origen}")
                valido = False
            elif not os.path.isdir(ruta_origen):
                self.errores.append(f"ERROR: Ruta origen no es un directorio (línea {i+1}): {ruta_origen}")
                valido = False

            # Validar que ruta destino o su directorio padre existe
            if os.path.exists(ruta_destino) and not os.path.isdir(ruta_destino):
                self.errores.append(
                    f"ERROR: Ruta destino existe pero no es un directorio (línea {i+1}): {ruta_destino}"
                )
                valido = False
            else:
                directorio_destino = os.path.dirname(ruta_destino)
                if directorio_destino and not os.path.exists(directorio_destino):
                    self.errores.append(
                        f"ERROR: Directorio destino padre no existe (línea {i+1}): {directorio_destino}"
                    )
                    valido = False

        return valido

    def calcular_hash(self, archivo):
        """Calcula el hash SHA256 de un archivo."""
        sha256_hash = hashlib.sha256()
        try:
            with open(archivo, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            self.errores.append(f"ERROR al calcular hash de {archivo}: {e}")
            return None

    def archivo_necesita_actualizacion(self, ruta_archivo_origen, ruta_archivo_destino):
        """
        Determina si el archivo de origen necesita ser copiado a destino.
        Compara fechas de modificación y contenido (hash).
        """
        # Si el archivo destino no existe, siempre copiar
        if not os.path.exists(ruta_archivo_destino):
            return True

        try:
            # Obtener fechas de modificación
            time_origen = os.path.getmtime(ruta_archivo_origen)
            time_destino = os.path.getmtime(ruta_archivo_destino)

            # Si origen es más reciente, copiar
            if time_origen > time_destino:
                # Verificar si hay delta comparando hashes
                hash_origen = self.calcular_hash(ruta_archivo_origen)
                hash_destino = self.calcular_hash(ruta_archivo_destino)

                if hash_origen and hash_destino and hash_origen != hash_destino:
                    return True
                elif not hash_origen or not hash_destino:
                    return True  # Si no se puede comparar, copiar para seguridad

            return False

        except Exception as e:
            self.errores.append(f"ERROR al comparar {ruta_archivo_origen} y {ruta_archivo_destino}: {e}")
            return False

    def copiar_carpeta_recursivo(self, ruta_origen, ruta_destino):
        """
        Copia una carpeta completa de forma recursiva.
        Detecta y copia solo archivos que han sido modificados si recent_only es True.
        """
        try:
            # Crear directorio destino si no existe
            os.makedirs(ruta_destino, exist_ok=True)

            # Recorrer todos los archivos y directorios
            for elemento in os.walk(ruta_origen):
                directorio_actual, subdirectorios, archivos = elemento

                # Calcular ruta relativa
                ruta_relativa = os.path.relpath(directorio_actual, ruta_origen)
                
                # Crear estructura de directorios en destino
                if ruta_relativa == '.':
                    directorio_destino_actual = ruta_destino
                else:
                    directorio_destino_actual = os.path.join(ruta_destino, ruta_relativa)
                    os.makedirs(directorio_destino_actual, exist_ok=True)

                # Procesar cada archivo
                for archivo in archivos:
                    ruta_archivo_origen = os.path.join(directorio_actual, archivo)
                    ruta_archivo_destino = os.path.join(directorio_destino_actual, archivo)

                    # Decidir si copiar
                    copiar = True
                    if self.recent_only and os.path.exists(ruta_archivo_destino):
                        copiar = self.archivo_necesita_actualizacion(ruta_archivo_origen, ruta_archivo_destino)

                    if copiar:
                        try:
                            shutil.copy2(ruta_archivo_origen, ruta_archivo_destino)
                            tamaño = os.path.getsize(ruta_archivo_destino)
                            self.tamaño_total += tamaño
                            self.archivos_copiados.append({
                                'origen': ruta_archivo_origen,
                                'destino': ruta_archivo_destino,
                                'size': tamaño
                            })
                        except Exception as e:
                            self.errores.append(f"ERROR al copiar archivo {ruta_archivo_origen}: {e}")
                    else:
                        self.archivos_skipped.append(ruta_archivo_origen)

            return True

        except Exception as e:
            self.errores.append(f"ERROR al copiar carpeta {ruta_origen}: {e}")
            return False

    def copiar_carpetas(self):
        """Copia las carpetas de origen a destino."""
        rutas_origen = self.leer_rutas(self.origen_file)
        rutas_destino = self.leer_rutas(self.destino_file)

        if not rutas_origen or not rutas_destino:
            self.errores.append("ERROR: No se pudieron leer las rutas")
            return False

        for idx, (ruta_origen, ruta_destino) in enumerate(zip(rutas_origen, rutas_destino), 1):
            try:
                print(f"\n[{idx}] Copiando: {ruta_origen}")
                print(f"    Destino: {ruta_destino}")
                
                # Copiar carpeta recursivamente
                if self.copiar_carpeta_recursivo(ruta_origen, ruta_destino):
                    print(f"    ✓ Carpeta copiada exitosamente")
                else:
                    print(f"    ✗ Error al copiar carpeta")

            except Exception as e:
                self.errores.append(f"ERROR al procesar {ruta_origen}: {e}")
                print(f"    ✗ Error: {e}")

        return len(self.archivos_copiados) > 0

    def generar_log(self):
        """Genera un archivo de log con el resumen del respaldo."""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write("REPORTE DE RESPALDO DE CARPETAS\n")
                f.write("=" * 70 + "\n\n")

                # Fecha y hora
                f.write(f"Fecha del respaldo: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Archivo de configuración origen: {self.origen_file}\n")
                f.write(f"Archivo de configuración destino: {self.destino_file}\n")
                f.write(f"Modo de copia: {'Solo cambios (con delta)' if self.recent_only else 'Copia completa'}\n\n")

                # Resumen
                f.write("-" * 70 + "\n")
                f.write("RESUMEN\n")
                f.write("-" * 70 + "\n")
                f.write(f"Total de archivos copiados: {len(self.archivos_copiados)}\n")
                f.write(f"Tamaño total copiado: {self._formato_tamaño(self.tamaño_total)}\n")
                f.write(f"Total de archivos omitidos: {len(self.archivos_skipped)}\n")
                f.write(f"Total de errores: {len(self.errores)}\n\n")

                # Archivos copiados
                if self.archivos_copiados:
                    f.write("-" * 70 + "\n")
                    f.write("ARCHIVOS COPIADOS\n")
                    f.write("-" * 70 + "\n")
                    for i, archivo in enumerate(self.archivos_copiados, 1):
                        f.write(f"{i}. {archivo['origen']}\n")
                        f.write(f"   → {archivo['destino']} ({self._formato_tamaño(archivo['size'])})\n")
                    f.write("\n")

                # Archivos omitidos
                if self.archivos_skipped:
                    f.write("-" * 70 + "\n")
                    f.write("ARCHIVOS OMITIDOS (Sin cambios)\n")
                    f.write("-" * 70 + "\n")
                    for i, archivo in enumerate(self.archivos_skipped, 1):
                        f.write(f"{i}. {archivo}\n")
                    f.write("\n")

                # Errores
                if self.errores:
                    f.write("-" * 70 + "\n")
                    f.write("ERRORES Y ADVERTENCIAS\n")
                    f.write("-" * 70 + "\n")
                    for error in self.errores:
                        f.write(f"• {error}\n")
                    f.write("\n")

                f.write("=" * 70 + "\n")
                f.write(f"Fin del reporte\n")

            print(f"\n✓ Log generado: {self.log_file}")
            return True

        except Exception as e:
            print(f"✗ Error al generar log: {e}")
            return False

    def _formato_tamaño(self, bytes_val):
        """Convierte bytes a formato legible."""
        for unidad in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.2f} {unidad}"
            bytes_val /= 1024.0
        return f"{bytes_val:.2f} TB"

    def ejecutar(self):
        """Ejecuta el proceso completo de respaldo."""
        print("\n" + "=" * 70)
        print("GESTOR DE RESPALDO DE CARPETAS")
        print("=" * 70 + "\n")

        # Validar rutas
        print("Validando rutas...")
        if not self.validar_rutas():
            print("\n✗ Validación fallida. Errores encontrados:")
            for error in self.errores:
                print(f"  • {error}")
            return False

        print("✓ Validación exitosa\n")

        # Copiar carpetas
        print("Iniciando respaldo...")
        if self.copiar_carpetas():
            print(f"\n✓ Respaldo completado: {len(self.archivos_copiados)} archivo(s) copiado(s)")
        else:
            print("\n⚠ Respaldo completado sin cambios o con errores")

        # Generar log
        print("\nGenerando log...")
        self.generar_log()

        # Mostrar resumen
        print("\n" + "-" * 70)
        print("RESUMEN FINAL")
        print("-" * 70)
        print(f"Archivos copiados: {len(self.archivos_copiados)}")
        print(f"Tamaño total: {self._formato_tamaño(self.tamaño_total)}")
        print(f"Archivos omitidos: {len(self.archivos_skipped)}")
        print(f"Errores: {len(self.errores)}")
        print("=" * 70 + "\n")

        return len(self.errores) == 0


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description="Script de respaldo de carpetas con validación y log",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python ctiRespaldo.py origen.txt destino.txt
  python ctiRespaldo.py origen.txt destino.txt --recent
  python ctiRespaldo.py origen.txt destino.txt --log mi_backup.log --recent
        """
    )

    parser.add_argument(
        'origen',
        help='Archivo con las rutas de carpetas origen'
    )
    parser.add_argument(
        'destino',
        help='Archivo con las rutas de carpetas destino'
    )
    parser.add_argument(
        '--recent',
        action='store_true',
        help='Solo copiar archivos modificados recientemente con delta'
    )
    parser.add_argument(
        '--log',
        default='backup_log.txt',
        help='Nombre del archivo de log (default: backup_log.txt)'
    )

    args = parser.parse_args()

    # Crear gestor y ejecutar
    manager = BackupManager(
        args.origen,
        args.destino,
        log_file=args.log,
        recent_only=args.recent
    )

    exitoso = manager.ejecutar()
    sys.exit(0 if exitoso else 1)


if __name__ == '__main__':
    main()


