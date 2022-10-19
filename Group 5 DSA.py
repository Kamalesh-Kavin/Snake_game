import pygame
import time
import random

lens=40
dis_width=1000
dis_height=700
class Apple:
    def __init__(self,parent):
        self.apple=pygame.image.load("Pics/foody.jpg").convert()
        self.parent=parent
        self.x=lens*3
        self.y=lens*3
    def draw(self):
        self.parent.blit(self.apple,(self.x,self.y))
        pygame.display.update()
    def move(self):
        self.x=random.randint(0,15)*lens
        self.y=random.randint(0,15)*lens
    
class Snake:
    def __init__(self,parent,length):
        self.length=length
        self.parent=parent
        self.block=pygame.image.load("Pics/body.jpg").convert()
        self.x=[lens]*length
        self.y=[lens]*length
        self.direction=None
    def draw(self):
        for i in range(self.length):
            self.parent.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.update()
    def walk(self):
        for i in range(-1,-self.length,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]
        if self.direction=='up':
            self.y[0]-=lens
        if self.direction=='down':
            self.y[0]+=lens
        if self.direction=='left':
            self.x[0]-=lens
        if self.direction=='right':
            self.x[0]+=lens
        self.draw()
    def inc_len(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)
    def move_left(self):
        self.direction='left'
    def move_right(self):
        self.direction='right'
    def move_up(self):
        self.direction='up'
    def move_down(self):
        self.direction='down'
        
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Group 5 DSA Project")
        self.bg_music()
        self.dis=pygame.display.set_mode((dis_width,dis_height))
        self.snake=Snake(self.dis,1)
        self.snake.draw()
        self.apple=Apple(self.dis)
        self.apple.draw()
    def out(self,x1,y1):
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            return True
        return False
    def eat(self,x1,y1,x2,y2):
        if x1>=x2 and x1<x2+lens:
            if y1>=y2 and y1<y2+lens:
                return True
        return False
    def bg_music(self):
        pygame.mixer.music.load("Audio/bg_music.mp3")
        pygame.mixer.music.play()
    def play(self):
        self.bg_img()
        self.snake.walk()
        self.apple.draw()
        self.disp()
        pygame.display.update()

        #snake eats apple
        if self.eat(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            sound=pygame.mixer.Sound("Audio/eat.mp3")
            pygame.mixer.Sound.play(sound)
            self.apple.move()
            self.snake.inc_len()

        #snake trying to eat itself
        for i in range(1,self.snake.length):
            if self.eat(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                sound=pygame.mixer.Sound("Audio/hit.mp3")
                pygame.mixer.Sound.play(sound)
                raise "Game over"
                        
    def disp(self):
        font=pygame.font.SysFont('Comic Sans MS',30)
        sr=self.snake.length-1
        score=font.render(f"Score: {self.snake.length-1}",True,(0,255,255))
        self.dis.blit(score,(850,10))
    def show_game_over(self):
        self.bg_img()
        font=pygame.font.SysFont('Comic Sans MS',30)
        l1=font.render(f"Game is over! Your score is {self.snake.length-1}",True,(0,255,255))
        self.dis.blit(l1,(200,300))
        l2=font.render("To play again press (C). To Quit press (Q)",True,(0,255,255))
        self.dis.blit(l2,(200,350))
        pygame.display.update()
        pygame.mixer.music.pause()
    def reset(self):
        self.snake=Snake(self.dis,1)
        self.apple=Apple(self.dis)
    def bg_img(self):
        bg=pygame.image.load("Pics/bg.jpg")
        self.dis.blit(bg,(0,0))
        pygame.display.update()
    def run(self):
        game=True
        pause=False
        while game:
            if self.out(self.snake.x[0],self.snake.y[0]):
                sound=pygame.mixer.Sound("Audio/hit.mp3")
                pygame.mixer.Sound.play(sound)
                self.show_game_over()
                pause=True
                self.reset()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    game=False
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_q:
                        game=False
                    if event.key==pygame.K_c:
                        pygame.mixer.music.unpause()
                        pause=False
                    if not pause:
                        if event.key==pygame.K_UP:
                            self.snake.move_up()
                        elif event.key==pygame.K_DOWN:
                            self.snake.move_down()
                        elif event.key==pygame.K_LEFT:
                            self.snake.move_left()
                        elif event.key==pygame.K_RIGHT:
                            self.snake.move_right()
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause=True
                self.reset()
            time.sleep(0.2)

if __name__=='__main__':
    a=Game()
    a.run()
