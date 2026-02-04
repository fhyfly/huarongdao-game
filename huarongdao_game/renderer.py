# -*- coding: utf-8 -*-
"""
华容道游戏渲染引擎
负责游戏画面的绘制和用户界面显示
"""

import pygame
import os
import random
import sys
from typing import Tuple, List, Optional
from config import *
from models import GameState, LeaderboardEntry


class GameRenderer:
    """游戏渲染器"""

    def __init__(self):
        pygame.init()
        # 设置UTF-8编码支持
        if sys.platform.startswith('win'):
            import locale
            try:
                locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
            except:
                try:
                    locale.setlocale(locale.LC_ALL, 'Chinese_China.936')
                except:
                    pass

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(get_text('game_title'))
        self.clock = pygame.time.Clock()

        # 加载字体 - 改进中文字体加载（添加详细调试信息）
        self.load_chinese_fonts()

        # 计算游戏区域（适配手机竖版）
        self.calculate_layout()

        # 加载图片
        self.images = {}
        self.sliced_images = {}  # 存储切割后的图片
        self.load_images()

    def load_chinese_fonts(self):
        """加载中文字体 - 改进版本，专门针对中文优化"""
        self.fonts = {}

        print("=== 字体加载调试信息 ===")

        # 直接使用系统字体路径，确保正确加载
        font_path = r"C:\Windows\Fonts\msyh.ttc"
        if os.path.exists(font_path):
            try:
                # 直接基于字体文件创建所有大小
                self.fonts = {
                    'small': pygame.font.Font(font_path, FONT_SIZES['SMALL']),
                    'medium': pygame.font.Font(font_path, FONT_SIZES['MEDIUM']),
                    'large': pygame.font.Font(font_path, FONT_SIZES['LARGE']),
                    'title': pygame.font.Font(font_path, FONT_SIZES['TITLE'])
                }
                print(f"✓ 直接使用字体文件创建成功: {font_path}")
                print("=== 字体加载完成 ===\n")

                # 测试中文显示
                self.test_chinese_rendering()
                return

            except Exception as e:
                print(f"✗ 直接字体文件加载失败: {e}")

        # 备用方案：使用SysFont
        try:
            self.fonts = {
                'small': pygame.font.SysFont('Microsoft YaHei', FONT_SIZES['SMALL']),
                'medium': pygame.font.SysFont('Microsoft YaHei', FONT_SIZES['MEDIUM']),
                'large': pygame.font.SysFont('Microsoft YaHei', FONT_SIZES['LARGE']),
                'title': pygame.font.SysFont('Microsoft YaHei', FONT_SIZES['TITLE'])
            }
            print("✓ 使用系统字体(Microsoft YaHei)")
            print("=== 字体加载完成 ===\n")

            # 测试中文显示
            self.test_chinese_rendering()
            return

        except Exception as e:
            print(f"✗ 系统字体加载失败: {e}")

        # 最后备选方案
        self.fonts = {
            'small': pygame.font.SysFont(None, FONT_SIZES['SMALL']),
            'medium': pygame.font.SysFont(None, FONT_SIZES['MEDIUM']),
            'large': pygame.font.SysFont(None, FONT_SIZES['LARGE']),
            'title': pygame.font.SysFont(None, FONT_SIZES['TITLE'])
        }
        print("✓ 使用默认字体")
        print("=== 字体加载完成 ===\n")

        # 测试中文显示
        self.test_chinese_rendering()

    def test_chinese_rendering(self):
        """测试中文字体渲染质量"""
        print("\n字体渲染测试:")
        test_texts = ['测试中文', '华容道游戏', '数字拼图']
        for text in test_texts:
            try:
                surface = self.fonts['large'].render(text, True, COLORS['BLACK'])
                size = surface.get_size()
                print(f"  '{text}' - 尺寸: {size}")

                # 检查像素质量
                if size[0] > 10:  # 确保有足够的像素进行采样
                    pixels = []
                    for x in [0, size[0]//2, size[0]-1]:
                        pixel_color = surface.get_at((x, size[1]//2))
                        pixels.append(str(pixel_color))

                    # 如果大部分像素都是透明的，说明渲染有问题
                    non_transparent_pixels = sum(1 for color_str in pixels if '0' not in color_str.split(',')[3])
                    if non_transparent_pixels >= 2:
                        print(f"    像素样本颜色: {pixels[:3]}")
                        print(f"    ✓ 渲染质量良好")
                    else:
                        print(f"    ⚠ 渲染质量可能有问题")
                else:
                    print(f"    ⚠ 尺寸过小，无法准确判断")
            except Exception as e:
                print(f"  '{text}' - 渲染失败: {e}")

    def calculate_layout(self):
        """计算界面布局参数"""
        # 信息显示区域高度（时间、步数等）
        self.info_height = 120

        # 边距设置
        horizontal_padding = 20
        vertical_padding = 15

        # 可用空间计算
        available_height = WINDOW_HEIGHT - self.info_height - 2 * vertical_padding
        available_width = WINDOW_WIDTH - 2 * horizontal_padding

        # 计算拼图区域（基于4×4标准）
        standard_size = 4
        self.tile_size = min(available_width, available_height) // standard_size

        # 居中放置游戏板
        board_size = self.tile_size * standard_size
        self.board_x = (WINDOW_WIDTH - board_size) // 2
        self.board_y = self.info_height + vertical_padding + (available_height - board_size) // 2

    def load_images(self):
        """加载游戏图片"""
        # 加载默认图片
        default_images = [
            "img-08cda7cc-aaea-4f35-76f5-befe1e4280bd.jpeg",
            "img-120366c0-9a28-4db3-6459-178806ddc81c.jpeg",
            "img-4730faff-69f3-4137-6aef-2b77b372d192.jpeg",
            "img-854736f6-ca8c-4ade-59b0-471d4734f4a7.jpeg",
            "img-e4fdd4e3-3f90-411e-5ef8-45f0441d6963.jpeg"
        ]

        for i, img_name in enumerate(default_images):
            try:
                # 使用配置的IMAGE_DIR路径
                img_path = os.path.join(IMAGE_DIR, img_name)
                if os.path.exists(img_path):
                    image = pygame.image.load(img_path)
                    self.images[f"default_{i}"] = image
                    print(f"成功加载图片: {img_name}")
                else:
                    print(f"图片不存在: {img_path}")
            except pygame.error as e:
                print(f"无法加载图片 {img_name}: {e}")

    def slice_image_for_puzzle(self, image, puzzle_size):
        """将图片切割成拼图块"""
        if image is None:
            return []

        width, height = image.get_size()
        tile_width = width // puzzle_size
        tile_height = height // puzzle_size

        sliced_tiles = []
        for row in range(puzzle_size):
            for col in range(puzzle_size):
                # 计算切割区域
                rect = pygame.Rect(
                    col * tile_width,
                    row * tile_height,
                    tile_width,
                    tile_height
                )
                # 切割图片
                tile = image.subsurface(rect)
                sliced_tiles.append(tile)

        return sliced_tiles

    def prepare_puzzle_images(self, game_state, selected_image_key=None):
        """为当前游戏准备拼图图片"""
        if game_state.current_mode == 'IMAGES' and game_state.size > 0:
            # 选择一张图片
            if self.images:
                if selected_image_key and selected_image_key in self.images:
                    # 使用指定的图片
                    base_image = self.images[selected_image_key]
                    print(f"选择了指定图片: {selected_image_key}")
                else:
                    # 随机选择一张图片
                    available_keys = list(self.images.keys())
                    base_image_key = random.choice(available_keys)
                    base_image = self.images[base_image_key]
                    print(f"随机选择了图片: {base_image_key}")
                
                # 切割图片
                sliced_tiles = self.slice_image_for_puzzle(base_image, game_state.size)
                
                # 存储切割后的图片（最后一个为空白）
                self.sliced_images = {}
                for i, tile in enumerate(sliced_tiles[:-1]):  # 不包括最后一块（空白）
                    self.sliced_images[i + 1] = tile

    def draw_main_menu(self):
        """绘制主菜单 - 适配手机竖版"""
        # 美化的背景
        self.screen.fill(COLORS['BACKGROUND'])

        # 顶部装饰条
        pygame.draw.rect(self.screen, COLORS['LIGHT_BLUE'], (0, 0, WINDOW_WIDTH, 60))

        # 标题
        title_text = self.fonts['title'].render(get_text('game_title'), True, COLORS['BLACK'])
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, 80))
        self.screen.blit(title_text, title_rect)

        # 右上角语言切换按钮
        lang_button_width = 100
        lang_button_height = 30
        lang_button_x = WINDOW_WIDTH - lang_button_width - 15
        lang_button_y = 25
        language_button = pygame.Rect(lang_button_x, lang_button_y, lang_button_width, lang_button_height)
        pygame.draw.rect(self.screen, COLORS['BUTTON_LANGUAGE'], language_button, border_radius=8)
        lang_text = self.fonts['small'].render(get_text('switch_language'), True, COLORS['WHITE'])
        lang_rect = lang_text.get_rect(center=language_button.center)
        self.screen.blit(lang_text, lang_rect)

        # 游戏模式选择区域
        mode_y = 150
        mode_text = self.fonts['large'].render(get_text('select_game_mode'), True, COLORS['BLACK'])
        self.screen.blit(mode_text, (WINDOW_WIDTH//2 - mode_text.get_width()//2, mode_y))

        # 按钮尺寸适配手机屏幕
        button_width = WINDOW_WIDTH - 80
        button_height = 50
        button_x = 40

        # 数字模式按钮
        numbers_button = pygame.Rect(button_x, mode_y + 50, button_width, button_height)
        pygame.draw.rect(self.screen, COLORS['BUTTON_PRIMARY'], numbers_button, border_radius=12)
        numbers_text = self.fonts['medium'].render(get_text('numbers_puzzle'), True, COLORS['WHITE'])
        numbers_rect = numbers_text.get_rect(center=numbers_button.center)
        self.screen.blit(numbers_text, numbers_rect)

        # 图片模式按钮
        images_button = pygame.Rect(button_x, mode_y + 120, button_width, button_height)
        pygame.draw.rect(self.screen, COLORS['BUTTON_SECONDARY'], images_button, border_radius=12)
        images_text = self.fonts['medium'].render(get_text('images_puzzle'), True, COLORS['WHITE'])
        images_rect = images_text.get_rect(center=images_button.center)
        self.screen.blit(images_text, images_rect)

        # 排行榜按钮
        leaderboard_button = pygame.Rect(button_x, mode_y + 190, button_width, button_height)
        pygame.draw.rect(self.screen, COLORS['BUTTON_INFO'], leaderboard_button, border_radius=12)
        leaderboard_text = self.fonts['medium'].render(get_text('view_leaderboard'), True, COLORS['WHITE'])
        leaderboard_rect = leaderboard_text.get_rect(center=leaderboard_button.center)
        self.screen.blit(leaderboard_text, leaderboard_rect)

        return numbers_button, images_button, leaderboard_button, language_button

    def draw_difficulty_menu(self, game_mode: str):
        """绘制难度选择菜单 - 适配手机竖版（仅保留EASY和MEDIUM）"""
        # 美化的背景
        self.screen.fill(COLORS['BACKGROUND'])

        # 顶部装饰条
        pygame.draw.rect(self.screen, COLORS['LIGHT_BLUE'], (0, 0, WINDOW_WIDTH, 60))

        # 标题
        mode_name = get_text('numbers_puzzle') if game_mode == 'NUMBERS' else get_text('images_puzzle')
        title_text = self.fonts['large'].render(f"{mode_name}", True, COLORS['BLACK'])
        subtitle_text = self.fonts['medium'].render(get_text('select_difficulty_level'), True, COLORS['DARK_GRAY'])

        title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, 70))
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH//2, 100))

        self.screen.blit(title_text, title_rect)
        self.screen.blit(subtitle_text, subtitle_rect)

        # 语言切换提示
        lang_hint = self.fonts['small'].render("Alt+L to switch language", True, COLORS['GRAY'])
        lang_hint_rect = lang_hint.get_rect(topright=(WINDOW_WIDTH - 15, 20))
        self.screen.blit(lang_hint, lang_hint_rect)

        # 难度选项 - 仅保留EASY和MEDIUM
        difficulties = ['EASY', 'MEDIUM']  # 删除了'HARD'
        diff_names = {
            'EASY': get_text('easy'),
            'MEDIUM': get_text('medium')
        }
        button_y = 180
        button_width = WINDOW_WIDTH - 80
        button_height = 55
        button_x = 40

        buttons = []
        for i, diff_key in enumerate(difficulties):
            button = pygame.Rect(button_x, button_y + i * 70, button_width, button_height)
            # 根据难度使用不同颜色
            color_map = {
                'EASY': COLORS['BUTTON_SECONDARY'],
                'MEDIUM': COLORS['BUTTON_PRIMARY']
            }
            pygame.draw.rect(self.screen, color_map[diff_key], button, border_radius=12)

            text = self.fonts['medium'].render(diff_names[diff_key], True, COLORS['WHITE'])
            text_rect = text.get_rect(center=button.center)
            self.screen.blit(text, text_rect)

            buttons.append((button, diff_key))

        # 如果是图片模式，添加图片选择按钮
        if game_mode == 'IMAGES':
            image_select_button = pygame.Rect(button_x, button_y + 2 * 70, button_width, button_height)
            pygame.draw.rect(self.screen, COLORS['BUTTON_TERTIARY'], image_select_button, border_radius=12)
            image_select_text = self.fonts['medium'].render(get_text('select_specific_image'), True, COLORS['WHITE'])
            image_select_rect = image_select_text.get_rect(center=image_select_button.center)
            self.screen.blit(image_select_text, image_select_rect)
            buttons.append((image_select_button, 'SELECT_IMAGE'))

        # 返回按钮
        back_button = pygame.Rect(20, WINDOW_HEIGHT - 70, 100, 50)
        pygame.draw.rect(self.screen, COLORS['GRAY'], back_button, border_radius=12)
        back_text = self.fonts['medium'].render(get_text('back'), True, COLORS['WHITE'])
        back_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, back_rect)
        buttons.append((back_button, 'BACK'))

        return buttons

    def draw_game_screen(self, game_state: GameState):
        """绘制游戏主界面 - 适配手机竖版"""
        # 美化的背景
        self.screen.fill(COLORS['BACKGROUND'])

        # 绘制顶部信息栏
        self.draw_game_info(game_state)

        # 绘制游戏板背景
        board_bg_padding = 8
        board_bg = pygame.Rect(
            self.board_x - board_bg_padding,
            self.board_y - board_bg_padding,
            self.tile_size * 4 + 2 * board_bg_padding,
            self.tile_size * 4 + 2 * board_bg_padding
        )
        pygame.draw.rect(self.screen, COLORS['GAME_BG'], board_bg, border_radius=18)
        pygame.draw.rect(self.screen, COLORS['BLUE'], board_bg, 3, border_radius=18)

        # 绘制游戏板
        self.draw_game_board(game_state)

        # 绘制控制按钮
        restart_button, menu_button = self.draw_control_buttons()

        return restart_button, menu_button

    def draw_game_info(self, game_state: GameState):
        """绘制游戏信息 - 适配手机竖版"""
        # 背景条
        info_bg = pygame.Rect(0, 0, WINDOW_WIDTH, self.info_height)
        pygame.draw.rect(self.screen, COLORS['LIGHT_BLUE'], info_bg)
        pygame.draw.line(self.screen, COLORS['BLUE'], (0, self.info_height), (WINDOW_WIDTH, self.info_height), 3)

        # 游戏信息
        info_y = 15
        left_x = 15
        right_x = WINDOW_WIDTH - 15

        # 难度信息
        diff_names = {
            'EASY': get_text('easy'),
            'MEDIUM': get_text('medium')
        }
        diff_text = self.fonts['medium'].render(
            f"{get_text('difficulty')} {diff_names.get(game_state.current_difficulty, 'Unknown')}",
            True, COLORS['BLACK']
        )
        self.screen.blit(diff_text, (left_x, info_y))

        # 语言切换提示
        lang_hint = self.fonts['small'].render("Alt+L: 切换语言", True, COLORS['DARK_GRAY'])
        self.screen.blit(lang_hint, (left_x, info_y + 25))

        # 时间
        time_display = game_state.stats.get_formatted_time() if game_state.stats and game_state.stats.game_started else "00:00"
        time_text = self.fonts['medium'].render(
            f"{get_text('time')} {time_display}",
            True, COLORS['BLACK']
        )
        time_rect = time_text.get_rect(topright=(right_x, info_y))
        self.screen.blit(time_text, time_rect)

        # 步数
        moves_count = game_state.stats.moves if game_state.stats else 0
        moves_text = self.fonts['medium'].render(
            f"{get_text('moves')} {moves_count}",
            True, COLORS['BLACK']
        )
        moves_rect = moves_text.get_rect(topright=(right_x, info_y + 25))
        self.screen.blit(moves_text, moves_rect)

    def draw_game_board(self, game_state: GameState):
        """绘制游戏板"""
        size = game_state.size
        tile_size = self.tile_size

        # 如果是图片模式且还没有准备图片，则准备图片
        if game_state.current_mode == 'IMAGES' and not self.sliced_images:
            self.prepare_puzzle_images(game_state)

        # 计算偏移量使不同大小的拼图都能居中显示
        offset = (4 - size) * tile_size // 2  # 4是标准大小
        start_x = self.board_x + offset
        start_y = self.board_y + offset

        for row in range(size):
            for col in range(size):
                number = game_state.board[row][col]

                # 计算位置
                x = start_x + col * tile_size
                y = start_y + row * tile_size

                if number == 0:
                    # 空格 - 使用更美观的设计
                    pygame.draw.rect(self.screen, COLORS['GAME_BG'],
                                   (x, y, tile_size, tile_size), border_radius=10)
                    pygame.draw.rect(self.screen, COLORS['GRAY'],
                                   (x, y, tile_size, tile_size), 2, border_radius=10)
                else:
                    # 绘制方块
                    if game_state.current_mode == 'NUMBERS':
                        self.draw_number_tile(x, y, tile_size, number)
                    else:
                        self.draw_image_tile(x, y, tile_size, number)

    def draw_number_tile(self, x: int, y: int, size: int, number: int):
        """绘制数字方块"""
        # 方块背景 - 使用渐变色效果
        pygame.draw.rect(self.screen, COLORS['BLUE'], (x, y, size, size), border_radius=10)
        pygame.draw.rect(self.screen, COLORS['BLACK'], (x, y, size, size), 2, border_radius=10)

        # 添加高光效果
        highlight = pygame.Surface((size-6, size//4), pygame.SRCALPHA)
        highlight.fill((255, 255, 255, 80))
        self.screen.blit(highlight, (x+3, y+3))

        # 数字文本
        font = self.fonts['large']
        if size < 80:  # 小方块使用较小字体
            font = self.fonts['medium']

        text = font.render(str(number), True, COLORS['WHITE'])
        text_rect = text.get_rect(center=(x + size//2, y + size//2))
        self.screen.blit(text, text_rect)

    def draw_image_tile(self, x: int, y: int, size: int, number: int):
        """绘制图片方块"""
        # 方块边框
        pygame.draw.rect(self.screen, COLORS['BLACK'], (x, y, size, size), 2, border_radius=10)

        # 如果有对应切片图片则绘制
        if number in self.sliced_images:
            sliced_image = self.sliced_images[number]
            # 缩放图片适应方块大小
            scaled_image = pygame.transform.scale(sliced_image, (size - 6, size - 6))
            self.screen.blit(scaled_image, (x + 3, y + 3))
        else:
            # 没有图片时显示数字作为后备
            self.draw_number_tile(x, y, size, number)

    def draw_control_buttons(self):
        """绘制控制按钮 - 适配手机竖版"""
        button_width = (WINDOW_WIDTH - 60) // 2
        button_height = 45
        button_spacing = 20
        bottom_y = WINDOW_HEIGHT - button_height - 20

        # 重新开始按钮
        restart_x = 20
        restart_button = pygame.Rect(restart_x, bottom_y, button_width, button_height)
        pygame.draw.rect(self.screen, COLORS['BUTTON_SECONDARY'], restart_button, border_radius=10)
        restart_text = self.fonts['medium'].render(get_text('restart'), True, COLORS['WHITE'])
        restart_rect = restart_text.get_rect(center=restart_button.center)
        self.screen.blit(restart_text, restart_rect)

        # 主菜单按钮
        menu_x = WINDOW_WIDTH - button_width - 20
        menu_button = pygame.Rect(menu_x, bottom_y, button_width, button_height)
        pygame.draw.rect(self.screen, COLORS['BUTTON_DANGER'], menu_button, border_radius=10)
        menu_text = self.fonts['medium'].render(get_text('menu'), True, COLORS['WHITE'])
        menu_rect = menu_text.get_rect(center=menu_button.center)
        self.screen.blit(menu_text, menu_rect)

        return restart_button, menu_button

    def draw_game_complete(self, game_state: GameState, auto_close_timer: Optional[int] = None):
        """绘制游戏完成界面 - 移除倒计时显示"""
        # 半透明覆盖层
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(COLORS['BLACK'])
        self.screen.blit(overlay, (0, 0))

        # 完成信息框
        box_width = WINDOW_WIDTH - 60
        box_height = 250  # 减少高度因为不需要倒计时显示
        box_x = 30
        box_y = (WINDOW_HEIGHT - box_height) // 2

        pygame.draw.rect(self.screen, COLORS['WHITE'], (box_x, box_y, box_width, box_height), border_radius=20)
        pygame.draw.rect(self.screen, COLORS['GREEN'], (box_x, box_y, box_width, box_height), 4, border_radius=20)

        # 完成文本
        complete_text = self.fonts['large'].render(get_text('congratulations'), True, COLORS['GREEN'])
        complete_rect = complete_text.get_rect(center=(WINDOW_WIDTH//2, box_y + 40))
        self.screen.blit(complete_text, complete_rect)

        # 成绩信息
        time_text = self.fonts['medium'].render(
            f"{get_text('completion_time')} {game_state.stats.get_formatted_time()}", True, COLORS['BLACK']
        )
        time_rect = time_text.get_rect(center=(WINDOW_WIDTH//2, box_y + 85))
        self.screen.blit(time_text, time_rect)

        moves_text = self.fonts['medium'].render(
            f"{get_text('completion_moves')} {game_state.stats.moves}", True, COLORS['BLACK']
        )
        moves_rect = moves_text.get_rect(center=(WINDOW_WIDTH//2, box_y + 125))
        self.screen.blit(moves_text, moves_rect)

        # 确定按钮（移除倒计时显示）
        ok_button = pygame.Rect(WINDOW_WIDTH//2 - 60, box_y + 170, 120, 40)
        pygame.draw.rect(self.screen, COLORS['BUTTON_PRIMARY'], ok_button, border_radius=10)
        ok_text = self.fonts['medium'].render(get_text('ok'), True, COLORS['WHITE'])
        ok_rect = ok_text.get_rect(center=ok_button.center)
        self.screen.blit(ok_text, ok_rect)

        return ok_button

    def draw_leaderboard(self, entries, game_state, current_filter_difficulty='EASY'):
        """绘制排行榜"""
        self.screen.fill(COLORS['BACKGROUND'])
        
        # 标题
        title_text = self.fonts['large'].render(get_text('leaderboard'), True, COLORS['BLACK'])
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, 50))
        self.screen.blit(title_text, title_rect)
        
        # 当前筛选条件显示 - 显示模式和难度
        filter_y = 90
        mode_text = get_text('numbers_puzzle') if game_state.current_mode == 'NUMBERS' else get_text('images_puzzle')
        diff_text = get_text('easy') if current_filter_difficulty == 'EASY' else get_text('medium')
        filter_text = self.fonts['medium'].render(f"模式: {mode_text} | 难度: {diff_text}", True, COLORS['DARK_GRAY'])
        filter_rect = filter_text.get_rect(center=(WINDOW_WIDTH//2, filter_y))
        self.screen.blit(filter_text, filter_rect)
        
        # 难度筛选按钮
        button_width = 80
        button_height = 30
        button_y = filter_y + 40
        easy_button = pygame.Rect(WINDOW_WIDTH//2 - button_width - 10, button_y, button_width, button_height)
        medium_button = pygame.Rect(WINDOW_WIDTH//2 + 10, button_y, button_width, button_height)
        
        # 简单难度按钮
        easy_color = COLORS['BUTTON_SECONDARY'] if current_filter_difficulty == 'EASY' else COLORS['GRAY']
        pygame.draw.rect(self.screen, easy_color, easy_button, border_radius=8)
        easy_text = self.fonts['small'].render(get_text('easy'), True, COLORS['WHITE'])
        easy_rect = easy_text.get_rect(center=easy_button.center)
        self.screen.blit(easy_text, easy_rect)
        
        # 中等难度按钮
        medium_color = COLORS['BUTTON_PRIMARY'] if current_filter_difficulty == 'MEDIUM' else COLORS['GRAY']
        pygame.draw.rect(self.screen, medium_color, medium_button, border_radius=8)
        medium_text = self.fonts['small'].render(get_text('medium'), True, COLORS['WHITE'])
        medium_rect = medium_text.get_rect(center=medium_button.center)
        self.screen.blit(medium_text, medium_rect)
        
        # 排行榜表头
        header_y = button_y + 50
        headers = ["排名", "玩家", "时间", "步数", "模式"]
        header_positions = [50, 120, 220, 300, 380]
        
        for i, header in enumerate(headers):
            header_text = self.fonts['medium'].render(header, True, COLORS['BLACK'])
            self.screen.blit(header_text, (header_positions[i], header_y))
        
        # 分隔线
        pygame.draw.line(self.screen, COLORS['GRAY'], (30, header_y + 30), (WINDOW_WIDTH - 30, header_y + 30), 2)
        
        # 排行榜条目
        if entries:
            entry_y = header_y + 50
            for i, entry in enumerate(entries[:10]):  # 显示前10名
                # 排名
                rank_text = self.fonts['medium'].render(str(i + 1), True, COLORS['BLACK'])
                self.screen.blit(rank_text, (header_positions[0], entry_y))
                
                # 玩家姓名
                name_text = self.fonts['medium'].render(entry.player_name[:8], True, COLORS['BLACK'])
                self.screen.blit(name_text, (header_positions[1], entry_y))
                
                # 时间
                time_text = self.fonts['medium'].render(f"{entry.time_seconds:.2f}s", True, COLORS['BLACK'])
                self.screen.blit(time_text, (header_positions[2], entry_y))
                
                # 步数
                moves_text = self.fonts['medium'].render(str(entry.moves), True, COLORS['BLACK'])
                self.screen.blit(moves_text, (header_positions[3], entry_y))
                
                # 模式
                mode_short = "数字" if entry.game_mode == 'NUMBERS' else "图片"
                mode_text = self.fonts['medium'].render(mode_short, True, COLORS['BLACK'])
                self.screen.blit(mode_text, (header_positions[4], entry_y))
                
                entry_y += 35
        else:
            # 无记录提示
            no_record_text = self.fonts['medium'].render("暂无记录", True, COLORS['GRAY'])
            no_record_rect = no_record_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(no_record_text, no_record_rect)
        
        # 操作按钮
        button_y = WINDOW_HEIGHT - 80
        button_width = 120
        button_height = 50
        
        # 返回按钮
        back_button = pygame.Rect(30, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, COLORS['GRAY'], back_button, border_radius=12)
        back_text = self.fonts['medium'].render(get_text('back'), True, COLORS['WHITE'])
        back_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, back_rect)
        
        # 清空按钮
        clear_button = pygame.Rect(WINDOW_WIDTH - button_width - 30, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, COLORS['RED'], clear_button, border_radius=12)
        clear_text = self.fonts['medium'].render(get_text('clear'), True, COLORS['WHITE'])
        clear_rect = clear_text.get_rect(center=clear_button.center)
        self.screen.blit(clear_text, clear_rect)
        
        return back_button, clear_button, easy_button, medium_button

    def draw_confirm_clear(self):
        """绘制确认清空排行榜界面"""
        # 半透明遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(COLORS['BLACK'])
        self.screen.blit(overlay, (0, 0))

        # 确认框
        box_width = 320
        box_height = 180
        box_x = (WINDOW_WIDTH - box_width) // 2
        box_y = (WINDOW_HEIGHT - box_height) // 2

        pygame.draw.rect(self.screen, COLORS['WHITE'], (box_x, box_y, box_width, box_height), border_radius=15)
        pygame.draw.rect(self.screen, COLORS['RED'], (box_x, box_y, box_width, box_height), 3, border_radius=15)

        # 警告标题
        warning_text = self.fonts['large'].render("⚠️ 警告", True, COLORS['RED'])
        warning_rect = warning_text.get_rect(center=(WINDOW_WIDTH//2, box_y + 30))
        self.screen.blit(warning_text, warning_rect)

        # 确认信息
        confirm_text1 = self.fonts['medium'].render("确定要清空排行榜吗？", True, COLORS['BLACK'])
        confirm_text2 = self.fonts['small'].render("此操作不可撤销！", True, COLORS['RED'])

        confirm_rect1 = confirm_text1.get_rect(center=(WINDOW_WIDTH//2, box_y + 70))
        confirm_rect2 = confirm_text2.get_rect(center=(WINDOW_WIDTH//2, box_y + 100))

        self.screen.blit(confirm_text1, confirm_rect1)
        self.screen.blit(confirm_text2, confirm_rect2)

        # 按钮区域
        button_y = box_y + 130
        button_width = 100
        button_height = 35

        # 确定按钮
        yes_button = pygame.Rect(box_x + 40, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, COLORS['BUTTON_DANGER'], yes_button, border_radius=8)
        yes_text = self.fonts['medium'].render("确定", True, COLORS['WHITE'])
        yes_rect = yes_text.get_rect(center=yes_button.center)
        self.screen.blit(yes_text, yes_rect)

        # 取消按钮
        no_button = pygame.Rect(box_x + box_width - button_width - 40, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, COLORS['BUTTON_PRIMARY'], no_button, border_radius=8)
        no_text = self.fonts['medium'].render("取消", True, COLORS['WHITE'])
        no_rect = no_text.get_rect(center=no_button.center)
        self.screen.blit(no_text, no_rect)

        return yes_button, no_button

    def draw_image_selection_menu(self, available_images):
        """绘制图片选择菜单"""
        self.screen.fill(COLORS['BACKGROUND'])
        
        # 标题
        title_text = self.fonts['large'].render(get_text('select_image'), True, COLORS['BLACK'])
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, 80))
        self.screen.blit(title_text, title_rect)
        
        # 随机选择按钮
        random_button = pygame.Rect(WINDOW_WIDTH//2 - 100, 150, 200, 50)
        pygame.draw.rect(self.screen, COLORS['BUTTON_SECONDARY'], random_button, border_radius=12)
        random_text = self.fonts['medium'].render(get_text('random_image'), True, COLORS['WHITE'])
        random_rect = random_text.get_rect(center=random_button.center)
        self.screen.blit(random_text, random_rect)
        
        # 图片预览区域
        preview_y = 230
        preview_width = 120
        preview_height = 120
        spacing = 20
        images_per_row = 3
        margin = (WINDOW_WIDTH - (images_per_row * preview_width + (images_per_row - 1) * spacing)) // 2
        
        image_buttons = []
        
        for i, (key, image) in enumerate(available_images.items()):
            row = i // images_per_row
            col = i % images_per_row
            
            x = margin + col * (preview_width + spacing)
            y = preview_y + row * (preview_height + spacing + 30)
            
            # 图片预览
            scaled_image = pygame.transform.scale(image, (preview_width, preview_height))
            self.screen.blit(scaled_image, (x, y))
            
            # 图片标签
            label_text = self.fonts['small'].render(f"图片{i+1}", True, COLORS['BLACK'])
            label_rect = label_text.get_rect(center=(x + preview_width//2, y + preview_height + 15))
            self.screen.blit(label_text, label_rect)
            
            # 可点击区域
            button_rect = pygame.Rect(x, y, preview_width, preview_height + 30)
            image_buttons.append((button_rect, key))
        
        # 返回按钮
        back_button = pygame.Rect(20, WINDOW_HEIGHT - 70, 100, 50)
        pygame.draw.rect(self.screen, COLORS['GRAY'], back_button, border_radius=12)
        back_text = self.fonts['medium'].render(get_text('back'), True, COLORS['WHITE'])
        back_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, back_rect)
        
        return random_button, image_buttons, back_button

    def get_tile_position(self, mouse_pos: Tuple[int, int], game_state: GameState) -> Tuple[int, int]:
        """根据鼠标位置获取对应的方块坐标"""
        x, y = mouse_pos
        size = game_state.size
        tile_size = self.tile_size

        # 计算偏移量
        offset = (4 - size) * tile_size // 2
        start_x = self.board_x + offset
        start_y = self.board_y + offset

        # 计算相对位置
        rel_x = x - start_x
        rel_y = y - start_y

        # 检查是否在游戏板范围内
        if 0 <= rel_x < size * tile_size and 0 <= rel_y < size * tile_size:
            col = rel_x // tile_size
            row = rel_y // tile_size
            return (row, col)

        return (-1, -1)

    def update_display(self):
        """更新显示"""
        pygame.display.flip()
        self.clock.tick(FPS)
