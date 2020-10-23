import pygame

class GObject(pygame.sprite.Sprite):
    def __init__(self, options):
        super().__init__()
        self.image = pygame.surface.Surface((options.w, options.h))
        self.image.fill(options.color)
        # self.rect = pygame.rect.Rect(options.x, options.y, options.w, options.h)
        self.rect = self.image.get_rect()
        self.rect.x = options.x
        self.rect.y = options.y

        self.moving = False
        self.collidable = False

    @property
    def left(self):
        return self.rect.left

    @property
    def right(self):
        return self.rect.right

    @property
    def top(self):
        return self.rect.top
 
    @property
    def bottom(self):
        return self.rect.bottom
 
    @property
    def width(self):
        return self.rect.width
 
    @property
    def height(self):
        return self.rect.height
 
    @property
    def center(self):
        return self.rect.center
 
    @property
    def centerx(self):
        return self.rect.centerx
 
    @property
    def centery(self):
        return self.rect.centery
 
    def move(self, dx, dy):
        self.rect = self.rect.move(dx, dy)
 
    def update(self):
        pass