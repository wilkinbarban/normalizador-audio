# Guía de contribución

Gracias por tu interés en contribuir a **Normalizador Audio**. Este documento explica cómo configurar el entorno y hacer contribuciones.

## Configuración del entorno

### 1. Fork y clona el repo

```bash
git clone https://github.com/TU_USUARIO/normalizador-audio.git
cd normalizador-audio
```

### 2. Crea un entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En macOS/Linux
# O en Windows:
venv\Scripts\activate
```

### 3. Instala dependencias de desarrollo

```bash
pip install -r requirements.txt
```

## Antes de hacer un push

### ✅ Ejecuta los tests localmente

```bash
pytest tests/ -v
```

**Todos deben pasar**. Si alguno falla, no hagas push.

### ✅ Verifica la sintaxis

```bash
python -m py_compile normalizador_app/**/*.py
```

### ✅ (Opcional) Corre análisis de calidad

```bash
pylint normalizador_app --exit-zero --max-line-length=120
bandit -r normalizador_app
```

## Flujo de contribución

1. **Crea una rama** desde `develop`:
   ```bash
   git checkout -b feature/tu-feature develop
   ```

2. **Haz cambios** en los archivos relevantes

3. **Escribe o actualiza tests** si es necesario:
   ```bash
   # Nuevo test:
   tests/test_nuevo_modulo.py
   ```

4. **Corre los tests locales** (ver arriba)

5. **Commit y push**:
   ```bash
   git add .
   git commit -m "feat: descripción clara de tu cambio"
   git push origin feature/tu-feature
   ```

6. **Abre un Pull Request** en GitHub con descripción clara

## Convenciones de código

- **PEP 8** — Sigue el estándar de Python
- **Docstrings** — Todas las funciones/clases deben tener docstring
- **Type hints** — Usa anotaciones de tipos cuando sea posible
- **Nombres claros** — Evita abreviaturas, prefiere claridad
- **Máx 120 caracteres** por línea

### Ejemplo:

```python
def analyze_audio_parameters(file_path: str, target_vol: int) -> dict | None:
    """
    Analiza parámetros de audio usando FFmpeg.
    
    Parameters
    ----------
    file_path : str
        Ruta al archivo de audio/video
    target_vol : int
        LUFS objetivo para loudnorm
    
    Returns
    -------
    dict | None
        Parámetros extraídos o None si hay error
    """
    ...
```

## Estructura de carpetas al agregar features

Si agregas un nuevo módulo, asegúrate de:

- ✅ Ponerlo en la carpeta correcta (`core/`, `services/`, `ui/`, `workers/`)
- ✅ Agregar `__init__.py` si es un paquete nuevo
- ✅ Crear tests en `tests/test_tu_modulo.py`
- ✅ Importar en los archivos correspondientes

## Tipos de commits (Semantic Commit)

Usa estos prefijos para claridad:

- `feat:` — Nueva feature
- `fix:` — Bug fix
- `docs:` — Cambios en documentación
- `refactor:` — Refactorización sin cambios de comportamiento
- `test:` — Agregar o actualizar tests
- `ci:` — Cambios en CI/CD
- `chore:` — Tareas varias (deps, etc)

Ejemplos:
```
feat: agregar exportación a Excel en reporte
fix: corregir colisión de claves en resultado
docs: actualizar README con ejemplos
test: agregar cobertura para audio_service
```

## Testing

### Estructura de un test

```python
import pytest
from unittest.mock import patch, MagicMock
from normalizador_app.services.audio_service import analyze_audio_parameters

class TestAnalyzeAudioParameters:
    @patch("normalizador_app.services.audio_service.subprocess.run")
    def test_analyze_success(self, mock_run):
        """Descripción clara de qué pruebas."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stderr = '{"input_i":-14.5}'
        mock_run.return_value = mock_result
        
        result = analyze_audio_parameters("/test/video.mp4", -14)
        
        assert result is not None
        assert result["input_i"] == -14.5
```

### Fixtures comunes

En `tests/conftest.py` hay fixtures reutilizables:

```python
@pytest.fixture
def temp_dir():
    """Directorio temporal para tests"""

@pytest.fixture
def sample_audio_profile():
    """Perfil de audio de ejemplo"""
```

Úsalas en tus tests:

```python
def test_my_feature(temp_dir, sample_audio_profile):
    # temp_dir y sample_audio_profile ya están listos
    pass
```

## CI/CD

Cuando hagas push, GitHub Actions ejecutará automáticamente:

1. **Tests** en Python 3.10-3.14, Windows/macOS/Linux
2. **Syntax check** — Validación de sintaxis
3. **Security check** — Bandit + análisis de secretos
4. **Coverage** — Reporte enviado a Codecov

Si alguno falla, el PR se marcará como rojo. **Debes corregirlo antes de mergear**.

## Reportar issues

Si encuentras un bug:

1. Crea un **issue** en GitHub con:
   - **Título claro**: "Bug: descripción"
   - **Steps to reproduce**: Pasos para reproducir
   - **Expected vs Actual**: Qué debería pasar vs qué pasa
   - **Environment**: OS, Python version, etc

2. Adjunta logs si es relevante:
   ```bash
   # Ver logs:
   cat normalizador_errors.log
   ```

## Preguntas o dudas

- Abre un **discussion** en GitHub
- O crea un **issue** con etiqueta `question`

¡Gracias por contribuir! 🎉
