import pygame
import random

# 1. 初始化
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("躲避幽灵 - 我的第一个游戏")
clock = pygame.time.Clock()

# 2. 游戏常量与变量
player_pos = pygame.Vector2(width / 2, height / 2)
player_radius = 15  # 小球半径

food_pos = pygame.Vector2(random.randint(20, width-20), random.randint(20, height-20))
food_radius = 8  # 食物半径

# --- 新增：敌人变量 ---
enemy_pos = pygame.Vector2(0, 0) # 从左上角出现
enemy_radius = 20
enemy_speed = 2.0  # 敌人初始速度

score = 0
game_over = False # 游戏状态开关
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72) # 用于显示 GAME OVER

running = True
while running:
    # 3. 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # --- 新增：重新开始逻辑 ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                # 重置所有游戏变量
                game_over = False
                score = 0
                player_pos = pygame.Vector2(width / 2, height / 2)
                enemy_pos = pygame.Vector2(0, 0)
                enemy_speed = 2.0

    if not game_over:
        # 4. 正常游戏逻辑
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: player_pos.y -= 5
        if keys[pygame.K_s]: player_pos.y += 5
        if keys[pygame.K_a]: player_pos.x -= 5
        if keys[pygame.K_d]: player_pos.x += 5

        # 边界限制
        player_pos.x = max(player_radius, min(width - player_radius, player_pos.x))
        player_pos.y = max(player_radius, min(height - player_radius, player_pos.y))

        # --- 新增：敌人AI逻辑（追踪玩家） ---
        # 计算从敌人到玩家的方向向量
        direction = player_pos - enemy_pos
        if direction.length() > 0:
            direction = direction.normalize() # 变成单位向量（长度为1的方向）
            enemy_pos += direction * enemy_speed # 朝玩家移动

        # 碰撞检测：玩家吃食物
        if player_pos.distance_to(food_pos) < player_radius + food_radius:
            score += 1
            enemy_speed += 0.2 # 越吃越快，难度增加！
            food_pos.x = random.randint(20, width-20)
            food_pos.y = random.randint(20, height-20)

        # --- 新增：碰撞检测：玩家撞到敌人 ---
        if player_pos.distance_to(enemy_pos) < player_radius + enemy_radius:
            game_over = True

    # 5. 渲染（画图）
    screen.fill("black")

    if not game_over:
        # 画食物、敌人和玩家
        pygame.draw.circle(screen, "green", food_pos, food_radius) # 食物改绿色
        pygame.draw.circle(screen, "red", enemy_pos, enemy_radius) # 敌人是红色
        pygame.draw.circle(screen, "white", player_pos, player_radius)

        # 显示分数
        score_text = font.render(f"Score: {score}", True, "white")
        screen.blit(score_text, (10, 10))
    else:
        # --- 新增：游戏结束画面 ---
        over_text = big_font.render("GAME OVER", True, "red")
        retry_text = font.render("Press 'R' to Restart", True, "white")
        final_score = font.render(f"Final Score: {score}", True, "yellow")
        
        # 居中显示
        screen.blit(over_text, (width/2 - 140, height/2 - 50))
        screen.blit(final_score, (width/2 - 80, height/2 + 20))
        screen.blit(retry_text, (width/2 - 110, height/2 + 80))

    pygame.display.flip()
    clock.tick(60)  # 限制60帧

pygame.quit()