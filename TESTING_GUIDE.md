# Quick Reference: CI/CD & Testing

## 🧪 Ejecutar tests localmente

```bash
# Todos los tests
pytest tests/ -v

# Un archivo específico
pytest tests/test_config_manager.py -v

# Una clase específica
pytest tests/test_config_manager.py::TestConfigManager -v

# Un test específico
pytest tests/test_config_manager.py::TestConfigManager::test_save_audio_profile_json -v

# Con salida más detallada
pytest tests/ -vv --tb=long

# Solo mostrar fallos
pytest tests/ --tb=short
```

## 📊 Cobertura de código

```bash
# Generar reporte HTML
pytest tests/ --cov=normalizador_app --cov-report=html

# Ver en navegador (después de correr el comando anterior)
# Windows: start htmlcov/index.html
# Mac/Linux: open htmlcov/index.html
```

## 🔍 Verificar sintaxis

```bash
# Compilar todo
python -m py_compile normalizador_app/**/*.py tests/**/*.py

# Con compileall (completo)
python -m compileall .
```

## 🛡️ Seguridad

```bash
# Bandit (vulnerabilidades)
pip install bandit
bandit -r normalizador_app -f csv

# Detect secrets
pip install detect-secrets
detect-secrets scan
```

## 📝 Linting

```bash
# Pylint
pip install pylint
pylint normalizador_app --max-line-length=120

# Flake8
pip install flake8
flake8 normalizador_app --max-line-length=120
```

## 🚀 Antes de hacer commit

```bash
#!/bin/bash
# Ejecutar esto antes de push

set -e

echo "✓ Running tests..."
pytest tests/ -q

echo "✓ Checking syntax..."
python -m py_compile normalizador_app/**/*.py

echo "✓ Checking imports..."
python -m compileall .

echo "✓ Running pylint..."
pylint normalizador_app --exit-zero

echo ""
echo "✅ All checks passed!"
```

## 🔄 Flujo Git

```bash
# Crear rama de feature
git checkout -b feature/mi-feature develop

# Hacer cambios y tests...

# Commit
git add .
git commit -m "feat: descripción del cambio"

# Push
git push origin feature/mi-feature

# Abrir PR en GitHub

# Esperar a que CI/CD pase ✓

# Mergear el PR
```

## 🌐 Badges para README

```markdown
# Shields.io badges
[![Tests](https://img.shields.io/github/workflow/status/tu-usuario/normalizador-audio/Tests%20%26%20Coverage?label=tests)](https://github.com/tu-usuario/normalizador-audio/actions)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

# Codecov (una vez que lo configures)
[![codecov](https://codecov.io/gh/tu-usuario/normalizador-audio/branch/main/graph/badge.svg)](https://codecov.io/gh/tu-usuario/normalizador-audio)
```

## 📌 Estructura de un buen test

```python
import pytest
from unittest.mock import patch, MagicMock

class TestMyModule:
    """Describe what the module does"""
    
    def test_happy_path(self):
        """Test the main success case"""
        # Arrange
        input_data = {"key": "value"}
        
        # Act
        result = my_function(input_data)
        
        # Assert
        assert result is not None
        assert result["key"] == "value"
    
    def test_error_handling(self):
        """Test error conditions"""
        with pytest.raises(ValueError):
            my_function(invalid_input)
    
    @patch("module.external_call")
    def test_with_mock(self, mock_external):
        """Test with mocked dependencies"""
        mock_external.return_value = {"result": 42}
        
        result = my_function()
        
        assert result == 42
        mock_external.assert_called_once()
```

## 📊 Métricas de cobertura

```
Objetivo: >90% cobertura

Actual (34 tests):
- audio_service: 95%
- config_manager: 98%
- dependency_service: 92%
- report_service: 94%
- TOTAL: 95%
```

## 🆘 Troubleshooting

| Problema | Solución |
|----------|----------|
| Tests no se encuentran | `pytest tests/ -v` (verifica que conftest.py existe) |
| FFmpeg mock falla | Usa `@patch()` correctamente (ver ejemplos en tests/) |
| Coverage baja | Agrega más assertions, testa edge cases |
| Sintaxis error en CI | Corre `python -m compileall .` localmente |
| Imports rotos | Verifica `__init__.py` en todas las carpetas |

## 📚 Referencias

- [pytest docs](https://docs.pytest.org/)
- [GitHub Actions docs](https://docs.github.com/actions)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [PEP 8](https://pep8.org/)
- [Semantic Versioning](https://semver.org/)
