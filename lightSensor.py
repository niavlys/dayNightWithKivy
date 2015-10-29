from jnius import PythonJavaClass, java_method, autoclass, cast

PythonActivity = autoclass('org.renpy.android.PythonActivity')
activity = PythonActivity.mActivity
Context = autoclass('android.content.Context')
Sensor = autoclass('android.hardware.Sensor')
SensorManager = autoclass('android.hardware.SensorManager')


class LightSensorListener(PythonJavaClass):
    __javainterfaces__ = ['android/hardware/SensorEventListener']

    def __init__(self):
        super(LightSensorListener, self).__init__()
        self.SensorManager = cast('android.hardware.SensorManager',
                    activity.getSystemService(Context.SENSOR_SERVICE))
        self.sensor = self.SensorManager.getDefaultSensor(Sensor.TYPE_LIGHT)
        self.value = None

    def enable(self):
        self.SensorManager.registerListener(self, self.sensor,
                    SensorManager.SENSOR_DELAY_NORMAL)

    def disable(self):
        self.SensorManager.unregisterListener(self, self.sensor)

    @java_method('(Landroid/hardware/SensorEvent;)V')
    def onSensorChanged(self, event):
        self.value = event.values[0]

    @java_method('(Landroid/hardware/Sensor;I)V')
    def onAccuracyChanged(self, sensor, accuracy):
        pass

class AndroidLightSensor(object):
    
    def __init__(self):
        super(AndroidLightSensor, self).__init__()
        self.bState = False

    def enable(self):
        if (not self.bState):
            self.listener = LightSensorListener()
            self.listener.enable()
            self.bState = True

    def disable(self):
        if (self.bState):
            self.bState = False
            self.listener.disable()
            del self.listener

    def getLight(self):
        if (self.bState):
            return self.listener.value
        else:
            return None

    def __del__(self):
        self._disable()
        super(self.__class__, self).__del__()
