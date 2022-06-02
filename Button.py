import pygame

class Button:
    def __init__(self,SCREEN,left=0,top=0,width=50,height=20,text=''):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.left,self.top,self.width,self.height)
        self.SCREEN = SCREEN
        self.border_color = (0,0,0)

        self.text = text
        self.font_size = 25
        self.font_object = pygame.font.Font('freesansbold.ttf', self.font_size)
        self.font_color = (0,0,0)


    def draw_button(self):
        pygame.draw.rect(self.SCREEN, self.border_color, self.rect, 1)

    def draw_text(self):
        text = self.font_object.render(self.text, True, self.font_color)
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        self.SCREEN.blit(text, text_rect)

    def draw(self):
        self.draw_button()
        self.draw_text()
    def update(self):
        self.draw()

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]








