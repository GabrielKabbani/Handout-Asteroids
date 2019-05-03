# -*- coding: utf-8 -*-

# Importando as bibliotecas necessárias.
import pygame
import random
import time
from os import path

# Estabelece a pasta que contem as figuras e sons.
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# Dados gerais do jogo.
WIDTH = 480 # Largura da tela
HEIGHT = 600 # Altura da tela
FPS = 60 # Frames por segundo

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Classe Jogador que representa a nave
class Player(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self,player_img):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
        self.image = player_img
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(player_img, (50, 38))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Centraliza embaixo da tela.
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        
        # Velocidade da nave
        self.speedx = 0
        
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = 25
    
    # Metodo que atualiza a posição da navinha
    def update(self):
        self.rect.x += self.speedx
        
        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

# Classe Mob que representa os meteoros
class Mob(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self,mob_img):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(mob_img, (50, 38))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Sorteia um lugar inicial em x
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        # Sorteia um lugar inicial em y
        self.rect.y = random.randrange(-100, -40)
        # Sorteia uma velocidade inicial
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 9)
        
        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * .85 / 2)
        
    # Metodo que atualiza a posição da navinha
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        # Se o meteoro passar do final da tela, volta para cima
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 9)
            
# Classe Bullet que representa os tiros
class Bullet(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, x, y, bullet_img):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        self.image = bullet_img
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    # Metodo que atualiza a posição da navinha
    def update(self):
        self.rect.y += self.speedy
        
        # Se o tiro passar do inicio da tela, morre.
        if self.rect.bottom < 0:
            self.kill()
            
#Classe que representa uma explosão de meteoro.
class Explosion (pygame.sprite.Sprite):
    #Construtor da classe
    def __init__(self,center,explosion_anim):
        #construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        #Carrega a animação de explosão
        self.explosion_anim = explosion_anim
        
        #inicia o processo de animação colocando a primeira imagem na tela
        self.frame=0
        self.image=self.explosion_anim[self.frame]
        self.rect= self.image.get_rect()
        self.rect.center=center
        
        #Guarda o tick da primeira imagem
        self.last_update= pygame.time.get_ticks()
        
        #Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos
        self.frame_ticks=50
        
    def update(self):
        #verifica o tick atual.
        now=pygame.time.get_ticks()
        
        #verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks=now-self.last_update
        
        #Se já está na hora de mudar de imagem.
        if elapsed_ticks>self.frame_ticks:
            #Marca o tick da nova imagem.
            self.last_update=now
            
            #avanca um quadro.
            self.frame+=1
            
            #verifica se ja chegou no final da animacao.
            if self.frame == len(self.explosion_anim):
                #se sim, tchau explosao!
                self.kill()
                
            else:
                #Se ainda nao cheogu ao fim da explosao, troca de imagem.
                center=self.rect.center
                self.image=self.explosion_anim[self.frame]
                self.rect=self.image.get_rect()
                self.rect.center=center
            
#carrega todos os assets de uma vez só
def load_assets(img_dir,snd_dir):
    assets={}
    assets["player_img"]= pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
    assets["mob_img"]= pygame.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()
    assets["bullet_img"]= pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
    assets["background"]= pygame.image.load(path.join(img_dir, "starfield.png")).convert()
    assets["boom_sound"]= pygame.mixer.Sound(path.join(snd_dir, "expl3.wav"))
    assets["destroy_sound"]= pygame.mixer.Sound(path.join(snd_dir, "expl6.wav"))
    assets["pew_sound"]= pygame.mixer.Sound(path.join(snd_dir, "pew.wav"))
    explosion_anim=[]
    for i in range(9):
        filename= "regularExplosion{0}.png".format(i)
        img=pygame.image.load(path.join(img_dir,filename)).convert()
        img=pygame.transform.scale(img,(32,32))
        img.set.colorkey(BLACK)
        explosion_anim.append(img)
    assets["explosion_anim"]=explosion_anim
    return assets
    
# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("Navinha")

#Carrega todos os assets uma vez só e guarda em um dicionário
assets=load_assets(img_dir,snd_dir)

# Variável para o ajuste de velocidade
clock = pygame.time.Clock()

# Carrega o fundo do jogo
background = assets["background"]
background_rect = background.get_rect()

# Carrega os sons do jogo
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)
boom_sound = assets["boom_sound"]
destroy_sound = assets["destroy_sound"]
pew_sound = assets["pew_sound"]

# Cria uma nave. O construtor será chamado automaticamente.
player = Player(assets["player_img"])


# Cria um grupo de todos os sprites e adiciona a nave.
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Cria um grupo só dos meteoros
mobs = pygame.sprite.Group()

# Cria um grupo para tiros
bullets = pygame.sprite.Group()

# Cria 8 meteoros e adiciona no grupo meteoros
for i in range(8):
    m = Mob(assets["mob_img"])
    all_sprites.add(m)
    mobs.add(m)

# Comando para evitar travamentos.
try:
    
    # Loop principal.
    pygame.mixer.music.play(loops=-1)
    running = True
    while running:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                running = False
            
            # Verifica se apertou alguma tecla.
            if event.type == pygame.KEYDOWN:
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    player.speedx = -8
                if event.key == pygame.K_RIGHT:
                    player.speedx = 8
                # Se for um espaço atira!
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top, assets["bullet_img"])
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    pew_sound.play()
                    
            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    player.speedx = 0
                if event.key == pygame.K_RIGHT:
                    player.speedx = 0
                    
        # Depois de processar os eventos.
        # Atualiza a acao de cada sprite.
        all_sprites.update()
        
        # Verifica se houve colisão entre tiro e meteoro
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits: # Pode haver mais de um
            # O meteoro e destruido e precisa ser recriado
            destroy_sound.play()
            m = Mob(assets["mob_img"]) 
            all_sprites.add(m)
            mobs.add(m)
            
            #no lugar do meteoro antigo, adicionar uma explosão.
            explosao=Explosion(hit.rect.center, assets["explosion_anim"])
            all_sprites.add(explosao)
        
        # Verifica se houve colisão entre nave e meteoro
        hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
        if hits:
            # Toca o som da colisão
            boom_sound.play()
            time.sleep(1) # Precisa esperar senão fecha
            
            running = False
    
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
finally:
    
    pygame.quit()
