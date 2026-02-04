# -*- coding: utf-8 -*-
"""
华容道游戏主程序
游戏入口点和主循环
"""

import pygame
import sys
from config import *
from renderer import GameRenderer
from controllers import GameController


def main():
    """主函数"""
    try:
        renderer = GameRenderer()
        controller = GameController()
        
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
            
            # 处理游戏事件
            if not controller.handle_events(events, renderer):  # 修复方法名
                running = False
            
            # 渲染当前屏幕
            controller.render_current_screen(renderer)
            
            # 控制帧率
            renderer.clock.tick(FPS)
            
    except Exception as e:
        print(f"游戏运行出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()