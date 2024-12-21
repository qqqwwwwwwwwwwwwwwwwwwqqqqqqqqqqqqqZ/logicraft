class Hero():
    def __init__(self, pos, land):
       self.mode = True # режим проходження крізь усе
       self.land = land
       self.hero = loader.loadModel('smiley')
       self.hero.setColor(1, 0.5, 0)
       self.hero.setScale(0.3)
       self.hero.setPos(pos)
       self.hero.reparentTo(render)
       self.cameraBind()        # розташовання камери
       self.accept_events()     # обробка подій

    # Метод для закріплення камери на гравці
    def cameraBind(self):
       # вимикаємо керування камерою за допомогою миші  
       base.disableMouse()
       # поворот камери на 180 градусів
       base.camera.setH(180)
       # прив'язуємо камеру до вузла об'єкта
       base.camera.reparentTo(self.hero)
       # встановлюємо камеру в задані координати
       base.camera.setPos(0, 0, 1.5)
       # властивість яка показує, що камера прикріплена 
       self.cameraOn = True


    # Метод для відкріплення камери від гравця
    def cameraUp(self):
        pos = self.hero.getPos()
        # розташовуємо вузол камери в певних координатах
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2]-3)
        # прив'язуємо камеру до вузла render
        base.camera.reparentTo(render)
        # включаємо управління мишкою
        base.enableMouse()
        # властивість яка показує, що камера відкріплена 
        self.cameraOn = False


    # Метод для зміни розташування камери
    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()


    # Метод для повороту гравця вліво
    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5) % 360)


    # Метод для повороту гравця вправо
    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)


    # Метод що дозволяє розділяти види рухів різних ігрових режимів
    def move_to(self, angle):
        if self.mode:
           self.just_move(angle)
        else:
           self.try_move(angle)    


    # Метод для переміщення у потрібні координати у будь-якому випадку
    def just_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)


    # Метод що повертає координати, в які переміститься персонаж, що стоїть у точці (x, y),
    # якщо він робить крок у напрямку angle'
    def look_at(self, angle):
        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())
        dx, dy = self.check_dir(angle)
        x_to = x_from + dx
        y_to = y_from + dy
        return x_to, y_to, z_from


    # Метод що повертає заокруглені зміни координат X, Y, відповідні переміщенню у бік кута angle
    def check_dir(self,angle):
        '''Координата Y зменшується, якщо персонаж дивиться на кут 0,
        та збільшується, якщо дивиться на кут 180.
        Координата X збільшується, якщо персонаж дивиться на кут 90,
        та зменшується, якщо дивиться на кут 270.  
           кут 0 (від 0 до 20)      ->        Y - 1
           кут 45 (від 25 до 65)    -> X + 1, Y - 1
           кут 90 (від 70 до 110)   -> X + 1
           від 115 до 155            -> X + 1, Y + 1
           від 160 до 200            ->        Y + 1
           від 205 до 245            -> X - 1, Y + 1
           від 250 до 290            -> X - 1
           від 290 до 335            -> X - 1, Y - 1
           від 340                   ->        Y - 1  '''
        if angle >= 0 and angle <= 20:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (-1, 0)
        elif angle <= 335:
            return (-1, -1)
        else:
            return (0, -1)


    # Метод руху вперед
    def forward(self):
        angle =(self.hero.getH()) % 360
        self.move_to(angle)
        

    
    # Метод руху назад
    def back(self):
       angle = (self.hero.getH()+180) % 360
       self.move_to(angle)
  

    # Метод руху вліо
    def left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)


    # Метод руху вправо
    def right(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)


    # Метод руху вгору
    def up(self):
        if self.mode:
           self.hero.setZ(self.hero.getZ() + 1)


    # Метод руху вниз
    def down(self):
        if self.mode and self.hero.getZ() > 1:
           self.hero.setZ(self.hero.getZ() - 1)


    # Метод для переключання ігрових режимів  
    def changeMode(self):
        if self.mode:
           self.mode = False
        else:
           self.mode = True


    # Метод для переміщення в основному ігровому режимі   
    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
           # маємо вільно. Можливо, треба впасти вниз:
           pos = self.land.findHighestEmpty(pos)
           self.hero.setPos(pos)
        else:
           # маємо зайнято. Якщо вийде, заберемося на цей блок:
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.isEmpty(pos):
               self.hero.setPos(pos)
               # не вийде забратися - стоїмо на місці


    def build(self):
       angle = self.hero.getH() % 360
       pos = self.look_at(angle)
       if self.mode:
           self.land.addBlock(pos)
       else:
           self.land.buildBlock(pos)


    def destroy(self):
       angle = self.hero.getH() % 360
       pos = self.look_at(angle)
       if self.mode:
           self.land.delBlock(pos)
       else:
           self.land.delBlockFrom(pos)


    # Метод для підключення обробки подій
    def accept_events(self):
        # зміна розташування камери 
        base.accept("c", self.changeView)
        # поворот вліво
        base.accept("arrow_left", self.turn_left)
        base.accept("arrow_left" + '-repeat', self.turn_left)
        # поворот вправо
        base.accept("arrow_right", self.turn_right)
        base.accept("arrow_right" + '-repeat', self.turn_right)
        # рух вперед
        base.accept("w", self.forward)
        base.accept("w" + '-repeat', self.forward)
        # рух назад
        base.accept("s", self.back)
        base.accept("s" + '-repeat', self.back)
        # рух вліво
        base.accept("a", self.left)
        base.accept("a" + '-repeat', self.left)
        # рух вправо
        base.accept("d", self.right)
        base.accept("d" + '-repeat', self.right)
        # рух вгору
        base.accept('arrow_up', self.up)
        base.accept('arrow_up' + '-repeat', self.up)
        # рух вниз
        base.accept('arrow_down', self.down)
        base.accept('arrow_down' + '-repeat', self.down)
        # переключання ігрового режима
        base.accept("z", self.changeMode)  

        base.accept("b", self.build)
        base.accept("n", self.destroy)
        base.accept("k",self.land.savemap)
        base.accept("l",self.land.loadMap)