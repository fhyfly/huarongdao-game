# 项目结构说明

## 📁 目录结构

```
huarongdao-game/
├── main.py                 # 项目主入口文件
├── setup.py               # Python包配置文件
├── requirements.txt       # 项目依赖列表
├── start-game.bat         # Windows一键启动脚本
├── README.md              # 项目主说明文档
├── .gitignore            # Git忽略文件配置
├── PROJECT_STRUCTURE.md   # 本文件 - 项目结构说明
│
├── src/                   # 源代码目录
│   ├── __init__.py       # Python包标识文件
│   ├── main.py           # 游戏主程序逻辑
│   ├── controllers.py    # 游戏控制器（事件处理）
│   ├── models.py         # 数据模型（游戏状态、排行榜等）
│   ├── renderer.py       # 渲染引擎（界面绘制）
│   └── config.py         # 配置文件（常量、设置等）
│
├── tests/                 # 测试目录
│   ├── __init__.py       # 测试包标识文件
│   └── test_game.py      # 游戏功能测试文件
│
├── docs/                  # 文档目录
│   ├── README.md         # 详细使用说明
│   ├── CHANGELOG.md      # 版本更新日志
│   ├── DEVELOPMENT.md    # 开发指南
│   ├── QUICK_START.md    # 快速开始指南
│   ├── SUMMARY.md        # 功能摘要
│   └── PROJECT_SUMMARY.md # 项目概要
│
└── assets/                # 资源目录
    ├── images/           # 图片资源文件
    │   ├── img-*.jpeg    # 默认游戏图片
    │   └── custom/       # 用户自定义图片目录
    ├── fonts/            # 字体文件目录
    └── data/             # 数据文件目录
        └── leaderboard.json # 排行榜数据文件
```

## 📂 各目录说明

### src/ - 源代码目录
存放所有Python源代码文件，采用标准的Python包结构。

**主要文件：**
- `main.py`: 游戏主循环和程序入口
- `controllers.py`: 游戏逻辑控制器，处理用户输入和游戏状态
- `models.py`: 数据模型，包含游戏状态、排行榜等核心数据结构
- `renderer.py`: 渲染引擎，负责所有界面绘制工作
- `config.py`: 配置文件，包含常量定义、路径配置等

### tests/ - 测试目录
存放单元测试和集成测试文件。

**测试文件：**
- `test_game.py`: 包含游戏核心功能的测试用例

### docs/ - 文档目录
存放项目相关的所有文档文件。

**文档文件：**
- `README.md`: 项目详细介绍和使用说明
- `CHANGELOG.md`: 版本更新历史记录
- `DEVELOPMENT.md`: 开发者指南和技术文档
- `QUICK_START.md`: 快速入门指南
- `SUMMARY.md`: 功能特性摘要
- `PROJECT_SUMMARY.md`: 项目总体概要

### assets/ - 资源目录
存放游戏运行所需的所有静态资源文件。

**子目录：**
- `images/`: 图片资源，包括默认游戏图片和用户自定义图片
- `fonts/`: 字体文件，用于界面文本渲染
- `data/`: 数据文件，如排行榜记录等持久化数据

## 🔄 数据流向

```
用户输入 → controllers.py → models.py → renderer.py → 显示输出
    ↑                                            ↓
    ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

## 🎯 设计原则

1. **MVC架构**: 严格分离模型(Model)、视图(View)、控制器(Controller)
2. **单一职责**: 每个模块只负责特定的功能
3. **配置集中**: 所有配置参数统一在config.py中管理
4. **资源隔离**: 静态资源与代码分离，便于维护
5. **测试覆盖**: 核心功能都有对应的测试用例

## 🚀 运行方式

### 开发模式
```bash
python main.py
```

### 测试模式
```bash
python tests/test_game.py
# 或
python -m unittest tests/test_game.py
```

### 生产模式
```bash
# Windows
start-game.bat

# 其他平台
python main.py
```

## 📦 打包分发

项目支持标准的Python包格式，可通过setup.py进行安装：

```bash
pip install .
# 或
python setup.py install
```

## 🔧 开发环境

建议使用虚拟环境进行开发：

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```