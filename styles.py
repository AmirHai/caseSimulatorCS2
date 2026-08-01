def set_inventory_skin_style(rarity_color):
    inventory_skin_stile = f"""
    QLabel {{
        background-color: #1a1a1a;
        border: 2px solid {rarity_color};
        border-radius: 12px;
    }}
    
    QLabel:hover {{
        /* Плавный игровой градиент, который активируется только при наведении */
        background: qlineargradient(
            x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 {rarity_color}, 
            stop: 0.6 #1a1a1a
        );
        border: 2px solid {rarity_color};
    }}
"""
    return inventory_skin_stile

def case_skin_style(rarity_color):
    skin_stile = f"""
    /* ОБЫЧНОЕ СОСТОЯНИЕ КАРТОЧКИ В КЕЙСЕ */
    QWidget {{
        background-color: #15161c;                  /* Глубокий темный фон */
        border: 1px solid #2d2f3d;                  /* Тонкая нейтральная рамка */
        border-bottom: 4px solid {rarity_color}; /* Яркая полоса редкости снизу */
        border-radius: 6px;                         /* Аккуратное скругление углов */
    }}
    
    /* ЭФФЕКТ ПРИ НАВЕДЕНИИ КУРСОРA */
    QWidget:hover {{
        background-color: #1c1d26;                  /* Подсветка фона */
        border: 1px solid {rarity_color};  /* Рамка окрашивается в цвет редкости */
        border-bottom: 4px solid {rarity_color}; /* Полоса снизу остается */
    }}
"""
    return skin_stile

def scrolling_skin_style(rarity_color):
    skin_stile = f"""
    QWidget {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 {rarity_color}, 
            stop: 0.10 {rarity_color},  /* Небольшая яркая полоса на самом верху */
            stop: 0.40 #141419,                   /* Быстрое затухание цвета сразу за прицелом P90 */
            stop: 0.80 #0a0a0d                    /* Глубокий темный фон под самим автоматом и текстом */
        );
        
        border-radius: 0px; 
        
        /* Тонкий разделитель между карточками в рулетке */
        border-right: 1px solid #1c1c1f;
        border-top: none;
        border-left: none;
        border-bottom: none;
    }}
"""
    return skin_stile

def dropped_skin_style(rarity_color):
    skin_stile = f"""
    SkinDropDialog {{
        background: qradialgradient(
            cx: 0.5, cy: 0.4, radius: 0.6,
            fx: 0.5, fy: 0.4,
            stop: 0 {rarity_color},   /* Фиолетовое свечение */
            stop: 0.61 #131316, 
            stop: 1.0 #09090b
        );
    }}
    /* Явно делаем все тексты прозрачными, чтобы они не создавали полос */
    QLabel {{
        background: transparent;
        border: none;
    }}
"""
    return skin_stile


def red_button_style():
    return """
    QPushButton {
        background-color: rgba(235, 75, 75, 0.1);  /* Полупрозрачный красный */
        border: 2px solid #eb4b4b;                 /* Четкая красная рамка */
        color: #eb4b4b;
        font-weight: bold;
        border-radius: 6px;
        padding: 8px 24px;
    }
    QPushButton:hover {
        background-color: #eb4b4b;                 /* Заливается полностью при наведении */
        color: #ffffff;
    }
"""

def green_button_style():
    return """
    QPushButton {
        background-color: rgba(75, 235, 120, 0.1); /* Полупрозрачный зеленый */
        border: 2px solid #4beb78;                 /* Зеленая рамка */
        color: #4beb78;
        font-weight: bold;
        border-radius: 6px;
        padding: 8px 24px;
    }
    QPushButton:hover {
        background-color: #4beb78;
        color: #000000;
    }
"""