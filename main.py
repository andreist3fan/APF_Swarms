import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
running = True
dt = 0

origin_offset = pygame.Vector2(50, 50)
play_area = pygame.Vector2(600, 600)

player_pos = pygame.Vector2(60, 60)
player_pos+= origin_offset
player_theoretical_radius = 20

target_pos = pygame.Vector2(440, 440)
target_pos+= origin_offset
target_theoretical_radius = 20

no_obstacles = 5
obstacle_positions = []
obstacle_theoretical_radius = 20


def setup():
    # create obstacles
    # For now, uniformly distribute obstacles in the play area
    for i in range(no_obstacles):
        obstacle_positions.append(pygame.Vector2(
            random.uniform(origin_offset.x, origin_offset.x+play_area.x),
            random.uniform(origin_offset.y, origin_offset.y+play_area.y)
        ))
    # create play area

def handle_movement():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt
    handle_collisions()
    # clamp player position to play ares
    player_pos.x = max(origin_offset.x, min(player_pos.x, origin_offset.x+play_area.x))
    player_pos.y = max(origin_offset.y, min(player_pos.y, origin_offset.y+play_area.y))
    print(player_pos)

def handle_collisions():
    # check if player has reached target
    if player_pos.distance_to(target_pos) < target_theoretical_radius:
        print("You win!")
        player_pos.x = 60
        player_pos.y = 60

    # check if player has hit any obstacles
    for obstacle in obstacle_positions:
        if player_pos.distance_to(obstacle) < obstacle_theoretical_radius + player_theoretical_radius:
            player_to_obstacle = player_pos - obstacle
            player_to_obstacle.normalize_ip()
            player_to_obstacle *= (300*dt)
            player_pos.x += player_to_obstacle.x
            player_pos.y += player_to_obstacle.y

def draw_objectives():
    # draw player
    pygame.draw.circle(screen, "blue", player_pos, player_theoretical_radius)
    # draw target
    pygame.draw.circle(screen, "red", target_pos, target_theoretical_radius)


def draw_obstacles():
    # draw play area bounds
    pygame.draw.rect(screen, "white", pygame.Rect(origin_offset, play_area), 1)

    # draw obstacles
    for obstacle in obstacle_positions:
        pygame.draw.circle(screen, "green", obstacle, obstacle_theoretical_radius)

if __name__ == "__main__":

    # randomly generate obstacles
    setup()

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # draw the player and target
        draw_objectives()

        # draw the obstacles
        draw_obstacles()

        # handle player movement (WASD) and collisions with obstacles
        handle_movement()

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()