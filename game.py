from direct.showbase.ShowBase import ShowBase
from map2pypro import Mapmanager
from nelsdfljkn import Hero
class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.map = Mapmanager()
        self.map.loadLand("land.txt")
        self.hero = Hero((10,15,2),self.map)
        base.camLens.setFov(90)
game = Game()
game.run()
