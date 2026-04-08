import pygame
import random

# 1. 初始化
pygame.init()
width, height = 800, 600 # 稍微放大一点舞台
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("星空突围 - Dash Edition")
clock = pygame.time.Clock()

# --- 视觉增强：生成随机星星背景 ---
stars = []
for _ in range(100):
    stars.append([random.randint(0, width), random.randint(0, height), random.random()])

# 2. 游戏变量
player_pos = pygame.Vector2(width / 2, height / 2)
player_radius = 12
player_speed = 5
player_trail = [] # 用于存储玩家的历史位置，制造“尾迹”

# 敌人管理
enemies = []
def spawn_enemy():
    return {"pos": pygame.Vector2(random.choice([0, width]), random.choice([0, height])), 
            "speed": random.uniform(1.5, 2.5)}
enemies.append(spawn_enemy())

food_pos = pygame.Vector2(random.randint(50, width-50), random.randint(50, height-50))
score = 0
game_over = False

# --- 新增：冲刺 (Dash) 变量 ---
dash_cooldown = 0
is_dashing = False

font = pygame.font.Font(None, 36)

running = True
while running:
    # 3. 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                # 重置
                game_over = False
                score = 0
                player_pos = pygame.Vector2(width / 2, height / 2)
                enemies = [spawn_enemy()]
            
            # --- 冲刺逻辑：按下空格 ---
            if event.key == pygame.K_SPACE and dash_cooldown <= 0 and not game_over:
                is_dashing = True
                dash_cooldown = 60 # 1秒冷却（60帧）

    if not game_over:
        # 4. 玩家移动逻辑
        keys = pygame.key.get_pressed()
        move_vec = pygame.Vector2(0, 0)
        if keys[pygame.K_w]: move_vec.y -= 1
        if keys[pygame.K_s]: move_vec.y += 1
        if keys[pygame.K_a]: move_vec.x -= 1
        if keys[pygame.K_d]: move_vec.x += 1
        
        if move_vec.length() > 0:
            move_vec = move_vec.normalize()
            
            # 如果正在冲刺，速度翻5倍
            current_speed = player_speed * 5 if is_dashing else player_speed
            player_pos += move_vec * current_speed
            is_dashing = False # 冲刺是一瞬间的

        # 记录尾迹点
        player_trail.append(list(player_pos))
        if len(player_trail) > 10: player_trail.pop(0) # 只保留最近10帧

        # 冷却计时
        if dash_cooldown > 0: dash_cooldown -= 1

        # 边界限制
        player_pos.x = max(player_radius, min(width - player_radius, player_pos.x))
        player_pos.y = max(player_radius, min(height - player_radius, player_pos.y))

        # 敌人AI与碰撞
        for e in enemies:
            dir_to_player = (player_pos - e["pos"])
            if dir_to_player.length() > 0:
                e["pos"] += dir_to_player.normalize() * e["speed"]
            
            if player_pos.distance_to(e["pos"]) < player_radius + 15:
                game_over = True

        # 吃食物
        if player_pos.distance_to(food_pos) < player_radius + 10:
            score += 1
            food_pos = pygame.Vector2(random.randint(50, width-50), random.randint(50, height-50))
            # 每拿3分增加一个敌人
            if score % 3 == 0:
                enemies.append(spawn_enemy())
            # 每拿1分稍微增加所有敌人速度
            for e in enemies: e["speed"] += 0.1

    # 5. 渲染
    screen.fill((10, 10, 25)) # 深蓝色背景

    # 画星星
    for s in stars:
        # 让星星闪烁一下
        brightness = random.randint(150, 255)
        pygame.draw.circle(screen, (brightness, brightness, brightness), (int(s[0]), int(s[1])), 1)

    if not game_over:
        # 画尾迹
        for i, pos in enumerate(player_trail):
            alpha = int(255 * (i / len(player_trail))) # 越旧的越透明
            color = (alpha // 2, alpha // 2, alpha) # 浅蓝色尾迹
            pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), player_radius)

        # 画玩家、敌人、食物
        pygame.draw.circle(screen, (0, 255, 255), player_pos, player_radius) # 玩家青色
        for e in enemies:
            pygame.draw.circle(screen, (255, 50, 50), e["pos"], 15) # 敌人红色
        pygame.draw.circle(screen, (255, 255, 0), food_pos, 8) # 食物黄色

        # UI
        score_text = font.render(f"Score: {score}   Dash: {'READY' if dash_cooldown <= 0 else 'Charging...'}", True, "white")
        screen.blit(score_text, (20, 20))
    else:
        # 死亡界面（略，保持之前的逻辑）
        msg = font.render("GAME OVER! Press 'R' to Restart", True, "white")
        screen.blit(msg, (width/2 - 150, height/2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()