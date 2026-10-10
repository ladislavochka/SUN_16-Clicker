from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.utils import hex_colormap, colormap
from kivy.metrics import sp, dp
from kivy.uix.image import Image
from kivy import platform
from kivy.properties import NumericProperty
from kivy.clock import Clock

class Menu(Screen):
   def __init__(self, **kw):
       super().__init__(**kw)

   def go_game(self, *args):
       self.manager.current = "game"
       self.manager.transition.direction = "left"

   def go_settings(self, *args):
       self.manager.current = "settings"
       self.manager.transition.direction = "up"

   def exit_app(self, *args):
       app.stop()

class Settings(Screen):
   def __init__(self, **kwargs):
       super().__init__(**kwargs)

   def go_menu(self, *args):
       self.manager.current = "menu"
       self.manager.transition.direction = "down"

class Fish(Image):
   fish_current = None
   fish_index = 0
   hp_current = None

   def on_kv_post(self, base_widget):
       self.GAME_SCREEN = self.parent.parent.parent
       return super().on_kv_post(base_widget)

   def new_fish(self, *args):
       self.fish_current = app.LEVELS[app.LEVEL][self.fish_index]
       self.source = app.FISHES[self.fish_current]['source']
       self.hp_current = app.FISHES[self.fish_current]['hp']
       self.opacity = 1

   def defeated(self):
       self.opacity = 0

   def on_touch_down(self, touch):
       if not self.collide_point(*touch.pos) or not self.opacity:
           return
       self.hp_current -= 1
       self.GAME_SCREEN.score += 1
       if self.hp_current <= 0:
           self.defeated()
           if len(app.LEVELS[app.LEVEL]) > self.fish_index + 1:
               self.fish_index += 1
               Clock.schedule_once(self.new_fish, 1.2)
           else:
               Clock.schedule_once(self.GAME_SCREEN.level_complete, 1.2)
               self.fish_index = 0
                         
       return super().on_touch_down(touch)

class Game(Screen):
   score = NumericProperty(0)
   def on_pre_enter(self, *args):
       self.score = 0
       app.LEVEL = 0
       self.ids.level_complete.opacity = 0
       self.ids.fish.fish_index = 0
       return super().on_pre_enter(*args)
  
   def on_enter(self, *args):
       self.start_game()
      
       return super().on_enter(*args)

   def start_game(self):
       self.ids.fish.new_fish()

   def level_complete(self, *args):
       self.ids.level_complete.opacity = 1

   def go_home(self):
       self.manager.current = "menu"
       self.manager.transition.direction = "right"

class MediumApp(App):
   LEVEL = 0
   FISHES = {
   'fish1':
       {'source': '', 'hp': 10},
   'fish2':
       {'source': '', 'hp': 20}
   }


   LEVELS = [
       ['fish1', 'fish1', 'fish2']
   ]

   def build(self):
       sm = ScreenManager()
       sm.add_widget(Menu(name="menu"))
       sm.add_widget(Game(name="game"))
       sm.add_widget(Settings(name="settings"))


       return sm

if platform != 'android':
   Window.size = (450, 900)

app = MediumApp()
app.run()