"""
ПРОГРАММА ДЛЯ БПЛА GEOSCAN С ЯНДЕКС.КАРТАМИ (без API ключа)
Школьный проект "ГеоПамять" - 6 класс
"""

import json
import os
import csv
from datetime import datetime

class ГеосканЯндексБезAPI:
    """Класс для работы с БПЛА GEOSCAN и Яндекс.Картами без API ключа"""
    
    def __init__(self):
        """Инициализация"""
        self.данные_дрона = []
    
    def получить_данные(self):
        print("🚁 Получение данных GEOSCAN...")
        
        данные = [
            {
                "файл": "GEOSCAN_школа_01.jpg",
                "широта": 55.918423,
                "долгота": 37.716871,
                "высота": 150.5,
                "время": "10:30:00",
                "описание": "Школа"
            },
            {
                "файл": "GEOSCAN_стадион_01.jpg",
                "широта": 55.917676,
                "долгота": 37.715534,
                "высота": 152.0,
                "время": "10:31:00",
                "описание": "Футбольное поле"
            },
            {
                "файл": "GEOSCAN_парк_01.jpg",
                "широта": 55.917558,
                "долгота": 37.717424,
                "высота": 153.5,
                "время": "10:32:00",
                "описание": "Парк"
            },
            {
                "файл": "GEOSCAN_спортплощадка_01.jpg",
                "широта": 55.917301,
                "долгота": 37.716215,
                "высота": 151.0,
                "время": "10:33:00",
                "описание": "Спортивная площадка"
            }
        ]
        
        return данные
    
    def загрузить_данные_из_файла(self, путь_к_файлу):
        """Загружает данные из файла"""
        if not os.path.exists(путь_к_файлу):
            print(f"❌ Файл не найден: {путь_к_файлу}")
            return []
        
        try:
            расширение = os.path.splitext(путь_к_файлу)[1].lower()
            
            if расширение == '.json':
                with open(путь_к_файлу, 'r', encoding='utf-8') as файл:
                    данные = json.load(файл)
            elif расширение == '.csv':
                данные = []
                with open(путь_к_файлу, 'r', encoding='utf-8') as файл:
                    reader = csv.DictReader(файл)
                    for строка in reader:
                        данные.append({
                            "файл": строка.get('Файл', ''),
                            "широта": float(строка.get('Широта', 0)),
                            "долгота": float(строка.get('Долгота', 0)),
                            "высота": float(строка.get('Высота', 0)),
                            "время": строка.get('Время', ''),
                            "описание": строка.get('Описание', '')
                        })
            else:
                print(f"❌ Неподдерживаемый формат: {расширение}")
                return []
            
            print(f"✅ Загружено {len(данные)} записей из файла")
            return данные
            
        except Exception as e:
            print(f"❌ Ошибка при загрузке файла: {e}")
            return []
    
    def создать_карту_без_api(self, данные, имя_файла="geoscan_map.html"):
        """
        Создает карту с Яндекс.Картами без API ключа
        Используем альтернативный способ встраивания карт
        """
        
        if not данные:
            print("❌ Нет данных для создания карты")
            return
        
        # Вычисляем средние координаты
        широты = [з['широта'] for з in данные]
        долготы = [з['долгота'] for з in данные]
        средняя_широта = sum(широты) / len(широты)
        средняя_долгота = sum(долготы) / len(долготы)
        
        print("🗺️ Создание карты с Яндекс.Картами...")
        
        # HTML с использованием статической карты
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>БПЛА GEOSCAN - Карта полета</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 3px solid #667eea;
        }}
        
        .header h1 {{
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            color: #666;
            font-size: 1.2em;
        }}
        
        .map-section {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }}
        
        @media (max-width: 768px) {{
            .map-section {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .static-map {{
            width: 100%;
            height: 500px;
            background: #f5f5f5;
            border-radius: 15px;
            overflow: hidden;
            position: relative;
        }}
        
        .map-image {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        
        .map-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: rgba(0,0,0,0.5);
            color: white;
            padding: 20px;
            text-align: center;
        }}
        
        .points-list {{
            background: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            overflow-y: auto;
            max-height: 500px;
        }}
        
        .point-card {{
            background: white;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
            transition: transform 0.3s ease;
            cursor: pointer;
        }}
        
        .point-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }}
        
        .point-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        .point-number {{
            background: #667eea;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }}
        
        .point-filename {{
            font-weight: bold;
            color: #333;
            font-size: 1em;
        }}
        
        .point-coords {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 5px;
        }}
        
        .point-description {{
            color: #888;
            font-size: 0.9em;
            font-style: italic;
            margin-top: 5px;
        }}
        
        .coordinates-section {{
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            margin-top: 30px;
        }}
        
        .coordinates-section h3 {{
            color: #667eea;
            margin-bottom: 20px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .coord-table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }}
        
        .coord-table th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
        }}
        
        .coord-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .coord-table tr:hover {{
            background: #f7fafc;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        .stat-label {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #e2e8f0;
            color: #666;
            font-size: 0.9em;
        }}
        
        /* Стили для скроллбара */
        .points-list::-webkit-scrollbar {{
            width: 8px;
        }}
        
        .points-list::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 4px;
        }}
        
        .points-list::-webkit-scrollbar-thumb {{
            background: #667eea;
            border-radius: 4px;
        }}
        
        .points-list::-webkit-scrollbar-thumb:hover {{
            background: #764ba2;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚁 БПЛА GEOSCAN - Карта полета</h1>
            <div class="subtitle">
                Школьный проект "ГеоПамять" | {datetime.now().strftime('%d.%m.%Y %H:%M')}
            </div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{len(данные)}</div>
                <div class="stat-label">Фотографий</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{min(з['высота'] for з in данные):.0f} м</div>
                <div class="stat-label">Мин. высота</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{max(з['высота'] for з in данные):.0f} м</div>
                <div class="stat-label">Макс. высота</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{данные[0]['время'][:5] if данные else '--'}</div>
                <div class="stat-label">Начало съемки</div>
            </div>
        </div>
        
        <div class="map-section">
            <div  id="map">
                <script src="https://api-maps.yandex.ru/2.1/?lang=ru_RU"></script>
                    <script>
                        // Создаем карту
                        ymaps.ready(init);
                        
                        function init() {{
                            var map = new ymaps.Map('map', {{
                                center: [{средняя_широта:.6f}, {средняя_долгота:.6f}],
                                zoom: 15
                            }});
"""
        
        # Добавляем метки для каждой фотографии
        for i, точка in enumerate(данные):
            html += f"""
                            var placemark{i} = new ymaps.Placemark([{точка['широта']}, {точка['долгота']}], {{
                                balloonContent: '<strong><img src="{точка["файл"]}" width="200"></div></strong><br>' +
                                            '📍Координаты: {точка['широта']}, {точка['долгота']}<br>' +
                                            '📏Высота: {точка["высота"]} м<br>' +
                                            '⏰Время: {точка["время"]}<br>' +
                                            'Описание: {точка.get('описание', 'Точка съемки БПЛА GEOSCAN')}'
                            }});
                            map.geoObjects.add(placemark{i});
"""
        
        html += f"""
                        }}
                    </script>
                
            </div>
            
            <div class="points-list">
                <h3 style="color: #667eea; margin-bottom: 20px;">📸 Точки съемки</h3>
"""
        
        # Добавляем карточки точек
        for i, точка in enumerate(данные):
            html += f"""
                <div class="point-card" onclick="showPoint({i})">
                    <div class="point-header">
                        <div class="point-number">{i+1}</div>
                        <div class="point-filename">{точка['файл']}</div>
                    </div>
                    <div class="point-coords">
                        📍 Широта: {точка['широта']:.6f}<br>
                        📍 Долгота: {точка['долгота']:.6f}
                    </div>
                    <div class="point-coords">
                        📏 Высота: {точка['высота']:.1f} м
                    </div>
                    <div class="point-coords">
                        ⏰ Время: {точка['время']}
                    </div>
                    <div class="point-description">
                        {точка.get('описание', 'Точка съемки БПЛА GEOSCAN')}
                    </div>
                </div>
"""
        
        html += f"""
            </div>
        </div>
        
        <div class="coordinates-section">
            <h3>📍 Координаты для Яндекс.Карт/Google Maps</h3>
            <table class="coord-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Точка</th>
                        <th>Широта</th>
                        <th>Долгота</th>
                        <th>Ссылка</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        # Добавляем строки таблицы с координатами
        for i, точка in enumerate(данные):
            # Создаем ссылку для Яндекс.Карт
            yandex_link = f"https://yandex.ru/maps/?ll={точка['долгота']},{точка['широта']}&mode=search&z=17.16&sll={точка['широта']},{точка['долгота']}"
            # Создаем ссылку для Google Maps
            google_link = f"https://www.google.com/maps?q={точка['широта']},{точка['долгота']}"
            
            html += f"""
                    <tr>
                        <td><strong>{i+1}</strong></td>
                        <td>{точка['файл']}</td>
                        <td>{точка['широта']:.6f}</td>
                        <td>{точка['долгота']:.6f}</td>
                        <td>
                            <a href="{yandex_link}" target="_blank" style="color: #667eea; margin-right: 10px;">
                                Яндекс.Карты
                            </a>
                            <a href="{google_link}" target="_blank" style="color: #34A853;">
                                Google Maps
                            </a>
                        </td>
                    </tr>
"""
        
        html += f"""
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>🚁 Проект выполнен с использованием данных БПЛА GEOSCAN</p>
            <p>Школьный проект "ГеоПамять" | {datetime.now().strftime('%Y')} г.</p>
            <p style="font-size: 0.8em; margin-top: 10px; color: #888;">
                Для создания интерактивной карты используйте координаты выше в Яндекс.Картах или Google Maps
            </p>
        </div>
    </div>

    <script>
        // Функция для показа информации о точке
        function showPoint(index) {{
            const point = {json.dumps(данные, ensure_ascii=False)};
            if (index >= 0 && index < point.length) {{
                const p = point[index];
                alert(
                    `Точка #${{index + 1}}\\n` +
                    `Файл: ${{p.файл}}\\n` +
                    `Координаты: ${{p.широта.toFixed(6)}}, ${{p.долгота.toFixed(6)}}\\n` +
                    `Высота: ${{p.высота}} м\\n` +
                    `Время: ${{p.время}}\\n` +
                    `Описание: ${{p.описание || 'Нет описания'}}`
                );
                
            }}
        }}
        
        // Функция для скачивания данных в JSON
        function downloadJSON() {{
            const data = {json.dumps(данные, ensure_ascii=False)};
            const dataStr = JSON.stringify(data, null, 2);
            const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
            const exportFileDefaultName = 'geoscan_data.json';
            
            const linkElement = document.createElement('a');
            linkElement.setAttribute('href', dataUri);
            linkElement.setAttribute('download', exportFileDefaultName);
            linkElement.click();
        }}
        
        // Функция для скачивания координат в CSV
        function downloadCSV() {{
            const points = {json.dumps(данные, ensure_ascii=False)};
            let csvContent = "data:text/csv;charset=utf-8,";
            csvContent += "Номер,Файл,Широта,Долгота,Высота,Время,Описание\\n";
            
            points.forEach((point, index) => {{
                const row = [
                    index + 1,
                    point.файл,
                    point.широта,
                    point.долгота,
                    point.высота,
                    point.время,
                    point.описание || ''
                ].join(",");
                csvContent += row + "\\n";
            }});
            
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "geoscan_coordinates.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }}
        
        // Добавляем кнопки для скачивания
        document.addEventListener('DOMContentLoaded', function() {{
            const footer = document.querySelector('.footer');
            const downloadButtons = `
                <div style="margin-top: 20px;">
                    <button onclick="downloadJSON()" style="background: #667eea; color: white; border: none; padding: 10px 20px; border-radius: 5px; margin-right: 10px; cursor: pointer;">
                        📥 Скачать JSON
                    </button>
                    <button onclick="downloadCSV()" style="background: #34A853; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">
                        📊 Скачать CSV
                    </button>
                </div>
            `;
            footer.insertAdjacentHTML('beforeend', downloadButtons);
        }});
    </script>
</body>
</html>"""
        
        # Сохраняем HTML файл
        with open(имя_файла, 'w', encoding='utf-8') as файл:
            файл.write(html)
        
        print(f"✅ Карта создана: {имя_файла}")
        
        return имя_файла
    
    
    def сохранить_данные(self, данные, имя_файла="geoscan_data.json"):
        """Сохраняет данные в JSON файл"""
        результат = {
            "проект": "ГеоПамять - БПЛА GEOSCAN",
            "дата_обработки": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "количество_точек": len(данные),
            "данные": данные,
            "инструкция": "Для просмотра на карте используйте координаты в Яндекс.Картах или Google Maps"
        }
        
        with open(имя_файла, 'w', encoding='utf-8') as файл:
            json.dump(результат, файл, ensure_ascii=False, indent=2)
        
        print(f"✅ Данные сохранены: {имя_файла}")
        
        # Также сохраняем в CSV для удобства
        csv_имя = имя_файла.replace('.json', '.csv')
        self.сохранить_в_csv(данные, csv_имя)
        
        return имя_файла
    
    def сохранить_в_csv(self, данные, имя_файла="geoscan_data.csv"):
        """Сохраняет данные в CSV файл"""
        with open(имя_файла, 'w', encoding='utf-8', newline='') as файл:
            writer = csv.writer(файл)
            writer.writerow(['Номер', 'Файл', 'Широта', 'Долгота', 'Высота', 'Время', 'Описание'])
            
            for i, точка in enumerate(данные):
                writer.writerow([
                    i + 1,
                    точка['файл'],
                    f"{точка['широта']:.6f}",
                    f"{точка['долгота']:.6f}",
                    f"{точка['высота']:.1f}",
                    точка['время'],
                    точка.get('описание', '')
                ])
        
        print(f"✅ Данные сохранены в CSV: {имя_файла}")

def главное_меню():
    """Главное меню программы"""
    
    обработчик = ГеосканЯндексБезAPI()
    данные = []
    фл_СоздаемКарту = 0

    while True:
        print("1️⃣. 🗺️ Создать карту с координатами")
        print("0️⃣. 🚪 Выход")
        
        выбор = input("\nВыберите действие (1 или 0): ").strip()
        
        if выбор == "1":
            if not данные:
                print("\n" + "-"*80)
                print("Загрузка данных GEOSCAN...")
                print("❌ Данные для отрисовки карты отсутствуют.")
                print("     2️⃣. 📥 Загрузить данные из файла (JSON/CSV)")
                print("     3️⃣. 📁 Использовать тестовые данные")

                выбор1 = input("\nВыберите действие (2 или 3): ").strip()
                if выбор1 == "2":
                    путь = input("Введите путь к файлу (или Enter для geoscan_coordinates.csv): ").strip()
                    if not путь:
                        путь = "geoscan_coordinates.csv"
                    
                        данные = обработчик.загрузить_данные_из_файла(путь)
                        фл_СоздаемКарту = 1
                elif выбор1 == "3":
                    данные = обработчик.получить_данные()
                    print("-"*80)
                    фл_СоздаемКарту = 1
            else:
                фл_СоздаемКарту = 1    
                
            
        elif выбор == "0":
            print("\n👋 Спасибо за использование программы!")
            print("   Успехов в проекте 'ГеоПамять'!")
            print("="*80)
            break
        
        else:
            print("❌ Неверный выбор")

        if фл_СоздаемКарту == 1:
            имя_файла = input("Имя для карты (Enter для geoscan_map.html): ").strip()
            if not имя_файла:
                имя_файла = "geoscan_map.html"
            обработчик.создать_карту_без_api(данные, имя_файла)
            print(f"\n✅ Откройте файл {имя_файла} в браузере")
            print("📌 Используйте ссылки в карте для просмотра точек в Яндекс.Картах")

# Запуск программы
if __name__ == "__main__":
    print("="*80)
    print("🚁 БПЛА GEOSCAN + Карты яндекс")

        
    # Запускаем главное меню
    главное_меню()