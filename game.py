import pygame
import sys

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TILE_SIZE = 32
PLAYER_SPEED = 4


def create_grass_tile():
    tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
    tile.fill((34, 177, 76))  # base green
    # simple checker pattern for pixel style
    for y in range(0, TILE_SIZE, 2):
        for x in range(0, TILE_SIZE, 2):
            tile.set_at((x, y), (23, 153, 45))
    return tile


def create_player_surface():
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surf.fill((194, 178, 128))  # simple brown armor
    pygame.draw.rect(surf, (120, 111, 100), (8, 8, 16, 16))  # face/visor
    return surf


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Medieval Demo")

    clock = pygame.time.Clock()

    grass = create_grass_tile()
    player_surf = create_player_surface()

    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT // 2

    portal_rect = pygame.Rect(400, 100, TILE_SIZE, TILE_SIZE * 2)
    portal_surf = pygame.Surface((TILE_SIZE, TILE_SIZE * 2), pygame.SRCALPHA)
    pygame.draw.ellipse(portal_surf, (150, 0, 150, 200), portal_surf.get_rect())

    enemy_rect = pygame.Rect(100, 300, TILE_SIZE, TILE_SIZE)
    enemy_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    enemy_surf.fill((200, 40, 40))
    enemy_dx = 2

    font = pygame.font.SysFont(None, 24)
    show_message = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_y += PLAYER_SPEED

        player_rect = pygame.Rect(player_x, player_y, TILE_SIZE, TILE_SIZE)
        show_message = player_rect.colliderect(portal_rect)

        enemy_rect.x += enemy_dx
        if enemy_rect.right >= SCREEN_WIDTH or enemy_rect.left <= 0:
            enemy_dx = -enemy_dx

        hit_enemy = player_rect.colliderect(enemy_rect)

        # draw background tiles
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for x in range(0, SCREEN_WIDTH, TILE_SIZE):
                screen.blit(grass, (x, y))

        # draw portal, enemy and player
        screen.blit(portal_surf, portal_rect.topleft)
        screen.blit(enemy_surf, enemy_rect.topleft)
        screen.blit(player_surf, (player_x, player_y))

        if show_message:
            text = font.render("Has encontrado el portal!", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))
        if hit_enemy:
            text = font.render("Te han golpeado!", True, (255, 0, 0))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 80))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
