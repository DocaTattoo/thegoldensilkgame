import random
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE, WHITE, LIGHT_GRAY
from player import Player
from platform_obj import Platform
from collectible import Collectible
from particle import Particle
from camera import Camera
from character import Character
from scenario import Scenario
from button import Button

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()

        self.font_small = pygame.font.Font(None, 30)
        self.font_medium = pygame.font.Font(None, 42)
        self.font_title = pygame.font.Font(None, 72)

        self.running = True
        self.state = "menu"
        self.volume = 0.7
        self.sound_enabled = True

        self.characters = [
            Character("Ragazzo", (60,150,255), "Stella", (255,230,50)),
            Character("Chef", (240,80,80), "Hamburger", (190,120,50)),
            Character("Tatuatore", (130,70,200), "Cartuccia", (80,80,90))
        ]
        self.selected_character = 0

        self.scenarios = [
            Scenario("Prato", (135,206,235), (70,180,80), (80,190,90)),
            Scenario("Tramonto", (245,155,110), (100,80,55), (255,190,100)),
            Scenario("Notte", (25,35,80), (100,110,150), (220,220,130)),
            Scenario("Spazio", (15,10,35), (100,80,170), (120,220,255))
        ]

        self.player = Player()
        self.camera = Camera()
        self.platforms, self.collectibles, self.particles = [], [], []
        self.score = 0
        self.collected = 0
        self.high_score = 0
        self.total_collected = 0
        self.platform_count = 0
        self.last_platform_y = SCREEN_HEIGHT - 70
        self.current_scenario = 0
        self.game_over = False
        self.paused = False

        self.create_buttons()
        self.start_game()

    def create_buttons(self):
        self.play_button = Button(80,230,320,70,"GIOCA")
        self.characters_button = Button(80,320,320,70,"PERSONAGGI")
        self.settings_button = Button(80,410,320,70,"IMPOSTAZIONI")
        self.stats_button = Button(80,500,320,70,"STATISTICHE")
        self.back_button = Button(80,650,320,65,"INDIETRO")

    def start_game(self):
        self.platforms.clear()
        self.collectibles.clear()
        self.particles.clear()
        self.camera.reset()
        self.score = self.collected = self.platform_count = 0
        self.current_scenario = 0
        self.game_over = self.paused = False
        self.last_platform_y = SCREEN_HEIGHT - 70
        self.platforms.append(Platform(SCREEN_WIDTH//2-100, SCREEN_HEIGHT-70, 200))
        self.player.reset(SCREEN_WIDTH//2-self.player.width//2, SCREEN_HEIGHT-140)
        for _ in range(15):
            self.generate_platform()

    def get_difficulty(self):
        return min(self.platform_count // 10, 15)

    def generate_platform(self):
        difficulty = self.get_difficulty()
        vertical_distance = 80 + difficulty * 3
        width = max(75, 145 - difficulty * 4)
        previous = self.platforms[-1]
        min_x = max(0, int(previous.x - 120))
        max_x = min(SCREEN_WIDTH - width, int(previous.x + previous.width - 20))
        if max_x < min_x:
            min_x, max_x = 0, SCREEN_WIDTH - width
        x = random.randint(min_x, max_x)
        y = self.last_platform_y - vertical_distance
        self.platforms.append(Platform(x,y,width))
        self.last_platform_y = y
        self.platform_count += 1

        if self.platform_count % 10 == 0:
            self.current_scenario = (self.current_scenario + 1) % len(self.scenarios)

        if random.random() < 0.75:
            c = self.characters[self.selected_character]
            self.collectibles.append(Collectible(x+width/2, y-55, c.item_name, c.item_color))

    def update(self):
        if self.game_over or self.paused:
            return
        self.player.update(self.platforms)
        while len(self.platforms) < 20 or self.platforms[-1].y - self.camera.y > -200:
            self.generate_platform()
        self.camera.update(self.player)

        for item in self.collectibles:
            item.update()
            if not item.collected and self.player.rect.colliderect(item.rect):
                self.collect_item(item)

        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.is_alive()]
        self.platforms = [p for p in self.platforms if p.y-self.camera.y < SCREEN_HEIGHT+200]
        self.collectibles = [c for c in self.collectibles if c.base_y-self.camera.y < SCREEN_HEIGHT+200]

        self.score = max(self.score, int(max(0,-self.camera.y)/10))
        if self.player.y - self.camera.y > SCREEN_HEIGHT + 100:
            self.end_game()

    def collect_item(self, item):
        item.collected = True
        self.score += 10
        self.collected += 1
        self.player.collect_item()
        for _ in range(18):
            self.particles.append(Particle(item.x, item.get_y(), item.color))

    def end_game(self):
        self.game_over = True
        self.high_score = max(self.high_score, self.score)
        self.total_collected += self.collected

    def draw_background(self):
        s = self.scenarios[self.current_scenario]
        self.screen.fill(s.background_color)
        if self.current_scenario == 1:
            pygame.draw.circle(self.screen, (255,220,80), (SCREEN_WIDTH-70,90), 45)
        elif self.current_scenario in (2,3):
            random.seed(5 if self.current_scenario == 2 else 10)
            for _ in range(50 if self.current_scenario == 2 else 40):
                x=random.randint(0,SCREEN_WIDTH); y=random.randint(0,SCREEN_HEIGHT)
                pygame.draw.circle(self.screen,(240,240,220) if self.current_scenario==2 else (180,220,255),
                                   (x,y), random.randint(1,3) if self.current_scenario==3 else 2)
            random.seed()

    def draw_game(self):
        self.draw_background()
        scenario = self.scenarios[self.current_scenario]
        for p in self.platforms:
            if -100 < p.y-self.camera.y < SCREEN_HEIGHT+100:
                p.draw(self.screen,self.camera,scenario)
        for c in self.collectibles:
            if -100 < c.base_y-self.camera.y < SCREEN_HEIGHT+100:
                c.draw(self.screen,self.camera)
        for p in self.particles:
            p.draw(self.screen)
        self.player.draw(self.screen,self.camera,self.characters[self.selected_character])
        self.draw_hud()
        if self.paused:
            self.draw_overlay("PAUSA","Tocca per continuare")
        if self.game_over:
            self.draw_overlay("GAME OVER",f"Punteggio: {self.score} - Tocca per ricominciare")

    def draw_hud(self):
        self.draw_text(f"Punti: {self.score}",self.font_small,WHITE,15,15,False)
        self.draw_text(f"Oggetti: {self.collected}",self.font_small,WHITE,15,48,False)
        self.draw_text(self.scenarios[self.current_scenario].name,self.font_small,WHITE,SCREEN_WIDTH-15,15,False)
        pygame.draw.rect(self.screen,(0,0,0),(SCREEN_WIDTH-65,50,50,45),border_radius=10)
        self.draw_text("II",self.font_small,WHITE,SCREEN_WIDTH-40,73)

    def draw_overlay(self,title,subtitle):
        overlay=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
        overlay.fill((0,0,0,180))
        self.screen.blit(overlay,(0,0))
        self.draw_text(title,self.font_title,WHITE,SCREEN_WIDTH//2,SCREEN_HEIGHT//2-60)
        self.draw_text(subtitle,self.font_small,WHITE,SCREEN_WIDTH//2,SCREEN_HEIGHT//2+20)

    def draw_menu(self):
        self.screen.fill((35,40,75))
        self.draw_text(GAME_TITLE,self.font_title,WHITE,SCREEN_WIDTH//2,110)
        for b in (self.play_button,self.characters_button,self.settings_button,self.stats_button):
            b.draw(self.screen,self.font_medium)
        self.draw_text("Versione prototipo",self.font_small,LIGHT_GRAY,SCREEN_WIDTH//2,SCREEN_HEIGHT-40)

    def draw_characters(self):
        self.screen.fill((30,35,60))
        self.draw_text("PERSONAGGI",self.font_title,WHITE,SCREEN_WIDTH//2,80)
        for i,c in enumerate(self.characters):
            x=40+i*145
            rect=pygame.Rect(x,180,125,300)
            pygame.draw.rect(self.screen,(80,170,100) if i==self.selected_character else (55,60,80),rect,border_radius=15)
            pygame.draw.circle(self.screen,(255,210,170),(x+62,235),28)
            pygame.draw.rect(self.screen,c.body_color,(x+35,265,55,90),border_radius=10)
            self.draw_text(c.name,self.font_small,WHITE,x+62,390)
            self.draw_text(c.item_name,self.font_small,LIGHT_GRAY,x+62,425)
        self.back_button.draw(self.screen,self.font_medium)

    def draw_settings(self):
        self.screen.fill((30,35,60))
        self.draw_text("IMPOSTAZIONI",self.font_title,WHITE,SCREEN_WIDTH//2,90)
        self.draw_text("Volume",self.font_medium,WHITE,SCREEN_WIDTH//2,220)
        pygame.draw.rect(self.screen,(70,70,80),(70,270,340,20),border_radius=10)
        pygame.draw.rect(self.screen,(80,180,100),(70,270,int(340*self.volume),20),border_radius=10)
        self.draw_text(f"{int(self.volume*100)}%",self.font_small,WHITE,SCREEN_WIDTH//2,320)
        Button(80,390,320,65,"SUONI: ON" if self.sound_enabled else "SUONI: OFF").draw(self.screen,self.font_medium)
        self.back_button.draw(self.screen,self.font_medium)

    def draw_statistics(self):
        self.screen.fill((30,35,60))
        self.draw_text("STATISTICHE",self.font_title,WHITE,SCREEN_WIDTH//2,90)
        self.draw_text(f"Record: {self.high_score}",self.font_medium,WHITE,SCREEN_WIDTH//2,230)
        self.draw_text(f"Oggetti raccolti: {self.total_collected}",self.font_medium,WHITE,SCREEN_WIDTH//2,300)
        self.draw_text(f"Personaggio: {self.characters[self.selected_character].name}",self.font_small,LIGHT_GRAY,SCREEN_WIDTH//2,380)
        Button(80,550,320,65,"INDIETRO").draw(self.screen,self.font_medium)

    def draw_text(self,text,font,color,x,y,center=True):
        surface=font.render(text,True,color)
        rect=surface.get_rect(center=(x,y)) if center else surface.get_rect(topleft=(x,y))
        self.screen.blit(surface,rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running=False
            elif event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
            elif event.type == pygame.KEYUP:
                self.handle_key_up(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_up()

    def handle_key_down(self,event):
        if event.key == pygame.K_ESCAPE:
            if self.state=="game": self.paused=not self.paused
            elif self.state!="menu": self.state="menu"
        if self.state=="game":
            if event.key in (pygame.K_LEFT,pygame.K_a): self.player.left_pressed=True
            if event.key in (pygame.K_RIGHT,pygame.K_d): self.player.right_pressed=True

    def handle_key_up(self,event):
        if self.state=="game":
            if event.key in (pygame.K_LEFT,pygame.K_a): self.player.left_pressed=False
            if event.key in (pygame.K_RIGHT,pygame.K_d): self.player.right_pressed=False

    def handle_mouse_down(self,pos):
        x,y=pos
        if self.state=="menu":
            if self.play_button.contains(pos): self.start_game(); self.state="game"
            elif self.characters_button.contains(pos): self.state="characters"
            elif self.settings_button.contains(pos): self.state="settings"
            elif self.stats_button.contains(pos): self.state="statistics"
        elif self.state=="characters":
            for i in range(len(self.characters)):
                if pygame.Rect(40+i*145,180,125,300).collidepoint(pos):
                    self.selected_character=i; return
            if self.back_button.contains(pos): self.state="menu"
        elif self.state=="settings":
            if pygame.Rect(70,240,340,80).collidepoint(pos):
                self.volume=max(0,min(1,(x-70)/340))
            elif pygame.Rect(80,390,320,65).collidepoint(pos):
                self.sound_enabled=not self.sound_enabled
            elif self.back_button.contains(pos): self.state="menu"
        elif self.state=="statistics":
            if pygame.Rect(80,550,320,65).collidepoint(pos): self.state="menu"
        elif self.state=="game":
            if self.game_over: self.start_game(); return
            if pygame.Rect(SCREEN_WIDTH-65,50,50,45).collidepoint(pos):
                self.paused=not self.paused; return
            if x < SCREEN_WIDTH/2: self.player.left_pressed=True
            else: self.player.right_pressed=True

    def handle_mouse_up(self):
        if self.state=="game":
            self.player.left_pressed=False
            self.player.right_pressed=False

    def draw(self):
        if self.state=="menu": self.draw_menu()
        elif self.state=="characters": self.draw_characters()
        elif self.state=="settings": self.draw_settings()
        elif self.state=="statistics": self.draw_statistics()
        elif self.state=="game": self.draw_game()
        pygame.display.flip()

    async def run(self):
        # Pygbag needs the loop to yield so the browser can process input and render frames.
        import asyncio
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            if self.state == "game":
                self.update()
            self.draw()
            await asyncio.sleep(0)
        pygame.quit()
