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

# Definindo a posição inicial do carro do jogador
car_x = SCREEN_WIDTH // 2 - car_width // 2
car_y = SCREEN_HEIGHT - car_height - 20
car_speed = 0

# Definindo a posição inicial da pista
track_height = track_image.get_rect().height
track_y = -track_height + SCREEN_HEIGHT  # Começa fora da tela para simular movimento
track_speed = 5  # Velocidade de movimento da pista

# Definindo a posição e velocidade inicial dos carros adversários
enemy_car_speed = 7
enemy_cars = []

# Limites da pista preta (área permitida para o movimento dos carros)
left_limit = 170  # Limite esquerdo da pista preta
right_limit = SCREEN_WIDTH - 150  # Limite direito da pista preta

# Função para criar novos carros adversários
def create_enemy_car():
    enemy_x = random.randint(left_limit, right_limit - enemy_car_width)
    enemy_y = random.randint(-600, -100)
    return [enemy_x, enemy_y]

# Adicionando alguns carros adversários no início
for _ in range(4):
    enemy_cars.append(create_enemy_car())

# Função para verificar colisão
def check_collision(player_rect, enemies):
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_car_width, enemy_car_height)
        if player_rect.colliderect(enemy_rect):
            return True
    return False

# Função principal do jogo
def game_loop():
    global car_x, car_y, car_speed, track_y

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
                    car_speed = -5
                elif event.key == pygame.K_RIGHT:
                    car_speed = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    car_speed = 0

        # Atualizando a posição do carro
        car_x += car_speed
        if car_x < left_limit:
            car_x = left_limit
        elif car_x > right_limit - car_width:
            car_x = right_limit - car_width

        # Atualizando a posição da pista
        track_y += track_speed
        if track_y >= 0:
            track_y = -track_height + SCREEN_HEIGHT

        # Movendo os carros adversários
        for enemy in enemy_cars:
            enemy[1] += enemy_car_speed
            if enemy[1] > SCREEN_HEIGHT:
                enemy[0] = random.randint(left_limit, right_limit - enemy_car_width)
                enemy[1] = random.randint(-600, -100)

        # Verificando colisões
        player_rect = pygame.Rect(car_x, car_y, car_width, car_height)
        if check_collision(player_rect, enemy_cars):
            print("Colisão! Game Over.")
            running = False

        # Desenhando na tela
        screen.blit(track_image, (0, track_y))
        screen.blit(car_image, (car_x, car_y))

        # Desenhando carros adversários
        for enemy in enemy_cars:
            screen.blit(enemy_car_image, (enemy[0], enemy[1]))

        pygame.display.update()
        clock.tick(60)

# Iniciando o jogo
game_loop()