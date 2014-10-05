from kivy.app import App
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty

import facebook
from auth import *

class Watson(FloatLayout):

    AUTH_KEY = StringProperty()
    MESSAGES = ObjectProperty()
    ME = "Jessie Salas"

    def authenticate(self):
        self.AUTH_KEY = getAuth()

    def getInfo(self, user, key):
        graph = facebook.GraphAPI(key)
        profile = graph.get_object(user)
        self.MESSAGES = graph.get_connections(profile['id'], 'outbox')
        self.MESSAGES = graph.get_connections(profile['id'], 'posts')
        exec("self.MESSAGES = {0}".format(self.MESSAGES)) #execute into python dictionary
        message_corpus=""
        for thing in self.MESSAGES['data']:
            #print thing
            for i in thing['comments']['data']:
                if 'from' in i.keys() and 'message' in i.keys():
                    if i['from']['name'] == self.ME:
                        message_corpus += i['message']
        print(message_corpus)
"""
                    try: 
                        if 'comments' in i['message'].keys():
                            #print i['message']['comments']
                            pass
                    except:
                        #print i['message']
                        pass
                else:
                    print i['from']
"""
                    
class Interface(App):
    def build(self):
        self.Instance = Watson()
        return self.Instance

if __name__ == '__main__':
    Interface().run()

    
