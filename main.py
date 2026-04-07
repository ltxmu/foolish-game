import pygame

# 初始化
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
running = True

# 玩家初始位置
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # 处理事件（比如点击关闭按钮）
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 填充背景颜色（蓝色）
    screen.fill("blue")

    # 画一个圆代表玩家
    pygame.draw.circle(screen, "white", player_pos, 40)

    # 获取按键并移动
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: player_pos.y -= 5
    if keys[pygame.K_s]: player_pos.y += 5
    if keys[pygame.K_a]: player_pos.x -= 5
    if keys[pygame.K_d]: player_pos.x += 5

    pygame.display.flip()
    clock.tick(60)  # 限制 60 帧

pygame.quit()