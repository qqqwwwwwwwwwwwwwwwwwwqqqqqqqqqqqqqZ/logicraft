import pickle
class Mapmanager():
    def __init__(self):
        # модель кубика лежить у файлі block.egg
        self.model = 'block.egg' 
        # використовуємо таку текстуру
        self.texture = 'block.png'        
        self.colors = [
           (0.2, 0.2, 0.35, 1),
           (0.2, 0.5, 0.2, 1),
           (0.7, 0.2, 0.2, 1),
           (0.5, 0.3, 0.0, 1)
        ] #rgba
        # створюємо основний вузол карти
        self.startNew()


   #Метод, що створює основу для нової карти
    def startNew(self):
        self.land = render.attachNewNode("Land") # вузол, до якого прив'язані всі блоки картки
   

    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors) - 1]
  
  
    def addBlock(self, position):
        # створення моделі
        self.block = loader.loadModel(self.model)
        # закріплення текстури на моделі
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)
        # встановлення кольору моделі
        self.color = self.getColor(int(position[2]))
        self.block.setColor(self.color)
        # додавння до блоку тегу та значення тегу (його позиція)   
        self.block.setTag("at", str(position))
        #прив'язуємо блок до вузла land
        self.block.reparentTo(self.land)


   #Метод, що обнуляє карту
    def clear(self):
        self.land.removeNode()
        self.startNew()


   #Метод, що створює карту землі з текстового файлу, повертає її розміри
    def loadLand(self, filename):
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                line = line.split(' ')
                for z in line:
                    for z0 in range(int(z)+1):
                       block = self.addBlock((x, y, z0))
                    x += 1
                y += 1
        return x,y
    

    # Метод дозволяє знайти всі блоки, що знаходяться за координатою pos 
    def findBlocks(self, pos):
       return self.land.findAllMatches("=at=" + str(pos))
    

    # Метод для визначення, чи зайнятий перед нами блок   
    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        else:
            return True

    # Метод для визначення верхнього незайнятого блоку     
    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)
    

    # Ставимо блок з урахуванням гравітації
    def buildBlock(self, pos):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addBlock(new)

    # видаляє блоки у зазначеній позиції
    def delBlock(self, position):
        blocks = self.findBlocks(position)
        for block in blocks:
            block.removeNode()

    
    def delBlockFrom(self, position):
        x, y, z = self.findHighestEmpty(position)
        pos = x, y, z - 1
        for block in self.findBlocks(pos):
            block.removeNode()
    def savemap(self):
        print("jlhkugydtckjgf")
        block = self.land.getChildren()
        with open("land.dat","wb") as file:
            pickle.dump(len(block),file)
            for b in block:
                x,y,z = b.getPos()
                pos = (int(x),int(y),int(z))
                pickle.dump(pos,file)
    def loadMap(self):
        self.clear()
        with open("land.dat","rb") as file:
            amount = pickle.load(file)
            for q in range(amount):
                pos = pickle.load(file)
                self.addBlock(pos)