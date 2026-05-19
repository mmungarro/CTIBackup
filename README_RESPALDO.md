# Script de Respaldo de Carpetas - ctiRespaldo.py

## Descripción

Script Python que realiza respaldos inteligentes de carpetas con todas sus subcarpetas y archivos:

- ✓ Copia carpetas completas de origen a destino de forma recursiva
- ✓ Mantiene la estructura de directorios y subdirectorios
- ✓ Solo copia archivos que han sido **modificados/creados recientemente** (con parámetro `--recent`)
- ✓ Compara archivos origen con destino mediante **hash SHA256** para detectar deltas
- ✓ Genera **log detallado** con fecha, cantidad de archivos copiados y listado
- ✓ Valida existencia de rutas origen y destino antes de ejecutar
- ✓ Crea directorios destino automáticamente si no existen
- ✓ Preserva timestamps y permisos de archivos

## Requisitos

- Python 3.6+
- No requiere dependencias externas (usa módulos estándar)

## Instalación

No se requiere instalación. Solo asegúrate de tener Python 3.6+ en tu sistema.

## Configuración

### Archivos de configuración

#### 1. `origen.txt`
Contiene las rutas de las **carpetas** que deseas respaldar. Ejemplo:

```
C:\datos\proyecto1
C:\datos\proyecto2
D:\documentos
```

#### 2. `destino.txt`
Contiene las rutas **destino** donde se copiarán las carpetas. Debe tener la **misma cantidad de líneas** que `origen.txt`. Ejemplo:

```
E:\backup\proyecto1
E:\backup\proyecto2
E:\backup\documentos
```

**Notas:**
- Las líneas que comienzan con `#` se ignoran (comentarios)
- Las rutas pueden ser absolutas o relativas
- Cada línea en `origen.txt` corresponde con la línea respectiva en `destino.txt`
- La carpeta origen debe existir (será copiada completa)
- La carpeta destino se crea automáticamente si no existe
- Se preserva la estructura completa de directorios y subdirectorios

## Uso

### Uso básico (copia todas las carpetas completas)

```bash
python ctiRespaldo.py origen.txt destino.txt
```

### Uso con modo "solo recientes" (copia solo cambios detectados)

```bash
python ctiRespaldo.py origen.txt destino.txt --recent
```

En este modo, el script para **cada archivo dentro de las carpetas**:
1. Verifica si el archivo existe en destino
2. Si no existe → lo copia
3. Si existe → compara fechas de modificación
4. Si origen es más reciente → compara contenido (hash)
5. Si el contenido es diferente → lo copia (hay delta)
6. Si es igual → lo omite (sin cambios)

### Especificar archivo de log personalizado

```bash
python ctiRespaldo.py origen.txt destino.txt --log mi_respaldo.log
```

### Combinar opciones

```bash
python ctiRespaldo.py origen.txt destino.txt --recent --log respaldo_2026.log
```

## Ejemplos prácticos

### Ejemplo 1: Respaldo completo

```bash
python ctiRespaldo.py origen.txt destino.txt
```

**Resultado:** Todas las carpetas y archivos en origen.txt se copiarán con su estructura completa a sus rutas destino correspondientes.

### Ejemplo 2: Respaldo incremental (solo cambios)

```bash
python ctiRespaldo.py origen.txt destino.txt --recent
```

**Resultado:** Solo se copiarán archivos que han sido modificados o no existen en destino. Las carpetas se mantienen sincronizadas.

### Ejemplo 3: Respaldo con log personalizado

```bash
python ctiRespaldo.py origen.txt destino.txt --log backup_20260518.log --recent
```

**Resultado:** Copia solo cambios y guarda el log en `backup_20260518.log`.

## Archivo de Log

El log generado contiene:

```
======================================================================
REPORTE DE RESPALDO DE CARPETAS
======================================================================

Fecha del respaldo: 18/05/2026 14:30:45
Archivo de configuración origen: origen.txt
Archivo de configuración destino: destino.txt
Modo de copia: Solo cambios (con delta)

----------------------------------------------------------------------
RESUMEN
----------------------------------------------------------------------
Total de archivos copiados: 12
Tamaño total copiado: 25.50 MB
Total de archivos omitidos: 5
Total de errores: 0

----------------------------------------------------------------------
ARCHIVOS COPIADOS
----------------------------------------------------------------------
1. C:\datos\proyecto1\main.py
   → E:\backup\proyecto1\main.py (2.50 KB)
2. C:\datos\proyecto1\config.ini
   → E:\backup\proyecto1\config.ini (512 B)
3. C:\datos\documentos\readme.txt
   → E:\backup\documentos\readme.txt (1.25 KB)
...
```

El log incluye:
- Fecha y hora del respaldo
- Modo de copia utilizado
- Resumen de operaciones (copiados, omitidos, errores)
- Listado completo de archivos copiados con tamaños
- Listado de archivos omitidos (sin cambios)
- Errores y advertencias (si los hay)

## Validaciones

El script realiza validaciones antes de ejecutar:

1. ✓ Verifica que `origen.txt` existe
2. ✓ Verifica que `destino.txt` existe
3. ✓ Verifica que el número de rutas origen = destino
4. ✓ Verifica que cada ruta origen es un **directorio** que existe
5. ✓ Verifica que los directorios destino padre existen (o pueden crearse)
6. ✓ Maneja errores durante la copia recursiva

Si hay errores de validación, el script muestra un mensaje detallado y no ejecuta la copia.

## Salida de pantalla

### Respaldo exitoso

```
======================================================================
GESTOR DE RESPALDO DE ARCHIVOS
======================================================================

Validando rutas...
✓ Validación exitosa

Iniciando respaldo...
✓ Copiado: C:\datos\documento.pdf → E:\backup\documento.pdf
✓ Copiado: C:\datos\imagen.jpg → E:\backup\imagen.jpg

✓ Respaldo completado: 2 archivo(s) copiado(s)

Generando log...
✓ Log generado: backup_log.txt

----------------------------------------------------------------------
RESUMEN FINAL
----------------------------------------------------------------------
Archivos copiados: 2
Archivos omitidos: 0
Errores: 0
======================================================================
```

### Error de validación

```
======================================================================
GESTOR DE RESPALDO DE ARCHIVOS
======================================================================

Validando rutas...

✗ Validación fallida. Errores encontrados:
  • ERROR: Archivo de configuración origen no existe: origen.txt
  • ERROR: Ruta origen no existe (línea 1): C:\datos\documento.pdf
======================================================================
```

## Características técnicas

### Copia Recursiva
- Copia automáticamente todas las subcarpetas y archivos
- Preserva la estructura completa de directorios
- Crea subdirectorios en destino según sea necesario

### Comparación de archivos (modo --recent)

1. **Si archivo destino no existe:** Copia automáticamente
2. **Si archivo destino existe:**
   - Compara `mtime` (fecha de modificación)
   - Si origen es más reciente:
     - Calcula hash SHA256 de origen
     - Calcula hash SHA256 de destino
     - Si hashes son diferentes: Copia (hay delta)
     - Si hashes son iguales: Omite (sin cambios)

### Preservación de atributos

- El script usa `shutil.copy2()` que preserva:
  - Timestamps (fecha de modificación)
  - Permisos de archivo
  - Metadatos básicos

## Solución de problemas

### Problema: "Archivo de configuración origen no existe"

**Solución:** Asegúrate que los archivos `origen.txt` y `destino.txt` estén en el mismo directorio que `ctiRespaldo.py` o especifica la ruta completa.

### Problema: "El número de rutas origen no coincide con destino"

**Solución:** Verifica que `origen.txt` y `destino.txt` tengan la misma cantidad de líneas (excluyendo comentarios).

### Problema: "Ruta origen no existe"

**Solución:** Verifica que las rutas en `origen.txt` son correctas y accesibles desde tu sistema.

### Problema: Archivos no se copian con --recent

**Solución:** Esto es correcto. Con `--recent`, solo se copian archivos modificados recientemente (comparando fechas) con delta (contenido diferente).

## Notas finales

- El script es seguro: no elimina archivos, solo copia
- Puedes ejecutarlo múltiples veces sin problemas
- Los archivos destino se sobrescriben solo si hay cambios
- Genera un log detallado para auditoría
- Soporta rutas con espacios y caracteres especiales

---

**Autor:** Script de respaldo inteligente
**Versión:** 1.0
**Python:** 3.6+
