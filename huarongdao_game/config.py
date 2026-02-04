# -*- coding: utf-8 -*-
"""
华容道游戏配置文件
包含游戏的各种配置参数
"""

import os

# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 游戏基本信息
GAME_TITLE = "华容道游戏"
GAME_VERSION = "1.0.0"

# 语言设置
LANGUAGE = "ZH"  # ZH: 中文, EN: 英文

# 游戏窗口设置 - 改为手机竖版适配
WINDOW_WIDTH = 480   # 手机宽度
WINDOW_HEIGHT = 800  # 手机高度
FPS = 60

# 颜色定义 (R, G, B) - 更美观的配色方案
COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'GRAY': (128, 128, 128),
    'LIGHT_GRAY': (240, 240, 240),
    'DARK_GRAY': (64, 64, 64),
    'BLUE': (70, 130, 180),  # Steel Blue
    'LIGHT_BLUE': (176, 224, 230),  # Powder Blue
    'GREEN': (60, 179, 113),  # Medium Sea Green
    'RED': (220, 20, 60),  # Crimson
    'YELLOW': (255, 215, 0),  # Gold
    'ORANGE': (255, 140, 0),  # Dark Orange
    'PURPLE': (147, 112, 219),  # Medium Purple
    'BACKGROUND': (245, 245, 245),  # Light Gray Background
    'GAME_BG': (250, 250, 250),  # Game Board Background
    'BUTTON_PRIMARY': (70, 130, 180),  # Primary Button Color
    'BUTTON_SECONDARY': (60, 179, 113),  # Secondary Button Color
    'BUTTON_TERTIARY': (147, 112, 219),  # Tertiary Button Color (Purple)
    'BUTTON_DANGER': (220, 20, 60),  # Danger Button Color
    'BUTTON_LANGUAGE': (255, 140, 0),  # Language Button Color (Orange)
    'BUTTON_INFO': (147, 112, 219),  # Info Button Color (Purple)
}

# 中英文文本
TEXTS = {
    "ZH": {
        "game_title": "华容道游戏",
        "select_game_mode": "选择游戏模式",
        "numbers_puzzle": "数字拼图",
        "images_puzzle": "图片拼图",
        "select_difficulty_level": "选择难度等级",
        "easy": "简单",
        "medium": "中等",
        "hard": "困难",
        "start_game": "开始游戏",
        "restart": "重新开始",
        "menu": "主菜单",
        "quit": "退出",
        "time": "时间:",
        "moves": "步数:",
        "difficulty": "难度:",
        "game_completed": "游戏完成!",
        "congratulations": "恭喜你!",
        "completion_time": "完成时间:",
        "completion_moves": "完成步数:",
        "ok": "确定",
        "leaderboard": "排行榜",
        "rank": "排名",
        "player": "玩家",
        "back_to_menu": "返回主菜单",
        "clear_leaderboard": "清空排行榜",
        "switch_language": "切换语言",
        "view_leaderboard": "查看排行榜",
        "select_image": "选择图片",
        "random_image": "随机图片",
        "select_specific_image": "选择特定图片",
        "back": "返回",
        "clear": "清空",
        "leaderboard": "排行榜",
        "select_difficulty": "选择难度"
    },
    "EN": {
        "game_title": "Huarongdao Game",
        "select_game_mode": "Select Game Mode",
        "numbers_puzzle": "Numbers Puzzle",
        "images_puzzle": "Images Puzzle",
        "select_difficulty_level": "Select Difficulty Level",
        "easy": "Easy",
        "medium": "Medium",
        "hard": "Hard",
        "start_game": "Start Game",
        "restart": "Restart",
        "menu": "Menu",
        "quit": "Quit",
        "time": "Time:",
        "moves": "Moves:",
        "difficulty": "Difficulty:",
        "game_completed": "Game Completed!",
        "congratulations": "Congratulations!",
        "completion_time": "Completion Time:",
        "completion_moves": "Completion Moves:",
        "ok": "OK",
        "leaderboard": "Leaderboard",
        "rank": "Rank",
        "player": "Player",
        "back_to_menu": "Back to Menu",
        "clear_leaderboard": "Clear Leaderboard",
        "switch_language": "Switch Language",
        "view_leaderboard": "View Leaderboard",
        "select_image": "Select Image",
        "random_image": "Random Image",
        "select_specific_image": "Select Specific Image",
        "back": "Back",
        "clear": "Clear",
        "leaderboard": "Leaderboard",
        "select_difficulty": "Select Difficulty"
    }
}

# 游戏难度设置 - 删除HARD难度
DIFFICULTY_LEVELS = {
    'EASY': {'size': 3, 'name': 'EASY'},
    'MEDIUM': {'size': 4, 'name': 'MEDIUM'}
}

# 游戏模式
GAME_MODES = {
    'NUMBERS': 'numbers',
    'IMAGES': 'images'
}

# 资源目录设置（相对于项目根目录）
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
IMAGE_DIR = os.path.join(ASSETS_DIR, "images")
CUSTOM_IMAGE_DIR = os.path.join(ASSETS_DIR, "images")  # 使用相同目录
DATA_DIR = os.path.join(ASSETS_DIR, "data")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

# 排行榜设置
LEADERBOARD_FILE = os.path.join(DATA_DIR, "leaderboard.json")
MAX_LEADERBOARD_ENTRIES = 30  # 限制存储30条记录

# 字体设置 - 适配手机屏幕
FONT_SIZES = {
    'SMALL': 14,
    'MEDIUM': 18,
    'LARGE': 24,
    'TITLE': 32
}

# 按键映射
KEY_MAPPINGS = {
    'UP': [ord('W'), ord('w'), 273],  # W, w, 上箭头
    'DOWN': [ord('S'), ord('s'), 274],  # S, s, 下箭头
    'LEFT': [ord('A'), ord('a'), 276],  # A, a, 左箭头
    'RIGHT': [ord('D'), ord('d'), 275],  # D, d, 右箭头
    'RESTART': [ord('R'), ord('r')],  # R, r
    'QUIT': [ord('Q'), ord('q')],  # Q, q
    'LANGUAGE_SWITCH': [ord('L'), ord('l'), 307, 308]  # L, l, 左Alt(307), 右Alt(308)
}

# 游戏完成自动关闭时间（秒）
AUTO_CLOSE_DELAY = 3

# 确保必要的目录存在
def create_directories():
    """创建必要的目录"""
    dirs = [IMAGE_DIR, CUSTOM_IMAGE_DIR, DATA_DIR, FONTS_DIR]
    for directory in dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)

def get_text(key):
    """获取当前语言的文本"""
    return TEXTS[LANGUAGE][key]

def switch_language():
    """切换语言"""
    global LANGUAGE
    LANGUAGE = "EN" if LANGUAGE == "ZH" else "ZH"
    return LANGUAGE