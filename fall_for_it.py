import pygame
import random



### CONSTANTS ###



# Time
FPS = 60

# Sizes and Positions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
PLAYER_STARTING_POS_X = 300
PLAYER_STARTING_POS_Y = 300
SCREEN_START_SCROLL_HEIGHT = 350
TILE_SIZE = 50

# Other
MAX_WORLD_MAP_GRID_ROWS = 18
MAX_ROWS_WITHOUT_PLAT = 5
MAX_PLAYER_HP = 3

### CLASSES ###



# Class: Player
class Player():

    def __init__(self, starting_X, starting_Y):
        
        playerImgIdle = pygame.image.load('img/Player/Player_Idle.png')
        self.image = pygame.transform.scale(playerImgIdle,(40,30))
        self.rect = self.image.get_rect()    
        self.rect.x = starting_X
        self.starting_X = starting_X
        self.rect.y = starting_Y
        self.starting_Y = starting_Y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.vel_y = 0 
        self.jumped = True
        self.scroll = 0
        self.clock_sum = 0
        self.old_time = 1
        self.old_frames = 1
        
        self.playerHP = MAX_PLAYER_HP
        self.playerTookDamage = False
        self.alive = True

    def update(self):

        #Player movement
        new_x = 0
        new_y = 0
        key = pygame.key.get_pressed()
        
        if key [pygame.K_UP] and self.jumped == False and self.vel_y == 0:
            self.vel_y = -20
            self.jumped = True
            
        if key[pygame.K_LEFT]:
            new_x -= 5 
            
        if key[pygame.K_RIGHT]:
            new_x += 5 

        #Animations
        if key[pygame.K_RIGHT] == False and key[pygame.K_LEFT] == False:
            playerImgIdle = pygame.image.load('img/Player/Player_Idle.png')
            self.image = pygame.transform.scale(playerImgIdle, (40, 30)) 
            
        if key[pygame.K_RIGHT] == True and key[pygame.K_LEFT] == False:
            playerImgRight = pygame.image.load('img/Player/Player_Right.png')
            self.image = pygame.transform.scale(playerImgRight, (40, 30))
            
        if key[pygame.K_RIGHT] == False and key[pygame.K_LEFT] == True:
            playerImgLeft = pygame.image.load('img/Player/Player_Left.png')
            self.image = pygame.transform.scale(playerImgLeft, (40, 30))
            
        if self.vel_y < 0:
            playerImgUp = pygame.image.load('img/Player/Player_Up.png')
            self.image = pygame.transform.scale(playerImgUp, (30, 40))
            
        if self.vel_y > 0:
            playerImgDown = pygame.image.load('img/Player/Player_Down.png')
            self.image = pygame.transform.scale(playerImgDown, (30, 40))

        # Gravity   
        self.vel_y += 1
        
        if self.vel_y > 10:
            self.vel_y = 10
            
        new_y += self.vel_y

        self.standingOnTile = False
        self.sideTouchingDamage = False
        # Collisions
        for tile in world.tile_list:
            
            # Y
            if tile[1].colliderect(self.rect.x, self.rect.y + new_y, self.width, self.height):    
                self.jumped = False
                
                if(tile[2] == 3):
                    self.damage_player()
                
                if(tile[2] == 2):
                    self.standingOnTile = True
                
                # Below ground corrections
                if self.vel_y < 0:
                    new_y = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                    
                # Above ground corrections
                elif self.vel_y >= 0:
                    new_y = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                
            # X
            if tile[1].colliderect(self.rect.x + new_x, self.rect.y, self.width, self.height):   
                new_x = 0

                if tile[2] == 3:
                    self.sideTouchingDamage = True     
                    
        # If Player is standing on tile and side-touches spike, it gets damaged
        if self.standingOnTile and self.sideTouchingDamage:
            self.damage_player()       
        
        # Update Player Position
        self.rect.x += new_x
        self.rect.y += new_y
        
        # Update Scroll Caused by Player Position
        self.scroll = 0

        if self.rect.y > SCREEN_START_SCROLL_HEIGHT:
            self.scroll = self.rect.y - SCREEN_START_SCROLL_HEIGHT
            self.rect.y = SCREEN_START_SCROLL_HEIGHT
            
        game_screen.blit(self.image, self.rect)

        
    def damage_player(self):
        
        # Possible animations... etc
        self.playerHP -= 1
        self.playerTookDamage = True
        
        if self.playerHP <= 0:
            self.kill_player()


    def kill_player(self):
        
        # Possible animations... etc
        self.alive = False
        pass
    
    def reset_player_pos(self):
        
        self.rect.x = self.starting_X
        self.rect.y = self.starting_Y
        
    def did_player_take_damage(self):
        
        if self.playerTookDamage:
            self.playerTookDamage = False
            return True
        
        return False
        

# Class: World Map       
class WorldMap():

    def __init__(self):
        
        # World Map Trap Layouts Grid Definitions
        self.no_plat_row = [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 9, 9 ]
        self.plat_layouts = [
            [ 1, 2, 2, 2, 2, 2, 2, 0, 0, 1, 9, 9 ],
            [ 1, 2, 2, 2, 2, 2, 0, 0, 0, 1, 9, 9 ],
            [ 1, 2, 2, 2, 2, 0, 0, 0, 0, 1, 9, 9 ],
            [ 1, 2, 2, 2, 0, 0, 0, 0, 0, 1, 9, 9 ],
            [ 1, 2, 2, 0, 0, 0, 0, 0, 0, 1, 9, 9 ],
            [ 1, 2, 0, 0, 0, 0, 0, 0, 0, 1, 9, 9 ],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 2, 1, 9, 9 ],
            [ 1, 0, 0, 0, 0, 0, 0, 2, 2, 1, 9, 9 ],
            [ 1, 0, 0, 0, 0, 0, 2, 2, 2, 1, 9, 9 ],
            [ 1, 0, 0, 0, 0, 2, 2, 2, 2, 1, 9, 9 ],
            [ 1, 0, 0, 0, 2, 2, 2, 2, 2, 1, 9, 9 ],
            [ 1, 0, 0, 2, 2, 2, 2, 2, 2, 1, 9, 9 ],

            [ 1, 3, 3, 2, 3, 3, 2, 0, 0, 1, 9, 9 ],
            [ 1, 3, 2, 3, 2, 3, 0, 0, 0, 1, 9, 9 ],
            [ 1, 2, 3, 2, 3, 0, 0, 0, 0, 1, 9, 9 ],
            [ 1, 3, 3, 2, 0, 0, 0, 0, 0, 1, 9, 9 ],
            [ 1, 2, 3, 0, 0, 0, 0, 0, 0, 1, 9, 9 ],
            [ 1, 3, 0, 0, 0, 0, 0, 0, 0, 1, 9, 9 ],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 3, 1, 9, 9 ],
            [ 1, 0, 0, 0, 0, 0, 0, 3, 2, 1, 9, 9 ],
            [ 1, 0, 0, 0, 0, 0, 2, 3, 2, 1, 9, 9 ],
            [ 1, 0, 0, 0, 0, 3, 2, 2, 3, 1, 9, 9 ],
            [ 1, 0, 0, 0, 2, 3, 3, 2, 3, 1, 9, 9 ],
            [ 1, 0, 0, 2, 3, 3, 2, 3, 2, 1, 9, 9 ],
            
            self.no_plat_row
            ]
        
        # World Map Grid Initial Definition
        self.reset_map()

        # Normal Block Definitions
        self.grass_block_img = pygame.image.load('img/map_block_grass.png')
        self.grass_block_surface = pygame.transform.scale(self.grass_block_img,(TILE_SIZE, TILE_SIZE)) 
        self.grass_block_rect = self.grass_block_surface.get_rect()

        # Grass Block Definitions
        self.block_img = pygame.image.load('img/map_block.png')
        self.block_surface = pygame.transform.scale(self.block_img,(TILE_SIZE, TILE_SIZE))
        self.block_rect = self.block_surface.get_rect()

        # Spikes Block Definitions
        self.spikes_img = pygame.image.load('img/Spikes.png')
        self.spikes_surface = pygame.transform.scale(self.spikes_img,(TILE_SIZE, TILE_SIZE+30))
        self.spikes_rect = self.spikes_surface.get_rect()
        
        # Other Variables
        self.gridbox_counter = 0
        self.map_scroll = 0
    
    # Stores player object    
    def update_player(self, curr_player):
        self.curr_player = curr_player
        
    # Update 
    def update_scrolling_map(self):
        
        self.map_scroll = self.map_scroll + self.curr_player.scroll

        if self.map_scroll > TILE_SIZE:
            self.map_scroll = self.map_scroll % TILE_SIZE
            
            if self.gridbox_counter <= MAX_ROWS_WITHOUT_PLAT:
                self.gridbox_counter += 1
                self.world_grid.pop(0)
                self.world_grid.append(self.no_plat_row)
                
            else :
                rand_int = random.randint(0, len(self.plat_layouts)-1)
                self.gridbox_counter = 0
                self.world_grid.pop(0)
                self.world_grid.append(self.plat_layouts[rand_int])    


    def draw(self):
        
        self.update_scrolling_map()
        
        self.tile_list = []
        row_count = 0
        for row in self.world_grid:
                col_count = 0

                for tile in row:
                    
                    if tile == 1:
                        self.block_rect = self.block_surface.get_rect()
                        self.block_rect.x = col_count * TILE_SIZE
                        self.block_rect.y = row_count * TILE_SIZE - self.map_scroll
                        tile_tpl = (self.block_surface, self.block_rect, tile)
                        self.tile_list.append(tile_tpl)

                    if tile == 2:
                        self.grass_block_rect = self.grass_block_surface.get_rect()
                        self.grass_block_rect.x = col_count * TILE_SIZE
                        self.grass_block_rect.y = row_count * TILE_SIZE - self.map_scroll
                        tile_tpl = (self.grass_block_surface, self.grass_block_rect, tile)
                        self.tile_list.append(tile_tpl)
                    
                    if tile == 3:
                        self.spikes_rect = self.spikes_surface.get_rect()
                        self.spikes_rect.x = col_count * TILE_SIZE
                        self.spikes_rect.y = row_count * TILE_SIZE - (self.map_scroll + 30)
                        tile_tpl = (self.spikes_surface, self.spikes_rect, tile)
                        self.tile_list.append(tile_tpl)

                    col_count += 1

                row_count += 1

        for tile in self.tile_list:
            game_screen.blit(tile[0],tile[1])
    
    
    def reset_map(self):
        self.world_grid = []
        for _ in range(MAX_WORLD_MAP_GRID_ROWS):
            self.world_grid.append(self.no_plat_row)
    

class Spikes(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        spike_img = pygame.image.load('img/Spike.png')
        self.image = pygame.transform.scale(spike_img,(40,30))
        self.rect = self.image.get_rect()    
        self.rect.x = x
        self.rect.y = y
     
 
 
### MAIN CODE ###       
      
      
        
# Intialize Pygame
pygame.init()

# Start Time Ticks
clock = pygame.time.Clock()

# Create the screen
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Title and Icon
pygame.display.set_caption("Fall for it")
icon = pygame.image.load('img/Fall_for_it_Game_Icon.png')
pygame.display.set_icon(icon)

# Initalize Game Objects
world = WorldMap()
player = Player(PLAYER_STARTING_POS_X, PLAYER_STARTING_POS_Y)
world.update_player(player)

# Game Loop
game_running = True
while game_running:

    # Game Background Color
    game_screen.fill((0,156,242))
    
    clock.tick(FPS)

    world.draw()
    player.update()
  
    pygame.display.update()
    
    if player.did_player_take_damage():
        world.reset_map()
        player.reset_player_pos()
        
    if player.alive == False:
        print("DEADGE")
        # reset world or something
        pass

    for event in pygame.event.get():
        # Close Window
        if event.type == pygame.QUIT:
            game_running = False


              
               
    
    
    