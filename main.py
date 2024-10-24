import pygame
import sys
import random
import time

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
shield_image = pygame.image.load("img/shield.png")  # Imagem de escudo

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
    "height": car_height,
    "shield": False,  # Estado do escudo
    "nitro": False    # Estado do nitro
}

# Definindo a posição inicial da pista
track_height = track_image.get_rect().height
track_y = -track_height + SCREEN_HEIGHT  # Começa fora da tela para simular movimento
track_speed = 5  # Velocidade inicial da pista

# Definindo a velocidade dos carros adversários
enemy_car_speed = 7
difficulty_increment = 0.001  # Incremento de dificuldade progressivo

# Limites da pista preta (área permitida para o movimento dos carros)
left_limit = 170  # Limite esquerdo da pista preta
right_limit = SCREEN_WIDTH - 150  # Limite direito da pista preta

# Pontuação
start_time = time.time()  # Momento em que o jogo começa
score = 0

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
    if player["shield"]:
        return False  # Se o jogador tem escudo, não há colisão

    player_rect = pygame.Rect(player["x"], player["y"], player["width"], player["height"])
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy["width"], enemy["height"])
        if player_rect.colliderect(enemy_rect):
            return True
    return False

# Função para exibir o HUD (Heads-Up Display)
def display_hud(score, shield_active, nitro_active):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Pontuação: {int(score)}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    if shield_active:
        shield_text = font.render("Escudo Ativo", True, (0, 255, 0))
        screen.blit(shield_text, (10, 50))

    if nitro_active:
        nitro_text = font.render("Nitro Ativo!", True, (0, 0, 255))
        screen.blit(nitro_text, (10, 90))

# Função para aplicar power-ups
def apply_power_ups():
    power_up_type = random.choice(["shield", "nitro"])
    if power_up_type == "shield":
        player_car["shield"] = True
        pygame.time.set_timer(pygame.USEREVENT + 1, 5000)  # Escudo ativo por 5 segundos
    elif power_up_type == "nitro":
        player_car["nitro"] = True
        pygame.time.set_timer(pygame.USEREVENT + 2, 3000)  # Nitro ativo por 3 segundos

# Função para exibir o menu de reinício
def display_restart_menu():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, (255, 0, 0))
    restart_text = font.render("Pressione R para reiniciar", True, (255, 255, 255))
    exit_text = font.render("Pressione ESC para sair", True, (255, 255, 255))

    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 120))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    game_loop()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Função principal do jogo
def game_loop():
    global track_y, track_speed, enemy_car_speed, score, start_time

    # Reinicializando o estado inicial do jogo
    player_car["x"] = SCREEN_WIDTH // 2 - car_width // 2
    player_car["speed"] = 0
    track_y = -track_height + SCREEN_HEIGHT
    track_speed = 5
    enemy_car_speed = 7
    player_car["shield"] = False
    player_car["nitro"] = False
    start_time = time.time()

    for enemy in enemy_cars:
        enemy["x"] = random.randint(left_limit, right_limit - enemy["width"])
        enemy["y"] = random.randint(-600, -100)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_car["speed"] = -5
                elif event.key == pygame.K_RIGHT:
                    player_car["speed"] = 5
                elif event.key == pygame.K_SPACE:  # Pressione ESPAÇO para ativar power-up aleatório
                    apply_power_ups()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_car["speed"] = 0

            # Eventos de expiração de power-ups
            if event.type == pygame.USEREVENT + 1:
                player_car["shield"] = False
            elif event.type == pygame.USEREVENT + 2:
                player_car["nitro"] = False

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

        # Aumentando a dificuldade com o tempo
        track_speed += difficulty_increment
        enemy_car_speed += difficulty_increment

        # Verificando colisões
        if check_collision(player_car, enemy_cars):
            display_restart_menu()
            return

        # Atualizando a pontuação
        score = time.time() - start_time

        # Desenhando na tela
        screen.blit(track_image, (0, track_y))
        screen.blit(car_image, (player_car["x"], player_car["y"]))

        # Desenhando carros adversários
        for enemy in enemy_cars:
            screen.blit(enemy_car_image, (enemy["x"], enemy["y"]))

        # Exibir HUD (pontuação, power-ups ativos)
        display_hud(score, player_car["shield"], player_car["nitro"])

        pygame.display.update()
        clock.tick(60)

# Iniciando o jogo
game_loop()
