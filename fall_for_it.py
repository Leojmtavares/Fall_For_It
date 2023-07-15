import pygame
from pygame import mixer
import random
import time



### CONSTANTS ###



# Time
FPS = 60

# Sizes and Positions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 900
PLAYER_STARTING_POS_X = 300
PLAYER_STARTING_POS_Y = 300
SCREEN_START_SCROLL_HEIGHT = 350
TILE_SIZE = 50

# Other
MAX_WORLD_MAP_GRID_ROWS = 19
MAX_ROWS_WITHOUT_PLAT = 5
MAX_PLAYER_HP = 3

### CLASSES ###



# Class: Player
class Player():

    def __init__(self, world, starting_X, starting_Y):
        
        playerImgIdle = pygame.image.load('img/Player/Player_Idle.png')
        self.image = pygame.transform.scale(playerImgIdle,(40,30))
        self.rect = self.image.get_rect() 
        self.world = world   
        self.rect.x = starting_X
        self.starting_X = starting_X
        self.rect.y = starting_Y
        self.starting_Y = starting_Y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.vel_y = 0 
        self.jumped = True
        self.scroll = 0
        self.scrollsum = 0
        self.clock_sum = 0
        self.old_time = 1
        self.old_frames = 1
        self.last_score = 0
        
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
        for tile in self.world.tile_list:
            
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

        self.scrollsum += self.scroll

        game_screen.blit(self.image, self.rect)

        
    def damage_player(self):
        
        self.playerHP -= 1
        self.playerTookDamage = True
        
        if self.playerHP <= 0:
            self.alive = False
    
    
    def reset_player_pos(self):
        
        self.rect.x = self.starting_X
        self.rect.y = self.starting_Y


    def did_player_take_damage(self):
        
        if self.playerTookDamage:
            self.playerTookDamage = False
            return True
        
        return False


    def full_player_reset(self):
        self.reset_player_pos()
        self.alive = True
        self.last_score = self.scrollsum
        self.scrollsum = 0
        self.playerHP = MAX_PLAYER_HP

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

# Class: User Interface
class UserInterface():

    def __init__(self, player, world):

        self.player = player
        self.world = world

        life_img_tmp = pygame.image.load('img/Life.png')
        self.life_img = pygame.transform.scale(life_img_tmp,(30,30))

        self.score_font = pygame.font.Font('PixelEmulator.ttf', 20)


    # Display player HP
    def display_hp(self, curr_hp):
        
        for hp in range(curr_hp):
            game_screen.blit(self.life_img, (500+35*hp, 50))


    def draw_ui(self):

        self.display_hp(self.player.playerHP)
        self.draw_score()
        

    def draw_score(self):

        score_text = self.score_font.render(str(self.player.scrollsum), True, (255,255,255))
        center_score_x = int(self.score_font.size(str(self.player.scrollsum))[0]/2)
        game_screen.blit(score_text, (550 - center_score_x , 100))

# Class: Button
class Button():

    def __init__(self, img, buttonPos, buttonSmallSizes, buttonBigSizes):
        
        self.isHoveringButton = False
        self.buttonOriginalX = buttonPos[0]
        self.buttonOriginalY = buttonPos[1]
        self.buttonSmallLength = buttonSmallSizes[0]
        self.buttonSmallHeight = buttonSmallSizes[1]
        self.buttonBigLength = buttonBigSizes[0]
        self.buttonBigHeight = buttonBigSizes[1]
        
        self.buttonLength = self.buttonSmallLength
        self.buttonHeight = self.buttonSmallHeight
        self.buttonX = self.buttonOriginalX
        self.buttonY = self.buttonOriginalY
        
        self.img = img
        

    def update(self):
        
        img_scale = pygame.transform.scale(self.img, (self.buttonLength, self.buttonHeight))
        game_screen.blit(img_scale, (self.buttonX, self.buttonY))
        

    def checkMousePosition(self, mousePos):
        
        if (mousePos[0] > self.buttonX and mousePos[0] < self.buttonX + self.buttonLength and 
            mousePos[1] > self.buttonY and mousePos[1] < self.buttonY + self.buttonHeight):
            
            self.buttonX = self.buttonOriginalX - (self.buttonBigLength - self.buttonSmallLength)/2
            self.buttonY = self.buttonOriginalY - (self.buttonBigHeight - self.buttonSmallHeight)/2
            
            self.buttonLength = self.buttonBigLength
            self.buttonHeight = self.buttonBigHeight
            
            self.isHoveringButton = True
            
        else:
            
            self.buttonX = self.buttonOriginalX
            self.buttonY = self.buttonOriginalY
            
            self.buttonLength = self.buttonSmallLength
            self.buttonHeight = self.buttonSmallHeight
            
            self.isHoveringButton = False
        

#Class: Window Selector
class WindowSelector():

    def __init__(self):
        self.curr_menu = 0
        self.quit_order = False

        # Initalize Game Objects
        self.world = WorldMap()
        self.player = Player(self.world, PLAYER_STARTING_POS_X, PLAYER_STARTING_POS_Y)
        self.ui = UserInterface(self.player, self.world)
        
        self.playButton =        Button(pygame.image.load('img/Buttons/Button_Play.png'),       (214,250),(172,48),(215,60))
        self.leaderboardButton = Button(pygame.image.load('img/Buttons/Button_Leaderboard.png'),(56,400),(488,48),(549,54))
        self.quitButton =        Button(pygame.image.load('img/Buttons/Button_Quit.png'),       (214,550),(172,48),(215,60))
        
        self.world.update_player(self.player)


    def main_menu(self):
        main_menu_running = True
        
        while main_menu_running:
            
            # Game Background Color
            game_screen.fill((0,156,242))
            
            self.playButton.checkMousePosition(pygame.mouse.get_pos())
            self.playButton.update()
            
            self.leaderboardButton.checkMousePosition(pygame.mouse.get_pos())
            self.leaderboardButton.update()
            
            self.quitButton.checkMousePosition(pygame.mouse.get_pos())
            self.quitButton.update()
            
            # Show cursor hand if hovering button
            if self.playButton.isHoveringButton or \
               self.leaderboardButton.isHoveringButton or \
               self.quitButton.isHoveringButton:
                   
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                
            else:
                
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
            clock.tick(FPS)

            pygame.display.update()


            for event in pygame.event.get():
                # Close Window
                if event.type == pygame.QUIT:
                    main_menu_running = False
                    self.quit_order = True
                    
                if event.type == pygame.MOUSEBUTTONDOWN and self.playButton.isHoveringButton:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    main_menu_running = False
                    self.curr_menu = 1
                    
                if event.type == pygame.MOUSEBUTTONDOWN and self.leaderboardButton.isHoveringButton:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    main_menu_running = False
                    self.curr_menu = 2
                    
                if event.type == pygame.MOUSEBUTTONDOWN and self.quitButton.isHoveringButton:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    main_menu_running = False
                    self.quit_order = True
                
                
    
    
    def play_game(self):
        # Game Loop
        play_game_running = True
        while play_game_running:

            # Game Background Color
            game_screen.fill((0,156,242))
            
            clock.tick(FPS)

            self.world.draw()
            self.player.update()   
            self.ui.draw_ui()
            
            if self.player.did_player_take_damage():
                self.world.reset_map()
                self.player.reset_player_pos()

            if self.player.alive == False:
                self.world.reset_map()
                self.player.full_player_reset()
                self.curr_menu = 3
                play_game_running = False
                continue
                
            pygame.display.update()

            for event in pygame.event.get():
                # Close Window
                if event.type == pygame.QUIT:
                    play_game_running = False
                    self.quit_order = True

                        
    def game_over(self):
        
        game_over_font = pygame.font.Font('PixelEmulator.ttf', 100)
        game_text = game_over_font.render('Game', True, (255,255,255))
        over_text = game_over_font.render('Over!', True, (255,255,255))

        game_screen.fill((0,156,242))
        game_screen.blit(game_text, (150, 200))
        game_screen.blit(over_text, (150, 350)) 

        pygame.display.update()
        
        start_gameover_time = time.time()
        while time.time() - start_gameover_time < 2.0:
             
            for event in pygame.event.get():
                # Close Window
                if event.type == pygame.QUIT:
                    self.quit_order = True
                    break
        
        self.curr_menu = 2
        
        
    def leaderboard(self):

        # Prepare Screen
        game_screen.fill((0,156,242))
        
        # Obtain All Previous Scores
        leaderboard_scores = []
        
        leaderboard_file = open("Leaderboard.txt", "r")
        leaderboard_file_lines = leaderboard_file.readlines()
        leaderboard_file.close()
        
        for line in leaderboard_file_lines:
            
            line_split = line.split(";")
            leaderboard_scores.append((line_split[0], int(line_split[1])))
        
        leaderboardShift = 150
        # Display All Previous Scores and Title
        if len(leaderboard_scores) > 0 and \
            self.player.last_score > 0 and \
            (self.player.last_score > leaderboard_scores[len(leaderboard_scores) - 1][1] or len(leaderboard_scores) < 10):
            leaderboardShift = 0    
        
        leaderboard_title_text = pygame.font.Font('PixelEmulator.ttf', 48).render('LEADERBOARD', True, (255,255,255))
        game_screen.blit(leaderboard_title_text, (300 - leaderboard_title_text.get_size()[0]/2.0, leaderboardShift + 50))
        
        leaderboard_title_text = pygame.font.Font('PixelEmulator.ttf', 18).render('Press Enter', True, (255,255,255))
        game_screen.blit(leaderboard_title_text, (300 - leaderboard_title_text.get_size()[0]/2.0, 850))
        
        score_counter = 0
            
        for score in leaderboard_scores:
            
            score_player_name_text = pygame.font.Font('PixelEmulator.ttf', 28).render(str(score[0])+": ", True, (255,255,255))
            score_player_score_text = pygame.font.Font('PixelEmulator.ttf', 28).render(str(score[1]), True, (255,255,255))
            game_screen.blit(score_player_name_text,  (180, leaderboardShift + 150+40*score_counter))
            game_screen.blit(score_player_score_text, (300, leaderboardShift + 150+40*score_counter))
            score_counter += 1

        pygame.display.update()

        if len(leaderboard_scores) > 0 and \
            self.player.last_score > 0 and \
            (self.player.last_score > leaderboard_scores[len(leaderboard_scores) - 1][1] or len(leaderboard_scores) < 10):
            
            new_highscore_text_1 = pygame.font.Font('PixelEmulator.ttf', 38).render('New Leaderboard', True, (0,255,0))
            new_highscore_text_2 = pygame.font.Font('PixelEmulator.ttf', 38).render('Score!', True, (0,255,0))
            new_highscore_text_3 = pygame.font.Font('PixelEmulator.ttf', 24).render('Insert Name (4 digits):', True, (255,255,255))
            
            game_screen.blit(new_highscore_text_1, (300 - new_highscore_text_1.get_size()[0]/2.0, 600))
            game_screen.blit(new_highscore_text_2, (300 - new_highscore_text_2.get_size()[0]/2.0, 650))
            game_screen.blit(new_highscore_text_3, (300 - new_highscore_text_3.get_size()[0]/2.0, 730))
            
            # Waits for user to input name of new Highscore
            userIsWriting = True
            user_text = ""
            
            while userIsWriting:
                
                for event in pygame.event.get():
                    
                    if event.type == pygame.QUIT:
                        self.quit_order = True
                        return
            
                    if event.type == pygame.KEYDOWN:
                        
                        if event.key==pygame.K_RETURN:
                            userIsWriting = False
                            if user_text == "":
                                user_text = " "
                            break
            
                        # Check for backspace
                        if event.key == pygame.K_BACKSPACE:
            
                            # get text input from 0 to -1 i.e. end.
                            if len(user_text) > 0:
                                user_text = user_text[:-1]
                            
                        else:
                            if len(user_text) < 4:
                                user_text += event.unicode
                
                input_rect = pygame.Rect(235, 770, 130, 50)
                input_text_surface = pygame.font.Font('PixelEmulator.ttf', 38).render(user_text, True, (0,0,0))
                pygame.draw.rect(game_screen, pygame.Color(255,255,255), input_rect)
                game_screen.blit(input_text_surface, (input_rect.x+7, input_rect.y+2))
                
                pygame.display.flip()

            # Check position that new score will be inserted
            score_pos = 0
            for score in leaderboard_scores:
                if int(score[1]) < self.player.last_score:
                    break
                score_pos += 1
                
            # Create new score tupple with new score and with the lowest score removed if there is more than 10
            if len(leaderboard_scores) >= 10:
                last_pos = len(leaderboard_scores)-1
            else:
                last_pos = len(leaderboard_scores)

            new_leaderboard_scores = leaderboard_scores[:score_pos] + \
                 [(str(user_text.upper()), self.player.last_score)] + \
                 leaderboard_scores[score_pos:last_pos]
            
            leaderboard_file = open("Leaderboard.txt", "w")
            
            for score in new_leaderboard_scores:
                leaderboard_file.write(str(score[0]) + ";" + str(score[1]) + "\n")
                
            leaderboard_file.close()
        
        else:
            stayInLeaderboard = True
            start_leaderboard_time = time.time()
            while time.time() - start_leaderboard_time < 2.0 and stayInLeaderboard:
                
                for event in pygame.event.get():
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            stayInLeaderboard = False
                            break
                        
                    # Close Window
                    if event.type == pygame.QUIT:
                        self.quit_order = True
                        stayInLeaderboard = False
                        break
        
        self.player.last_score = 0
        
        window_selector.curr_menu = 0
        
        
        
        


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

# Play music
mixer.init()
mixer.music.load("background_music.mp3")
mixer.music.set_volume(0.04)
mixer.music.play(-1)


window_selector = WindowSelector()

window_running = True
while window_running:

    # Window Selection 
    if window_selector.curr_menu == 0:
        window_selector.main_menu()   

    elif window_selector.curr_menu == 1:
        window_selector.play_game()
        
    elif window_selector.curr_menu == 2:
        window_selector.leaderboard()

    elif window_selector.curr_menu == 3:
        window_selector.game_over()

    # Close Window
    if window_selector.quit_order:
        window_running = False
     
    