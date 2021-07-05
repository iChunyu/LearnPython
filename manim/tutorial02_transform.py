"""
本文件用以练习 manim 常见的物体变换方法：
    shift
    move_to
    scale
    rotate
    flip
    stretch
    to_corner, to_edge
    align_to
    next_to
    set_width, set_height
参考资料： https://www.bilibili.com/video/BV1p54y197cC
XiaoCY 2020-12-03
"""

#%% 初始化
from manimlib.imports import *

"""
基础知识：
    1. 三维 ndarray 数组表示一个点的坐标，平面情况下第三维为0；
    2. 单位长度取决于 consatants.py/FRAME_HEIGHT，其值默认为8，即整个画面高度为8个单位；
    3. 平面情形画面中心为坐标原点，右、上分别为x、y轴正向；
    4. 几个常用的单位方向
        RIGHT = np.array([1,0,0])
        LEFT = np.array([-1,0,0])
        UP = np.array([0,1,0])
        DOWN = np.array([0,-1,0])
        同理，对角线方向单位向量： UR, UL, DR, DL 
        四个方向边界： TOP, BOTTOM, RIGHT_SIDE, LEFT_SIDE

注意:
    1. 这里主要讨论物体的变换，不包括变换过程的动画；
    2. 如果要生成变换的动画，就需要将变化放在 play 中，并以字典的形式给出参数，详见源码；
    3. play 内的动画是物体变换前后的转换，而不是变换对应的动画，如 rotate。
"""

#%% shift
"""
shift(*vectors)
根据传入的向量将物体进行移动
当传入多个向量时，会先对向量相加，然后再进行移动
"""

class try_shift(Scene):
    def construct(self):
        coin = SVGMobject(
            "coin.svg",
            color = BLUE,
            stroke_width = 0.00
        )
        smirk = ImageMobject("smirk.png")
        
        coin.shift(5*LEFT)
        self.play(FadeIn(coin))
        self.play(coin.shift,10*RIGHT,run_time=3)
        # 下面这一行表示 shift 是基于物体当前位置进行移动的
        self.play(coin.shift,2*UP)
        smirk.shift(5*RIGHT,2*UP)
        self.remove(coin)
        self.add(smirk)
        self.wait(1)
        self.play(FadeOutAndShiftDown(smirk), run_time=2)

#%% move_to
"""
move_to(point_or_mobject, aligned_edge=array([0.0, 0.0, 0.0]), coor_mask=array([1, 1, 1]))
根据目标位置对物体进行移动
传入的第一个参数为移动的目标位置，可以是坐标或者物品
可选参数包括：
    对齐方式 aligned_edge： 默认中心对齐 (ORIGIN)
    移动维度 coor_mask： 三维 ndarray，分别表示在三个方向位移的倍数
        coor_mask 的使用意味着物体并非一定移动到目标位置
        而是根据当前位置和目标位置之间的位移进行缩放
"""

class try_moveto(Scene):
    def construct(self):
        coin = SVGMobject('coin.svg',color = BLUE)
        coin.shift(LEFT*5)

        coin.move_to(UP*2,aligned_edge = RIGHT)
        self.play(ShowCreation(coin))
        self.play(coin.move_to,DOWN*2)
        self.play(coin.move_to,
            {"point_or_mobject":RIGHT*2,
            "coor_mask":np.array([1,2,0])}
        )
        self.wait(1)

#%% scale
"""
scale(scale_factor, **kwargs)
根据传入的第一个参数对物体进行缩放
可选参数主要是缩放基准：
    沿着边缘缩放 about_edge = UP/DOWN/LEFT/RIGHT
    沿着某点缩放 about_point = np.array([*,*,*])
"""

class try_scale(Scene):
    def construct(self):
        coin = SVGMobject('coin.svg',color = BLUE, height = 1)

        self.play(ShowCreation(coin))
        self.play(coin.scale,2)
        self.play(coin.scale,
            {"scale_factor": 0.5,
            "about_edge": DOWN
            }
        )
        self.play(coin.scale,
            {"scale_factor": 2,
            "about_point": LEFT*2+DOWN*3}
        )

#%% rotate
"""
rotate(angle, axis=OUT, **kwargs)
传入的第一个参数为旋转角度（默认为弧度，可用 DEGREES 变量转化）
传入的第二个参数为旋转轴（主要是方向），符合右手定则
可选参数为旋转点 about_point = np.array([*,*,*])，默认为物体自身中心

特别地，当旋转点为原点时，还可以使用 rotate_about_origin(angle, axis=OUT)
"""

class try_rotate(Scene):
    def construct(self):
        coin1 = SVGMobject('coin.svg',color = BLUE)
        coin2 = SVGMobject('coin.svg',color = RED)

        coin1.rotate(PI, axis = OUT)
        self.play(FadeIn(coin1))
        self.play(coin1.rotate,
            {"angle": 180*DEGREES,
            "axis": IN}
        )
        self.wait(1)
        self.remove(coin1)

        # 上面的动画与下面的动画相同
        # 说明放在 play 内的变换实际上是先进行变换
        # 根据变换前后的物体依据 Transform 生成动画
        coin1.rotate(PI, axis = OUT)
        self.play(FadeIn(coin1))
        self.play(ReplacementTransform(coin1,coin2))
        self.wait(1)
        self.remove(coin2)

        # 下面这个例子进一步说明生成的动画不是传入的旋转
        coin = SVGMobject('coin.svg',color = BLUE)
        coin.shift(2*RIGHT)
        self.play(FadeIn(coin))
        self.play(coin.rotate,
            {"angle": 180*DEGREES,
            "axis": OUT,
            "about_point": ORIGIN}
        )
        self.wait(1)

        # 剧透：旋转动画可以使用 Rotating
        self.play(
            Rotating(
                coin,
                radians = PI,
                axis = OUT,
                about_point = ORIGIN
            )
        )
        self.wait(1)

#%% flip
"""
默认情况下，flip 方法将物体沿着其自身中心竖线左右翻转
可以给定关键字参数指定对称轴方向和位置
    对称轴方向 axis
    对称轴位置 about_point
flip 实际上是三维空间旋转得到的
"""

class try_flip(Scene):
    def construct(self):
        good1 = SVGMobject('good.svg',color=RED)

        good2 = SVGMobject('good.svg',color=BLUE)
        good2.shift(4*LEFT)
        good2.flip()

        good3 = SVGMobject('good.svg',color=GREEN)
        good3.shift(4*RIGHT)
        good3.flip(axis=UR)

        good4 = SVGMobject('good.svg',color=YELLOW)
        good4.shift(4*RIGHT)
        good4.flip(axis=UR,about_point=2*RIGHT)

        self.play(
            FadeIn(good1),
            FadeIn(good2),
            FadeIn(good3),
            FadeIn(good4)
        )
        self.wait(3)

#%% stretch
"""
stretch(factor, dim, **kwargs) 将原来的物体进行拉伸
    拉伸倍数 factor
    拉伸维度 dim： 0 -> x, 1 -> y, 2 -> z
可选参数：
    基准点 about_point = np.array([*,*,*])
    基准边缘 about_edge ，物体自己的边缘
"""

class try_stretch(Scene):
    def construct(self):
        mob = SVGMobject("favo.svg",color=BLUE)
        mob.stretch(2,0)
        
        self.play(FadeIn(mob))
        self.play(mob.stretch,
            {"factor":2,
            "dim":1,
            "about_edge":DOWN})
        self.wait(1)

#%% to_corner, to_edge
"""
to_corner(corner=array([- 1.0, - 1.0, 0.0]), buff=0.5)
to_edge(edge=array([- 1.0, 0.0, 0.0]), buff=0.5)
将物体分别与角落和边缘对齐，buff 为指定的间距
"""

class try_tocorner(Scene):
    def construct(self):
        good = SVGMobject("good.svg",color=RED_B,height=0.5)
        coin = SVGMobject("coin.svg",color=BLUE,height=0.5,stroke_width=0.1)
        favo = SVGMobject("favo.svg",color=YELLOW,height=0.5)

        good.to_corner()
        coin.to_corner(UL,buff=1)
        favo.to_edge(UP)

        self.play(
            FadeIn(good),
            FadeIn(coin),
            FadeIn(favo)
        )
        self.wait(1)
        self.play(coin.to_corner,DR)
        self.wait(1)

#%% align_to
"""
align_to(mobject_or_point, direction=array([0.0, 0.0, 0.0]), alignment_vect=array([0.0, 1.0, 0.0]))
    mobject_or_point 对齐的参考对象/参考点 
    direction 默认不做任何对齐，三维 ndarray，向不为 0 的维度对齐
    alignment_vect 【该参数似乎不常用】
"""

class try_alignto(Scene):
    def construct(self):
        good = SVGMobject("good.svg",color=RED_B,height=2)
        coin = SVGMobject("coin.svg",color=BLUE,height=0.5,stroke_width=0.1)

        good.move_to(RIGHT*2+UP)
        coin.move_to(2*LEFT+DOWN)

        self.play(FadeIn(good),FadeIn(coin))
        self.play(coin.align_to,
            {"mobject_or_point":good,
            "direction":RIGHT}
        )
        self.wait(1)
        self.play(coin.align_to,
            {"mobject_or_point":good,
            "direction":UL}
        )
        self.wait(1)

#%% next_to
"""
 next_to(mobject_or_point, 
    direction=array([1.0, 0.0, 0.0]), 
    buff=0.25, 
    aligned_edge=array([0.0, 0.0, 0.0]), 
    submobject_to_align=None, 
    index_of_submobject_to_align=None, 
    coor_mask=array([1, 1, 1]))
将一个物体靠近另一个物体或参考点，由第一个参数指定
    direction 给定对齐的方向：UP，DOWN，LEFT，RIGHT
    buff 为对齐的间距
    aligned_edge 为对齐的边界：UP，DOWN，LEFT，RIGHT，ORIGIN
当对象是 VGroup 时，指定其中某个元素进行对齐
    submobject_to_align 自己要进行移动的参考元素
    index_of_submobject_to_align 目标对齐元素的索引
"""

class try_nextto(Scene):
    def construct(self):
        good = SVGMobject("good.svg",color=RED_B,height=1)
        coin = SVGMobject("coin.svg",color=BLUE,height=2,stroke_width=0.1)
        good.shift(DL*2.5)

        self.play(FadeIn(coin),FadeIn(good))
        self.play(good.next_to,
            {"mobject_or_point":coin,
            "direction":RIGHT}
        )
        self.wait(0.3)
        self.play(good.next_to,
            {"mobject_or_point":coin,
            "direction":UP,
            "aligned_edge":LEFT,
            "buff":0}
        )
        self.wait(1)
        self.remove(good,coin)

        A = TexMobject("A_0","A_1","A_2","A_3","A_4").shift(UP)
        B = TexMobject("B_0","B_1","B_2").shift(DOWN)
        self.play(FadeIn(A),FadeIn(B))
        self.play(B.next_to,
            {"mobject_or_point":A,
            "direction":UP}
        )
        self.wait(0.3)
        self.play(B.next_to,
            {"mobject_or_point":A[2],
            "direction":DOWN,
            "aligned_edge":LEFT}
        )
        self.wait(0.3)
        self.play(B.next_to,
            {"mobject_or_point":A[0],
            "direction":DOWN,
            "aligned_edge":LEFT,
            "submobject_to_align":B[1]}
        )
        self.wait(0.3)
        self.play(B.next_to,
            {"mobject_or_point":A,
            "direction":DOWN,
            "aligned_edge":LEFT,
            "submobject_to_align":B[1],
            "index_of_submobject_to_align":3}
        )
        self.wait(1)

#%% set_width, set_height
"""
set_width(width, stretch=False)    设置物体的宽度（高度默认等比例缩放）
set_height(height, stretch=False)  设置恶徒的高度（宽度默认等比例缩放）
在没有设置 stretch = True 时上述命令与 scale 相同
"""

class try_setwidth(Scene):
    def construct(self):
        coin = SVGMobject("coin.svg",color=BLUE,height=1,stroke_width=0.1)

        self.play(FadeIn(coin))
        self.play(coin.set_width,2)
        self.wait(0.3)
        self.play(coin.scale,0.5)
        self.wait(0.3)
        self.play(coin.set_width,
            {"width":2,
            "stretch":True}
        )
        self.wait(1)