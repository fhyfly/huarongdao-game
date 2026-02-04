# 华容道游戏开发指南

## 🛠️ 开发环境设置

### 基础要求
- Python 3.7 或更高版本
- 代码编辑器（推荐 VS Code 或 PyCharm）
- Git 版本控制

### 依赖安装
```bash
pip install pygame==2.5.2
```

或者批量安装：
```bash
pip install -r requirements.txt
```

## 🏗️ 项目架构

### MVC 架构设计
```
Controllers (控制器层)
    ├── GameController - 游戏主控制器
    └── 事件处理和状态管理

Models (模型层)  
    ├── GameState - 游戏状态
    ├── Leaderboard - 排行榜数据
    └── GameStats - 统计信息

Views/Renderer (视图层)
    └── GameRenderer - 渲染引擎
```

### 核心组件说明

#### Controllers 控制器
- **GameController**: 处理用户输入、游戏逻辑和状态转换
- **GameScreen**: 枚举类型，管理不同的游戏界面状态

#### Models 模型
- **GameState**: 存储当前游戏状态（棋盘、难度、模式等）
- **GameStats**: 管理游戏统计数据（时间、步数等）
- **Leaderboard**: 处理排行榜数据的存储和检索

#### Renderer 渲染器
- **GameRenderer**: 负责所有界面绘制工作
- 支持多种分辨率适配
- 包含字体管理和图片处理

## 🔧 开发流程

### 1. 环境准备
```bash
# 克隆项目
git clone <repository-url>
cd huarongdao-game

# 安装依赖
pip install -r requirements.txt
```

### 2. 代码开发
```bash
# 运行游戏
python main.py

# 运行测试
python test_game.py
```

### 3. 调试技巧
- 使用 `print()` 输出调试信息（注意及时清理）
- 查看终端输出了解游戏状态
- 利用测试用例验证功能正确性

## 📊 代码规范

### 命名约定
- 类名：PascalCase (`GameController`)
- 函数/方法：snake_case (`handle_event`)
- 常量：UPPER_CASE (`WINDOW_WIDTH`)
- 私有成员：下划线前缀 (`_init_fonts`)

### 注释规范
```python
def handle_main_menu(self, event, renderer) -> bool:
    """
    处理主菜单事件（仅支持鼠标操作）
    
    Args:
        event: pygame事件对象
        renderer: 渲染器实例
        
    Returns:
        bool: 是否继续运行游戏
    """
```

### 类型注解
```python
from typing import Optional, List, Tuple

def draw_leaderboard(self, leaderboard_entries: List[LeaderboardEntry]) -> Tuple[pygame.Rect, pygame.Rect]:
    """绘制排行榜界面"""
```

## 🧪 测试策略

### 单元测试
```bash
python test_game.py
```

测试覆盖：
- ✅ 游戏状态初始化
- ✅ 方块移动逻辑
- ✅ 可解性算法
- ✅ 排行榜功能
- ✅ 数据持久化
- ✅ 界面交互流程

### 手动测试清单
- [ ] 数字模式游戏流程
- [ ] 图片模式游戏流程
- [ ] 难度切换功能
- [ ] 语言切换功能
- [ ] 排行榜显示和筛选
- [ ] 排行榜清空确认
- [ ] 图片选择流程
- [ ] 计时器准确性
- [ ] 界面适配性

## 🎨 界面开发

### 颜色主题管理
```python
# config.py
COLORS = {
    'PRIMARY': (70, 130, 180),
    'SECONDARY': (60, 179, 113),
    'BACKGROUND': (245, 245, 245),
    # ... 更多颜色定义
}
```

### 字体系统
- 自动检测系统中文字体
- 支持字体降级机制
- 多尺寸字体管理

### 响应式设计
- 基于480×800竖屏优化
- 相对位置计算
- 弹性布局适配

## 🔐 最佳实践

### 性能优化
- 图片资源预加载
- 字体对象复用
- 避免重复计算

### 内存管理
- 及时清理不用的对象
- 图片缓存管理
- 防止内存泄漏

### 错误处理
```python
try:
    # 可能出错的代码
    font = pygame.font.Font(font_path, size)
except pygame.error as e:
    # 降级处理
    print(f"字体加载失败: {e}")
    font = pygame.font.Font(None, size)
```

### 用户体验规范
- **纯鼠标操作**: 避免混合键盘鼠标操作，保持交互一致性
- **流程自然性**: 界面跳转应该符合用户直觉和操作习惯
- **信息简洁性**: 界面显示应突出重点，避免信息冗余
- **反馈及时性**: 用户操作应有明确的视觉或状态反馈

### 安全性考虑
- **数据保护**: 敏感操作（如清空数据）必须增加确认步骤
- **状态验证**: 跨界面状态传递需要完整性校验
- **异常处理**: 关键功能要有完善的错误恢复机制

## 🚀 发布准备

### 版本管理
遵循语义化版本号：`主版本.次版本.修订号`

### 打包注意事项
- 确保所有资源文件路径正确
- 测试不同操作系统的兼容性
- 验证依赖包版本一致性

### 文档更新
- 更新 CHANGELOG.md 记录所有变更
- 完善 README.md 反映最新功能
- 补充用户手册和技术文档
- 更新测试用例和验证清单

## 🤝 贡献指南

### Pull Request 流程
1. Fork 项目仓库
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

### 代码审查要点
- 功能正确性
- 代码质量
- 性能影响
- 兼容性考虑
- 用户体验一致性

## 📚 学习资源

### Pygame 官方文档
https://www.pygame.org/docs/

### Python 最佳实践
- PEP 8 代码风格指南
- 类型注解使用
- 异常处理模式

### 游戏开发参考
- MVC 架构模式
- 状态机设计
- 事件驱动编程

### UX/UI 设计原则
- 简洁性原则：界面元素应简洁明了
- 一致性原则：操作逻辑和视觉风格保持统一
- 可访问性原则：考虑不同用户的使用需求
- 反馈原则：及时给予用户操作结果反馈