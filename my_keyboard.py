import pygame
import time

class Keyboard:

    def __init__(self):
        pygame.init()
        win = pygame.display.set_mode((200, 200))
        self.pressed_keys = None

    def get_all_keys(self):
        self.pressed_keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            pass

    def get_key(self, key_name):
        ans = False
        my_key = getattr(pygame, f'K_{key_name}')
        if self.pressed_keys[my_key]:
            ans = True

        pygame.display.update()

        return ans


def main():
    keys = Keyboard()
    keys.get_all_keys()
    print(keys.get_key('LCTRL'))


if __name__ == '__main__':
    while True:
        main()
        time.sleep(0.1)