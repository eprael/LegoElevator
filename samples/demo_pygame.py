import pygame

pygame.init()
# screen = pygame.display.set_mode((500, 500))
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    state = pygame.key.get_pressed()
    if state[pygame.K_SPACE]:
        print("spacebar was pressed")
    if state[pygame.K_q]:
        done = True

pygame.quit()