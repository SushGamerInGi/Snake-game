from random import randrange
import pygame

SCREEN_SIZE = WIDTH, HEIGHT = 800, 800 
FPS = 6
BLOCK_SIZE = 40
BACKGROUND_COLOR = (35, 35, 35)

screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

run = True
pause = False

class Sprite(pygame.sprite.Sprite):
    def __init__(self, *groups, color, coordinate):
        super().__init__(*groups)
        self.image = pygame.Surface(size=(BLOCK_SIZE, BLOCK_SIZE))
        x, y = coordinate
        self.rect = self.image.get_rect(x=x, y=y)
        self.image.fill(color)

class Head(Sprite):
    dx, dy = 0, 0
    
    class Segment(Sprite):
        def __init__(self, *groups, color, coordinate):
            super().__init__(*groups, color=color, coordinate=coordinate)

    def __init__(self, *groups, color, coordinate):
        super().__init__(*groups, color=color, coordinate=coordinate)
        self.segments = pygame.sprite.Group()

    def update(self):
        key = pygame.key.get_pressed()
        
        if key[pygame.K_w] or key[pygame.K_UP] :
            self.dx, self.dy = 0, -1
            
        if key[pygame.K_s] or key [pygame.K_DOWN]:
            self.dx, self.dy = 0, +1
            
        if key[pygame.K_a] or key [pygame.K_LEFT]:
            self.dx, self.dy = -1, 0
        
        if key[pygame.K_d] or key [pygame.K_RIGHT]:
            self.dx, self.dy = 1, 0
        
        if not(self.dx == 0 and self.dy ==0):
            center = self.rect.center
            for segment in self.segments.sprites():
                segment.rect.center, center = center, segment.rect.center
            
            self.rect.x += BLOCK_SIZE * self.dx
            self.rect.y += BLOCK_SIZE * self.dy

            segment_hint = pygame.sprite.spritecollide(self, self.segments, False)
            if segment_hint:
                exit()
        
            if self.rect.x < 0 or self.rect.x >= WIDTH or self.rect.y < 0 or self.rect.y >= HEIGHT:
                exit()  
    def add_segment(self):
        last_segment = self.segments.sprites()[-1] if self.segments.sprites() else self
        self.Segment(all_sprites, self.segments, color="#143F14", coordinate=(
            last_segment.rect.x-self.dx*BLOCK_SIZE, 
            last_segment.rect.y-self.dy*BLOCK_SIZE
        ))


class Apple(Sprite):
    def __init__(self, *groups, color="#FF0000"):
        coordinate = (randrange(BLOCK_SIZE, WIDTH - BLOCK_SIZE, BLOCK_SIZE),
                    randrange(BLOCK_SIZE, HEIGHT - BLOCK_SIZE, BLOCK_SIZE))
        super().__init__(*groups, color=color, coordinate=coordinate)
    

all_sprites = pygame.sprite.Group()
apples = pygame.sprite.Group()
head = Head(all_sprites, color="#00FF00", coordinate=(randrange(BLOCK_SIZE, WIDTH - BLOCK_SIZE, BLOCK_SIZE), 
                        randrange(BLOCK_SIZE, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)))
apple = Apple(all_sprites, apples)

while run:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                run = False
            case pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

    screen.fill(BACKGROUND_COLOR)
    
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, "#606060", (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, "#606060", (0, y), (WIDTH, y))
    
    all_sprites.update()
    
    
    # if head.rect.colliderect(apple.rect):
    #     head.grow_snake()  
    #     apple.kill()  
    #     apple = Apple(all_sprites)  

    apple_hint = pygame.sprite.spritecollide(head, apples, True)
    if apple_hint:
        for apple in apple_hint:
            Apple(all_sprites, apples)  
            head.add_segment() 
    
    all_sprites.draw(screen)

    pygame.display.update()

pygame.quit()