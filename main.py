import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Definindo as dimensões da janela do jogo
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Corrida Python")

# Carregando imagens
car_image = pygame.image.load("img/car.png")
enemy_car_image = pygame.image.load("img/enemy_car.png")
track_image = pygame.image.load("img/track.png")

# Definindo dimensões do carro
car_width = car_image.get_rect().width
car_height = car_image.get_rect().height

enemy_car_width = enemy_car_image.get_rect().width
enemy_car_height = enemy_car_image.get_rect().height

# Dicionário para representar o carro do jogador
player_car = {
    "x": SCREEN_WIDTH // 2 - car_width // 2,
    "y": SCREEN_HEIGHT - car_height - 20,
    "speed": 0,
    "width": car_width,
    "height": car_height
}

# Definindo a posição inicial da pista
track_height = track_image.get_rect().height
track_y = -track_height + SCREEN_HEIGHT  # Começa fora da tela para simular movimento
track_speed = 5  # Velocidade de movimento da pista

# Definindo a velocidade dos carros adversários
enemy_car_speed = 7

# Limites da pista preta (área permitida para o movimento dos carros)
left_limit = 170  # Limite esquerdo da pista preta
right_limit = SCREEN_WIDTH - 150  # Limite direito da pista preta

# Função para criar um dicionário representando um novo carro adversário
def create_enemy_car():
    return {
        "x": random.randint(left_limit, right_limit - enemy_car_width),
        "y": random.randint(-600, -100),
        "width": enemy_car_width,
        "height": enemy_car_height
    }

# Lista de dicionários para armazenar os carros adversários
enemy_cars = [create_enemy_car() for _ in range(4)]

# Função para verificar colisão
def check_collision(player, enemies):
    player_rect = pygame.Rect(player["x"], player["y"], player["width"], player["height"])
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy["width"], enemy["height"])
        if player_rect.colliderect(enemy_rect):
            return True
    return False

# Função principal do jogo
def game_loop():
    global track_y

    clock = pygame.time.Clock()
    running = True

    while running:
        # Verificando eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Controles do carro
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_car["speed"] = -5
                elif event.key == pygame.K_RIGHT:
                    player_car["speed"] = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_car["speed"] = 0

        # Atualizando a posição do carro
        player_car["x"] += player_car["speed"]
        if player_car["x"] < left_limit:
            player_car["x"] = left_limit
        elif player_car["x"] > right_limit - player_car["width"]:
            player_car["x"] = right_limit - player_car["width"]

        # Atualizando a posição da pista
        track_y += track_speed
        if track_y >= 0:
            track_y = -track_height + SCREEN_HEIGHT

        # Movendo os carros adversários
        for enemy in enemy_cars:
            enemy["y"] += enemy_car_speed
            if enemy["y"] > SCREEN_HEIGHT:
                enemy["x"] = random.randint(left_limit, right_limit - enemy["width"])
                enemy["y"] = random.randint(-600, -100)

        # Verificando colisões
        if check_collision(player_car, enemy_cars):
            print("Colisão! Game Over.")
            running = False

        # Desenhando na tela
        screen.blit(track_image, (0, track_y))
        screen.blit(car_image, (player_car["x"], player_car["y"]))

        # Desenhando carros adversários
        for enemy in enemy_cars:
            screen.blit(enemy_car_image, (enemy["x"], enemy["y"]))

        pygame.display.update()
        clock.tick(60)

# Iniciando o jogo
game_loop()
