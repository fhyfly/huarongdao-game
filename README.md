# 华容道游戏 Huarongdao Game

一款经典的益智游戏，使用Python和Pygame开发。支持数字拼图和图片拼图两种模式，具有排行榜功能和中英文界面切换。

A classic puzzle game developed with Python and Pygame. Supports both number puzzle and image puzzle modes, featuring leaderboard functionality and Chinese/English interface switching.

## 🎮 游戏特色 Game Features

- **双模式游戏** - 数字拼图和图片拼图
- **难度选择** - 简单和中等两个难度级别  
- **智能计时** - 精确到0.01秒的成绩记录
- **排行榜系统** - 记录最佳成绩，支持清空确认和难度筛选
- **多语言支持** - 中英文界面实时切换
- **手机适配** - 480×800竖屏分辨率优化
- **纯鼠标操作** - 简洁直观的交互体验
- **图片自定义** - 支持随机选择或指定图片进行拼图

## 🚀 快速开始 Quick Start

### 系统要求 System Requirements
- Python 3.7 或更高版本
- Windows/Mac/Linux 操作系统
- 50MB 硬盘空间

### 安装步骤 Installation Steps

1. **克隆或下载项目**
   ```
   git clone https://github.com/yourusername/huarongdao-game.git
   cd huarongdao-game
   ```

2. **安装依赖**
   ```
   pip install pygame==2.5.2
   ```

3. **启动游戏**
   ```
   python huarongdao_game/main.py
   ```

## 🎯 游戏玩法 Game Play

### 基本规则 Basic Rules
- 点击相邻的数字/图片块移动到空白位置
- 将所有块按顺序排列完成拼图
- 目标：用最少的步数和最短的时间完成游戏

### 操作说明 Controls
- **鼠标点击** - 选择要移动的方块
- **语言切换** - 点击界面右上角的语言按钮或按 Alt+L
- **排行榜清空** - 点击清空按钮后需要二次确认
- **图片选择** - 图片模式下可随机选择或指定特定图片

### 游戏模式 Game Modes
1. **数字模式** - 传统的数字拼图
2. **图片模式** - 使用自定义图片的拼图游戏
   - 支持随机图片选择
   - 支持指定图片选择
   - 5张精美图片资源可供选择

## 🏆 排行榜 Leaderboard

游戏会自动记录您的最佳成绩：

### 核心功能 Core Features
- 按完成时间排序（精确到0.01秒）
- 显示玩家姓名、时间和步数
- 支持按难度和游戏模式分类统计
- 最多保存30条记录
- 清空操作需要二次确认保护

### 高级功能 Advanced Features
- **难度筛选** - 可在排行榜界面切换查看简单/中等难度的最佳成绩
- **模式区分** - 清晰标识数字模式和图片模式的成绩
- **实时更新** - 筛选条件变化时立即刷新显示

## 🌍 多语言支持 Multi-language Support

游戏支持中英文界面切换：
- 游戏过程中随时切换语言
- 所有文本即时更新
- 保持游戏状态不受影响

快捷键：`Alt + L`

## 📱 手机适配 Mobile Adaptation

专为手机竖屏优化：
- 480×800分辨率设计
- 大按钮适合触控操作
- 简洁直观的界面布局

## 🛠️ 开发说明 Development Guide

### 项目结构 Project Structure
```
huarongdao-game/
├── huarongdao_game/    # 游戏源代码目录
│   ├── __init__.py
│   ├── main.py         # 主程序入口
│   ├── controllers.py  # 游戏控制器
│   ├── models.py       # 数据模型
│   ├── renderer.py     # 渲染引擎
│   └── config.py       # 配置文件
├── tests/              # 测试目录
│   └── test_game.py    # 单元测试
├── docs/               # 文档目录
│   ├── README.md       # 详细文档
│   ├── CHANGELOG.md    # 更新日志
│   └── ...             # 其他文档
├── assets/             # 资源目录
│   ├── images/         # 图片资源
│   └── data/           # 数据文件
├── requirements.txt    # 依赖列表
└── .gitignore          # Git忽略文件
```

### 运行测试 Running Tests
```bash
python tests/test_game.py -v
```

### 自定义图片 Custom Images
将您的图片放入 `assets/images/` 目录，游戏会随机选择使用。

## 📋 系统要求 Requirements

- **Python**: 3.7+
- **Pygame**: 2.5.2
- **操作系统**: Windows 10+, macOS 10.14+, Linux
- **内存**: 100MB RAM
- **存储**: 50MB 硬盘空间

## 🔧 故障排除 Troubleshooting

### 常见问题 Common Issues

**Q: 中文字体显示为方块**
A: 游戏会自动检测系统字体，如果仍有问题请确保系统安装了中文字体。

**Q: 图片模式无法加载图片**
A: 检查 `assets/images/` 目录是否存在支持的图片格式(.png, .jpg, .jpeg)。

**Q: 排行榜文件损坏**
A: 删除 `assets/data/leaderboard.json` 文件，游戏会自动创建新的空排行榜。

**Q: 游戏启动后立即退出**
A: 检查是否有未处理的异常，查看控制台输出的错误信息。

### 调试模式 Debug Mode
运行测试可以验证游戏各功能是否正常：
```bash
python tests/test_game.py
```

## 📄 许可证 License

MIT License - 详见 LICENSE 文件

## 🙏 致谢 Acknowledgements

- Pygame 社区提供的强大游戏开发框架
- 所有参与测试和提供反馈的用户

## 📞 联系方式 Contact

如有问题或建议，请提交 Issue 或联系开发者。

---

**享受游戏！Have fun!** 🎮