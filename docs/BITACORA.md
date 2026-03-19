# Bitácora técnica — CI Pipeline DevSecOps (CYOM 569)

Documento de seguimiento del proyecto: decisiones, incidentes de pipeline y resultados.  
**Repositorio:** [cyom569-project-task-2-ci-pipeline](https://github.com/ivanofmg/cyom569-project-task-2-ci-pipeline)  
**Documentación de producto:** ver `README.md` en la raíz del repositorio.

---

## Resumen ejecutivo

Se entregó una aplicación **Flask** mínima **containerizada** con **Docker** y un pipeline de **GitHub Actions** que ejecuta, en cada cambio sobre `main`, validación de sintaxis, **lint** con **flake8**, análisis estático de seguridad con **Bandit** y construcción de imagen Docker.  

Durante la puesta en marcha se corrigieron fallos típicos de CI: reglas de estilo (flake8) y una alerta **Bandit B104** por enlace a todas las interfaces (`0.0.0.0`), resuelta con **variables de entorno** y configuración explícita en el **Dockerfile**. Se añadió exclusión de entornos virtuales locales en Bandit para evitar ruido en el escaneo.

**Estado final:** pipeline verde (flake8, Bandit, build Docker).

---

## Índice

1. [2026-03-19 — Inicialización del proyecto](#2026-03-19--inicialización-del-proyecto)  
2. [2026-03-19 — Docker y contenedor](#2026-03-19--docker-y-contenedor)  
3. [2026-03-19 — Pipeline CI (GitHub Actions)](#2026-03-19--pipeline-ci-github-actions)  
4. [2026-03-19 — Fallos de lint (flake8)](#2026-03-19--fallos-de-lint-flake8)  
5. [2026-03-19 — Fallo de seguridad (Bandit B104)](#2026-03-19--fallo-de-seguridad-bandit-b104)  
6. [2026-03-19 — Alcance del escaneo Bandit](#2026-03-19--alcance-del-escaneo-bandit)  
7. [2026-03-19 — Cierre: CI estable](#2026-03-19--cierre-ci-estable)  
8. [Aprendizajes y próximos pasos](#aprendizajes-y-próximos-pasos)

---

## 2026-03-19 — Inicialización del proyecto

### Objetivo

Establecer la base del repositorio con una aplicación Python ejecutable y dependencias declaradas.

### Actividades

- Estructura del proyecto en entorno local (`C:\dev\...`).
- Repositorio Git y remoto en GitHub.
- Implementación de `app.py` (Flask) y `requirements.txt`.

### Notas

- Prioridad inicial: funcionalidad y trazabilidad antes de optimizar documentación.

---

## 2026-03-19 — Docker y contenedor

### Objetivo

Empaquetar la aplicación en una imagen reproducible.

### Actividades

- Instalación y verificación de Docker Desktop (WSL2 en Windows).
- Creación de `Dockerfile`.
- Construcción y ejecución local de la imagen.

Comandos de referencia:

```bash
docker --version
docker info
docker build -t cyom569-ci-pipeline .
docker run -p 5000:5000 cyom569-ci-pipeline
```

### Resultado

- Servicio accesible en `http://127.0.0.1:5000`.
- Endpoint `/health` operativo.

### Incidencias

| Problema | Resolución |
|----------|------------|
| `docker` no reconocido en terminal de VS Code | Uso de PowerShell del sistema / revisión de PATH; reinicio del entorno según fuera necesario |

---

## 2026-03-19 — Pipeline CI (GitHub Actions)

### Objetivo

Automatizar validación, calidad, seguridad y build en cada integración a `main`.

### Actividades

- Creación de `.github/workflows/ci.yml`.
- Etapas configuradas: checkout, Python 3.11, dependencias, `py_compile`, flake8, Bandit, `docker build`.

### Resultado

- Ejecuciones disparadas correctamente en `push` / pull request hacia `main`.

---

## 2026-03-19 — Fallos de lint (flake8)

### Síntoma

El job de lint fallaba con infracciones PEP 8, entre ellas:

- **E302 / E305** — espaciado entre definiciones de funciones.
- **W292** — falta de nueva línea al final del archivo.
- **E501** — línea mayor a 79 caracteres (incluido un comentario largo en una iteración posterior).

### Acciones

- Ajuste de líneas en blanco y formato.
- Nueva línea final de archivo.
- Acortado o partición de comentarios para cumplir **E501**.

### Resultado

- `flake8 . --count --statistics` en verde dentro del workflow.

### Conclusión técnica

El lint actúa como **umbral de calidad**: errores menores bloquean el pipeline, lo que reduce deuda técnica y mantiene un estilo uniforme.

---

## 2026-03-19 — Fallo de seguridad (Bandit B104)

### Síntoma

```
B104: Possible binding to all interfaces (hardcoded_bind_all_interfaces)
```

### Causa raíz

Uso explícito en código de:

```python
app.run(host="0.0.0.0", port=5000)
```

Bandit interpreta el bind a `0.0.0.0` como riesgo de exposición a todas las interfaces cuando está **hardcodeado**.

### Solución adoptada

1. **Código:** lectura de `HOST` y `PORT` desde el entorno, con valores por defecto seguros para desarrollo (`127.0.0.1`, `5000`).
2. **Dockerfile:** `ENV HOST=0.0.0.0` y `ENV PORT=5000` para conservar el comportamiento esperado en contenedor (aceptar tráfico externo al mapear puertos).

### Resultado

- Bandit deja de reportar B104 en el código de aplicación.
- Comportamiento en Docker preservado.

### Conclusión técnica

Separar **intención de despliegue** (contenedor / orquestación) de **valores por defecto en código fuente** alinea buenas prácticas **12-factor**, configuración segura por defecto y herramientas de análisis estático.

---

## 2026-03-19 — Alcance del escaneo Bandit

### Síntoma

Con un árbol `.venv` (u otra carpeta `venv`) dentro del workspace, Bandit podía reportar hallazgos en **dependencias** (ruido, no atribuible al código del proyecto).

### Solución en CI

Actualización del comando de Bandit para excluir directorios de entorno virtual:

```bash
bandit -r . -ll -x .venv -x venv
```

*(Equivalente en el workflow a dos banderas `-x`, según versión de Bandit.)*

### Resultado

- Informe centrado en el código del repositorio.
- Menos falsos positivos operativos.

---

## 2026-03-19 — Cierre: CI estable

### Estado verificado

| Control | Estado |
|---------|--------|
| Sintaxis (`py_compile`) | OK |
| flake8 | OK |
| Bandit (`-ll`, exclusiones venv) | Sin hallazgos en código app |
| `docker build` | OK |

### Observación

La duración aproximada del job depende de GitHub Actions y de la caché de imágenes; el diseño del pipeline prioriza **gates claros** sobre optimización extrema de tiempo en esta fase.

---

## Aprendizajes y próximos pasos

### Aprendizajes

- La integración continua **materializa** normas de calidad y seguridad: lo que no está automatizado tiende a degradarse.
- Detalles pequeños (longitud de línea, `HOST`) pueden **bloquear** el pipeline; es un coste aceptable a cambio de consistencia.
- El análisis estático debe **acotarse** al código propio cuando el escaneo recursivo incluye `site-packages` vía venv en el árbol del proyecto.

### Próximos pasos sugeridos

- **pip-audit** (o equivalente) para vulnerabilidades en dependencias.
- **Trivy** (u otro scanner) sobre la imagen Docker.
- Tests automatizados (pytest) como etapa obligatoria.
- Etapa de despliegue (CD) si el curso o el producto lo requieren.

---

## Conclusión del proyecto (bitácora)

Este entregable muestra un **pipeline CI** con controles **DevSecOps** básicos pero reales: calidad con flake8, SAST con Bandit, configuración por entorno, contenedor verificado en build, y registro de incidentes y resoluciones en esta bitácora para auditoría y portafolio profesional.
