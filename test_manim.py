"""
Simple Manim test scene to verify installation
简单的 Manim 测试场景，用于验证安装
"""
from manim import *

class TestScene(Scene):
    def construct(self):
        # Create a simple text animation
        # 创建一个简单的文本动画
        text = Text("Manim is working!", font_size=48)
        self.play(Write(text))
        self.wait(1)
        self.play(FadeOut(text))
