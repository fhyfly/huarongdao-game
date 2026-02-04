# -*- coding: utf-8 -*-
"""
华容道游戏测试文件
用于验证核心功能的正确性
"""

import unittest
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from huarongdao_game.models import GameState, Leaderboard, LeaderboardEntry
    from huarongdao_game.config import DIFFICULTY_LEVELS
except ImportError:
    # 如果上面的方式不行，尝试直接导入
    sys.path.insert(0, os.path.join(project_root, 'huarongdao_game'))
    from models import GameState, Leaderboard, LeaderboardEntry
    from config import DIFFICULTY_LEVELS


class TestGameState(unittest.TestCase):
    """游戏状态测试"""
    
    def setUp(self):
        """测试前准备"""
        self.game_state = GameState()
    
    def test_initialize_board_3x3(self):
        """测试3x3游戏板初始化"""
        self.game_state.initialize_board(3, 'NUMBERS')
        self.assertEqual(self.game_state.size, 3)
        self.assertEqual(len(self.game_state.board), 3)
        self.assertEqual(len(self.game_state.board[0]), 3)
        
        # 检查是否包含0-8的所有数字
        flat_board = [num for row in self.game_state.board for num in row]
        self.assertIn(0, flat_board)
        for i in range(1, 9):
            self.assertIn(i, flat_board)
    
    def test_initialize_board_4x4(self):
        """测试4x4游戏板初始化"""
        self.game_state.initialize_board(4, 'NUMBERS')
        self.assertEqual(self.game_state.size, 4)
        self.assertEqual(len(self.game_state.board), 4)
        self.assertEqual(len(self.game_state.board[0]), 4)
        
        # 检查是否包含0-15的所有数字
        flat_board = [num for row in self.game_state.board for num in row]
        self.assertIn(0, flat_board)
        for i in range(1, 16):
            self.assertIn(i, flat_board)
    
    def test_is_solvable_algorithm(self):
        """测试可解性算法"""
        # 测试已知可解的排列
        solvable_3x3 = [1, 2, 3, 4, 5, 6, 7, 8, 0]  # 已完成状态
        self.assertTrue(self.game_state._is_solvable(solvable_3x3, 3))
        
        # 测试已知不可解的排列
        unsolvable_3x3 = [1, 2, 3, 4, 5, 6, 8, 7, 0]  # 交换7和8
        self.assertFalse(self.game_state._is_solvable(unsolvable_3x3, 3))
    
    def test_move_tile_valid(self):
        """测试有效移动"""
        self.game_state.initialize_board(3, 'NUMBERS')
        empty_row, empty_col = self.game_state.empty_pos
        
        # 尝试移动相邻的方块
        if empty_row > 0:
            target_row, target_col = empty_row - 1, empty_col
        else:
            target_row, target_col = empty_row + 1, empty_col
            
        result = self.game_state.move_tile(target_row, target_col)
        self.assertTrue(result)
        self.assertEqual(self.game_state.empty_pos, (target_row, target_col))
        self.assertEqual(self.game_state.stats.moves, 1)
    
    def test_move_tile_invalid(self):
        """测试无效移动"""
        self.game_state.initialize_board(3, 'NUMBERS')
        empty_row, empty_col = self.game_state.empty_pos
        
        # 尝试移动不相邻的方块
        target_row, target_col = (empty_row + 2) % 3, (empty_col + 2) % 3
        result = self.game_state.move_tile(target_row, target_col)
        self.assertFalse(result)
        self.assertEqual(self.game_state.stats.moves, 0)


class TestLeaderboard(unittest.TestCase):
    """排行榜测试"""
    
    def setUp(self):
        """测试前准备"""
        self.test_file = "test_leaderboard.json"
        self.leaderboard = Leaderboard(self.test_file)
        self.leaderboard.entries = []  # 清空用于测试
    
    def setUp(self):
        """测试前准备"""
        # 使用临时文件避免影响实际数据
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.leaderboard = Leaderboard(self.temp_file.name)

    def tearDown(self):
        """测试后清理"""
        if hasattr(self, 'temp_file') and os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_add_entry(self):
        """测试添加排行榜条目"""
        entry = LeaderboardEntry(
            player_name="测试玩家",
            time_seconds=120,
            moves=50,
            difficulty="EASY",
            game_mode="NUMBERS",
            timestamp=1000.0
        )
        
        self.leaderboard.add_entry(entry)
        self.assertEqual(len(self.leaderboard.entries), 1)
        self.assertEqual(self.leaderboard.entries[0].player_name, "测试玩家")
    
    def test_sorting(self):
        """测试排行榜排序"""
        # 添加多个条目
        entries = [
            LeaderboardEntry("玩家1", 120, 50, "EASY", "NUMBERS", 1000.0),
            LeaderboardEntry("玩家2", 90, 40, "EASY", "NUMBERS", 1001.0),
            LeaderboardEntry("玩家3", 150, 60, "EASY", "NUMBERS", 1002.0)
        ]
        
        for entry in entries:
            self.leaderboard.add_entry(entry)
        
        # 检查排序是否正确（按时间升序）
        self.assertEqual(len(self.leaderboard.entries), 3)
        self.assertEqual(self.leaderboard.entries[0].player_name, "玩家2")  # 最快的排第一
        self.assertEqual(self.leaderboard.entries[1].player_name, "玩家1")
        self.assertEqual(self.leaderboard.entries[2].player_name, "玩家3")
    
    def test_clear_leaderboard(self):
        """测试清空排行榜"""
        # 添加一些条目
        entries = [
            LeaderboardEntry("玩家1", 120, 50, "EASY", "NUMBERS", 1000.0),
            LeaderboardEntry("玩家2", 90, 40, "EASY", "NUMBERS", 1001.0)
        ]
        
        for entry in entries:
            self.leaderboard.add_entry(entry)
        
        # 确认有条目
        self.assertEqual(len(self.leaderboard.entries), 2)
        
        # 清空排行榜
        self.leaderboard.clear_leaderboard()
        
        # 确认已清空
        self.assertEqual(len(self.leaderboard.entries), 0)
        # 确认文件也被清空
        self.leaderboard.load_leaderboard()
        self.assertEqual(len(self.leaderboard.entries), 0)


class TestUtils(unittest.TestCase):
    """工具函数测试"""
    
    def test_difficulty_levels(self):
        """测试难度级别配置（仅测试现有难度）"""
        # 测试现有的难度级别
        self.assertIn('EASY', DIFFICULTY_LEVELS)
        self.assertIn('MEDIUM', DIFFICULTY_LEVELS)
        self.assertNotIn('HARD', DIFFICULTY_LEVELS)  # HARD已被删除
        
        self.assertEqual(DIFFICULTY_LEVELS['EASY']['size'], 3)
        self.assertEqual(DIFFICULTY_LEVELS['MEDIUM']['size'], 4)


def run_tests():
    """运行所有测试"""
    print("开始运行华容道游戏测试...")
    print("=" * 50)
    
    # 创建测试加载器
    loader = unittest.TestLoader()
    
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试用例
    test_suite.addTests(loader.loadTestsFromTestCase(TestGameState))
    test_suite.addTests(loader.loadTestsFromTestCase(TestLeaderboard))
    test_suite.addTests(loader.loadTestsFromTestCase(TestUtils))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 输出结果
    print("=" * 50)
    print(f"测试完成!")
    print(f"运行测试数: {result.testsRun}")
    print(f"失败数: {len(result.failures)}")
    print(f"错误数: {len(result.errors)}")
    
    if result.failures:
        print("\n失败详情:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\n错误详情:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)