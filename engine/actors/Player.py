import pygame

from engine.Spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self, options):
        super().__init__()
        
        self.color = options.color
        self.speed = options.speed

        self.spritesheet = Spritesheet("MC_TopViewSheet.png") # Starting with TopView
        self.image = self.spritesheet.getImage(163, 6, 24, 45)

        # TODO: Set up walking frame arrays (ideally via some config code)

        # self.image = some reference to a blit image
        self.rect = self.image.get_rect() # or more static bounding box for AABB (axis-aligned bounding box)
        # self.rect = pygame.rect.Rect(options.x, options.y, options.w, options.h)

        self.moving = False
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.direction = None

        self.collidable = True

        self.CoolDown = 300

    def toggle_movement(self, direction):
        if direction == 'left':
            self.moving_left = not self.moving_left
            # self.image = self.spritesheet.getImage(263, 6, 24, 45)
        elif direction == 'right':
            self.moving_right = not self.moving_right
            # self.image = self.spritesheet.getImage(363, 6, 24, 45)
        elif direction == 'up':
            self.moving_up = not self.moving_up
            # self.image = self.spritesheet.getImage(63, 6, 24, 45)
        elif direction == 'down':
            self.moving_down = not self.moving_down
            # self.image = self.spritesheet.getImage(163, 6, 24, 45)

    def move(self, dx, dy):
        self.rect = self.rect.move(dx, dy)

    def update(self):
        # Movement Update
        self.moving = False
        self.direction = ""
        if self.moving_left:
            dx = -(min(self.speed, self.rect.left))
            self.moving = True
            self.direction = 'left '
            self.image = self.spritesheet.getImage(268, 5, 16, 45)
        elif self.moving_right:
            dx = min(self.speed, 800 - self.rect.right)
            self.moving = True
            self.direction = 'right '
            self.image = self.spritesheet.getImage(368, 5, 16, 45)
        if self.moving_up:
            dy = -(min(self.speed, self.rect.top))
            self.moving = True
            self.direction += 'up'
            self.image = self.spritesheet.getImage(63, 6, 24, 45)
        elif self.moving_down:
            dy = min(self.speed, 600 - self.rect.bottom)
            self.moving = True
            self.direction += 'down'
            self.image = self.spritesheet.getImage(163, 6, 24, 45)
            
        if not self.moving:
            self.direction = None
            self.image = self.spritesheet.getImage(163, 6, 24, 45)
            return

        self.direction = self.direction.strip()
            
        if not 'dx' in vars():
            dx = 0
        if not 'dy' in vars():
            dy = 0
            
        self.move(dx, dy)

    # def draw(self, surface):
    #     self.draw(surface)

    def drawDebug(self, surface):
        # font = pygame.font.Font(pygame.font.get_default_font(), 12)
        font = pygame.font.SysFont("sysfont10", 30)
        text = font.render("Direction: %s" % self.direction, False, (255, 255, 255))
        textRect = text.get_rect()
        surface.fill((255, 0, 255))
        surface.blit(text, textRect)
        # xwidth = 800
        # yhight = 600
        # self.screen = pygame.surface.Surface((800, 600))
        # surface.blit(text, (0, 0))