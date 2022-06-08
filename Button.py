import pygame


class Button:
    def __init__(self, SCREEN: pygame.display, left: int = 0, top: int = 0, width: int = 50, height: int = 20,
                 text: str = '') -> None:
        self.__left = left
        self.__top = top
        self.__width = width
        self.__height = height
        self.__rect = pygame.Rect(self.__left, self.__top, self.__width, self.__height)
        self.__SCREEN = SCREEN
        self.__border_color = (0, 0, 0)

        self.__text = text
        self.__font_size = 25
        self.__font_object = pygame.font.Font('freesansbold.ttf', self.__font_size)
        self.__font_color = (0, 0, 0)

    def set_pos(self, left: int, top: int, width: int, height: int) -> None:
        if left < 0 or top < 0 or width < 0 or height < 0:
            raise ValueError("negative coordinates")

        self.__left = left
        self.__top = top
        self.__width = width
        self.__height = height

    def get_pos(self):
        return self.__left, self.__top, self.__width, self.__height

    def set_rect(self, rect: pygame.rect):
        self.__rect = rect

    def get_rect(self):
        return self.__rect

    def set_screen(self, screen: pygame.display):
        self.__SCREEN = screen

    def get_screen(self):
        return self.__SCREEN

    def set_border_color(self, color: tuple[int, int, int]):
        for i in range(3):
            if color[i] < 0 or color[i] > 255:
                raise ValueError("Color must be between 0 adn 255")
        self.__border_color = color

    def get_border_color(self):
        return self.__border_color

    def get_text(self):
        return self.__text

    def set_text(self, text: str):
        self.__text = text

    def set_font_size(self, size: int):
        if size < 1:
            raise ValueError("Font size must be >0")
        self.__font_size = size

    def get_font_size(self):
        return self.__font_size

    def set_font(self, font_obj: pygame.font.Font):
        self.__font_object = font_obj

    def get_font(self):
        return self.__font_object

    def set_font_color(self, color: tuple[int, int, int]):
        for i in range(3):
            if color[i] < 0 or color[i] > 255:
                raise ValueError("Color must be between 0 adn 255")
        self.__font_color = color

    def draw_button(self) -> None:
        pygame.draw.rect(self.__SCREEN, self.__border_color, self.__rect, 1)

    def draw_text(self) -> None:
        text = self.__font_object.render(self.__text, True, self.__font_color)
        text_rect = text.get_rect()
        text_rect.center = self.__rect.center
        self.__SCREEN.blit(text, text_rect)

    def draw(self) -> None:
        self.draw_button()
        self.draw_text()

    def update(self) -> None:
        self.draw()

    def is_clicked(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        return self.__rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]
