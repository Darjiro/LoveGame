import pygame as pg
pg.init()
from random import randrange

class Button:
    def __init__(self, image:pg.Surface, screen_size:tuple, direction_x:int, direction_y:int):
        self.image = pg.image.load(f"./src/images/{image}.png")
        self.btn_size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.direction_x = direction_x # -1 or 1
        self.direction_y = direction_y # -1 or 1
        self.screen_size = screen_size
        self.position()
    
    def position(self):
        #We get center of screen for take a reference
        center_x = (self.screen_size[0] /2) - (self.btn_size[0] /2)
        center_y = (self.screen_size[1] /2) - (self.btn_size[1] /2)
        
        self.rect.x = 0
        self.rect.y = 0

        #position acording to direction        
        if self.direction_x == 1:
            self.rect.x = center_x + self.btn_size[0] *2
            
        if self.direction_x == -1:
            self.rect.x = center_x - self.btn_size[0] *2
            
        if self.direction_y == 1:
            self.rect.y = center_y + self.btn_size[1] * 2
            
        if self.direction_y == -1:
            self.rect.y = center_y - self.btn_size[1] * 2
    
        return (self.rect.x, self.rect.y)
        
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

def render_text(text, color, x, y, font, screen):
    img = font.render(text, True, color)
    rect = img.get_rect()
    rect.centerx = x
    rect.centery = y
    screen.blit(img, rect)

def check_mouse_pos(mouse_pos, btn):
    if mouse_pos[0] >= btn.rect.x and mouse_pos[0] <= btn.rect.x + btn.rect.width:
            if mouse_pos[1] >= btn.rect.y and mouse_pos[1] <= btn.rect.y + btn.rect.height:
                return True
    else:
        return False
    
def main():
    SCREEN_SIZE = (550, 550)
    pg.display.set_caption("Love Game")    
    icon = pg.image.load("./src/images/icon.png")
    pg.display.set_icon(icon)
    screen = pg.display.set_mode(SCREEN_SIZE)
    font = pg.font.SysFont('inkfree', 32, italic = True, bold = True)
    
    pg.mixer.music.load("./src/music/background.mp3")
    pg.mixer.music.play()
    
    #images
    win_image = pg.image.load("./src/images/win_image.png")
    background_image = pg.image.load("./src/images/background.jpg")
    rect_win_image = win_image.get_rect()
    rect_background_image = background_image.get_rect()
    
    #center images
    rect_win_image.centerx = SCREEN_SIZE[0] //2
    rect_win_image.centery = SCREEN_SIZE[1] //2
    
    rect_background_image.centerx = SCREEN_SIZE[0] //2
    rect_background_image.centery = SCREEN_SIZE[1] //2
    
    run = True
    won = False
    fps = pg.time.Clock()
    
    btn_yes = Button("yes", SCREEN_SIZE, -1, 1)
    btn_no = Button("no", SCREEN_SIZE, 1, 1) 
    
    #main loop
    while run:
        fps.tick(60)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        #LOGIC
        mouse_pos = pg.mouse.get_pos()
        mouse_click = pg.mouse.get_pressed()
        
        #setting randoms positions to no_button
        x = randrange(0, SCREEN_SIZE[0] - btn_no.rect.width)
        y = randrange(0, SCREEN_SIZE[1] - btn_no.rect.height)
        
        #Checking if mouse pos is inside of the button "no"
        if check_mouse_pos(mouse_pos, btn_no):    
            btn_no.rect.x = x
            btn_no.rect.y = y
        
        #Cheking click for win
        if check_mouse_pos(mouse_pos, btn_yes) and mouse_click[0]:
            pg.mixer.music.stop()
            pg.mixer.music.load("./src/music/accept_music.mp3")
            pg.mixer.music.play()
            won = True
            
        if not check_mouse_pos(mouse_pos, btn_yes) and mouse_click[0] and not won:
            wrong_click = pg.mixer.Sound("./src/music/wrong_click.mp3")
            wrong_click.play()
                   
        #DRAW
        if not won:
            screen.fill(pg.Color("white"))
            screen.blit(background_image, (rect_background_image.x, rect_background_image.y))
            btn_yes.draw(screen)
            btn_no.draw(screen)            
            render_text("¿You wanna be my girlfriend :)?", pg.Color("red"),SCREEN_SIZE[0] //2, 50, font, screen)
            
        if won:
            screen.fill(pg.Color("white"))
            render_text("Always i knew it :3", pg.Color("red"),SCREEN_SIZE[0] //2, 50, font, screen)
            screen.blit(win_image, (rect_win_image.x, rect_win_image.y))
        
        pg.display.update()

    pg.quit()
if __name__ == "__main__":
    main()