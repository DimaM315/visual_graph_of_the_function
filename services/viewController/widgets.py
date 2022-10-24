import pygame
from loguru import logger 

from settings import *


logger.add("logs/info.log", format="{time} | {level} | {message}", level="INFO", compression="zip", rotation="50 KB")


class InputBox:
    # Accepts the characters for input when pressing Enter
	# processes the entered value. Deletes the previously entered values
	# when pressing backspace, but doesn`t touch the placeholder

    def __init__(self, x, y, w, h, pg_font, plch):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = plch
        
        self.plch = plch
        
        self.pg_font = pg_font
        self.txt_surface = self.pg_font.render(self.text, True, self.color)
        self.active = False

        # Maximum number of characters for self.text
        self.limited_chars = 20 


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box
            self.color = GREEN if self.active else GRAY
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    logger.info('Entered: ' + self.text)
                    self.text = self.plch
                    self.active = False
                    self.color = GREEN if self.active else GRAY
                elif event.key == pygame.K_BACKSPACE and len(self.text) > len(self.plch):
                    self.text = self.text[:-1]
                else:
                    if len(self.text) <  self.limited_chars:
                        self.text += self.__allowed_chars(event.unicode)
                # Re-render the text
                self.txt_surface = self.pg_font.render(self.text, True, self.color)


    def update(self):
        # Resize the box if the text is too long
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width


    def draw(self, screen):
        # Blit the text and the rect 
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


    def __allowed_chars(self, event_unicode:str)->str:
        # restrict the user in the ability to use other characters except:
        # x 0-9 ^ + - .
        if event_unicode not in ALLOWED_CHARS_LIST:
            print("we dont type any char except: 0-9 x + - ^ . () /")
            return ''
        return event_unicode



class Button:
    def __init__(self, x, y, w, h, pg_font, plch):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = plch
        
        self.plch = plch
        self.blick = False
        
        self.pg_font = pg_font
        self.txt_surface = self.pg_font.render(self.text, True, WHITE)


    def on_the_element(self, event):
        # Check event - click on the button
        return self.rect.collidepoint(event.pos)              


    def draw(self, screen):
        # Blit the text and the rect 
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+10))
        if self.blick:
            pygame.draw.rect(screen, GREEN, self.rect, 2)
        else:
            pygame.draw.rect(screen, BLUE, self.rect, 2)


    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.on_the_element(event):
                #print("Mouse moved")
                pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.on_the_element(event):
                self.blick = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.on_the_element(event):
                self.blick = False


    def change_active(self):
        self.blick = not self.blick