from manim import *
from os import system


class Circle2Square(Scene):
    def construct(self):
        circle = Circle()
        square = Square()

        self.play(Create(circle))
        self.play(Transform(circle, square))


class Square2Circle(Scene):
    def construct(self):
        square = Square()
        circle = Circle().scale(2)

        self.play(Create(square))
        self.play(Rotate(square, PI))
        self.play(ScaleInPlace(square,2))
        self.play(Transform(square, circle))


if __name__ == '__main__':
    system('manim -pqk Circle2Square.py Square2Circle')
