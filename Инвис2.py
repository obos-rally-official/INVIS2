import sys
import math as m
import numpy as np
import random
from PySide6.QtGui import (QFont, QColor, QPainter, QBrush, 
                          QPen, QRadialGradient, QConicalGradient,
                          QTextDocument, QPixmap, QLinearGradient)
from PySide6.QtWidgets import QGraphicsOpacityEffect
from PySide6.QtCore import (Qt, QTimer, QPointF, QPropertyAnimation, 
                           QEasingCurve, QRectF, QSize, QParallelAnimationGroup,)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QDialog,
    QVBoxLayout, QLineEdit, QLabel, QHBoxLayout, QSizePolicy,
    QPushButton, QTextEdit, QGraphicsDropShadowEffect, QGraphicsEffect,
    QScrollArea
)
from PySide6.QtCore import Property
import pyqtgraph as pg

pg.setConfigOptions(antialias=True, useOpenGL=True, enableExperimental=True)

SPACE_STYLE = """
    QWidget {
        background-color: #0A0A12;
        color: #C0C0FF;
        font-family: "Orbitron";
        font-weight: medium;
    }
    QTabWidget::pane {
        margin-top: 20px;
        border: 2px solid #30304D;
        border-radius: 8px;
        margin: 4px;
        background: #10101A;
    }
    QTabBar::tab {
        background: #1A1A2F;
        color: #7F7FFF;
        padding: 12px 24px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        font-size: 12pt;
        border: 1px solid #30304D;
    }
    QTabBar::tab:selected {
        background: #2A2A4F;
        color: #00FFFF;
        border-bottom: 3px solid #00FFFF;
    }
    QLineEdit {
        background: #151523;
        border: 2px solid #30304D;
        border-radius: 6px;
        padding: 10px;
        font-size: 12pt;
        color: #00FFE5;
        selection-background-color: #0066FF;
    }
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #0066FF, stop:1 #00CCFF);
        border-radius: 8px;
        padding: 15px 30px;
        font-size: 14pt;
        font-weight: bold;
        color: #001133;
        text-transform: uppercase;
        min-width: 200px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #0055DD, stop:1 #00BBEE);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #0044CC, stop:1 #00AAEE);
    }
    .error {
        color: #FF4444;
        font-weight: bold;
        font-size: 12pt;
    }
    .planet_section {
        border: 2px solid #30304D;
        border-radius: 12px;
        padding: 20px;
        background: #10101A;
    }
    #planet_info {
        font-size: 14pt;
        color: #7F7FFF;
        padding: 15px;
    }
    .comment {
        font-style: italic;
        color: #6060A0;
        margin-bottom: 10px;
        font-size: 12pt;
    }
    .cyber-border {
        border: 2px solid #00FFFF;
        border-radius: 8px;
        padding: 15px;
        background: #10101A;
    }
    QTextEdit {
        background: #151523;
        border: 2px solid #30304D;
        color: #C0C0FF;
        font-size: 12pt;
        padding: 10px;
    }
"""

PLANET_INFO = {
    "меркурий": """Меркурий: ближайший к Солнцу и полный парадоксов<br><br>
    Древний странник<br>
    Меркурий известен с античности: его наблюдали вавилоняне (назвали «Набу»), греки — «Гермес», римляне дали имя бога-посланника за быстрое движение. Первые детальные снимки сделал зонд «Маринер-10» в 1974 году, открыв кратеры и гигантские уступы — следы остывания ядра.<br><br>
    Мир крайностей<br>
    - Температура: От -180°C (ночная сторона) до +430°C (дневная).<br>
    - Поверхность: Кратеры, базальтовые равнины и скалы до 3 км высотой.<br>  
    - Ядро: Занимает 85% радиуса — вероятно, осталось после столкновения, «сорвавшего» кору.<br>
    - Суточный цикл: Один день длится 176 земных суток из-за резонанса вращения 3:2.<br>
    - Гравитационные аномалии: Смещение перигелия Меркурия подтвердило Общую теорию относительности.<br><br>
    Научная загадка: В 2012 году зонд «Мессенджер» обнаружил лёд в полярных кратерах. Возможно, его занесли кометы.<br><br>
    Культура и восприятие<br>
    - Миф: В алхимии Меркурий символизировал ртуть и изменчивость.<br>
    - Поп-культура: В фильме «Солярис» упоминается меркурианская станция.<br>
    -Психология восприятия: его пейзаж — почти без изменений в течение миллиардов лет — заставляет задуматься о цене стабильности.<br>
    - Заблуждение: «Меркурий горячее Венеры» — нет, из-за отсутствия атмосферы он быстро теряет тепло.<br><br>
    <i>Если ты ближе всех к свету, это не значит, что тебя видно первым.</i>""",

    "венера": """Венера: ад в бархатной обёртке<br><br>
    Лжеблизнец<br>
    Венеру считали «близнецом Земли» до 1960-х, когда зонды СССР («Венера-7») выявили: давление 93 бар, температура +470°C, дожди из серной кислоты. Атмосфера — CO₂ с облаками, отражающими 75% света.<br><br>
    Тайны под облаками<br>
    - Вращение: В обратную сторону (один день = 243 земных).<br>
    - Вулканы: Радарные карты показали тысячи вулканов. В 2023 году найдены признаки активных извержений.<br>
    -Возможен эффект «обратной эволюции» — планета могла быть обитаема, но эффект запустился слишком рано.<br>
    - Теория: Возможно, когда-то здесь были океаны, но парниковый эффект их испарил.<br>
    - Радиолокационные карты: Поверхность изучается через облака.<br>
    - Тепловой буфер: Густая атмосфера создаёт постоянную термическую нагрузку, разрушая электронику за часы.<br><br>
    Культурная связность<br>
    - *Литература*: В повести Брэдбери «И грянул гром» Венера — джунгли (отражение старых гипотез).<br>
    - Название: В честь богини любви — из-за красоты на утреннем небе.<br>
    - Заблуждение: «На Венере можно увидеть поверхность» — облака непрозрачны, рельеф изучают радарами.<br>
    - Символизм: В культуре Венера олицетворяет соблазн, при этом в науке она — образ катастрофической красоты.<br>
    - Психологический эффект: Резкое несоответствие визуального и реального стало метафорой для ложных ожиданий в культуре.<br><br>
    <i>Облака вспоминают море,но слёз их не видит земля.</i>""",

    "земля": """Земля: хрупкий оазис<br><br>
    От геоцентризма к голубой точке<br>
    Долгое время Землю считали центром Вселенной. В 1968 году фото «Восход Земли» с Луны показало её уязвимость в космосе.<br><br>
    Уникальность в цифрах<br>
    - Биосфера: Единственная планета с подтверждённой жизнью.<br>
    - Тектоника плит: Формирует ландшафт и регулирует климат.<br>
    - Луна: Гигантский спутник, стабилизирующий ось вращения.<br>
    - Климат: С 1850 года средняя температура выросла на 1.1°C — следствие индустриализации.<br>
    - Связь социума: 90% населения сосредоточено в северном полушарии, где формируются культурные нормы.<br>
    - Педагогический эффект: Земля служит базой для сравнительной планетологии и экологической мысли.<br><br>
    Мифы и реальность<br>
    - Заблуждение: «Земля идеально круглая» — сплюснута у полюсов на 43 км.<br>
    - Культура: В скандинавских мирах — диск, в индуизме — на слонах и черепахе, а кто-то ваще думает, что это пончик.<br>
    - Теория: «Гипотеза Геи» — Земля как саморегулирующийся организм. Спорна, но вдохновила экологов.<br>
    - Символизм: Земля часто изображается как мать, дающая и отбирающая — образ, перекочевавший из древних религий в современные движения.<br><br>
    <i>Не центр, но зеркало Вселенной, в котором она смотрит на себя.</i>""",

    "марс": """Марс: красная загадка<br><br>
    От «каналов» до марсоходов<br>
    В 1877 году Джованни Скиапарелли «увидел» каналы, породив миф о марсианах. Реальность открыли миссии: «Викинг-1» (1976), «Кьюриосити» (2012), «Персеверанс» (2021).<br><br>
    Следы воды и метана<br>
    - Рельеф: Долина Маринер (в 10 раз глубже Гранд-Каньона).<br>
    - Атмосфера: 95% CO₂, давление 0.6% земного.<br>
    - Жизнь?: В 2018 году обнаружено подлёдное озеро.<br>
    - Магнитные «призраки»: Остаточные магнитные аномалии в коре.<br><br>
    Культура и будущее<br>
    - Литература: «Марсианские хроники» Брэдбери, «Марсианин» Вейера.<br>
    -Астрономия и общество: Более 40% опрошенных в ряде стран (вкл. США) уверены, что Марс уже был обитаем, хотя научно это лишь гипотеза.<br>
    - Колонизация: Илон Маск планирует город на Марсе к 2050 году. Проблемы: радиация, низкая гравитация.<br>
    - Архетип: В массовой культуре — символ перезапуска, бегства и сопротивления.<br>
    -"Всегда буду против": в научной фантастике Марс почти всегда — символ революции, сепарации от Земли. Это отражает глубокий архетип желания начать заново.<br>
    - Психологический эффект: Его цвет и безжизненность формируют образ далёкого одиночества.<br><br>
    <i>Пески,пески...И ни одно облачко не коснётся шляпы походной твоей.</i>""",

    "юпитер": """Юпитер: царь бурь<br><br>
    Открытие Галилея<br>
    В 1610 году Галилей увидел 4 спутника (Ио, Европа, Ганимед, Каллисто), доказав, что не всё вращается вокруг Земли.<br><br>
    Гигантские тайны<br>
    - Большое Красное Пятно: Антициклон размером с Землю.<br>
    - Кольца: Обнаружены «Вояджером-1» в 1979 — тёмные, из пыли.<br>
    - Радиация: Мощные пояса убивают электронику.<br>
    - Металлический водород: Под облаками океан, генерирующий магнитное поле сильнее земного в 20 000 раз.<br><br>
    Роль в Солнечной системе<br>
    - Гравитационный щит: Защищает внутренние планеты от многих комет и астероидов.<br>
    - Символизм: Образ власти и центра тяжести, как реальный, так и культурный.<br>
    - Педагогика масштаба: Используется для визуализации астрономических соотношений.<br>
    - Кино: В «2010: Одиссея Два» превращается в звезду.<br><br>
    <i>Ах,сколь мал я перед ним!-
    Бабочка упорхнула с куста...Помнит ли он о ней?.</i>""",

    "сатурн": """Сатурн: властелин колец<br><br>
    Кольца: ледяное великолепие-<br>
    Частицы льда (от микрон до метров) создают структуру в тысячи колец. Толщина — не более 100 метров.
    вероятно, кольца образовались всего 100 млн лет назад — это геологически «вчера»<br><br>
    Спутники-сокровища<br>
    - Титан: Единственный спутник с плотной атмосферой.<br>
    - Энцелад: Подлёдный океан — цель поисков жизни.<br>
    - Япет: Контраст тёмного и светлого полушарий — загадка происхождения.<br>
    - Феба: Нерегулярная орбита, вращение «спиной» к Сатурну, возможно захваченный объект.<br><br>
    Звук Сатурна: с помощью радиоданных Кассини удалось «услышать» Сатурн — его магнитные волны звучат как электронная музыка под водой<br><br>
    Философия и культура<br>
    - Астрология: Сатурн ассоциируется с временем и кармой.<br>
    - Философия: В античной культуре Сатурн ассоциировался не только с временем, но и с внутренней зрелостью, завершением цикла.<br>
    - Заблуждение: «Кольца твердые» — они состоят из пыли и льда.<br>
    - Кино: В «Интерстелларе» кольца Сатурна стали вратами в иное измерение.<br><br>
    <i>И кольца плывут — не замыкаясь в вечность, как отсроченная мысль.</i>""",

    "уран": """Уран: ледяной гигант на боку<br><br>
    Эту планету современники просто не поняли. Как им вообще доверять?<br><br>
    Уильям Гершель обнаружил Уран в 1781 году, приняв его за комету. Первая планета, найденная с помощью телескопа.<br><br>
    Наклон и аномалии<br>
    - Ось вращения: Наклонена на 98° — возможно, из-за столкновения.<br>
    - Цвет: Сине-зелёный от метана.<br>
    - Кольца: Темные, открыты в 1977 году при затмении звезды.<br>
    - Температурный парадокс: Уран излучает почти столько же тепла, сколько получает от Солнца, что до сих пор не объяснено окончательно..<br><br>
    Мифы и факты<br>
    - Название: Уран — греческий бог неба, отец Сатурна (Кроноса).<br>
    - Культура: В романе «Космическая одиссея 2061» Уран колонизирован.<br>
    - Заблуждение: «Уран и Нептун — близнецы» — нет, у Урана меньше внутреннего тепла и иная структура.<br>
    - Тема инаковости: Уран — символ уклонения от нормы, тихой нестандартности.<br>
    В культуре часто игнорируется (даже в «Интерстелларе» его обошли). Это превращает Уран в социологическую метафору незаметного гения.<br>
    - Роль в открытиях: Открыл понятие внешней планеты, не видимой невооружённым глазом.<br>
    - Теория: Под слоем льда и водорода — алмазные дожди, формирующиеся при высоком давлении.<br><br>
    <i>Повернулся на бок — и все подумали, что сломался. А он просто иначе мыслит.</i>""",

    "нептун": """Нептун: последний великан<br><br>
    Планета, открытая математикой<br>
    В 1846 году Урбен Леверье и Джон Адамс независимо вычислили положение Нептуна по отклонениям орбиты Урана. Обнаружен Иоганном Галле в Берлинской обсерватории.<br><br>
    Царство ветров и льда<br>
    - Ветра: До 2100 км/ч — самые быстрые в Солнечной системе.<br>
    - Тритон: Ретроградная орбита, гейзеры жидкого азота.<br>
    - Большое Тёмное Пятно: Шторм, исчезнувший к 1994 году.<br>
    - Внутренний нагрев: Температуры в ядре до 4700°C. Генерирует конвекцию, питающую ураганы.<br><br>
    Культурный код<br>
    - Название: В честь римского бога морей.<br>
    - Литература: Упоминается в «Путешествиях Гулливера» и научной фантастике XX века.<br>
    - Символизм: Образ далеких глубин — как в океане, так и в психике человека.<br>
    - Тема дистанции: Самая удалённая из известных планет в классическом представлении.<br>
    - Роль в открытиях: Первый случай обнаружения планеты исключительно по расчётам — победа разума над глазом.<br><br>
    <i>Море без дна —
    и всё же оно плывёт
    в молчании числа.</i>""",

    "кашиик": """Кашиик: лесной мир вуки<br><br>
    Родная планета вуки. Она тут ваще по рофлу такто🚀.""",

    "татуин": """Татуин: двойная пустыня<br><br>
    Песчаная планета с двумя солнцами. Она тут ваще по рофлу такто🚀.""",

     "плутон": """Плутон: изгнанник пояса Койпера<br><br>
    Карликовая планета с сердцем из льда<br>
    Открыт в 1930 году Клайдом Томбо. В 2015 году зонд «Новые горизонты» передал первые снимки.<br><br>
    Геология и загадки<br>
    - Спутник Харон: Диаметр 1200 км — центр масс находится вне Плутона.<br>
    - Ледники из азота и горы водяного льда.<br>
    - Атмосфера: Азот, метан и CO. Замерзает при удалении от Солнца.<br>
    - Сердце Плутона: Регион Томбо, яркий ледяной рельеф в форме сердца.<br><br>
    Культура и символизм<br>
    - Астрология: Ассоциируется с трансформацией и подземным миром.<br>
    - История: Потеря статуса планеты вызвала глобальные споры о природе научной истины.<br>
    - Поп-культура: Персонаж Плуто от Disney, 1931 г., назван в честь планеты.<br>
    - Философия: Плутон — метафора изгнания и возвращения, граница известного.<br>
    - Психологический эффект: Его «пониженный статус» вызывает эмпатию и культурную ностальгию.<br><br>
    <i>Снег, что выпал
    за гранью карт
    и остался в памяти детства.</i>"""
}

PLANETS = {
    "меркурий": {
        "radius": 2440,
        "gradient": [QColor(100, 100, 100), QColor(70, 70, 70)],
        "mu": 2.18776e13,        
        "comment": ("«Икар всё ближе к лучезарному солнцу»☀️", "Brush Script MT")
    },
    "венера": {
        "radius": 6052,
        "gradient": [QColor(255, 215, 180), QColor(255, 165, 0)],
        "mu": 3.24829e14,       
        "comment": ("«И дольше века длится день»🌅", "Monotype Corsiva")
    },
    "земля": {
        "radius": 6371,
        "gradient": [QColor(30, 144, 255), QColor(34, 139, 34)],
        "mu": 3.98866e14,       
        "comment": ("«В глобус весь мир поместился!»🌍", "Comic Sans MS")
    },
    "марс": {
        "radius": 3390,
        "gradient": [QColor(139, 0, 0), QColor(205, 92, 92)],
        "mu": 4.2811395e13,     
        "comment": ("«Красный песок — Ветер шепчет тайны.Одни ли мы тут?»👽", 'Bahnschrift')
    },
    "юпитер": {
        "radius": 69911,
        "gradient": [QColor(184, 115, 51), QColor(139, 69, 19)],
        "mu": 1.2673e17,        
        "comment": ("«Жаркого лета разгар! Как облака клубятся на Грозовой горе!»⛈️", "Impact")
    },
    "сатурн": {
        "radius": 58232,
        "gradient": [QColor(245, 245, 220), QColor(210, 180, 140)],
        "mu": 3.78856e16,       
        "comment": ("«Колечко, выйди на крылечко!»💫", "Bradley Hand")
    },
    "уран": {
        "radius": 25362,
        "gradient": [QColor(175, 238, 238), QColor(95, 158, 160)],
        "mu": 5.78956e15,       
        "comment": ("«Гулливер лёг на бок»🛌", "Lucida Handwriting")
    },
    "нептун": {
        "radius": 24622,
        "gradient": [QColor(25, 25, 112), QColor(70, 130, 180)],
        "mu": 6.8034e15,        
        "comment": ("«Ветер, ветер! Ты могуч...»🌬️", "Papyrus")
    },
    "кашиик": {
        "radius": 12000,
        "gradient": [QColor(34, 139, 34), QColor(0, 100, 0)],
        "mu": 5.0e14,           
        "comment": ("«ветер в деревьях свистит - песнь об истории древних вуки»🌳", "Arial Black")
    },
    "татуин": {
        "radius": 6500,
        "gradient": [QColor(255, 215, 0), QColor(139, 69, 19)],
        "mu": 3.2e13,           
        "comment": ("«Два солнца — двойные проблемы»🌞🌞", "Impact")
    },
    "плутон": {
        "radius": 1188,
        "gradient": [QColor(167, 116, 93), QColor(225, 223, 215)],
        "mu": 8.69e11,  # км³/с² (расчётное значение)
        "comment": ("«Нет,я не Байрон,я другой!..»💔 (Рисунок там есть,правдв он малююсенький)", "Century Gothic")
    }
}

class StarfieldWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.stars = []
        self.init_stars()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_stars)
        self.timer.start(50)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.4)

        def resizeEvent(self, event):
            self.init_stars()
            super().resizeEvent(event)

    def init_stars(self):
        for _ in range(150):
            self.stars.append({
                "pos": QPointF(
                    random.uniform(0, self.width()),
                    random.uniform(0, self.height())
                ),
                "size": random.uniform(0.5, 1.5),
                "speed": random.uniform(0.1, 0.3),
                "direction": random.choice([-1, 1])
            })

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        
        for star in self.stars:
            gradient = QRadialGradient(star["pos"], star["size"])
            gradient.setColorAt(0, QColor(255, 255, 255, 150))
            gradient.setColorAt(1, QColor(255, 255, 255, 0))
            painter.setBrush(QBrush(gradient))
            painter.drawEllipse(star["pos"], star["size"], star["size"])

    def animate_stars(self):
        for star in self.stars:
            star["pos"].setX(star["pos"].x() + star["speed"] * star["direction"])
            if star["pos"].x() < 0 or star["pos"].x() > self.width():
                star["direction"] *= -1
        self.update()

class CyberButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet(SPACE_STYLE)
        self.setFixedHeight(50)
        self.effect = QGraphicsDropShadowEffect()
        self.effect.setColor(QColor(0, 255, 255, 100))
        self.effect.setBlurRadius(15)
        self.setGraphicsEffect(self.effect)
        self.anim = QPropertyAnimation(self.effect, b"color")
        self.anim.setDuration(1500)
        self.anim.setStartValue(QColor(0, 255, 255, 100))
        self.anim.setEndValue(QColor(0, 200, 255, 150))
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim.setLoopCount(-1)
        self.anim.start()

class PlanetWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.planet_data = None
        self.rotation_angle = 0
        self.animation_group = QParallelAnimationGroup()
        self.max_planet_radius = 69911  # Радиус Юпитера как базовый для масштабирования
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.init_animations()
        self.setMinimumSize(200, 200)  # Минимальный размер для видимости
        self.max_planet_radius = max(p["radius"] for p in PLANETS.values())

    def init_animations(self):
        self.rotation_anim = QPropertyAnimation(self, b"rotation")
        self.rotation_anim.setDuration(25000)
        self.rotation_anim.setStartValue(0)
        self.rotation_anim.setEndValue(360)
        self.rotation_anim.setLoopCount(-1)
        self.rotation_anim.setEasingCurve(QEasingCurve.Linear)
        self.animation_group.addAnimation(self.rotation_anim)

    def calculate_scale(self):
        # Рассчитываем масштаб для самой большой планеты (90% доступного пространства)
        content_margin = 0.9
        available_size = self.width() * content_margin
        return available_size / (2 * self.max_planet_radius)

    def paintEvent(self, event):
        if not self.planet_data:
            return
            
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)
        
        # Фоновый градиент
        bg_gradient = QLinearGradient(0, 0, self.width(), self.height())
        bg_gradient.setColorAt(0, QColor(10, 10, 30))
        bg_gradient.setColorAt(1, QColor(30, 10, 50))
        painter.fillRect(self.rect(), bg_gradient)

        # Динамическое масштабирование
        scale = self.calculate_scale()
        planet_radius = self.planet_data['radius'] * scale
        center = QPointF(self.width()/2, self.height()/2)

        painter.save()
        painter.translate(center)
        painter.rotate(self.rotation_angle)

        # Ядро планеты
        core_gradient = QRadialGradient(0, 0, planet_radius*0.5)
        core_gradient.setColorAt(0, QColor(255, 255, 255, 50))
        core_gradient.setColorAt(1, Qt.transparent)
        painter.setBrush(QBrush(core_gradient))
        painter.drawEllipse(QRectF(-planet_radius*0.7, -planet_radius*0.7, 
                             planet_radius*1.4, planet_radius*1.4))

        # Основная планета
        planet_gradient = QRadialGradient(0, 0, planet_radius)
        colors = self.planet_data['gradient']
        for i, color in enumerate(colors):
            planet_gradient.setColorAt(i/(len(colors)-1), color)
        
        painter.setBrush(QBrush(planet_gradient))
        painter.setPen(QPen(QColor(200, 200, 255, 150), 2))
        painter.drawEllipse(QRectF(-planet_radius, -planet_radius, 
                            planet_radius*2, planet_radius*2))

        # Атмосфера
        atmosphere_gradient = QRadialGradient(0, 0, planet_radius*1.2)
        atmosphere_gradient.setColorAt(0, QColor(200, 200, 255, 30))
        atmosphere_gradient.setColorAt(1, Qt.transparent)
        painter.setBrush(QBrush(atmosphere_gradient))
        painter.drawEllipse(QRectF(-planet_radius*1.2, -planet_radius*1.2, 
                                  planet_radius*2.4, planet_radius*2.4))

        painter.restore()

    def set_planet(self, data):
        self.planet_data = data
        self.animation_group.start()
        self.update()

    def getRotation(self):
        return self.rotation_angle

    def setRotation(self, angle):
        self.rotation_angle = angle
        self.update()

    rotation = Property(float, getRotation, setRotation)

    def resizeEvent(self, event):
        size = min(event.size().width(), event.size().height())
        self.setFixedSize(size, size)
        super().resizeEvent(event)

class PlanetInfoDialog(QDialog):
    def __init__(self, planet_name):
        super().__init__()
        self.setWindowTitle(f"Инфосеть: {planet_name.capitalize()}")
        self.setFixedSize(720, 600)
        self.setStyleSheet("""
            background: #10101A;
            color: #C0C0FF;
            border: 2px solid #30304D;
            border-radius: 12px;
        """)
        
        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setHtml(PLANET_INFO.get(planet_name, "<i>Данные недоступны</i>"))
        self.text_edit.setFont(QFont("Orbitron", 12))
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background: #151523;
                border: 2px solid #30304D;
                color: #C0C0FF;
                padding: 15px;
                border-radius: 8px;
            }
        """)
        
        close_btn = CyberButton("Закрыть")
        close_btn.clicked.connect(self.accept)
        
        layout.addWidget(self.text_edit)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)
        self.setLayout(layout)

class SplashScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Инициализация системы")
        self.setFixedSize(1024, 768)
        self.setStyleSheet("""
            background: qradialgradient(
                cx:0.5, cy:0.5, radius: 1,
                stop:0 #00001A, stop:1 #000000
            );
            color: #00FFFF;
        """)
        
        layout = QVBoxLayout()
        self.starfield = StarfieldWidget()
        
        title = QLabel("Инвис-2")
        title.setFont(QFont("Orbitron", 32, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-family: 'Bahnschrift', 'Bahnschrift Condensed', 'Arial Narrow', sans-serif;
                font-weight: 600;
                font-size: 28pt;
                letter-spacing: 1.5px;
                text-transform: uppercase;
                margin: 15px 0;
            }
        """)
        
        text = QLabel("""<div align='center' style='font-size:14pt'>
            <p>Версия 2.3.5 | Галактическая система координат</p>
            <p>© 2425 Swag Team.inc</p>
            <p style='color:#6060A0'>Инициализация гипердвигателя...</p>
        </div>""")

        # В методе __init__ класса SplashScreen после создания title добавить:
        credits = QLabel("""<div align='center' style='font-size:12pt; color:#7F7FFF; margin-top:20px'>
            Данная программа разработана силёнками студентов группы М6О-109БВ-24.<br>
            Сия суть имена создателей: Гневшева Матрёна, Левченко Олеся,<br> 
            Полтавец Сергей, Нещадимов Лев.<br>
            Мудрец и руководитель: Вадим Бикеев.<br>
            <span style='color:#6060A0'>Тыдыщ скибяу пау</span>
            </div>""")
        layout.addWidget(credits)
        
        self.progress = QLabel()
        self.progress.setAlignment(Qt.AlignCenter)
        
        self.btn = CyberButton("АКТИВИРОВАТЬ СИСТЕМУ")
        self.btn.clicked.connect(self.accept)
        
        layout.addWidget(title)
        layout.addWidget(text)
        layout.addWidget(self.progress)
        layout.addWidget(self.btn)
        self.setLayout(layout)
        
        self.loading_anim = QPropertyAnimation(self.progress, b"text")
        self.loading_anim.setDuration(3000)
        self.loading_anim.setStartValue("[■□□□□□□□□□] 10%")
        self.loading_anim.setEndValue("[■■■■■■■■■■] 100%")
        self.loading_anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.loading_anim.start()

class Ui_MainWindow:

    def __init__(self):
        self.current_planet = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 900)
        MainWindow.setStyleSheet(SPACE_STYLE)
        
        self.starfield = StarfieldWidget()
        self.starfield.setFixedSize(MainWindow.size())

        self.centralwidget = QWidget(MainWindow)
        self.central_layout = QVBoxLayout(self.centralwidget)
        self.central_layout.setContentsMargins(10, 10, 10, 10)
        
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setStyleSheet("QTabWidget::pane { border: 0; }")
        
        self.setup_planet_selection_tab()
        self.setup_flight_start_tab()
        self.setup_two_phase_tab()
        self.setup_three_phase_tab()
        self.setup_description_tab()
        
        self.central_layout.addWidget(self.tabs)
        MainWindow.setCentralWidget(self.centralwidget)

    def apply_first_impulse(self):
        self.ui.two_phase_impulse_btn.setProperty("applied", True)

    def apply_second_impulse(self):
        self.ui.three_phase_impulse_btn.setProperty("applied", True)

    def setup_planet_selection_tab(self):
        self.planet_selection_tab = QWidget()
        self.tabs.addTab(self.planet_selection_tab, "⏺ ГЛАВНАЯ")
    
        layout = QVBoxLayout(self.planet_selection_tab)
        layout.setContentsMargins(20, 20, 20, 20)
    
        input_section = QWidget()
        input_section.setStyleSheet(".planet_section")
        input_layout = QVBoxLayout(input_section)
    
        self.planet_input = QLineEdit()
        self.planet_input.setPlaceholderText("ВВЕДИТЕ НАЗВАНИЕ ПЛАНЕТЫ")
        self.planet_input.setStyleSheet("font-size: 14pt;")
    
        self.error_label = QLabel()
        self.error_label.setWordWrap(True)
        self.error_label.setTextFormat(Qt.TextFormat.RichText)
        self.error_label.setStyleSheet("color: #FF4444; font-weight: bold; font-size: 12pt;")
        self.error_label.setVisible(False)
    
        info_container = QHBoxLayout()
        self.planet_widget = PlanetWidget()
        self.planet_info = QLabel()
        self.planet_info.setObjectName("planet_info")
        self.planet_info.setFixedWidth(300)
        
    
    # Добавляем элементы в контейнер
        info_container.addStretch()
        info_container.addWidget(self.planet_widget)
        info_container.addStretch()
        info_container.addWidget(self.planet_info)
    
    # Устанавливаем минимальный размер для виджета планеты
        self.planet_widget.setMinimumSize(400, 400)
    
        self.more_info_btn = CyberButton("ПОЛНЫЙ ОТЧЁТ")
        self.more_info_btn.setEnabled(False)
    
        input_layout.addWidget(self.planet_input)
        input_layout.addWidget(self.error_label)
        input_layout.addLayout(info_container)  # Добавляем контейнер один раз
        input_layout.addWidget(self.more_info_btn, alignment=Qt.AlignCenter)
    
        layout.addWidget(input_section)

        self.planet_widget.setSizePolicy(
            QSizePolicy.MinimumExpanding, 
            QSizePolicy.MinimumExpanding
        )
    
    # Добавить контейнер с выравниванием
        planet_container = QWidget()
        planet_layout = QVBoxLayout(planet_container)
        #planet_layout.addWidget(self.planet_widget, 0, Qt.AlignCenter)
    
        info_container.addWidget(planet_container)
        info_container.addWidget(self.planet_info)
    
    # Установить минимальный размер
        self.planet_widget.setMinimumSize(300, 300)

    def show_flight_info(self):
        dlg = QDialog(self.centralwidget)  # ← или dlg = QDialog() — если без привязки
        dlg.setWindowTitle("Гомановский двухимпульсный перелёт")
        dlg.setStyleSheet("background-color: #10101A; color: #C0C0FF; padding: 20px;")
        dlg.setFixedSize(750, 650)

        layout = QVBoxLayout(dlg)
        text = QTextEdit()
        text.setReadOnly(True)
        text.setHtml("""
            <h2>Гомановский двухимпульсный перелёт: космический "танец" между орбитами 🌌</h2>
            <p>Этот маневр, предложенный немецким инженером Вальтером Гоманом в 1925 году, стал классикой космической баллистики.</p>
            <h3>Как это работает?</h3>
            <ol>
                <li><b>Первый импульс</b> — ускорение в перицентре.</li>
                <li><b>Пассивный полёт</b> — движение по полуэллипсу до апоцентра.</li>
                <li><b>Второй импульс</b> — коррекция до круговой орбиты.</li>
            </ol>
           <h3>Почему это эффективно?</h3>
          <ul>
              <li>Минимум топлива: оптимально для R₂/R₁ &lt;≈ 11.94</li>
              <li>Простота и симметрия: легко рассчитывается</li>
          </ul>
           <h3>Применения</h3>
           <ul>
               <li>Переход на геостационарную орбиту</li>
               <li>Полет к Венере или Марсу</li>
                <p style='color:#6060A0'><i>А вот для полёта к Луне гомановский маневр уже не подойдёт — здесь включают другие методы</i></p>
           </ul>
           <h3>Нюансы 🚀</h3>
           <ul>
                <li>При значении R₂/R₁ &lt;≈ от 11.94 до 15.58 нужно считать двух- и трехимпульсные перелёты,ища более выгодный</li>
               <li>Для R₂ &gt; 15.58 R₁ выгоднее трёхимпульсный манёвр</li>
               <li>Можно комбинировать с гравиманёврами</li>
           </ul>
           <p style='color:#6060A0'><i>Пример: с орбиты 200 км до 1000 км — суммарный ΔV ≈ 0.5 км/с</i></p>
            <ul>
            <h3>Итог:</h3>
            <ul>
            <li>Гомановский перелёт — это не просто формула, </li>
            а базовый язык космической навигации, который помогает инженерам "танцевать" между орбитами, экономя драгоценное топливо</li>
       """)
        close_btn = CyberButton("Закрыть")
        close_btn.clicked.connect(dlg.accept)

        layout.addWidget(text)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)
        dlg.setLayout(layout)
        dlg.exec()



    def setup_flight_start_tab(self):
        self.flight_start_tab = QWidget()
        self.tabs.addTab(self.flight_start_tab, "⏺ НАЧАЛЬНЫЕ УСЛОВИЯ")
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        
        
        target_group = QWidget()
        target_group.setStyleSheet(".cyber-border")
        target_layout = QHBoxLayout(target_group)
        target_layout.setSpacing(20)

        info_note = QLabel("""
            <div style='color:#7F7FFF; font-family:"Courier New", monospace; font-size:12pt; margin-bottom:15px'>
                ⚠ Все значения орбит задаются от поверхности планеты (в км)
            </div>
        """)
        layout.insertWidget(0, info_note)
        
        left_col = QVBoxLayout()
        self.apoapsis = QLineEdit()
        self.apoapsis.setPlaceholderText("АПОЦЕНТР (КМ)")
        self.periapsis = QLineEdit()
        self.periapsis.setPlaceholderText("ПЕРИЦЕНТР (КМ)")
        left_col.addWidget(QLabel("Параметры целевой орбиты:"))
        left_col.addWidget(self.apoapsis)
        left_col.addWidget(self.periapsis)
        
        right_col = QVBoxLayout()
        self.eccentricity = QLineEdit()
        self.eccentricity.setPlaceholderText("ЭКСЦЕНТРИСИТЕТ")
        self.semi_major_axis = QLineEdit()
        self.semi_major_axis.setPlaceholderText("БОЛЬШАЯ ПОЛУОСЬ (КМ)")
        right_col.addWidget(QLabel("Альтернативные параметры:"))
        right_col.addWidget(self.eccentricity)
        right_col.addWidget(self.semi_major_axis)
        
        target_layout.addLayout(left_col)
        target_layout.addLayout(right_col)
        
        initial_group = QWidget()
        initial_group.setStyleSheet(".cyber-border")
        initial_layout = QHBoxLayout(initial_group)
        self.r1_input = QLineEdit()
        self.r1_input.setPlaceholderText("РАДИУС НАЧАЛЬНОЙ ОРБИТЫ (КМ)")
        initial_layout.addWidget(QLabel("Начальные условия:"))
        initial_layout.addWidget(self.r1_input)
        
        self.start_btn = CyberButton("РАССЧИТАТЬ ΔV")
        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: #00FFE5; font-size: 14pt;")
        
        layout.addWidget(target_group)
        layout.addWidget(initial_group)
        layout.addWidget(self.start_btn, alignment=Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        scroll.setWidget(content)
        self.flight_start_tab_layout = QVBoxLayout(self.flight_start_tab)
        self.flight_start_tab_layout.addWidget(scroll)

    def setup_two_phase_tab(self):
        self.two_phase_tab = QWidget()
        self.tabs.addTab(self.two_phase_tab, "⏺ ПЕРВЫЙ ИМПУЛЬС")
    
        main_layout = QVBoxLayout(self.two_phase_tab)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15) 
        
        control_panel = QHBoxLayout()
        self.two_phase_impulse_btn = CyberButton("ПРИМЕНИТЬ ΔV₁")
        self.two_phase_result_label = QLabel("ОЖИДАНИЕ РАСЧЁТОВ...")
        self.two_phase_result_label.setStyleSheet("color: #00FFE5; font-size: 14pt;")
        control_panel.addWidget(self.two_phase_impulse_btn)
        control_panel.addWidget(self.two_phase_result_label)
    
        main_layout.addLayout(control_panel)

        self.two_phase_plot = pg.PlotWidget()
        self.two_phase_plot.setBackground('#0A0A12')
        self.two_phase_plot.getAxis('left').setPen(pg.mkPen('#6060A0'))
        self.two_phase_plot.getAxis('bottom').setPen(pg.mkPen('#6060A0'))
        self.two_phase_plot.showGrid(x=True, y=True, alpha=0.3)
        self.two_phase_plot.setAspectLocked(True)
        
        self.two_phase_planet = pg.ScatterPlotItem(
            pos=[(0, 0)],
            size=(self.current_planet['radius'] * 2 if self.current_planet else 10000),
            pxMode=False, 
            brush=pg.mkBrush('#6060A0'),
            pen=pg.mkPen('#00FFFF', width=2)
        )
        self.two_phase_initial_orbit = pg.PlotCurveItem(
            pen=pg.mkPen('#FF6600', width=2)
        )
        self.two_phase_transfer_orbit = pg.PlotCurveItem(
            pen=pg.mkPen('#FFFFFF', width=2, style=Qt.DashLine)
        )
        self.two_phase_satellite = pg.ScatterPlotItem(
            size=8,
            brush=pg.mkBrush('#FFD700'),
            pen=pg.mkPen('#000000', width=1)
        )
        
        self.two_phase_plot.addItem(self.two_phase_planet)
        self.two_phase_plot.addItem(self.two_phase_initial_orbit)
        self.two_phase_plot.addItem(self.two_phase_transfer_orbit)
        self.two_phase_plot.addItem(self.two_phase_satellite)
    
        
        control_panel.addWidget(self.two_phase_impulse_btn)
        control_panel.addWidget(self.two_phase_result_label)
        
        main_layout.addLayout(control_panel)
        main_layout.addWidget(self.two_phase_plot)

    def setup_three_phase_tab(self):
        self.three_phase_tab = QWidget()
        self.tabs.addTab(self.three_phase_tab, "⏺ ВТОРОЙ ИМПУЛЬС")
    
        main_layout = QVBoxLayout(self.three_phase_tab)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        self.three_phase_plot = pg.PlotWidget()
        self.three_phase_plot.setBackground('#0A0A12')
        self.three_phase_plot.getAxis('left').setPen(pg.mkPen('#6060A0'))
        self.three_phase_plot.getAxis('bottom').setPen(pg.mkPen('#6060A0'))
        self.three_phase_plot.showGrid(x=True, y=True, alpha=0.3)
        self.three_phase_plot.setAspectLocked(True)
        
        control_panel = QHBoxLayout()
        self.three_phase_impulse_btn = CyberButton("ПРИМЕНИТЬ ΔV₂")
        self.three_phase_result_label = QLabel("ОЖИДАНИЕ РАСЧЁТОВ...")
        self.three_phase_result_label.setStyleSheet("color: #00FFE5; font-size: 14pt;")
        control_panel.addWidget(self.three_phase_impulse_btn)
        control_panel.addWidget(self.three_phase_result_label)
    
        main_layout.addLayout(control_panel)

        self.three_phase_planet = pg.ScatterPlotItem(
            pos=[(0, 0)],
            size=(self.current_planet['radius'] * 2 if self.current_planet else 10000),
            pxMode=False, 
            brush=pg.mkBrush('#6060A0'),
            pen=pg.mkPen('#00FFFF', width=2)
        )
        self.three_phase_initial_orbit = pg.PlotCurveItem(
            pen=pg.mkPen('#FF6600', width=2)
        )
        self.three_phase_transfer_orbit = pg.PlotCurveItem(
            pen=pg.mkPen('#FFFFFF', width=2)
        )
        self.three_phase_final_orbit = pg.PlotCurveItem(
            pen=pg.mkPen('#00FF00', width=2)
        )
        self.three_phase_satellite = pg.ScatterPlotItem(
            size=8,
            brush=pg.mkBrush('#FFD700'),
            pen=pg.mkPen('#000000', width=1)
        )
        
        self.three_phase_plot.addItem(self.three_phase_planet)
        self.three_phase_plot.addItem(self.three_phase_initial_orbit)
        self.three_phase_plot.addItem(self.three_phase_transfer_orbit)
        self.three_phase_plot.addItem(self.three_phase_final_orbit)
        self.three_phase_plot.addItem(self.three_phase_satellite)
        
        control_panel.addWidget(self.three_phase_impulse_btn)
        control_panel.addWidget(self.three_phase_result_label)

        main_layout.addLayout(control_panel)
        main_layout.addWidget(self.three_phase_plot)

    def setup_description_tab(self):
        self.description_tab = QWidget()
        self.tabs.addTab(self.description_tab, "⏺ ОПИСАНИЕ")
        
        layout = QVBoxLayout(self.description_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        
        description = QLabel("""
            <h2 style='color:#00FFFF'>ДВУХИМПУЛЬСНЫЙ МАНЁВР ГОМАНА</h2>
            <p style='font-size:14pt'>Оптимальная траектория перехода между орбитами, 
            требующая минимальных энергетических затрат. Включает два импульса:</p>
            <ul>
                <li>ΔV₁: Переход на трансферную орбиту</li>
                <li>ΔV₂: Коррекция на целевую орбиту</li>
            </ul>
            <p style='color:#6060A0'>Используется в межпланетных перелётах с 2025 года</p>
        """)
        # В методе setup_description_tab после добавления description:
        description.setText("""
            <h2 style='color:#00FFFF'>ДВУХИМПУЛЬСНЫЙ МАНЁВР ГОМАНА</h2>
            <p style='font-size:14pt'>Программа для подсчёта общего импульса для 
            <span style='font-weight:bold;color:#00FF00'>двухимпульсного перелёта</span> 
            в двумерном пространстве с его визуализацией на графике. Все расчёты выполняются 
            автоматически в программе и не требуют внешнего вмешательства.</p>
            <p style='font-size:14pt'>Двухимпульсный перелёт — это орбитальный манёвр, 
            который включает в себя два импульса работы двигателя: для входа на траекторию 
            и для схода с неё. Траектория называется 
            <b style='color:#00FF00'>Гомановской</b> (названа в честь Вальтера Гомана, 1925 год).</p>
            <p style='color:#6060A0; font-size:12pt'>Используется в межпланетных перелётах с 2025 года</p>
        """)
        description.setWordWrap(True)
        
        self.results_label = QLabel()
        self.results_label.setStyleSheet("""
            font-size: 14pt;
            color: #00FFE5;
            padding: 15px;
            background: #151523;
            border-radius: 8px;
            border: 2px solid #30304D;
        """)
        
        self.funny_label = QLabel()
        self.funny_label.setStyleSheet("""
            font-family: "Comic Sans MS";
            color: #FFD700;
            font-size: 14pt;
            text-align: center;
        """)
        
        layout.addWidget(description)
        layout.addWidget(self.results_label)
        layout.addWidget(self.funny_label)

        self.funny_phrases = [
            "воот такие пироги",
            "Вот солнце ударяет по вершине- с сиреневою дымкой исчезает вес трёх тысяч чи паденья водопада. И чувство - Млечный путь свергается с небес",
            "тут кста есть реально планеты из звёздных войн(кашиик и татуин)",
            "Мелькнула на миг...В красоте своей нерасцветшей - Лик вечерней луны.",
            "Уж осени конец, Но верит в будущие дни Зелёный мандарин",
            "мы до сих пор не знаем сколько слонов в африке",
            "хакуна матата",
            "Перед вишней в цвету Померкла в облачной дымке Пристыженная луна",
            "Коль мирозданья круг есть некое кольцо,В нём, без сомнения, мы — камень драгоценный",
            "Солнца лик сквозь тучи рвётся — Тайну вечности нарушь!В каждой капле дождь смеётся:«Я — частица этой лужи»",
            "Взгляни на небо: в чёрной мгле Миры, как бисер, нанизаны.Но те, что светят в вышине,Уже погасли за туманом"
            "Вчера работало-Сегодня не работает... - Windows такой.",
            "Три вещи несомненны: смерть, налоги и потеря данных...Угадайте, что произошло."
            "Сбой превращает ваш дорогой компьютер в простой камень.",
            "стих дождь-последняя капля на земь упала. Обновите данные и начните сначала",
            "Цветы опали - мотылёк кружит напрасно...Обновить цикл?",
            "Седая яблоня уж оцветает - и каждый цвет опавший обещает плод...",
            "Кама шур дурын Пелькыскетлэн вордӥз — Тӧдьы вишняез(У Камы-реки Вышивка времён увяла… Вишня в белом — ждёт[удм.])",
            "Тулыс бертчыз — Вишня вож сямен шуыса… Тӧдьы ар — мусъем.(Весна умчалась — Вишня зелёным вздохнула… Белый год — в сердце стучит[удм.])"
        ]
    
        self.funny_label = QLabel()
        self.funny_label.setStyleSheet("""
            font-family: 'Bahnschrift SemiLight';
            color: #7F7FFF;
            font-size: 12pt;
            text-align: center;
                margin: 10px 0;
            padding: 0 15px;
        """)
        self.funny_label.setWordWrap(True)
        self.funny_label.setMinimumWidth(400)
        self.funny_label.setMaximumWidth(600)

        self.more_about_btn = CyberButton("Больше про перелёты")
        self.more_about_btn.clicked.connect(self.show_flight_info)
        layout.addWidget(self.more_about_btn, alignment=Qt.AlignRight)

    
        layout.addWidget(description)
        layout.addWidget(self.results_label)
        layout.addWidget(self.funny_label)
        layout.addStretch() 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setMaximumSize(1920, 1080)
        self.splash = SplashScreen()
        if self.splash.exec() == QDialog.Accepted:
            self.init_main_ui()
        else:
            sys.exit()
        self.resizeEvent = self.on_window_resize
        self.general_error = "Произошли ошибки. Мы не скажем вам, где и почему.\n- Ленивые программисты..."


    def format_error(self, specific_error):
        return f"{self.general_error}🛑 {specific_error}"


    def on_window_resize(self, event):
        """Обработчик изменения размера окна"""
        self.update_graphics()
        super().resizeEvent(event)

    def update_graphics(self):
        """Обновление графики при изменении размера окна"""
        if hasattr(self.ui, 'planet_widget'):
            self.ui.planet_widget.update()  
    
    def init_main_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("ОРБИТАЛЬНЫЙ КАЛЬКУЛЯТОР МАИ-109БВ")
        
        self.current_planet = None
        self.current_orbit = None
        self.r_initial = None
        self.dv1 = 0
        self.dv2 = 0
        
        self.ui.planet_input.textChanged.connect(self.handle_planet_input)
        self.ui.more_info_btn.clicked.connect(self.show_planet_info)
        self.ui.start_btn.clicked.connect(self.calculate_flight)
        self.ui.two_phase_impulse_btn.clicked.connect(self.apply_first_impulse)
        self.ui.three_phase_impulse_btn.clicked.connect(self.apply_second_impulse)
        
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.setInterval(50)
        self.animation_angle = 0
        self.ui.tabs.currentChanged.connect(self.on_tab_changed)
        self.ui.planet_input.textChanged.connect(self.handle_planet_input)

    def handle_planet_input(self):
        text = self.ui.planet_input.text().strip().lower()
        self.ui.error_label.setVisible(False)
        self.ui.planet_input.setStyleSheet("")
        self.ui.more_info_btn.setEnabled(False)

    def on_tab_changed(self, index):
        """Обработчик переключения вкладок"""
        if index == 2: 
            self.update_graphics()
        elif index == 3:  
            self.update_graphics()

    def handle_planet_input(self):
        text = self.ui.planet_input.text().strip().lower()
        self.ui.error_label.setVisible(False)
        self.ui.planet_input.setStyleSheet("")
        self.ui.more_info_btn.setEnabled(False)
        

        
        if planet := PLANETS.get(text):
            self.current_planet = planet.copy()
            self.current_planet['name'] = text
            self.ui.planet_widget.set_planet(planet)
            
            info = (
                f"<b>{text.upper()}</b><br>"
                f"Радиус: {planet['radius']} км<br>"
                f"μ: {planet['mu']:.3e} км³/с²"
            )
            self.ui.planet_info.setText(info)
            
            comment, font = planet['comment']
            self.ui.error_label.setText(f'<span style="color:#6060A0; font-family:{font}">{comment}</span>')
            self.ui.error_label.setVisible(True)
            
            self.ui.more_info_btn.setEnabled(True)
        elif text:
            custom_error = """
                <div style='
                    color: #7F7FFF; 
                    font-family: "Courier New", monospace; 
                    font-size: 12pt; 
                    margin-bottom: 15px;
                '>
                    Вместо звукового сигнала<br>
                    Или грубого сообщения об ошибке —<br>
                    Эти слова: «Планета не найдена»...<br>
                </div>
            """
            self.ui.error_label.setText(self.general_error + custom_error)
            self.ui.error_label.setVisible(True)
        
        
    def validate_input(self, value):
        if not value:
            raise ValueError("Дао, что видимо глазу, Не истинно, пока пусто поле это")
        value = value.replace(',', '.').strip()
        if not value.replace('.', '').isdigit():
            raise ValueError("Серьёзная ошибка. Все ярлыки исчезли. НЕКОРРЕКТНЫЙ ФОРМАТ")
        return float(value)

    def calculate_flight(self):
        self.ui.two_phase_impulse_btn.setProperty("applied", False)
        self.ui.three_phase_impulse_btn.setProperty("applied", False)
        try:
            self.ui.status_label.clear()
            
            if not self.current_planet:
                raise ValueError("Пропасть меж углеродом и кремнием —Программе не везвести моста:ВЫБЕРИТЕ ПЛАНЕТУ НА ВКЛАДКЕ 'ГЛАВНАЯ'")
            
            mu = self.current_planet['mu'] 
            planet_radius = self.current_planet['radius']*1000
            
            if self.ui.apoapsis.text() and self.ui.periapsis.text():
                apo = self.validate_input(self.ui.apoapsis.text()) * 1000 + planet_radius
                peri = self.validate_input(self.ui.periapsis.text()) * 1000 + planet_radius
                a_target = (apo + peri) / 2
                e_target = (apo - peri) / (apo + peri)
                r_a = apo
            else:
                e_target = self.validate_input(self.ui.eccentricity.text())
                a_target = self.validate_input(self.ui.semi_major_axis.text()) + planet_radius
                apo = a_target * (1 + e_target)
                peri = a_target * (1 - e_target)
                r_a = apo
            
            r_initial = self.validate_input(self.ui.r1_input.text()) * 1000 + planet_radius
            self.r_initial = r_initial
            
            dv_total, dv1, dv2 = self.deltaV(mu, r_initial, a_target, e_target)
            self.dv1 = dv1
            self.dv2 = dv2
            
            self.current_orbit = {
                'a': a_target,
                'e': e_target,
                'apoapsis': apo,
                'periapsis': peri
            }

            self.ui.status_label.setText(
                f"ΔV: {dv_total:.2f} м/с | "
                f"Апоцентр: {(a_target*(1+e_target)-planet_radius)/1000:.1f} км | "
                f"Эксцентриситет: {e_target:.3f}"
            )
            
            self.ui.results_label.setText(
                f"ОБЩИЙ ИМПУЛЬС: {dv_total:.2f} м/с\n"
                f"ΔV₁: {dv1:.2f} м/с | ΔV₂: {dv2:.2f} м/с"
            )
            
            self.update_graphics()
            self.start_animation()

            if e_target < 0 or e_target >= 1:
                raise ValueError("Ветер терплет лилию — Лепестки вразброс на ветру:Эксцентриситет 0 ≤ e < 1")
  
            self.ui.funny_label.setText(random.choice(self.ui.funny_phrases))
            self.ui.status_label.setText(
                f"ΔV: {dv_total:.2f} м/с | "
                f"Апоцентр: {(a_target*(1+e_target)-planet_radius)/1000:.1f} км | "
                f"Эксцентриситет: {e_target:.3f}"
            )
            
        except Exception as e:
            self.ui.status_label.setText(self.format_error(f"ОШИБКА: {str(e)}"))
            self.ui.status_label.setStyleSheet("color: #FF4444;")
            self.ui.funny_label.clear()

    def deltaV(self, mu, r_initial, a_target, e_target):
        try:
            r_a = a_target * (1 + e_target)
            transfer_a = (r_initial + r_a) / 2
            
            v_initial = m.sqrt(mu / r_initial)
            v_transfer_peri = m.sqrt(mu * (2/r_initial - 1/transfer_a))
            dv1 = abs(v_transfer_peri - v_initial)
            
            v_transfer_apo = m.sqrt(mu * (2/r_a - 1/transfer_a))
            r_a_target = a_target * (1 + e_target)  # Апоцентр целевой орбиты
            v_target_apo = m.sqrt(mu * (2/r_a_target - 1/a_target))
            dv2 = abs(v_target_apo - v_transfer_apo)
            
            return dv1 + dv2, dv1, dv2
            
        except:
            raise ValueError(
                """Код был исполнен рвения,<br>
                Обдумывал запрос,<br>
                Но чипы подвели :<br>
                <b>НЕВОЗМОЖНО РАССЧИТАТЬ ОРБИТУ</b>"""
            )

    def update_graphics(self):
        if not self.current_orbit or not self.current_planet:
            return

        
        # Общие параметры
        planet_radius = self.current_planet['radius']
        color = self.current_planet['gradient'][0]
        base_size = max(15, planet_radius * 0.002)
        theta = np.linspace(0, 2 * np.pi, 100)

        # Обновление графики для вкладки "Первый импульс"
        if hasattr(self.ui, 'two_phase_initial_orbit'):
            # Начальная круговая орбита
            r_initial = (self.r_initial - planet_radius) if self.r_initial else 0
            x_initial = r_initial * np.cos(theta)
            y_initial = r_initial * np.sin(theta)
            self.ui.two_phase_initial_orbit.setData(x_initial / 1e3, y_initial / 1e3)

            # Переходная орбита (очищается до применения импульса)
            if not self.ui.two_phase_impulse_btn.property("applied"):
                self.ui.two_phase_transfer_orbit.setData([], [])

            # Планета
            planet_radius = self.current_planet['radius']
            self.ui.two_phase_planet.setData(
                pos=[(0, 0)],
                size=planet_radius * 2,
                brush=pg.mkBrush(color),
                pen=pg.mkPen(color.darker(150), width=1.5)
            )

        # Обновление графики для вкладки "Второй импульс"

        if hasattr(self.ui, 'three_phase_initial_orbit'):
    # Начальная круговая орбита
            r_initial = (self.r_initial - planet_radius) if self.r_initial else 0
            x_initial = r_initial * np.cos(theta)
            y_initial = r_initial * np.sin(theta)
            self.ui.three_phase_initial_orbit.setData(x_initial / 1e3, y_initial / 1e3)

        if hasattr(self.ui, 'three_phase_final_orbit'):
            # Переходная орбита (только после первого импульса)
            if self.ui.two_phase_impulse_btn.property("applied"):
                a_transfer = (self.r_initial + self.current_orbit['a'] * (1 + self.current_orbit['e'])) / 2
                e_transfer = (self.current_orbit['a'] * (1 + self.current_orbit['e']) - self.r_initial) / (self.current_orbit['a'] * (1 + self.current_orbit['e']) + self.r_initial)
                r_transfer = a_transfer * (1 - e_transfer**2) / (1 + e_transfer * np.cos(theta)) - planet_radius
                x_transfer = r_transfer * np.cos(theta)
                y_transfer = r_transfer * np.sin(theta)
                self.ui.three_phase_transfer_orbit.setData(x_transfer / 1e3, y_transfer / 1e3)
            else:
                self.ui.three_phase_transfer_orbit.setData([], [])

            # Финальная орбита (очищается до применения второго импульса)
            if not self.ui.three_phase_impulse_btn.property("applied"):
                self.ui.three_phase_final_orbit.setData([], [])

            # Планета
            planet_radius = self.current_planet['radius']
            self.ui.three_phase_planet.setData(
                pos=[(0, 0)],
                size=planet_radius * 2,
                brush=pg.mkBrush(color),
                pen=pg.mkPen(color.darker(150), width=1.5
            ))

            

    def apply_first_impulse(self):
        self.ui.two_phase_impulse_btn.setProperty("applied", True)
        self.ui.two_phase_result_label.setText(f"ΔV₁: {self.dv1:.2f} м/с")
    
    # Обновление графики переходной орбиты
        planet_radius = self.current_planet['radius']
        a_transfer = (self.r_initial + self.current_orbit['a'] * (1 + self.current_orbit['e'])) / 2
        e_transfer = (self.current_orbit['a'] * (1 + self.current_orbit['e']) - self.r_initial) / (self.current_orbit['a'] * (1 + self.current_orbit['e']) + self.r_initial)
    
        theta = np.linspace(0, 2*np.pi, 100)
        r = a_transfer*(1 - e_transfer**2)/(1 + e_transfer*np.cos(theta)) - planet_radius
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        self.ui.two_phase_transfer_orbit.setData(x/1e3, y/1e3)
    
        self.animation_angle = 0
        self.animation_timer.start()

    def apply_second_impulse(self):
        self.ui.three_phase_result_label.setText(f"ΔV₂: {self.dv2:.2f} м/с")
        self.ui.three_phase_impulse_btn.setProperty("applied", True)
        self.animation_angle = np.pi
        self.animation_timer.start()

        a = self.current_orbit['a']
        e = self.current_orbit['e']
        planet_radius = self.current_planet['radius']
        theta = np.linspace(0, 2 * np.pi, 100)
        r_orbit = (a * (1 - e**2) / (1 + e * np.cos(theta))) - planet_radius
        x = r_orbit * np.cos(theta)
        y = r_orbit * np.sin(theta)
        self.ui.three_phase_final_orbit.setData(x / 1e3, y / 1e3)



    def update_animation(self):
        if not self.current_planet or not self.current_orbit:
            return

        planet_radius = self.current_planet['radius']
        self.animation_angle += 0.05
        if self.animation_angle > 2 * np.pi:
            self.animation_angle = 0

    # Для вкладки "Первый импульс"
        if self.ui.tabs.currentIndex() == 2:
            if self.ui.two_phase_impulse_btn.property("applied"):
            # Движение по переходной орбите после импульса
                a_transfer = (self.r_initial + self.current_orbit['a'] * (1 + self.current_orbit['e'])) / 2
                e_transfer = (self.current_orbit['a'] * (1 + self.current_orbit['e']) - self.r_initial) / (self.current_orbit['a'] * (1 + self.current_orbit['e']) + self.r_initial)
                r = a_transfer * (1 - e_transfer**2) / (1 + e_transfer * np.cos(self.animation_angle)) - planet_radius
            else:
            # Движение по начальной круговой орбите
                r = self.r_initial - planet_radius

            x = r * np.cos(self.animation_angle)
            y = r * np.sin(self.animation_angle)
            self.ui.two_phase_satellite.setData([x/1e3], [y/1e3])

    # Для вкладки "Второй импульс"
        elif self.ui.tabs.currentIndex() == 3:
            if self.ui.three_phase_impulse_btn.property("applied"):
            # Движение по финальной орбите после второго импульса
                a = self.current_orbit['a']
                e = self.current_orbit['e']
                r = a * (1 - e**2) / (1 + e * np.cos(self.animation_angle)) - planet_radius
            else:
            # Движение по переходной орбите (после первого импульса)
                a_transfer = (self.r_initial + self.current_orbit['a'] * (1 + self.current_orbit['e'])) / 2
                e_transfer = (self.current_orbit['a'] * (1 + self.current_orbit['e']) - self.r_initial) / (self.current_orbit['a'] * (1 + self.current_orbit['e']) + self.r_initial)
                r = a_transfer * (1 - e_transfer**2) / (1 + e_transfer * np.cos(self.animation_angle)) - planet_radius

            x = r * np.cos(self.animation_angle)
            y = r * np.sin(self.animation_angle)
            self.ui.three_phase_satellite.setData([x/1e3], [y/1e3])

    def start_animation(self):
        if not self.animation_timer.isActive():
            self.animation_timer.start()

    def show_planet_info(self):
        if self.current_planet:
            dialog = PlanetInfoDialog(self.current_planet['name'])
            dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Orbitron", 10))
    window = MainWindow()
    
    star_effect = QGraphicsOpacityEffect(window.ui.starfield)
    window.ui.starfield.setGraphicsEffect(star_effect)
    anim = QPropertyAnimation(star_effect, b"opacity")
    anim.setDuration(2000)
    anim.setStartValue(0.5)
    anim.setEndValue(1.0)
    anim.setEasingCurve(QEasingCurve.InOutSine)
    anim.setLoopCount(-1)
    anim.start()
    
    window.show()
    sys.exit(app.exec())
