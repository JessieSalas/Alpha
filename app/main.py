from kivy.app import App
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, BooleanProperty

import facebook

class Watson(FloatLayout):

    def list_notebooks(self):
        notes = self.get_notebooks()
        with self.canvas:
            layout = GridLayout(rows = len(notes))
            layout.size = self.size
            for note in notes:
                bot = Button(text=note,pos_hint_x = .7, width=100)
                bot.bind(on_press=self.lame)
                layout.add_widget(bot)

    def getLikes(self, user, key):
        graph = facebook.GraphAPI(key)
        profile = graph.get_object(user)
        posts = graph.get_connections(profile['id'], 'posts')
        print(posts)


class Interface(App):
    def build(self):
        self.Instance = Watson()
        return self.Instance

if __name__ == '__main__':
    Interface().run()

    
