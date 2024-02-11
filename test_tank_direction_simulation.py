import pygame
import sys
import math

# Inicializar o Pygame
pygame.init()

# Definir as dimensões da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Controle de Triângulo com WASD")

# Definir as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definir variáveis do triângulo
triangle_size = 40
triangle_x = WIDTH // 2
triangle_y = HEIGHT // 2
triangle_speed = 5
triangle_angle = 0
triangle_dx, triangle_dy = 0, 0


# Função para desenhar um triângulo
def draw_triangle(x, y, size, angle):
    points = [(x + size * math.cos(angle), y + size * math.sin(angle))]
    for i in range(1, 3):
        points.append((
            x + size * math.cos(angle + i * 2 * math.pi / 3),
            y + size * math.sin(angle + i * 2 * math.pi / 3)
        ))
    pygame.draw.polygon(screen, WHITE, points)


def change_triangle_direction(speed, angle):
    return speed * math.cos(angle), speed * math.sin(angle)


# Loop principal do jogo
running = True
while running:
    # Lidar com eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Verificar as teclas pressionadas
    keys = pygame.key.get_pressed()
    triangle_dx, triangle_dy = 0, 0
    if keys[pygame.K_w] and keys[pygame.K_d]:
        triangle_angle = -math.pi / 3
        triangle_dx, triangle_dy = change_triangle_direction(triangle_speed, triangle_angle)
    elif keys[pygame.K_w] and keys[pygame.K_a]:
        triangle_angle = -2 * math.pi / 3
        triangle_dx, triangle_dy = change_triangle_direction(triangle_speed, triangle_angle)
    elif keys[pygame.K_s] and keys[pygame.K_d]:
        triangle_angle = math.pi / 3
        triangle_dx, triangle_dy = change_triangle_direction(triangle_speed, triangle_angle)
    elif keys[pygame.K_s] and keys[pygame.K_a]:
        triangle_angle = 2 * math.pi / 3
        triangle_dx, triangle_dy = change_triangle_direction(triangle_speed, triangle_angle)
    elif keys[pygame.K_w]:
        triangle_angle = -math.pi / 2
        triangle_dx, triangle_dy = change_triangle_direction(triangle_speed, triangle_angle)
    elif keys[pygame.K_s]:
        triangle_angle = math.pi / 2
        triangle_dx, triangle_dy = change_triangle_direction(triangle_speed, triangle_angle)
    elif keys[pygame.K_a]:
        triangle_angle = math.pi
        triangle_dx, triangle_dy = change_triangle_direction(triangle_speed, triangle_angle)
    elif keys[pygame.K_d]:
        triangle_angle = 0
        triangle_dx, triangle_dy = change_triangle_direction(triangle_speed, triangle_angle)

    # Atualizar a posição do triângulo
    triangle_x += triangle_dx
    triangle_y += triangle_dy

    # Limpar a tela
    screen.fill(BLACK)

    # Desenhar o triângulo na tela
    draw_triangle(triangle_x, triangle_y, triangle_size, triangle_angle)

    # Atualizar a tela
    pygame.display.flip()

    # Controlar a taxa de atualização
    pygame.time.Clock().tick(60)

# Encerrar o Pygame
pygame.quit()
sys.exit()
