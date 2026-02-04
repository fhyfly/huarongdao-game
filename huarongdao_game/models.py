# -*- coding: utf-8 -*-
"""
华容道游戏数据模型
包含游戏状态、排行榜条目等数据结构
"""

import json
import time
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import config


@dataclass
class GameStats:
    """游戏统计信息"""
    start_time: float = 0.0
    moves: int = 0
    is_active: bool = False  # 默认不激活，等待游戏开始
    game_started: bool = False  # 标记游戏是否真正开始
    final_time: float = 0.0  # 存储最终完成时间
    
    def start_timer(self):
        """开始计时"""
        if not self.game_started:
            self.start_time = time.time()
            self.is_active = True
            self.game_started = True
            print(f"计时器启动: {self.start_time}")  # 调试信息
    
    def stop_timer(self):
        """停止计时并记录最终时间"""
        if self.is_active and self.game_started:
            self.final_time = time.time() - self.start_time
            self.is_active = False
            # print(f"计时器停止: 最终时间 {self.final_time:.2f}秒")  # 调试信息
    
    def get_elapsed_time(self) -> float:
        """获取已用时间"""
        if self.is_active and self.game_started:
            elapsed = time.time() - self.start_time
            # print(f"实时时间: {elapsed:.2f}秒")  # 调试信息
            return elapsed
        elif self.final_time > 0:
            # print(f"最终时间: {self.final_time:.2f}秒")  # 调试信息
            return self.final_time
        return 0
    
    def get_formatted_time(self) -> str:
        """获取格式化的时间字符串"""
        elapsed = self.get_elapsed_time()
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        return f"{minutes:02d}:{seconds:02d}"


@dataclass
class LeaderboardEntry:
    """排行榜条目"""
    player_name: str
    time_seconds: float  # 改为float类型以支持小数
    moves: int
    difficulty: str
    game_mode: str
    timestamp: float
    
    def __post_init__(self):
        """在初始化后处理数据"""
        # 确保时间精度为0.01秒
        self.time_seconds = round(self.time_seconds, 2)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict):
        """从字典创建实例"""
        return cls(**data)
    
    def get_formatted_time(self) -> str:
        """获取格式化的时间显示（精确到0.01秒）"""
        minutes = int(self.time_seconds // 60)
        seconds = self.time_seconds % 60
        return f"{minutes:02d}:{seconds:05.2f}"  # 格式化为 mm:ss.SS


class Leaderboard:
    """排行榜管理类"""
    
    def __init__(self, filename: str = None):
        # 如果没有提供文件名，使用配置中的默认路径
        self.filename = filename or config.LEADERBOARD_FILE
        self.entries: List[LeaderboardEntry] = []
        self.load_leaderboard()
    
    def load_leaderboard(self):
        """从文件加载排行榜"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.entries = [LeaderboardEntry.from_dict(entry) for entry in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.entries = []
    
    def save_leaderboard(self):
        """保存排行榜到文件"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                data = [entry.to_dict() for entry in self.entries]
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存排行榜失败: {e}")
    
    def add_entry(self, entry: LeaderboardEntry):
        """添加新的排行榜条目"""
        self.entries.append(entry)
        # 按时间排序
        self.entries.sort(key=lambda x: (x.time_seconds, x.moves))
        # 保持最大条目数
        self.entries = self.entries[:config.MAX_LEADERBOARD_ENTRIES]
        self.save_leaderboard()
    
    def clear_leaderboard(self):
        """清空排行榜"""
        self.entries = []
        self.save_leaderboard()
    
    def get_entries_by_difficulty_and_mode(self, difficulty: str, mode: str) -> List[LeaderboardEntry]:
        """获取特定难度和模式的排行榜"""
        filtered = [entry for entry in self.entries 
                   if entry.difficulty == difficulty and entry.game_mode == mode]
        return sorted(filtered, key=lambda x: (x.time_seconds, x.moves))[:config.MAX_LEADERBOARD_ENTRIES]


class GameState:
    """游戏状态管理"""
    
    def __init__(self):
        self.board: List[List[int]] = []
        self.size: int = 0
        self.empty_pos: tuple = (0, 0)
        self.stats: Optional[GameStats] = None
        self.is_solved: bool = False
        self.current_difficulty: str = 'EASY'
        self.current_mode: str = 'NUMBERS'
        self.game_ready: bool = False  # 标记游戏是否准备好开始
        
    def initialize_board(self, size: int, mode: str = 'NUMBERS'):
        """初始化游戏板"""
        self.size = size
        self.current_mode = mode
        
        # 创建有序的数字板
        numbers = list(range(1, size * size))
        numbers.append(0)  # 0表示空格
        
        # 打乱数组
        import random
        random.shuffle(numbers)
        
        # 确保可解性
        while not self._is_solvable(numbers, size):
            random.shuffle(numbers)
        
        # 转换为二维数组
        self.board = []
        for i in range(size):
            row = []
            for j in range(size):
                num = numbers[i * size + j]
                row.append(num)
                if num == 0:
                    self.empty_pos = (i, j)
            self.board.append(row)
        
        # 初始化统计数据（不激活计时器）
        self.stats = GameStats(start_time=0)
        self.is_solved = False
        self.game_ready = True  # 标记游戏已准备好
    
    def start_game(self):
        """正式开始游戏（启动计时器）"""
        if self.stats and self.game_ready and not self.stats.game_started:
            self.stats.start_timer()
    
    def _is_solvable(self, numbers: List[int], size: int) -> bool:
        """检查排列是否可解"""
        inversions = 0
        for i in range(len(numbers)):
            for j in range(i + 1, len(numbers)):
                if numbers[i] != 0 and numbers[j] != 0 and numbers[i] > numbers[j]:
                    inversions += 1
        
        if size % 2 == 1:
            # 奇数尺寸：逆序数必须是偶数
            return inversions % 2 == 0
        else:
            # 偶数尺寸：逆序数的奇偶性必须与空格所在行数的奇偶性相同
            empty_row = numbers.index(0) // size
            return (inversions + empty_row) % 2 == 0
    
    def move_tile(self, row: int, col: int) -> bool:
        """移动指定位置的方块"""
        if not self.stats:
            return False
            
        # 如果游戏还没开始，第一次移动时启动游戏
        if self.game_ready and not self.stats.game_started:
            self.start_game()
            
        empty_row, empty_col = self.empty_pos
        
        # 检查是否相邻
        if abs(row - empty_row) + abs(col - empty_col) != 1:
            return False
        
        # 交换位置
        self.board[empty_row][empty_col] = self.board[row][col]
        self.board[row][col] = 0
        self.empty_pos = (row, col)
        
        # 更新步数
        self.stats.moves += 1
        print(f"移动次数: {self.stats.moves}")  # 调试信息
        
        # 检查是否完成
        self._check_solved()
        
        return True
    
    def move_direction(self, direction: str) -> bool:
        """按方向移动（已废弃，仅保留用于兼容性）"""
        # 这个方法不再使用，但保留以防万一
        empty_row, empty_col = self.empty_pos
        
        if direction == 'UP' and empty_row < self.size - 1:
            return self.move_tile(empty_row + 1, empty_col)
        elif direction == 'DOWN' and empty_row > 0:
            return self.move_tile(empty_row - 1, empty_col)
        elif direction == 'LEFT' and empty_col < self.size - 1:
            return self.move_tile(empty_row, empty_col + 1)
        elif direction == 'RIGHT' and empty_col > 0:
            return self.move_tile(empty_row, empty_col - 1)
        
        return False
    
    def _check_solved(self):
        """检查游戏是否完成"""
        expected = 1
        for i in range(self.size):
            for j in range(self.size):
                if i == self.size - 1 and j == self.size - 1:
                    # 最后一个应该是0
                    if self.board[i][j] != 0:
                        return
                else:
                    if self.board[i][j] != expected:
                        return
                    expected += 1
        
        # 游戏完成
        self.is_solved = True
        if self.stats:
            self.stats.stop_timer()
        print("游戏完成!")  # 调试信息
    
    def restart_game(self):
        """重新开始游戏"""
        if self.stats:
            self.stats.is_active = False
            self.stats.game_started = False
        self.initialize_board(self.size, self.current_mode)
    
    def get_completion_time(self) -> float:
        """获取完成时间（精确到0.01秒）"""
        if self.stats and not self.stats.is_active and self.stats.game_started:
            elapsed = time.time() - self.stats.start_time
            return round(elapsed, 2)
        return 0.0
    
    def is_game_active(self) -> bool:
        """检查游戏是否正在进行"""
        return self.stats is not None and self.stats.is_active
    
    def is_game_ready(self) -> bool:
        """检查游戏是否准备好"""
        return self.game_ready