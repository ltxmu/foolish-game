import pygame
import random

# 1. 初始化
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("我的第一个小游戏")
clock = pygame.time.Clock()
running = True

# 2. 游戏变量
player_pos = pygame.Vector2(width / 2, height / 2)

# --- 修改点 1：调小球的半径 ---
# 原来可能是 40 或者 20，现在我们改成 15，球会看起来更精致
player_radius = 15 

# 食物变量
food_pos = pygame.Vector2(random.randint(20, width-20), random.randint(20, height-20))
food_radius = 8  # 食物也相应调小一点点

# 分数和字体
score = 0
font = pygame.font.Font(None, 36)

while running:
    # 3. 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 4. 玩家移动逻辑 (速度也可以根据球的大小微调，这里保持 5)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: player_pos.y -= 5
    if keys[pygame.K_s]: player_pos.y += 5
    if keys[pygame.K_a]: player_pos.x -= 5
    if keys[pygame.K_d]: player_pos.x += 5

    # 边界限制
    if player_pos.x < player_radius: player_pos.x = player_radius
    if player_pos.x > width - player_radius: player_pos.x = width - player_radius
    if player_pos.y < player_radius: player_pos.y = player_radius
    if player_pos.y > height - player_radius: player_pos.y = height - player_radius

    # 碰撞检测
    distance = player_pos.distance_to(food_pos)
    if distance < player_radius + food_radius:
        score += 1
        food_pos.x = random.randint(20, width-20)
        food_pos.y = random.randint(20, height-20)

    # 5. 渲染（画图）
    
    # --- 修改点 2：背景色换成黑色 ---
    screen.fill("black") 

    # 画食物（红色）
    pygame.draw.circle(screen, "red", food_pos, food_radius)
    
    # 画玩家（白色）
    pygame.draw.circle(screen, "white", player_pos, player_radius)

    # 显示分数
    score_text = font.render(f"Score: {score}", True, "white")
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)  # 限制 60 帧

pygame.quit()