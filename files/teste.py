import pygame

pygame.init()

win = pygame.display.set_mode((500,480))
pygame.display.set_caption("Teste")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

bulletSound= pygame.mixer.Sound('bullet.wav')
hitSound= pygame.mixer.Sound('hit.wav')
music= pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

clock= pygame.time.Clock()

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount= 10
        self.left= False
        self.right= False
        self.walkCount= 0
        self.standing = True
        self.hitbox=(self.x+17, self.y+11, 29, 52)
        
    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount=0
            
        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x,self.y))
        self.hitbox=(self.x+17, self.y+11, 29, 52)
        #pygame.draw.rect(win,(255,0,0), self.hitbox, 2)

    def hit(self):
        self.isJump=False
        self.jumpCount=10
        self.x=60
        self.y=410
        self.walkCount=0
        font1=pygame.font.SysFont('comicsans', 50, True)
        text=font1.render("-5",1,(255,0,0))
        win.blit(text,((500/2 - (text.get_width()//2)), 200))
        pygame.display.update()
        i=0
        while i<300:
            pygame.time.delay(10)
            i+=1
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    i=301
                    pygame.quit()
    
class projectile(object):
    def __init__ (self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
        
    def draw(self,win):
        pygame.draw.circle(win,self.color, (self.x, self.y), self.radius)
        

class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkCount=0
        self.vel = 3
        self.path = [self.x,self.end]
        self.hitbox=(self.x+17, self.y+2, 31, 57)
        self.visible=True
        self.health=10

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount+1 >= 33:
                self.walkCount=0
            if self.vel>0:
                win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount+=1
            else:
                win.blit(self.walkLeft[self.walkCount//3],(self.x, self.y))
                self.walkCount += 1
            self.hitbox=(self.x+17, self.y+2, 31, 57)
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1]-20, 50, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1]-20, 50-(5*(10-self.health)), 10))
            #pygame.draw.rect(win,(255,0,0), self.hitbox, 2)

    def move(self):
        if self.vel>0:
            if self.x+self.vel<self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel *-1
                self.walkCount=0
        else:
            if self.x - self.vel > self.path [0]:
                self.x += self. vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
                
    def hit(self):
        if self.health>0:
            self.health-=1
        else:
            self.visible=False
        

def redrawGameWindow():
    win.blit(bg,(0,0))
    man.draw(win)
    text = font.render('Score = ' + str(score), 1, (0,0,0))
    win.blit(text, (370, 10))
    for bullet in bullets:
        bullet.draw(win)
    goblin.draw(win)
    
    pygame.display.update()

font = pygame.font.SysFont('comicsans',30,True)
score= 0
goblin=enemy(100,410,64,64,450)
man = player(5,410,64,64)
run = True
bullets = []
shootLoop=0

while run == True:
    clock.tick(27)
    if goblin.visible:
        if man.hitbox[1]<goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0]+man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0]+goblin.hitbox[2]:
                man.hit()
                score-=5
        
    if shootLoop>0:
        shootLoop+=1
    if shootLoop>3:
        shootLoop=0
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if goblin.visible:
            if bullet.y-bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x+bullet.radius>goblin.hitbox[0] and bullet.x-bullet.radius<goblin.hitbox[0]+goblin.hitbox[2]:
                    hitSound.play()
                    goblin.hit()
                    bullets.pop(bullets.index(bullet))
                    score+=1
        if bullet.x<500 and bullet.x>0:
            bullet.x+= bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    k = pygame.key.get_pressed()
    if k[pygame.K_SPACE] and shootLoop==0:
        bulletSound.play()
        if man.left:
            facing=-1
        else:
            facing=1
        if len(bullets)<20:
            bullets.append(projectile(round(man.x + man.width//2), round(man.y + man.height//2), 6, (0,0,0), facing))
        shootLoop=1

    if k[pygame.K_LEFT] and man.x>0:
        man.x = man.x - man.vel
        man.left=True
        man.right=False
        man.standing= False
        
    elif k[pygame.K_RIGHT] and man.x + man.width < 500:
        man.x = man.x + man.vel
        man.left=False
        man.right=True
        man.standing=False
    else:
        man.standing= True
        man.walkCount= 0
        
    if not (man.isJump):
        '''if k[pygame.K_UP] and man.y > 0:
            man.y = man.y - man.vel
        if k[pygame.K_DOWN] and man.y < 500 - man.height:
            man.y = man.y + man.vel'''
        if k[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount>= -10:
            neg = 1
            if man.jumpCount<0:
                neg = -1
            man.y = man.y - (((man.jumpCount ** 2) // 2) * neg)
            man.jumpCount = man.jumpCount - 1
        else:
            man.isJump = False
            man.jumpCount = 10
    
    redrawGameWindow()
    
    

pygame.quit()
