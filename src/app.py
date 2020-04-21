#!/usr/bin/python
# coding=utf-8

from kivy.app import App  # Package: Kivy
from kivy.uix.label import Label


class MyApp(App):
    def build(self):
        return Label(text='Hello, World!')
