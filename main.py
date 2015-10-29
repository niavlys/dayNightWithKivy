'''
DayLight switching example for kivy
===================================

'''
__version__ = '0.0.1'

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty,NumericProperty
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock

global lightSensor

from kivy import platform
if platform == 'android':
    from lightSensor import AndroidLightSensor
    lightSensor = AndroidLightSensor()
else:
    lightSensor = None


class DL_BoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(DL_BoxLayout, self).__init__(**kwargs)
        App.get_running_app().bind(dayNight = self.switchDayNight)

    def switchDayNight(self,inst,dayNight):
        if dayNight:
            self.backgroundColor=(1,1,1,1)
        else:
            self.backgroundColor=(0,0,0,1)

class DL_Label(Label):
    def __init__(self, **kwargs):
        super(DL_Label, self).__init__(**kwargs)
        App.get_running_app().bind(dayNight = self.switchDayNight)

    def switchDayNight(self,inst,dayNight):
        if dayNight:
            self.color=(0,0,0,1)
        else:
            self.color=(1,1,1,1)

class TestApp(App):
    dayNight = BooleanProperty(None)
    threshold = NumericProperty(10) #adapt this value according to your hardware

    def autoDayNight(self,active):
        self.root.ids.dayNightSwitch.disabled = active
        if lightSensor:
            if active:
                lightSensor.enable()
                Clock.schedule_interval(self._isDay,1/20.)
            else:
                lightSensor.disable()
                Clock.unschedule(self._isDay)
                #reset switch value according to current dayNight value
                self.root.ids.dayNightSwitch.active = self.dayNight
                
    def _isDay(self,dt):
        if lightSensor.getLight() < self.threshold:
            self.dayNight = False
        else:
            self.dayNight = True

    def on_pause(self):
        if lightSensor:
            lightSensor.disable()
        return True

    def on_resume(self):
        if lightSensor:
            lightSensor.enable()

if __name__ == '__main__':
    TestApp().run()
