# Ejemplos de Configuración Reales

## Ejemplo 1: Respaldo de Proyectos de Desarrollo

**origen.txt**
```
# Proyectos de desarrollo para respaldo
C:\Proyectos\ProyectoPython
C:\Proyectos\ProyectoWeb
D:\Desarrollo\ProyectoNode
```

**destino.txt**
```
# Respaldo en disco externo
E:\Respaldos\ProyectoPython
E:\Respaldos\ProyectoWeb
E:\Respaldos\ProyectoNode
```

**Comando:**
```bash
python ctiRespaldo.py origen.txt destino.txt --recent --log respaldo_desarrollo.log
```

**Resultado:** Copia recursivamente todas las subcarpetas, archivos .py, .js, .json, etc. Solo copia cambios.

---

## Ejemplo 2: Respaldo de Documentos Empresariales

**origen.txt**
```
# Documentos importantes
C:\Documentos\Contratos
C:\Documentos\Informes
C:\Documentos\Proyectos
D:\Datos\Clientes
```

**destino.txt**
```
# Servidor de respaldo
\\servidor\respaldos\Contratos
\\servidor\respaldos\Informes
\\servidor\respaldos\Proyectos
\\servidor\respaldos\Clientes
```

**Comando:**
```bash
python ctiRespaldo.py origen.txt destino.txt --recent
```

---

## Ejemplo 3: Respaldo de Aplicación Completa

**origen.txt**
```
# Aplicación completa con estructura
C:\Aplicaciones\MiApp
```

**destino.txt**
```
# Respaldo en NAS
\\nas\backups\produccion\MiApp
```

**Comando:**
```bash
python ctiRespaldo.py origen.txt destino.txt --log backup_app.log
```

**Estructura copiada:**
```
MiApp/
├── src/
│   ├── main.py
│   ├── config.ini
│   └── modules/
│       ├── auth.py
│       ├── database.py
│       └── utils.py
├── data/
│   ├── usuarios.db
│   └── config.json
├── logs/
│   └── app.log
└── README.md
```

---

## Ejemplo 4: Respaldo Múltiple con Múltiples Ubicaciones

**origen.txt**
```
# Múltiples ubicaciones
C:\Proyecto1
D:\Datos_Produccion
E:\Configuracion_Sistemas
F:\Backups_Locales
```

**destino.txt**
```
# Centralizado
G:\Respaldo_Maestro\Proyecto1
G:\Respaldo_Maestro\Datos_Produccion
G:\Respaldo_Maestro\Configuracion_Sistemas
G:\Respaldo_Maestro\Backups_Locales
```

**Comando:**
```bash
python ctiRespaldo.py origen.txt destino.txt --recent
```

---

## Ejemplo 5: Respaldo Selectivo con Comentarios

**origen.txt**
```
# Respaldo selectivo - algunas carpetas deshabilitadas
C:\Proyectos\Activos\App_Produccion
C:\Proyectos\Activos\API_Backend

# En revisión - no respaldar:
# C:\Proyectos\En_Revision\ExperimentoA
# C:\Proyectos\Archivado\Antiguo

D:\Datos_Criticos\BaseDatos
```

**destino.txt**
```
# Destinos correspondientes
E:\Respaldos\App_Produccion
E:\Respaldos\API_Backend

# En revisión - no respaldar:
# E:\Respaldos\ExperimentoA
# E:\Respaldos\Antiguo

E:\Respaldos\BaseDatos
```

**Comando:**
```bash
python ctiRespaldo.py origen.txt destino.txt --recent
```

---

## Automatización: Script Batch (Windows)

**respaldo_automatico_diario.bat**
```batch
@echo off
REM Script de respaldo automático diario
REM Se ejecuta diariamente vía Tareas Programadas

cd C:\JavaProjects\python\python_ethical\macaddress

REM Respaldo incremental con timestamp
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)

echo [%date% %time%] Iniciando respaldo incremental...
python ctiRespaldo.py origen.txt destino.txt --recent --log respaldo_%mydate%_%mytime%.log

if %errorlevel% equ 0 (
    echo [%date% %time%] Respaldo completado exitosamente
) else (
    echo [%date% %time%] Error en el respaldo
)

REM Enviar email si deseas notificación (opcional)
REM powershell -ExecutionPolicy Bypass "Send-MailMessage -To admin@example.com -From respaldos@example.com -Subject 'Respaldo Completado' -Body 'El respaldo se ha completado' -SmtpServer smtp.example.com"
```

---

## Automatización: Script Bash (Linux/Mac)

**respaldo_automatico.sh**
```bash
#!/bin/bash

# Script de respaldo automático para Linux/Mac

cd /home/usuario/proyectos/macaddress

# Respaldo incremental con fecha
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOGFILE="respaldo_${TIMESTAMP}.log"

echo "[$(date)] Iniciando respaldo..." >> ${LOGFILE}

python3 ctiRespaldo.py origen.txt destino.txt --recent --log ${LOGFILE}

if [ $? -eq 0 ]; then
    echo "[$(date)] Respaldo completado exitosamente" >> ${LOGFILE}
    # Enviar notificación (opcional)
    # mail -s "Respaldo Automático Completado" admin@example.com < ${LOGFILE}
else
    echo "[$(date)] Error en el respaldo" >> ${LOGFILE}
    # mail -s "Error en Respaldo Automático" admin@example.com < ${LOGFILE}
fi

# Limpiar logs antiguos (más de 30 días)
find . -name "respaldo_*.log" -mtime +30 -delete
```

---

## Configuración en Cron Job (Linux)

**Respaldo diario a las 2:00 AM:**

```bash
# Abrir crontab
crontab -e

# Agregar la línea para respaldo diario:
0 2 * * * cd /home/usuario/proyectos/macaddress && python3 ctiRespaldo.py origen.txt destino.txt --recent --log respaldo_$(date +\%Y\%m\%d).log 2>&1

# O con notificación por email:
0 2 * * * cd /home/usuario/proyectos/macaddress && python3 ctiRespaldo.py origen.txt destino.txt --recent --log respaldo_$(date +\%Y\%m\%d).log 2>&1 | mail -s "Respaldo del $(date +\%d/\%m/\%Y)" admin@example.com
```

---

## Configuración en Tareas Programadas (Windows)

**Crear tarea automática:**

1. Abre **Tareas Programadas**
2. Crea una nueva tarea:
   - **Nombre:** "Respaldo Automático Diario"
   - **Desencadenador:** 
     - Tipo: Diario
     - Hora: 02:00 AM
     - Frecuencia: Todos los días
   - **Acción:**
     - Programa: `C:\Python39\python.exe`
     - Argumentos: `ctiRespaldo.py origen.txt destino.txt --recent`
     - Iniciar en: `C:\JavaProjects\python\python_ethical\macaddress`
   - **Opciones:**
     - Ejecutar solo si el usuario está conectado: No
     - Ejecutar con privilegios máximos: Sí (si lo requiere)

---

## Script de Verificación de Respaldos

**verificar_respaldos.py**
```python
import os
from datetime import datetime, timedelta

def verificar_ultimo_respaldo(directorio_logs, horas_max=25):
    """Verifica que el último respaldo se completó hace menos de X horas."""
    
    logs = [f for f in os.listdir(directorio_logs) if f.startswith("respaldo_") and f.endswith(".log")]
    
    if not logs:
        print("❌ No se encontraron logs de respaldo")
        return False
    
    logs_ordenados = sorted(logs, reverse=True)
    ultimo_log = logs_ordenados[0]
    
    with open(os.path.join(directorio_logs, ultimo_log), 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificaciones
    checks = {
        "Validación exitosa": "Validación" in contenido and "exitosa" in contenido,
        "Respaldo completado": "Respaldo completado" in contenido,
        "Sin errores": "Total de errores: 0" in contenido,
    }
    
    print(f"Último respaldo: {ultimo_log}")
    print("\nVerificaciones:")
    for check, resultado in checks.items():
        print(f"  {'✓' if resultado else '❌'} {check}")
    
    return all(checks.values())

# Usar:
# verificar_ultimo_respaldo(".")
```

---

## Mejores Prácticas

1. **Usar rutas absolutas** para máxima compatibilidad y evitar cambios de directorio
2. **Ejecutar --recent regularmente** (diario) para respaldos incrementales eficientes
3. **Guardar logs con timestamp** para mantener historial completo
4. **Verificar logs regularmente** para detectar problemas tempranamente
5. **Mantener múltiples copias** en ubicaciones diferentes (3-2-1 backup rule)
6. **Documentar configuración** con comentarios en los archivos .txt
7. **Probar regularmente** que los respaldos se restauran correctamente
8. **Usar disco/NAS externo** para mayor redundancia y seguridad
9. **Excluir carpetas temp** (comentarlas en origen.txt si es necesario)
10. **Monitorear espacio** en disco de destino para evitar fallos

---

## Troubleshooting

### El respaldo dice "sin cambios" cuando debería haber cambios

**Solución:** El hash de los archivos es idéntico. Esto es correcto - el archivo no cambió.

### Algunos archivos no se copian

**Solución:** Verifica permisos de lectura en origen y escritura en destino. El log detallará los errores.

### El respaldo es muy lento

**Solución:** Descomenta archivos grandes innecesarios en origen.txt, o usa carpetas origen más pequeñas.

### Error "Carpeta origen no existe"

**Solución:** Verifica que las rutas en origen.txt sean correctas y accesibles. Usa rutas absolutas.

