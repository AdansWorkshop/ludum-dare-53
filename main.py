## Drifty Delivery Service
import pyglet, math, random
from pyglet.window import key
from pyglet.media import *
from pyglet.gl import * 
window = pyglet.window.Window(width = 960, height = 540)
window.set_caption("Drifty Delivery Service")
main_batch = pyglet.graphics.Batch()
fg_batch = pyglet.graphics.Batch()
end_batch = pyglet.graphics.Batch()
ui_batch = pyglet.graphics.Batch()
audioPlayer = pyglet.media.Player()
audioPlayer2 = pyglet.media.Player()
keys = {key.W: False, key.S: False, key.A: False, key.D: False}
class Started():
    def __init__(self):
        self.started = False
    def start(self):
        self.started = True
    def stop(self):
        self.started = False

imgs = [[pyglet.image.load("assets/11.png"), pyglet.image.load("assets/12.png"), pyglet.image.load("assets/13.png")], [pyglet.image.load("assets/21.png"), pyglet.image.load("assets/22.png"), pyglet.image.load("assets/23.png")], [pyglet.image.load("assets/31.png"), pyglet.image.load("assets/32.png"), pyglet.image.load("assets/33.png")]]
roadSegments = []
packages = []
houseImgs = [pyglet.image.load("assets/houseleft.png"), pyglet.image.load("assets/houseright.png")]
houses = []
class Score():
    def __init__(self):
        self.score = 0
    def inc(self, score):
        self.score += score

engine = StaticSource(load("assets/engine.wav"))
audioPlayer2.queue(engine)
delivered = StaticSource(load("assets/delivered.wav"))


def newPackage():
    r = random.randrange(0, 24)
    if r in packages:
        return newPackage()
    else:
        return r

def dist(x1, y1, x2, y2):
    return math.sqrt(((x2-x1)**2) + ((y2-y1)**2))

class EndScreen():
    def __init__(self):
        self.bgOpacity = 0
        self.fgOpacity = 0
        self.endBg = pyglet.shapes.Rectangle(0, 0, 960, 540, (0, 0, 0, 0), end_batch)
        self.endScore = pyglet.text.Label("0", "Arial", 48, False, False, False, (255, 255, 255, 0), 480, 270, 1, 100, 50, 'center', 'center', 'center', False, None, end_batch)
        self.gameOver = pyglet.text.Label("Game Over!", "Arial", 72, False, False, False, (255, 255, 255, 0), 480, 360, 1, 400, 100, 'center', 'center', 'center', False, None, end_batch)
    def update(self, bgOpacity, fgOpacity, score):
        self.endBg.color = [0,0,0,math.floor(230 * bgOpacity)]
        self.endScore.color = [255,255,255,math.floor(255 * fgOpacity)]
        self.gameOver.color = [255,255,255,math.floor(255 * fgOpacity)]
        t = ""
        if score == 16:
            t = "You Win!!!"
        elif score >= 12:
            t = "So Close!!"
        elif score >= 8:
            t = "Almost!"
        else:
            t = "Game Over"
        self.gameOver.text = t
        self.endScore.text = str(score) + "/16"

class House():
    def __init__(self, index):
        self.pos = 270 + (540*index)
        self.side = random.randrange(0, 2)
        img = houseImgs[self.side]
        self.sprite = pyglet.sprite.Sprite(img, 0, self.pos, 2)
        self.sprite.batch = fg_batch
        self.label = pyglet.text.Label(str(index), "Arial", 24, False, False, False, (0, 0, 0, 255), 78 + (self.side * 780), self.pos + 262, 3, 28, 20, 'left', 'baseline', 'center')
        self.label.batch = fg_batch

    def update(self, dt):
        self.pos -= dt * 400
        self.sprite.update(0, self.pos, 2)
        self.label.position = [78 + (self.side * 780), 262 + self.pos, 3]

for h in range(24):
    houses.append(House(h))

class RoadSegment():
    def __init__(self, start, end, position):
        self.pos = position
        self.start = start
        self.end = end
        self.sprite = pyglet.sprite.Sprite(imgs[start][end], 0, self.pos)
        self.pend = True
    def update(self, dt):
        self.pos -= dt * 400
        self.sprite.update(0, self.pos)
        if self.pos >= 0:
            self.pend = False
        elif self.pend == False:
            roadSegments.append(RoadSegment(self.end, random.randrange(0, 3), 540))
            self.pend = True
        if self.pos <= -540:
            del self.sprite
            roadSegments.remove(self)
            del self


class Car():
    def __init__(self, x, y, direction : float, color, scale, turnRate, windscreenColor):
        self.x = x
        self.y = y
        self.dir = direction
        self.color = color
        self.wColor = windscreenColor
        self.vel = 0
        self.turnRate = turnRate
        self.w = scale * 64
        self.h = scale * 32
        self.rect = None
        img = pyglet.image.load("assets/car.png")
        self.sprite = pyglet.sprite.Sprite(img, self.x + self.w/2, self.y + self.h/2)
        self.sprite.color = self.color[:-1]
        self.cross = dist(0, 0, self.w/2, self.h/2)
        self.d = self.x
        self.dx = 0
        self.g = 0
        self.pendThrow = True
        self.throwTimer = 0
        self.pixCol = [0,0,0, 255]
    def update(self, dt):
        self.rect = pyglet.shapes.Rectangle(self.x, self.y, self.w, self.h, self.wColor)
        self.rect.anchor_position = (self.w/2, self.h/2)
        self.rect.rotation = self.dir
        self.sprite.update(self.x - (math.cos(self.dir * (-math.pi/180)) * (self.w * .625)) - (math.cos(self.dir * (-math.pi/180) + 90) * (self.h/2 + 1)), self.y - (math.sin(self.dir * (-math.pi/180)) * (self.w * 0.625)) - (math.sin(self.dir * (-math.pi/180) + 90) * (self.h/2 + 1)), None, self.dir, scale_x=self.w/64, scale_y=self.h/32)
        self.dx = self.x
        if started.started:
            self.input(dt)
            self.x += math.cos(self.dir * (-math.pi/180)) * dt * -200
            if self.pixCol == [0, 170, 0, 255]:
                started.stop()
                ended.start()
        if self.dir < 30 or self.dir > 150:
            if random.randrange(0, 4) == 1:
                self.pendThrow = False
            else:
                self.pendThrow = True
        elif self.pendThrow == False:
            if len(packages) != 0 and self.throwTimer >= 1.5:
                r = random.randrange(0, len(packages))
                thrownPackages.append(Package(packages[r], self.x, self.y, self.dir))
                packages.pop(r)
                self.throwTimer = 0
            self.pendThrow = True
        self.throwTimer += dt

    def input(self, dt): 
        if keys[key.A]:
            self.dir -= self.turnRate * dt
        elif keys[key.D]:
            self.dir += self.turnRate * dt
        self.dir = self.dir % 360
    
    def collide(self):
            a = (GLubyte * 4)(0)
            glReadPixels(math.floor(self.x), math.floor(self.y), 1, 1, GL_RGBA, GL_UNSIGNED_BYTE, a)
            self.pixCol = [a[0], a[1], a[2], 255]

class Package():
    def __init__(self, houseNum, x, y, dir):
        self.houseNum = houseNum
        img = pyglet.image.load("assets/package.png")
        self.x = x
        self.y = y
        self.dir = dir
        self.sprite = pyglet.sprite.Sprite(img, self.x, self.y)
        self.sprite.batch = fg_batch
        self.sprite.scale = 1.5
        self.label = pyglet.text.Label(str(houseNum), "Arial", 10, False, False, False, (0, 0, 0, 255), self.x + 2, self.y + 31*self.sprite.scale, 2, 12, 9, 'left', 'top', 'center')
        self.label.batch = fg_batch
        thrownPackages.append(self)
        self.collided = False
    
    def update(self, dt):
        self.x += math.cos(self.dir * (-math.pi/180)) * 600 * dt
        self.y += (math.sin(self.dir * (-math.pi/180))) * 600 * dt
        self.sprite.update(self.x, self.y)
        self.label.position = [self.x + 2, self.y + (31 * self.sprite.scale), 2]
        if dist(self.x + (16 * self.sprite.scale), self.y + (16 * self.sprite.scale), 88 + (784 * houses[self.houseNum].side), 307 + (houses[self.houseNum].pos)) < 86:
            self.collided = True
        elif self.collided:
            self.collided = False
            thrownPackages.remove(self)
            score.inc(2)
            audioPlayer.queue(delivered)
            del self
        elif self.x < -128 or self.x > 1088:
            thrownPackages.remove(self)
            del self    


truck = Car(480, 250, 90, (255, 255, 255, 255), 2, 90, (0, 255, 255, 255))
roadSegments = [RoadSegment(1, random.randrange(0, 3), 270)]
currentSegment = 0
started = Started()
ended = Started()
score = Score()
fadeTime = Score()
packages = []
for i in range(8):
    packages.append(newPackage())
packages.sort()
thrownPackages = []
deliveredPackages = []

startBanner = pyglet.sprite.Sprite(pyglet.image.load("assets/startbanner.png"), 0, 0, 0)
uiImg = pyglet.image.load("assets/ui.png")

endScreen = EndScreen()

@window.event
def on_key_press(symbol, modifiers):
    for k in keys:
        if symbol == k:
            keys[k] = True
    if symbol == key.SPACE:
        started.start()
    if started.started and len(packages) != 0:
        if symbol == key.Q:
            thrownPackages.append(Package(packages[0], truck.x, truck.y, truck.dir + 90))
            packages.pop(0)
        if symbol == key.E:
            thrownPackages.append(Package(packages[0], truck.x, truck.y, truck.dir - 90))
            packages.pop(0)

@window.event
def on_key_release(symbol, modifiers):
    for k in keys:
        if symbol == k:
            keys[k] = False

@window.event
def on_draw():
    window.clear()
    pyglet.sprite.Sprite(pyglet.image.load("assets/start.png"), 0, 0).draw()
    main_batch.draw()
    for r in roadSegments:
        r.sprite.draw()
    fg_batch.draw()
    startBanner.draw()
    truck.collide()
    truck.rect.draw()
    truck.sprite.draw()

    pyglet.sprite.Sprite(uiImg, 0, 0, 2).draw()
    pyglet.text.Label(str(packages).removeprefix("[").removesuffix("]"), "Arial", 22, False, False, False, (47, 47, 47, 255), 620, 10, 2).draw()
    pyglet.text.Label(str(score.score) + "/16", "Arial", 24, False, False, False, (47, 47, 47, 255), 10, 10, 2).draw()
    if ended.started: 
        end_batch.draw()

def update(dt):
    truck.update(dt)
    if started.started:
        for r in roadSegments:
            r.update(dt)
        for h in houses:
            h.update(dt)
        sbPos = startBanner.position
        startBanner.update(sbPos[0], sbPos[1] + dt * 120,)
        audioPlayer.play()
    for p in thrownPackages:
        p.update(dt)
    
    if len(packages) == 0 and len(thrownPackages) == 0:
        started.stop()
        ended.start()
    
    if ended.started:
        fade(dt)
    

def sigmoid(x, o):
    return 1 / (1 + math.exp(o - (10 * x)))

def fade(dt):
    fadeTime.inc(dt)
    bgFade = sigmoid(fadeTime.score, 10)
    fgFade = sigmoid(fadeTime.score, 20)
    endScreen.update(bgFade, fgFade, score.score)
pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()
