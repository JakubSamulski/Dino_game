import pygame_textinput
import pygame


# TODO napisac to ładniej i zrobic walidacje
class Textbox(pygame_textinput.TextInputVisualizer):
    def __init__(self, left:int=0, top:int=0, width:int=10, height:int=25, default_text:str='')->None:

        super().__init__()
        self.__left = left
        self.__top = top
        self.__width = width
        self.__height = height
        self.__is_active = False
        self.__default_text = default_text
        self.__has_been_clicked = -1
        self.__border_color = (0, 0, 0)
        self.__font_object = pygame.font.Font('freesansbold.ttf', 25)
        self.__rect = super(Textbox, self).surface.get_rect()
        self.__rect.left = self.__left - 5
        self.__rect.top = self.__top - 3
        self.__rect.width = self.__width
        self.__rect.height = self.__height + 4

        if self.__default_text != '':
            self.set_default_text()


    def set_size(self, left:int=0, top:int=0, width:int=10, height:int=25)->None:
        self.__left = left
        self.__top = top
        self.__width = width
        self.__height = height
    def get_size(self):
        return self.__left,self.__top,self.__width,self.__height

    def set_font_color(self, color: tuple[int, int, int]):
        for i in range(3):
            if color[i] < 0 or color[i] > 255:
                raise ValueError("Color must be between 0 adn 255")
        self.font_color = color

    def get_font_color(self):
        return self.font_color

    def set_default_text(self)->None:
        self.value = self.__default_text
        self.set_font_color((170, 170, 170))

    def set_font(self, font_obj: pygame.font.Font):
        self.__font_object = font_obj

    def get_font(self):
        return self.__font_object
    def set_rect(self, rect: pygame.rect):
        self.__rect = rect

    def get_rect(self):
        return self.__rect

    def set_border_color(self, color: tuple[int, int, int])->None:
        for i in range(3):
            if color[i] < 0 or color[i] > 255:
                raise ValueError("Color must be between 0 adn 255")
        self.__border_color = color

    def get_text(self)->str:
        return self.value
    def set_text(self,text:str):
        self.value =text

    def update(self, events: pygame.event.Event, SCREEN:pygame.display)->None:
        '''
        function called every frame
        :param events: result of pygane.event.get()
        :param SCREEN: pygame display
        :return: none
        '''

        # print(self.font_color)
        def draw():
            if (self.__rect.width < self.surface.get_rect().width):
                self.__rect.width = self.surface.get_rect().width
            elif self.__rect.width > self.surface.get_rect().width and self.surface.get_rect().width > self.__width:
                self.__rect.width = self.surface.get_rect().width
            pygame.draw.rect(SCREEN, self.__border_color, self.__rect, 2)
            # print(self.surface.get_rect().width)
            SCREEN.blit(self.surface, (self.__left, self.__top))

        # SCREEN.blit(self.surface, (200, 200))
        mousePos = pygame.mouse.get_pos()
        # print(mousePos)
        # pygame.draw.rect(SCREEN, (255, 0, 0), self.rect, 2)
        # print(self.rect)
        # checks if textbox should be active or not and calls update if it is active
        if self.__has_been_clicked == 0:
            self.value = ''
            self.__has_been_clicked = 1

        if self.__rect.collidepoint(mousePos) and pygame.mouse.get_pressed()[0] and not self.__is_active:
            self.__has_been_clicked = 0
            self.__is_active = True
            self.font_color = (0, 0, 0)
        elif not self.__rect.collidepoint(mousePos) and pygame.mouse.get_pressed()[0] and self.__is_active:
            self.__is_active = False
            self.cursor_visible = False
        if self.__is_active:
            super().update(events)
        draw()
