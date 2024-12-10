import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(60, 60)
target_pos = pygame.Vector2(1240, 680)

no_obstacles = 5
obstacle_positions = []


def setup():
    # create obstacles
    for i in range(no_obstacles):
        obstacle_positions.append(pygame.Vector2(
            random.randint(40, 1240), random.randint(40, 680)
        ))


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

    # clamp player position to screen
    player_pos.x = max(40, min(player_pos.x, 1240))
    player_pos.y = max(40, min(player_pos.y, 680))
    handle_collisions()


def handle_collisions():
    # check if player has reached target
    if player_pos.distance_to(target_pos) < 40:
        print("You win!")
        player_pos.x = 60
        player_pos.y = 60

    # check if player has hit any obstacles
    for obstacle in obstacle_positions:
        if player_pos.distance_to(obstacle) < 80:
            player_to_obstacle = player_pos - obstacle
            player_to_obstacle.normalize_ip()
            player_to_obstacle *= (300*dt)
            player_pos.x += player_to_obstacle.x
            player_pos.y += player_to_obstacle.y

def draw_objectives():
    # draw player
    pygame.draw.circle(screen, "blue", player_pos, 40)
    # draw target
    pygame.draw.circle(screen, "red", target_pos, 40)


def draw_obstacles():
    for obstacle in obstacle_positions:
        pygame.draw.circle(screen, "green", obstacle, 40)

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