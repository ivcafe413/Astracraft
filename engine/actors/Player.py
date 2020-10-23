import pygame

from engine.Spritesheet import Spritesheet
from engine.actors.GObject import GObject

class Player(GObject):
    def __init__(self, options):
        super().__init__(options)
        
        # self.color = options.color
        self.speed = options.speed

        self.spritesheet = Spritesheet("MC_TopViewSheet.png") # Starting with TopView
        self.image = self.spritesheet.getImage(163, 6, 24, 45)

        # TODO: Set up walking frame arrays (ideally via some config code)

        # self.image = some reference to a blit image
        self.rect = self.image.get_rect() # or more static bounding box for AABB (axis-aligned bounding box)
        self.rect.x = options.x
        self.rect.y = options.y
        # self.rect = pygame.rect.Rect(options.x, options.y, options.w, options.h)

        # self.moving = False # Set in GObject
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.direction = None

        self.collidable = True # Override Collidable

        self.WalkUp = []
        self.WalkDown = []
        self.WalkLeft = []
        self.WalkRight = []

        self.spritesheet = Spritesheet("MC_TopViewSheet.png")
        image = self.spritesheet.getImage(13, 6, 24, 45)
        self.WalkUp.append(image)
        image = self.spritesheet.getImage(63, 6, 24, 44)
        self.WalkUp.append(image)
        image = self.spritesheet.getImage(13, 55, 24, 45)
        self.WalkUp.append(image)
        image = self.spritesheet.getImage(113, 6, 24, 45)
        self.WalkDown.append(image)
        image = self.spritesheet.getImage(163, 6, 24, 44)
        self.WalkDown.append(image)
        image = self.spritesheet.getImage(113, 55, 24, 45)
        self.WalkDown.append(image)
        image = self.spritesheet.getImage(221, 5, 16, 45)
        self.WalkLeft.append(image)
        image = self.spritesheet.getImage(267, 5, 16, 45)
        self.WalkLeft.append(image)
        image = self.spritesheet.getImage(220, 55, 16, 45)
        self.WalkLeft.append(image)
        image = self.spritesheet.getImage(318, 5, 16, 45)
        self.WalkRight.append(image)
        image = self.spritesheet.getImagec
        self.WalkRight.append(image)
        image = self.spritesheet.getImage(319, 55, 16, 45)
        self.WalkRight.append(image)

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
        pos = self.rect.x + self.screen.world_shift
        # pos = 100
        if self.moving_left:
            dx = -(min(self.speed, self.rect.left))
            self.moving = True
            self.direction = 'left '
            self.image = self.spritesheet.getImage(267, 5, 16, 45)
            frame = (pos // 30) % len(self.WalkLeft)
            self.image = self.WalkLeft[frame]
        elif self.moving_right:
            dx = min(self.speed, 800 - self.rect.right)
            self.moving = True
            self.direction = 'right '
            self.image = self.spritesheet.getImage(368, 5, 16, 45)
            frame = (pos // 30) % len(self.WalkUp)
            self.image = self.WalkRight[frame]
        if self.moving_up:
            dy = -(min(self.speed, self.rect.top))
            self.moving = True
            self.direction += 'up'
            self.image = self.spritesheet.getImage(63, 6, 24, 44)
            frame = (pos // 30) % len(self.WalkUp)
            self.image = self.WalkUp[frame]
        elif self.moving_down:
            dy = min(self.speed, 600 - self.rect.bottom)
            self.moving = True
            self.direction += 'down'
            self.image = self.spritesheet.getImage(163, 6, 24, 44)
            frame = (pos // 30) % len(self.WalkUp)
            self.image = self.WalkDown[frame]
            
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
        font = pygame.font.SysFont("sysfont10", 24)
        text = font.render("Direction: %s" % self.direction, False, (255, 255, 255))
        textRect = text.get_rect()
        # surface.fill((255, 0, 255))
        surface.blit(text, textRect)
        # xwidth = 800
        # yhight = 600
        # self.screen = pygame.surface.Surface((800, 600))
        # surface.blit(text, (0, 0))