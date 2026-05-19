# Referencia Rápida - ctiRespaldo.py

## Instalación y Prueba Rápida

```bash
# 1. Crear estructura de prueba
python crear_estructura_prueba.py

# 2. Ver archivos de configuración creados
type origen_prueba.txt
type destino_prueba.txt

# 3. Ejecutar respaldo completo
python ctiRespaldo.py origen_prueba.txt destino_prueba.txt

# 4. Ver el log generado
type backup_log.txt
```

## Comandos Principales

| Comando | Descripción | Copia |
|---------|-------------|-------|
| `python ctiRespaldo.py origen.txt destino.txt` | Respaldo completo de carpetas | Todas |
| `python ctiRespaldo.py origen.txt destino.txt --recent` | Solo cambios en archivos | Solo modificados |
| `python ctiRespaldo.py origen.txt destino.txt --log custom.log` | Log personalizado | Todas |
| `python ctiRespaldo.py origen.txt destino.txt --recent --log respaldo.log` | Cambios + log | Solo modificados |

## Archivos de Configuración

**origen.txt** - Carpetas a respaldar:
```
C:\datos\proyecto1
C:\datos\proyecto2
D:\documentos
```

**destino.txt** - Rutas destino (mismo número de líneas):
```
E:\backup\proyecto1
E:\backup\proyecto2
E:\backup\documentos
```

## Salida Esperada

```
======================================================================
GESTOR DE RESPALDO DE CARPETAS
======================================================================

Validando rutas...
✓ Validación exitosa

Iniciando respaldo...

[1] Copiando: C:\datos\proyecto1
    Destino: E:\backup\proyecto1
    ✓ Carpeta copiada exitosamente
[2] Copiando: C:\datos\proyecto2
    Destino: E:\backup\proyecto2
    ✓ Carpeta copiada exitosamente

✓ Respaldo completado: 15 archivo(s) copiado(s)

Generando log...
✓ Log generado: backup_log.txt

----------------------------------------------------------------------
RESUMEN FINAL
----------------------------------------------------------------------
Archivos copiados: 15
Tamaño total: 45.30 MB
Archivos omitidos: 3
Errores: 0
======================================================================
```

## Opciones de Parámetros

```
Parámetros obligatorios:
  origen.txt    - Archivo con rutas de carpetas origen
  destino.txt   - Archivo con rutas de carpetas destino

Parámetros opcionales:
  --recent      - Solo copiar archivos modificados recientemente con delta
  --log archivo - Especificar nombre del archivo de log (default: backup_log.txt)
```

## Lógica de Copia (Modo --recent)

```
Para cada archivo dentro de las carpetas:

┌─ ¿Archivo destino existe?
│
├─ NO → Copiar
│
└─ SÍ
   └─ ¿Origen más reciente que destino?
      │
      ├─ NO → Omitir
      │
      └─ SÍ
         └─ ¿Hash diferente?
            │
            ├─ SÍ → Copiar (hay delta)
            │
            └─ NO → Omitir (sin cambios)
```

## Ejemplos Prácticos

### Ejemplo 1: Primer respaldo completo
```bash
python ctiRespaldo.py origen.txt destino.txt
```
✓ Copia todas las carpetas y subcarpetas

### Ejemplo 2: Respaldos incrementales (ejecutar periódicamente)
```bash
python ctiRespaldo.py origen.txt destino.txt --recent
```
✓ Solo copia archivos nuevos o modificados

### Ejemplo 3: Respaldo diario con identificador
```bash
python ctiRespaldo.py origen.txt destino.txt --log respaldo_daily.log --recent
```
✓ Crea log diario con cambios incrementales

## Validaciones Ejecutadas

- ✓ origen.txt existe
- ✓ destino.txt existe
- ✓ Número de rutas coinciden
- ✓ Todas las rutas origen son directorios que existen
- ✓ Directorios destino padre existen o pueden crearse

## Log Generado

El archivo de log contiene:
- Fecha y hora del respaldo
- Total de archivos copiados y tamaño total
- Total de archivos omitidos
- Listado completo de archivos copiados con tamaños
- Listado de archivos omitidos
- Errores y advertencias (si los hay)

## Notas Importantes

⚠️ **Importante:**
- origen.txt y destino.txt deben tener el MISMO número de líneas
- El script NO elimina archivos, solo copia
- Los archivos se preservan con timestamp y permisos
- Se copia la carpeta **completa** con toda su estructura

💡 **Tips:**
- Comenta líneas en origen.txt y destino.txt con `#` para deshabilitarlas
- Usa rutas absolutas para máxima compatibilidad
- Ejecuta con `--recent` para respaldos incrementales eficientes
- Mantén logs anteriores para auditoría

❌ **Errores comunes:**
- Especificar archivos en lugar de carpetas en origen.txt
- Diferente número de líneas en origen.txt vs destino.txt
- Rutas con espacios sin entrecomillas
- Directorios destino padre sin permisos de escritura

