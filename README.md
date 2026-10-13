# Калькулятор

Простой оконный калькулятор на Python и Tkinter. Поддерживает сложение,
вычитание, умножение, деление, десятичные числа и скобки.

## Запуск из исходников

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\calculator.exe
```

## Сборка Windows EXE

```powershell
.\build.ps1
```

Готовый файл появится по адресу `dist\Calculator.exe`.
