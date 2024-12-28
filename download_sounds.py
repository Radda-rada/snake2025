import urllib.request
import os

# Создаем папку sounds, если её нет
if not os.path.exists('sounds'):
    os.makedirs('sounds')

# Ссылки на звуковые файлы (обновленные)
sound_files = {
    'bell.wav': 'https://www.soundjay.com/misc/sounds/bell-ringing-01.wav',
    'game_over.mp3': 'https://www.soundjay.com/misc/sounds/fail-buzzer-03.mp3',
    'jingle_bells.mp3': 'https://www.soundjay.com/misc/sounds/christmas-music-01.mp3'
}

def download_file(url, filepath):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        return True
    except Exception as e:
        print(f"Ошибка при загрузке: {e}")
        return False

print("Начинаем загрузку звуковых файлов...")

# Загружаем каждый файл
for filename, url in sound_files.items():
    filepath = os.path.join('sounds', filename)
    if not os.path.exists(filepath):
        print(f'Загрузка {filename}...')
        if download_file(url, filepath):
            print(f'{filename} успешно загружен')
        else:
            print(f'Не удалось загрузить {filename}')
    else:
        print(f'{filename} уже существует')

print("\nЗагрузка завершена!") 