import pygame_textinput
import pygame

# TODO napisac to ładniej i zrobic walidacje
class Textbox(pygame_textinput.TextInputVisualizer):
    def __init__(self, left=0, top=0, width=10, height=25, default_text=''):

        super().__init__()

        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.is_active = False
        self.default_text = default_text
        self.has_been_clicked = -1
        self.initialize()
        self.border_color = (0, 0, 0)
        self.font_object = pygame.font.Font('freesansbold.ttf', 25)

    def initialize(self):
        self.rect = super(Textbox, self).surface.get_rect()
        self.rect.left = self.left - 5
        self.rect.top = self.top -3
        self.rect.width = self.width
        self.rect.height = self.height + 4

        if self.default_text != '':
            self.set_default_text()

    def setSize(self, left=0, top=0, width=10, height=25):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def set_font_color(self, color: tuple[3]):
        self.font_color = color

    def set_default_text(self):
        self.value = self.default_text
        self.set_font_color((170, 170, 170))

    def set_border_color(self, color: tuple[int, int, int]):
        self.border_color = color

    def get_text(self):
        return self.value








    def update(self, events: pygame.event.Event, SCREEN):
        '''
        function called every frame
        :param events: result of pygane.event.get()
        :param SCREEN: pygame display
        :return: none
        '''

        # print(self.font_color)
        def draw():
            if (self.rect.width < self.surface.get_rect().width):
                self.rect.width = self.surface.get_rect().width
            elif self.rect.width > self.surface.get_rect().width and self.surface.get_rect().width > self.width:
                self.rect.width = self.surface.get_rect().width
            pygame.draw.rect(SCREEN, self.border_color, self.rect, 2)
            # print(self.surface.get_rect().width)
            SCREEN.blit(self.surface, (self.left, self.top))

        # SCREEN.blit(self.surface, (200, 200))
        mousePos = pygame.mouse.get_pos()
        # print(mousePos)
        # pygame.draw.rect(SCREEN, (255, 0, 0), self.rect, 2)
        # print(self.rect)
        # checks if textbox should be active or not and calls update if it is active
        if self.has_been_clicked == 0:
            self.value = ''
            self.has_been_clicked = 1

        if self.rect.collidepoint(mousePos) and pygame.mouse.get_pressed()[0] and not self.is_active:
            self.has_been_clicked = 0
            self.is_active = True
            self.font_color = (0, 0, 0)
        elif not self.rect.collidepoint(mousePos) and pygame.mouse.get_pressed()[0] and self.is_active:
            self.is_active = False
            self.cursor_visible = False
        if self.is_active:
            super().update(events)
        draw()
