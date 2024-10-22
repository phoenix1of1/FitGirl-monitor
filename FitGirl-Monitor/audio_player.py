from playsound import playsound

class AudioPlayer:
    def __init__(self, audio_file):
        self.audio_file = audio_file
        self.enabled = True

    def play(self):
        if self.enabled:
            playsound(self.audio_file)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False