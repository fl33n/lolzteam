## Установка

### 1. Клонировать репозиторий;
### 2. Создать виртуальное окружение внутри, введя команду:
```
python3 -m venv venv
```
### 3. Создать переменные окружения TOKEN и DB_PATH, отредактировав файл source/.env:
```
TOKEN=1234567890:AAElbvYpe3ILiTva70-TQR7q1C1SEt3g5ZBiaM
DB_PATH=data/base/base.sqlite
```
### 4. Активировать виртуальное окружение командой:  
*  Windows:
```
venv\Scripts\activate.bat
```
*  Linux:
```
source venv/bin/activate
```
### 5. Установить зависимости командой:
```
pip3 install -r requirements.txt
```
### 6. Запустить бота при помощи файла main.py:
```
cd source
python3 main.py
```
