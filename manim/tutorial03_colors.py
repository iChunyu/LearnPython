"""
本文件用来练习颜色相关的表示和相关方法

参考资料： https://www.bilibili.com/video/BV1vZ4y1x7hT
XiaoCY 2020-12-06
"""

#%% 初始化
from manimlib.imports import *

"""
颜色的基本表示
    RGB模式：字符串或数组，如 "#83B31F", np.array([152,252,54])
    manim 默认定义了颜色常量，效果参考： https://elteoremadebeethoven.github.io/manim_3feb_docs.github.io/html/_static/colors/colors.html
    默认颜色中，结尾为 _C 的可以省略，即 BLUE_C = BLUE
"""

#%% 颜色表示方法相互转换
""" 
颜色的数据类型
    rgb 0~1 小数
    int_rgb 0~255 整数
    hex 字符串
    Color 整合以上表示的 manim 类
常用函数包括
    hex_to_rgb
    rgb_to_hex
    color_to_rgb
    rgb_to_color
    color_to_int_rgb
其他说明
    hex 和 Color 之间没有必要转换
    hex 和 Color 都能放入 set_color 方法
"""

class try_colortocolor(Scene):
    def construct(self):
        hex_color = "#FB7299"
        rgb_color = hex_to_rgb(hex_color)
        int_rbg_color = color_to_int_rgb(hex_color)

        hex_text = Text('hex: "{0}"'.format(hex_color),
            font = 'Noto Sans CJK SC')
        rgb_text = Text('rbg: [{0:.2f}, {1:.2f}, {2:.2f}]'.format(*rgb_color),
            font = 'Noto Sans CJK SC')
        int_rgb_text = Text('int_rgb: [{0:d}, {1:d}, {2:d}]'.format(*int_rbg_color),
            font = 'Noto Sans CJK SC')
        group = VGroup(hex_text, rgb_text, int_rgb_text)
        group.arrange(DOWN).set_color(hex_color)

        for k in range(3):
            self.play(FadeIn(group[k]))
            self.wait(0.3)
        self.wait(2)

#%% 颜色的运算函数
"""
常用运算函数
    invet_color(color) 
        颜色反色，输入 hex 或 Color，输出 Color
    interpolate_color(color1, color2, alpha)
        在两个颜色之间以比例 alpha 插值
        伪代码：color1 * alpha + color2 * (1-alpha)
    average_color(*colors)
        传入多个颜色，返回平均颜色
    color_gradient(reference_colors, length_of_output)
        传入参考颜色列表和需要的长度 n
        输出长度为 n 的颜色梯度序列
    random_color()
        随即返回一个预定义的颜色
"""

class try_colorfcn(Scene):
    def construct(self):
        coin = SVGMobject("coin.svg",
            color = BLUE)
        
        self.play(FadeIn(coin))
        self.wait(1)

        self.play(coin.set_color,
            invert_color(BLUE)
        )
        self.wait(1)

        self.play(coin.set_color,
            interpolate_color(RED, GREEN, 0.3)
        )
        self.wait(1)

        self.play(coin.set_color,
            average_color(RED,GREEN,BLUE)
        )
        self.wait(1)

        for k in range(50):
            self.play(
                coin.set_color,
                random_color(),
                run_time = 0.1
            )
        self.wait(1)

#%% 物体颜色的设置
"""
这里仅讨论 VMobject 及其子类的上色方法
相关属性有
    stroke_color, stroke_opacity
    fill_color, fill_opacity
    background_stroke_color, background_stroke_opacity
相关方法有
    set_color(color)
        直接给定颜色将同时设置 stroke_color 和 fill_color，opacity 保持不变
    set_stroke(color=None, width=None, opacity=None)
        改变颜色、线宽、不透明度
    set_fill(color=None, opacity=None)
        改变颜色、不透明度
    set_background_stroke(color=None, width=None, opacity=None)
        设置背景的颜色、线宽、不透明度
"""

class try_setcolor(Scene):
    def construct(self):
        coin = SVGMobject("coin.svg",
            stroke_color = BLUE,
            fill_color = RED)
        
        self.play(FadeIn(coin))
        self.wait(1)

        self.play(coin.set_stroke,
            {"color":PINK,
            "width":2,
            "opacity":0.7}
        )
        self.wait(1)

        self.play(coin.set_fill,
            {"color":GREEN,
            "opacity":0.4
            }
        )
        self.wait(1)

#%% 子物体上颜色
"""
给 VGroup 的所有子物体上颜色
    set_color(color)
        将所有子物体上同一颜色
    set_color_by_gradient(×colors)
        从头到尾根据给定的参考颜色产生梯度并上色
    set_colors_by_radial_gradient(
        center = vg.get_center(),        # 默认为物体中心
        radius = 1,
        inner_color = BLUE,
        outer_color = RED
    )
        根据半径上梯度颜色，给定中心点和内外颜色，中间自动插值
"""

class try_colorgroup(Scene):
    def construct(self):
        coin = SVGMobject("coin.svg",
            color = BLUE,
            height = 1)
        row = VGroup(coin,coin.copy(),coin.copy())
        row.arrange(RIGHT)
        group = VGroup(row,row.copy(),row.copy())
        group.arrange(DOWN)
        group.move_to(ORIGIN)

        self.play(FadeIn(group))
        self.wait(1)

        self.play(group.set_color, RED_B)
        self.wait(1)

        self.play(group.set_color_by_gradient,
            [RED,GREEN,BLUE]
        )
        self.wait(1)

        self.play(group.set_colors_by_radial_gradient,
            {"radius":1.5,
            "inner_color": BLUE,
            "outer_color": RED
            }
        )
        self.wait(1)

#%% 光泽与渐变颜色
"""
set_sheen(factor, direction=None)
    给物体增加光泽，给定尺度（0为没有光泽变化）和光泽变化方向
set_sheen_direction(direction)
    仅改变光泽方向
set_color([BLUE, RED, GREEN])
    可以通过传入列表来设置渐变色，并结合 set_sheen_directio 改变方向
"""

class try_sheen(Scene):
    def construct(self):
        coin = SVGMobject("coin.svg",
            color = BLUE)
        
        self.play(FadeIn(coin))
        self.wait(1)

        self.play(coin.set_sheen,
            {"factor":3,
            "direction":RIGHT}
        )
        self.wait(1)

        self.play(coin.set_sheen_direction,DOWN)
        self.wait(1)

        self.play(coin.set_color,
            [RED,GREEN,BLUE]
        )
        self.wait(1)