import pyautogui
import keyboard
import time
import os
import json
import random

def get_position(prompt):
    print(prompt)
    keyboard.wait('enter')
    pos = pyautogui.position()
    print(f"Выбранная точка: {pos}")
    return pos

def save_coordinates(swipes, filename='coordinates.json'):
    with open(filename, 'w') as f:
        json.dump(swipes, f)
    print(f"Координаты сохранены в файл {filename}.")

def load_coordinates(filename='coordinates.json'):
    if not os.path.exists(filename):
        return None
    with open(filename, 'r') as f:
        swipes = json.load(f)
    return swipes

def save_settings(settings, filename='settings.json'):
    with open(filename, 'w') as f:
        json.dump(settings, f)
    print(f"Настройки сохранены в файл {filename}.")

def load_settings(filename='settings.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None

def get_user_input():
    settings = load_settings()

    if settings:
        print(f"Загружены настройки из файла: {settings}")
        use_saved = input("Использовать сохранённые настройки? (y/n): ").lower() == 'y'
        if use_saved:
            return settings
    
    num_iterations = int(input("Введите количество повторений свайпа (по умолчанию 20): ") or 20)
    min_interval = float(input("Введите минимальный интервал между действиями (по умолчанию 1 сек): ") or 1)
    max_interval = float(input("Введите максимальный интервал между действиями (по умолчанию 3 сек): ") or 3)
    swipe_duration = float(input("Введите скорость свайпа в секундах (по умолчанию 1 сек): ") or 1)

    settings = {
        'num_iterations': num_iterations,
        'min_interval': min_interval,
        'max_interval': max_interval,
        'swipe_duration': swipe_duration
    }

    save = input("Сохранить настройки для будущего использования? (y/n): ").lower() == 'y'
    if save:
        save_settings(settings)
    
    return settings

def main():
    filename = 'coordinates.json'
    swipes = load_coordinates(filename)

    if not swipes:
        swipes = []
        num_swipes_to_record = 3
        print(f"Файл с координатами не найден. Запишите {num_swipes_to_record} свайпов.")
        for i in range(num_swipes_to_record):
            print(f"Запись свайпа {i+1}/{num_swipes_to_record}")
            start_pos = get_position("Переместите курсор в начальную точку и нажмите Enter.")
            end_pos = get_position("Переместите курсор в конечную точку и нажмите Enter.")
            swipes.append({'start': {'x': start_pos[0], 'y': start_pos[1]},
                           'end': {'x': end_pos[0], 'y': end_pos[1]}})
        
        save_coordinates(swipes, filename)
    else:
        print(f"Загружены координаты из файла {filename}.")

    # Получение настроек от пользователя
    settings = get_user_input()
    num_iterations = settings['num_iterations']
    min_interval = settings['min_interval']
    max_interval = settings['max_interval']
    swipe_duration = settings['swipe_duration']

    print("Скрипт выполнит несколько свайпов и нажатий клавиши 'End' с рандомным выбором записанных свайпов и интервалом.")
    print("Переключитесь на нужное окно.")
    time.sleep(5)

    for i in range(num_iterations):
        # Рандомный выбор свайпа
        swipe = random.choice(swipes)
        start_pos = (swipe['start']['x'], swipe['start']['y'])
        end_pos = (swipe['end']['x'], swipe['end']['y'])

        print(f"Выполнение свайпа {i+1}/{num_iterations}...")
        pyautogui.moveTo(start_pos)
        pyautogui.dragTo(end_pos, duration=swipe_duration)
        
        # Нажатие клавиши 'End'
        pyautogui.press('end')
        
        # Пауза с рандомным интервалом
        interval = random.uniform(min_interval, max_interval)
        print(f"Ждем {interval:.2f} секунд перед следующим действием.")
        time.sleep(interval)

    print("Все действия выполнены.")

if __name__ == "__main__":
    main()
