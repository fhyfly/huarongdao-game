# -*- coding: utf-8 -*-
"""
华容道游戏控制器
处理用户输入和游戏逻辑控制
"""

import pygame
import time
from enum import Enum
from typing import Optional
from config import *
from models import GameState, Leaderboard, LeaderboardEntry


class GameScreen(Enum):
    """游戏屏幕枚举"""
    MAIN_MENU = "main_menu"
    DIFFICULTY_SELECT = "difficulty_select"
    IMAGE_SELECT = "image_select"  # 新增图片选择界面
    GAME_PLAY = "game_play"
    GAME_COMPLETE = "game_complete"
    LEADERBOARD = "leaderboard"
    CONFIRM_CLEAR = "confirm_clear"  # 新增：确认清空排行榜界面


class GameController:
    """游戏控制器"""
    
    def __init__(self):
        self.game_state = GameState()
        self.leaderboard = Leaderboard()
        self.current_screen = GameScreen.MAIN_MENU
        self.selected_mode = 'NUMBERS'
        self.selected_image = None  # 新增：记录选择的图片
        self.pending_completion_entry = None
        self.auto_close_timer = 0
        self.last_auto_close_update = 0
        self.completion_start_time = 0
        self.game_state.current_difficulty = 'EASY'  # 初始化默认难度
        self.leaderboard_filter_difficulty = 'EASY'  # 新增：排行榜筛选难度
    
    def handle_events(self, events, renderer=None):
        """处理游戏事件"""
        for event in events:
            if event.type == pygame.QUIT:
                return False
            
            elif self.current_screen == GameScreen.IMAGE_SELECT:
                result = self.handle_image_selection(event, renderer)
                if result is not None:
                    return result
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.current_screen == GameScreen.MAIN_MENU:
                    return self.handle_main_menu(event, renderer)
                elif self.current_screen == GameScreen.DIFFICULTY_SELECT:
                    return self.handle_difficulty_select(event, renderer)
                elif self.current_screen == GameScreen.GAME_PLAY:
                    return self.handle_game_play(event, renderer)
                elif self.current_screen == GameScreen.GAME_COMPLETE:
                    return self.handle_game_complete(event, renderer)
                elif self.current_screen == GameScreen.LEADERBOARD:
                    return self.handle_leaderboard(event, renderer)
                elif self.current_screen == GameScreen.CONFIRM_CLEAR:
                    return self.handle_confirm_clear(event, renderer)
            
            elif event.type == pygame.KEYDOWN:
                if event.key in KEY_MAPPINGS['QUIT']:
                    return False
        
        return True
    
    def handle_main_menu(self, event, renderer) -> bool:
        """处理主菜单事件（仅支持鼠标操作）"""
        if event.type == pygame.MOUSEBUTTONDOWN and renderer:
            numbers_button, images_button, leaderboard_button, language_button = renderer.draw_main_menu()
            
            if numbers_button.collidepoint(event.pos):
                self.selected_mode = 'NUMBERS'
                self.current_screen = GameScreen.DIFFICULTY_SELECT
            elif images_button.collidepoint(event.pos):
                self.selected_mode = 'IMAGES'
                self.current_screen = GameScreen.DIFFICULTY_SELECT
            elif leaderboard_button.collidepoint(event.pos):
                # 点击排行榜按钮
                self.current_screen = GameScreen.LEADERBOARD
            elif language_button.collidepoint(event.pos):
                # 点击语言切换按钮
                switch_language()
        
        return True
    
    def handle_difficulty_select(self, event, renderer) -> bool:
        """处理难度选择事件"""
        if event.type == pygame.MOUSEBUTTONDOWN and renderer:
            buttons = renderer.draw_difficulty_menu(self.selected_mode)
            
            for button, action in buttons:
                if button.collidepoint(event.pos):
                    if action == 'SELECT_IMAGE':
                        # 图片模式下的选择特定图片按钮
                        self.current_screen = GameScreen.IMAGE_SELECT
                    elif action == 'BACK':
                        # 返回按钮
                        self.current_screen = GameScreen.MAIN_MENU
                    elif action in DIFFICULTY_LEVELS:
                        # 正常的难度选择
                        self.start_new_game(action, renderer)
                        self.current_screen = GameScreen.GAME_PLAY
                    break
        
        elif event.type == pygame.KEYDOWN:
            if event.key in KEY_MAPPINGS['QUIT']:
                self.current_screen = GameScreen.MAIN_MENU
        
        return True
    
    def handle_image_selection(self, event, renderer) -> bool:
        """处理图片选择事件"""
        if event.type == pygame.MOUSEBUTTONDOWN and renderer:
            random_button, image_buttons, back_button = renderer.draw_image_selection_menu(renderer.images)
            
            # 随机选择按钮
            if random_button.collidepoint(event.pos):
                self.selected_image = None  # 表示随机选择
                self.current_screen = GameScreen.DIFFICULTY_SELECT  # 返回难度选择界面
            
            # 具体图片选择
            for button_rect, image_key in image_buttons:
                if button_rect.collidepoint(event.pos):
                    self.selected_image = image_key
                    self.current_screen = GameScreen.DIFFICULTY_SELECT  # 返回难度选择界面
                    break
            
            # 返回按钮
            if back_button.collidepoint(event.pos):
                self.current_screen = GameScreen.DIFFICULTY_SELECT
        
        elif event.type == pygame.KEYDOWN:
            if event.key in KEY_MAPPINGS['QUIT']:
                self.current_screen = GameScreen.DIFFICULTY_SELECT
        
        return True
    
    def handle_game_play(self, event, renderer) -> bool:
        """处理游戏进行中的事件（仅支持鼠标操作）"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 处理鼠标点击
            restart_button, menu_button = renderer.draw_game_screen(self.game_state)
            
            if restart_button.collidepoint(event.pos):
                self.restart_current_game(renderer)
            elif menu_button.collidepoint(event.pos):
                self.current_screen = GameScreen.MAIN_MENU
            else:
                # 处理游戏板点击
                tile_pos = renderer.get_tile_position(event.pos, self.game_state)
                if tile_pos != (-1, -1):
                    row, col = tile_pos
                    if self.game_state.move_tile(row, col):
                        # 检查是否完成游戏
                        if self.game_state.is_solved:
                            self.prepare_game_completion()
        
        return True
    
    def handle_game_complete(self, event, renderer) -> bool:
        """处理游戏完成事件 - 移除自动倒计时，改为纯手动确认"""
        if event.type == pygame.MOUSEBUTTONDOWN and renderer:
            # 绘制完成界面（不显示倒计时）
            ok_button = renderer.draw_game_complete(self.game_state, None)
            if ok_button.collidepoint(event.pos):
                # 点击确定按钮，添加到排行榜并跳转
                if self.pending_completion_entry:
                    self.leaderboard.add_entry(self.pending_completion_entry)
                    self.pending_completion_entry = None
                self.current_screen = GameScreen.LEADERBOARD
                return True
        
        return True
    
    def handle_leaderboard(self, event, renderer) -> bool:
        """处理排行榜事件（支持难度筛选）"""
        if event.type == pygame.MOUSEBUTTONDOWN and renderer:
            back_button, clear_button, easy_button, medium_button = renderer.draw_leaderboard(
                self.leaderboard.get_entries_by_difficulty_and_mode(
                    self.leaderboard_filter_difficulty, 
                    self.game_state.current_mode
                ),
                self.game_state,
                self.leaderboard_filter_difficulty
            )
            
            if back_button.collidepoint(event.pos):
                self.current_screen = GameScreen.MAIN_MENU
            elif clear_button.collidepoint(event.pos):
                # 点击清空按钮，跳转到确认界面
                self.current_screen = GameScreen.CONFIRM_CLEAR
            elif easy_button.collidepoint(event.pos):
                # 选择简单难度排行榜
                self.leaderboard_filter_difficulty = 'EASY'
            elif medium_button.collidepoint(event.pos):
                # 选择中等难度排行榜
                self.leaderboard_filter_difficulty = 'MEDIUM'
        
        return True
    
    def handle_confirm_clear(self, event, renderer) -> bool:
        """处理确认清空排行榜事件"""
        if event.type == pygame.MOUSEBUTTONDOWN and renderer:
            yes_button, no_button = renderer.draw_confirm_clear()
            
            if yes_button.collidepoint(event.pos):
                # 确认清空
                self.leaderboard.clear_leaderboard()
                self.current_screen = GameScreen.LEADERBOARD
            elif no_button.collidepoint(event.pos):
                # 取消清空
                self.current_screen = GameScreen.LEADERBOARD
        
        return True
    
    def start_new_game(self, difficulty: str, renderer=None):
        """开始新游戏"""
        size = DIFFICULTY_LEVELS[difficulty]['size']
        self.game_state.initialize_board(size, self.selected_mode)
        self.game_state.current_difficulty = difficulty
        
        # 如果是图片模式，准备拼图图片
        if self.selected_mode == 'IMAGES' and renderer:
            renderer.sliced_images = {}  # 清空之前的切片
            renderer.prepare_puzzle_images(self.game_state, self.selected_image)
    
    def restart_current_game(self, renderer=None):
        """重新开始当前游戏"""
        if self.game_state.size > 0:
            self.game_state.restart_game()
            # 如果是图片模式，重新准备拼图图片
            if self.game_state.current_mode == 'IMAGES' and renderer:
                renderer.sliced_images = {}
                renderer.prepare_puzzle_images(self.game_state)
    
    def prepare_game_completion(self):
        """准备游戏完成处理"""
        # 停止计时器并获取最终时间
        self.game_state.stats.stop_timer()
        
        # 获取玩家姓名
        player_name = self.get_player_name()
        
        # 创建排行榜条目
        completion_time = self.game_state.stats.get_elapsed_time()
        self.pending_completion_entry = LeaderboardEntry(
            player_name=player_name,
            time_seconds=completion_time,
            moves=self.game_state.stats.moves,
            difficulty=self.game_state.current_difficulty,
            game_mode=self.game_state.current_mode,
            timestamp=time.time()
        )
        
        self.current_screen = GameScreen.GAME_COMPLETE
    
    def get_player_name(self) -> str:
        """获取玩家姓名（简化版本，实际应用中可能需要弹出输入框）"""
        return "Player" if LANGUAGE == "EN" else "玩家"
    
    def render_current_screen(self, renderer):
        """渲染当前屏幕"""
        if self.current_screen == GameScreen.MAIN_MENU:
            renderer.draw_main_menu()
        elif self.current_screen == GameScreen.DIFFICULTY_SELECT:
            renderer.draw_difficulty_menu(self.selected_mode)
        elif self.current_screen == GameScreen.IMAGE_SELECT:
            renderer.draw_image_selection_menu(renderer.images)
        elif self.current_screen == GameScreen.GAME_PLAY:
            renderer.draw_game_screen(self.game_state)
        elif self.current_screen == GameScreen.GAME_COMPLETE:
            renderer.draw_game_complete(self.game_state, None)
        elif self.current_screen == GameScreen.LEADERBOARD:
            entries = self.leaderboard.get_entries_by_difficulty_and_mode(
                self.leaderboard_filter_difficulty,
                self.game_state.current_mode
            )
            renderer.draw_leaderboard(entries, self.game_state, self.leaderboard_filter_difficulty)
        elif self.current_screen == GameScreen.CONFIRM_CLEAR:
            renderer.draw_confirm_clear()
        
        renderer.update_display()
    
    def update_game_logic(self, dt: float):
        """更新游戏逻辑"""
        if self.game_state.stats and self.game_state.stats.game_started:
            self.game_state.stats.update_timer(dt)
            # 移除实时时间输出到控制台
            # elapsed = self.game_state.stats.get_elapsed_time()
            # print(f"实时时间: {elapsed:.2f}秒")
