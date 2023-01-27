Данный проект создан для тренировки навыков применения паттернов и архитектур.

# Структура
## Пакеты
![Пакеты](https://raw.githubusercontent.com/PavelAltynnikov/pygame-sandbox/master/packages.png)
## Классы
![Классы](https://raw.githubusercontent.com/PavelAltynnikov/pygame-sandbox/master/classes.png)
## Генерация
`pyreverse -o png sandbox --output-directory diagrams`

# Окружение
```
Интерпретатор:  Python 3.10  
Зависимости:    requirements.txt
```

## Создание
`py -3.10 -m venv venv`

## Активация
Windows

`. env/Scripts/activate`  

Linux

`. env/bin/activate`

## Установка зависимостей
`python -m pip install -r requirements.txt`

# Запуск
## Игра
`python -m sandbox`

## Тесты
На текущий момент тесты мануальные.  
`python tests/test_module_name.py`
