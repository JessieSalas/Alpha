from kivy.app import App
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty,ListProperty

import facebook
from auth import *
from stats import *

from kivy.garden.graph import Graph

class Alpha(FloatLayout):

    Patient_message = StringProperty()

    AUTH_KEY = StringProperty()
    ME = StringProperty()
    
    MESSAGES = StringProperty() #one big string
    POSTS = StringProperty()  #one big string
    SLEEP_REGULARITY= NumericProperty() #list of string times
    LIKES = ListProperty() #list of string categories

    def waiter(self):
        self.Patient_message = "Thanks for logging in! We'll take it from here."

    def authenticate(self):
        self.AUTH_KEY = getAuth()

    def sleepRegularity(self,time_list):
        return getSleepRegularity(time_list)

    def variability(self,messages):
        return getVariability(messages)

    def likeIndex(self,likes):
        return getLikeIndex(likes)

    def getInfo(self, user, key):
        graph = facebook.GraphAPI(key)
        profile = graph.get_object(user)
        MESSAGES_TEMP = graph.get_connections(profile['id'], 'outbox')
        POSTS_TEMP = graph.get_connections(profile['id'], 'posts')
        LIKES_TEMP = graph.get_connections(profile['id'], 'likes')
        self.ME = profile['first_name'] + " " + profile['last_name']
        exec("MESSAGES_TEMP = {0}".format(MESSAGES_TEMP)) #execute into python dictionary
        message_corpus=""
        post_corpus=""
        post_time_corpus = []
        likes_corpus = []

        for like in LIKES_TEMP['data']:
            likes_corpus.append(like['category'])

        for post in POSTS_TEMP['data']:
            post_time_corpus.append(post['updated_time'])
            post_corpus += post['story']

        for thing in MESSAGES_TEMP['data']:
            for i in thing['comments']['data']:
                if 'from' in i.keys() and 'message' in i.keys():
                    if i['from']['name'] == self.ME:
                        message_corpus += i['message']

        self.MESSAGES = message_corpus
        self.POSTS = post_corpus
        self.SLEEP_REGULARITY = self.sleepRegularity(post_time_corpus)
        self.LIKES = likes_corpus

class Interface(App):
    def build(self):
        self.Instance = Alpha()
        return self.Instance

if __name__ == '__main__':
    Interface().run()

