"""
Complex Manim Example - 复杂 Manim 示例
This example demonstrates multiple Manim features:
这个示例展示了多个 Manim 功能：
- Mathematical formulas (数学公式)
- 2D shapes and transformations (2D 图形和变换)
- Animations and transitions (动画和过渡)
- Color gradients (颜色渐变)
- Grouping and positioning (分组和定位)
"""

from manim import *
import numpy as np

class ComplexExample(Scene):
    def construct(self):
        # 1. Title with gradient color
        # 标题带渐变色
        title = Text(
            "Complex Manim Example",
            font_size=60,
            gradient=(BLUE, PURPLE, RED)
        )
        title.to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait(1)
        
        # 2. Mathematical formula with LaTeX
        # 数学公式（LaTeX）
        formula = MathTex(
            r"e^{i\pi} + 1 = 0",
            font_size=72
        )
        formula.next_to(title, DOWN, buff=1)
        self.play(Write(formula), run_time=2)
        self.wait(1)
        
        # 3. Create a circle that transforms
        # 创建一个会变换的圆
        circle = Circle(radius=1.5, color=BLUE)
        circle.shift(LEFT * 3)
        
        # 4. Create a square
        # 创建一个正方形
        square = Square(side_length=2, color=GREEN)
        square.shift(RIGHT * 3)
        
        # 5. Animate shapes appearing
        # 动画显示图形
        self.play(
            Create(circle),
            Create(square),
            run_time=2
        )
        self.wait(0.5)
        
        # 6. Transform circle to square
        # 将圆变换为正方形
        self.play(
            Transform(circle, square.copy()),
            run_time=2
        )
        self.wait(0.5)
        
        # 7. Create a group of shapes
        # 创建一组图形
        shapes = VGroup(
            Circle(radius=0.5, color=RED),
            Square(side_length=1, color=YELLOW),
            Triangle(color=ORANGE)
        )
        shapes.arrange(RIGHT, buff=0.5)
        shapes.shift(DOWN * 2)
        
        self.play(
            FadeIn(shapes),
            run_time=1.5
        )
        self.wait(0.5)
        
        # 8. Rotate the group
        # 旋转组
        self.play(
            Rotate(shapes, PI, about_point=shapes.get_center()),
            run_time=2
        )
        self.wait(0.5)
        
        # 9. Create a number line
        # 创建数轴
        number_line = NumberLine(
            x_range=[-3, 3, 1],
            length=6,
            include_numbers=True,
            font_size=24
        )
        number_line.shift(DOWN * 3.5)
        
        self.play(Create(number_line), run_time=1.5)
        self.wait(0.5)
        
        # 10. Animate a dot moving on the number line
        # 动画显示点在数轴上移动
        dot = Dot(color=RED)
        dot.move_to(number_line.n2p(-2))
        
        self.play(FadeIn(dot), run_time=0.5)
        self.play(
            dot.animate.move_to(number_line.n2p(2)),
            run_time=3,
            rate_func=there_and_back
        )
        
        # 11. Create a function graph
        # 创建函数图像
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=3,
            axis_config={"color": BLUE},
            tips=False,
        )
        axes.shift(UP * 0.5 + RIGHT * 0.5)
        
        # Sine wave
        # 正弦波
        graph = axes.plot(
            lambda x: np.sin(x),
            color=YELLOW,
            x_range=[-3, 3]
        )
        
        self.play(
            Create(axes),
            Create(graph),
            run_time=2
        )
        self.wait(1)
        
        # 12. Final fade out
        # 最终淡出
        self.play(
            FadeOut(VGroup(title, formula, circle, square, shapes, number_line, dot, axes, graph)),
            run_time=2
        )
        self.wait(0.5)
        
        # 13. DIC JUMPING End Credits - 片尾动画
        # Clear everything first
        # 先清除所有内容
        self.clear()
        
        # Create "DIC JUMPING" text
        # 创建"DIC JUMPING"文字
        dic_text = Text("DIC", font_size=80, weight=BOLD, color=BLUE)
        jumping_text = Text("JUMPING", font_size=80, weight=BOLD, color=ORANGE)
        
        # Arrange the text
        # 排列文字
        end_credits = VGroup(dic_text, jumping_text)
        end_credits.arrange(RIGHT, buff=0.5)
        end_credits.move_to(ORIGIN)
        
        # Create individual letters for jumping animation
        # 为跳跃动画创建单独的字母
        dic_letters = VGroup(*[Text(char, font_size=80, weight=BOLD, color=BLUE) for char in "DIC"])
        jumping_letters = VGroup(*[Text(char, font_size=80, weight=BOLD, color=ORANGE) for char in "JUMPING"])
        
        # Arrange letters
        # 排列字母
        dic_letters.arrange(RIGHT, buff=0.2)
        jumping_letters.arrange(RIGHT, buff=0.2)
        
        # Position the letter groups
        # 定位字母组
        all_letters = VGroup(dic_letters, jumping_letters)
        all_letters.arrange(RIGHT, buff=0.5)
        all_letters.move_to(ORIGIN)
        
        # Animate letters appearing one by one
        # 逐个显示字母
        for letter in dic_letters:
            letter.shift(UP * 2)  # Start above
            self.play(
                letter.animate.shift(DOWN * 2),
                run_time=0.3
            )
        
        self.wait(0.2)
        
        # Animate "JUMPING" letters
        # 动画显示"JUMPING"字母
        for letter in jumping_letters:
            letter.shift(UP * 2)  # Start above
            self.play(
                letter.animate.shift(DOWN * 2),
                run_time=0.3
            )
        
        self.wait(0.5)
        
        # Make all letters jump together
        # 让所有字母一起跳跃
        for _ in range(3):
            self.play(
                all_letters.animate.shift(UP * 0.5),
                run_time=0.3,
                rate_func=there_and_back
            )
            self.wait(0.2)
        
        # Add a subtitle
        # 添加副标题
        subtitle = Text(
            "VisualKiwi Project",
            font_size=36,
            color=GRAY
        )
        subtitle.next_to(all_letters, DOWN, buff=1)
        
        self.play(FadeIn(subtitle), run_time=1)
        self.wait(1)
        
        # Final effect: Scale and fade
        # 最终效果：缩放和淡出
        self.play(
            all_letters.animate.scale(1.2),
            subtitle.animate.scale(1.1),
            run_time=1
        )
        self.wait(0.5)
        
        # Add sparkle effect with dots
        # 添加闪烁效果（用点）
        sparkles = VGroup(*[
            Dot(radius=0.1, color=YELLOW).move_to(
                all_letters.get_center() + 
                np.array([np.cos(angle), np.sin(angle), 0]) * 2
            )
            for angle in np.linspace(0, 2*PI, 12, endpoint=False)
        ])
        
        self.play(
            *[FadeIn(sparkle, scale=2) for sparkle in sparkles],
            run_time=0.8
        )
        self.wait(0.5)
        
        # Final fade out
        # 最终淡出
        self.play(
            FadeOut(VGroup(all_letters, subtitle, sparkles)),
            run_time=2
        )
        self.wait(0.5)
