import pygame
import json
import pytmx




pygame.init()




screen = pygame.display.set_mode((960, 640))
pygame.display.set_caption("Dungeon Adventure")
clock = pygame.time.Clock()




font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 60)




WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
DARK_GRAY = (45, 45, 45)
BLUE = (60, 120, 220)
GREEN = (60, 180, 100)
RED = (200, 60, 60)




background_image = pygame.image.load("graphics/login.png").convert()
background_image = pygame.transform.scale(background_image, (960, 640))




player_image = pygame.image.load("graphics/knight.jpeg").convert()
player_image = pygame.transform.scale(player_image, (30, 30))




table_image = pygame.image.load("graphics/knight.jpeg").convert()
table_image = pygame.transform.scale(table_image, (240, 130))
table_rect = pygame.Rect(360, 255, 240, 130)








tiled_map = pytmx.load_pygame("maps/map1/room1.tmx", pixelalpha=True)


background = pygame.Surface((960, 640)).convert_alpha()


def draw_image_layers():
    background.fill((0, 0, 0, 0))


    for layer in tiled_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:


                tile_image = tiled_map.get_tile_image_by_gid(gid)
                if tile_image:
                    pixel_x = x * tiled_map.tilewidth
                    pixel_y = y * tiled_map.tileheight


                    background.blit(tile_image, (pixel_x, pixel_y))








class Knight(pygame.sprite.Sprite):
    def __init__(self, image, spawning_location):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=spawning_location)
        self.unlocked = True
        self.hp = 6
        self.armor = 5
        self.energy = 180
        self.speed = 6.5
        self.level = 1
        self.damage = 4
        self.skill_unlocked = True
        self.skill_name = "Shield"
    def move(self, keys, walls=None, bounds=None):
        dx = 0
        dy = 0
        if pygame.K_w in keys or pygame.K_UP in keys:
            dy -= self.speed


        if pygame.K_s in keys or pygame.K_DOWN in keys:
            dy += self.speed


        if pygame.K_a in keys or pygame.K_LEFT in keys:
            dx -= self.speed


        if pygame.K_d in keys or pygame.K_RIGHT in keys:
            dx += self.speed


        movement = pygame.math.Vector2(dx, dy)


        if movement.length() > 0:
            movement = movement.normalize() * self.speed
        self.rect.x += round(movement.x)




        if walls:
            for wall in walls:
                if self.rect.colliderect(wall):
                    if movement.x > 0:
                        self.rect.right = wall.left
                    elif movement.x < 0:
                        self.rect.left = wall.right




        self.rect.y += round(movement.y)




        if walls:
            for wall in walls:
                if self.rect.colliderect(wall):
                    if movement.y > 0:
                        self.rect.bottom = wall.top
                    elif movement.y < 0:
                        self.rect.top = wall.bottom




        if bounds:
            self.rect.clamp_ip(bounds)




    def attack(self, cursor_location):




        dx = cursor_location[0] - self.rect.centerx
        dy = cursor_location[1] - self.rect.centery




        if abs(dx) > abs(dy):




            if dx > 0:
                return pygame.Rect(
                    self.rect.right,
                    self.rect.centery - 35,
                    70,
                    70
                )




            return pygame.Rect(
                self.rect.left - 70,
                self.rect.centery - 35,
                70,
                70
            )




        if dy > 0:
            return pygame.Rect(
                self.rect.centerx - 35,
                self.rect.bottom,
                70,
                70
            )




        return pygame.Rect(
            self.rect.centerx - 35,
            self.rect.top - 70,
            70,
            70
        )




    def skill(self):
        if self.skill_unlocked and self.energy >= 30:
            self.energy -= 30
            return "Knight shield activated"




        return None






class Priestess(pygame.sprite.Sprite):




    def __init__(self, image, spawning_location):
        super().__init__()




        self.image = image
        self.rect = self.image.get_rect(center=spawning_location)




        self.unlocked = False
        self.hp = 3
        self.armor = 5
        self.energy = 200
        self.speed = 6.5
        self.level = 1
        self.damage = 3




        self.skill_unlocked = False
        self.skill_name = "Healing"




    def move(self, keys, walls=None, bounds=None):




        dx = 0
        dy = 0




        if pygame.K_w in keys or pygame.K_UP in keys:
            dy -= self.speed
        if pygame.K_s in keys or pygame.K_DOWN in keys:
            dy += self.speed
        if pygame.K_a in keys or pygame.K_LEFT in keys:
            dx -= self.speed
        if pygame.K_d in keys or pygame.K_RIGHT in keys:
            dx += self.speed




        movement = pygame.math.Vector2(dx, dy)




        if movement.length() > 0:
            movement = movement.normalize() * self.speed




        self.rect.x += round(movement.x)




        if walls:
            for wall in walls:
                if self.rect.colliderect(wall):
                    if movement.x > 0:
                        self.rect.right = wall.left
                    elif movement.x < 0:
                        self.rect.left = wall.right




        self.rect.y += round(movement.y)




        if walls:
            for wall in walls:
                if self.rect.colliderect(wall):
                    if movement.y > 0:
                        self.rect.bottom = wall.top
                    elif movement.y < 0:
                        self.rect.top = wall.bottom




        if bounds:
            self.rect.clamp_ip(bounds)




    def attack(self, cursor_location):




        dx = cursor_location[0] - self.rect.centerx
        dy = cursor_location[1] - self.rect.centery




        if abs(dx) > abs(dy):
            if dx > 0:
                return pygame.Rect(self.rect.right, self.rect.centery - 35, 70, 70)
            return pygame.Rect(self.rect.left - 70, self.rect.centery - 35, 70, 70)




        if dy > 0:
            return pygame.Rect(self.rect.centerx - 35, self.rect.bottom, 70, 70)




        return pygame.Rect(self.rect.centerx - 35, self.rect.top - 70, 70, 70)




    def skill(self):




        if self.skill_unlocked and self.energy >= 40:
            self.energy -= 40
            self.hp += 1
            return "Priestess healed 1 HP"




        return None






class Assassin(pygame.sprite.Sprite):




    def __init__(self, image, spawning_location):
        super().__init__()




        self.image = image
        self.rect = self.image.get_rect(center=spawning_location)




        self.unlocked = False
        self.hp = 4
        self.armor = 4
        self.energy = 180
        self.speed = 6.5
        self.level = 1
        self.damage = 5




        self.skill_unlocked = False
        self.skill_name = "Dash"




    def move(self, keys, walls=None, bounds=None):




        dx = 0
        dy = 0




        if pygame.K_w in keys or pygame.K_UP in keys:
            dy -= self.speed
        if pygame.K_s in keys or pygame.K_DOWN in keys:
            dy += self.speed
        if pygame.K_a in keys or pygame.K_LEFT in keys:
            dx -= self.speed
        if pygame.K_d in keys or pygame.K_RIGHT in keys:
            dx += self.speed




        movement = pygame.math.Vector2(dx, dy)




        if movement.length() > 0:
            movement = movement.normalize() * self.speed




        self.rect.x += round(movement.x)




        if walls:
            for wall in walls:
                if self.rect.colliderect(wall):
                    if movement.x > 0:
                        self.rect.right = wall.left
                    elif movement.x < 0:
                        self.rect.left = wall.right




        self.rect.y += round(movement.y)




        if walls:
            for wall in walls:
                if self.rect.colliderect(wall):
                    if movement.y > 0:
                        self.rect.bottom = wall.top
                    elif movement.y < 0:
                        self.rect.top = wall.bottom




        if bounds:
            self.rect.clamp_ip(bounds)




    def attack(self, cursor_location):




        dx = cursor_location[0] - self.rect.centerx
        dy = cursor_location[1] - self.rect.centery




        if abs(dx) > abs(dy):
            if dx > 0:
                return pygame.Rect(self.rect.right, self.rect.centery - 35, 70, 70)
            return pygame.Rect(self.rect.left - 70, self.rect.centery - 35, 70, 70)




        if dy > 0:
            return pygame.Rect(self.rect.centerx - 35, self.rect.bottom, 70, 70)




        return pygame.Rect(self.rect.centerx - 35, self.rect.top - 70, 70, 70)




    def skill(self):




        if self.skill_unlocked and self.energy >= 30:
            self.energy -= 30
            return "Assassin dash activated"




        return None






class Berserker(pygame.sprite.Sprite):




    def __init__(self, image, spawning_location):
        super().__init__()




        self.image = image
        self.rect = self.image.get_rect(center=spawning_location)




        self.unlocked = False
        self.hp = 9
        self.armor = 3
        self.energy = 150
        self.speed = 6.5
        self.level = 1
        self.damage = 5




        self.skill_unlocked = False
        self.skill_name = "Rage"




    def move(self, keys, walls=None, bounds=None):
        dx = 0
        dy = 0




        if pygame.K_w in keys or pygame.K_UP in keys:
            dy -= self.speed
        if pygame.K_s in keys or pygame.K_DOWN in keys:
            dy += self.speed
        if pygame.K_a in keys or pygame.K_LEFT in keys:
            dx -= self.speed
        if pygame.K_d in keys or pygame.K_RIGHT in keys:
            dx += self.speed




        movement = pygame.math.Vector2(dx, dy)




        if movement.length() > 0:
            movement = movement.normalize() * self.speed


        self.rect.x += round(movement.x)


        if walls:
            for wall in walls:
                if self.rect.colliderect(wall):
                    if movement.x > 0:
                        self.rect.right = wall.left
                    elif movement.x < 0:
                        self.rect.left = wall.right
        self.rect.y += round(movement.y)
        if walls:
            for wall in walls:
                if self.rect.colliderect(wall):
                    if movement.y > 0:
                        self.rect.bottom = wall.top
                    elif movement.y < 0:
                        self.rect.top = wall.bottom
        if bounds:
            self.rect.clamp_ip(bounds)




    def attack(self, cursor_location):
        dx = cursor_location[0] - self.rect.centerx
        dy = cursor_location[1] - self.rect.centery




        if abs(dx) > abs(dy):
            if dx > 0:
                return pygame.Rect(self.rect.right, self.rect.centery - 35, 70, 70)
            return pygame.Rect(self.rect.left - 70, self.rect.centery - 35, 70, 70)




        if dy > 0:
            return pygame.Rect(self.rect.centerx - 35, self.rect.bottom, 70, 70)




        return pygame.Rect(self.rect.centerx - 35, self.rect.top - 70, 70, 70)




    def skill(self):
        if self.skill_unlocked and self.energy >= 30:
            self.energy -= 30
            return "Berserker rage activated"




        return None






class Paladin(pygame.sprite.Sprite):
    def __init__(self, image, spawning_location):
        super().__init__()




        self.image = image
        self.rect = self.image.get_rect(center=spawning_location)




        self.unlocked = False
        self.hp = 1
        self.armor = 8
        self.energy = 120
        self.speed = 6.5
        self.level = 1
        self.damage = 4




        self.skill_unlocked = False
        self.skill_name = "Holy Protection"




    def move(self, keys, walls=None, bounds=None):
        dx = 0
        dy = 0


        if pygame.K_w in keys or pygame.K_UP in keys:
            dy -= self.speed
        if pygame.K_s in keys or pygame.K_DOWN in keys:
            dy += self.speed
        if pygame.K_a in keys or pygame.K_LEFT in keys:
            dx -= self.speed
        if pygame.K_d in keys or pygame.K_RIGHT in keys:
            dx += self.speed


        movement = pygame.math.Vector2(dx, dy)




        if movement.length() > 0:
            movement = movement.normalize() * self.speed




        self.rect.x += round(movement.x)




        if walls:
            for wall in walls:
                if self.rect.colliderect(wall):
                    if movement.x > 0:
                        self.rect.right = wall.left
                    elif movement.x < 0:
                        self.rect.left = wall.right


        self.rect.y += round(movement.y)


        if walls:
            for wall in walls:
                if self.rect.colliderect(wall):
                    if movement.y > 0:
                        self.rect.bottom = wall.top
                    elif movement.y < 0:
                        self.rect.top = wall.bottom


        if bounds:
            self.rect.clamp_ip(bounds)




    def attack(self, cursor_location):
        dx = cursor_location[0] - self.rect.centerx
        dy = cursor_location[1] - self.rect.centery


        if abs(dx) > abs(dy):
            if dx > 0:
                return pygame.Rect(self.rect.right, self.rect.centery - 35, 70, 70)
            return pygame.Rect(self.rect.left - 70, self.rect.centery - 35, 70, 70)


        if dy > 0:
            return pygame.Rect(self.rect.centerx - 35, self.rect.bottom, 70, 70)
        return pygame.Rect(self.rect.centerx - 35, self.rect.top - 70, 70, 70)




    def skill(self):
        if self.skill_unlocked and self.energy >= 30:
            self.energy -= 30
            return "Paladin protection activated"


        return None




characters = {
    "Knight": Knight(player_image, (100, 100)),
    "Priestess": Priestess(player_image, (100, 100)),
    "Assassin": Assassin(player_image, (100, 100)),
    "Berserker": Berserker(player_image, (100, 100)),
    "Paladin": Paladin(player_image, (100, 100))
}


selected_character = "Knight"
coins = 0




def load_accounts():
    try:
        with open("accounts.json", "r") as f:
            return json.load(f)


    except (FileNotFoundError, json.JSONDecodeError):
        return {}




def save_accounts(accounts):
    with open("accounts.json", "w") as f:
        json.dump(accounts, f, indent=4)




accounts = load_accounts()




current_user = ""
username = ""
password = ""




active_input = None
login_mode = "login"
message = ""




def get_save_file():
    return current_user + "_save.json"




def save_game():
    if not current_user:
        return


    saved_characters = {}


    for name, character in characters.items():


        saved_characters[name] = {
            "unlocked": character.unlocked,
            "hp": character.hp,
            "armor": character.armor,
            "energy": character.energy,
            "speed": character.speed,
            "level": character.level,
            "damage": character.damage,
            "skill_unlocked": character.skill_unlocked
        }


    data = {
        "coins": coins,
        "selected_character": selected_character,
        "characters": saved_characters
    }


    with open(get_save_file(), "w") as f:
        json.dump(data, f, indent=4)






def load_game():
    global coins, selected_character


    try:
        with open(get_save_file(), "r") as f:
            data = json.load(f)


    except (FileNotFoundError, json.JSONDecodeError):
        return False


    coins = data.get("coins", 0)
    selected_character = data.get("selected_character", "Knight")


    saved_characters = data.get("characters", {})


    for name, character in characters.items():
        if name in saved_characters:
            saved_data = saved_characters[name]


            character.unlocked = saved_data.get("unlocked", character.unlocked)
            character.hp = saved_data.get("hp", character.hp)
            character.armor = saved_data.get("armor", character.armor)
            character.energy = saved_data.get("energy", character.energy)
            character.speed = saved_data.get("speed", character.speed)
            character.level = saved_data.get("level", character.level)
            character.damage = saved_data.get("damage", character.damage)
            character.skill_unlocked = saved_data.get("skill_unlocked", character.skill_unlocked)


    if selected_character not in characters:
        selected_character = "Knight"


    return True






def has_save():
    try:
        with open(get_save_file(), "r") as f:
            data = json.load(f)
        return "characters" in data


    except (FileNotFoundError, json.JSONDecodeError):
        return False




username_rect = pygame.Rect(330, 250, 300, 45)
password_rect = pygame.Rect(330, 320, 300, 45)
submit_rect = pygame.Rect(380, 400, 200, 55)
switch_rect = pygame.Rect(330, 475, 300, 40)








def handle_account(event):




    global username, password
    global active_input, login_mode
    global message, current_user, game_state




    if event.type == pygame.MOUSEBUTTONDOWN:


        if username_rect.collidepoint(event.pos):
            active_input = "username"


        elif password_rect.collidepoint(event.pos):
            active_input = "password"


        elif submit_rect.collidepoint(event.pos):


            if username == "" or password == "":
                message = "Please enter username and password"




            elif login_mode == "register":
                if username in accounts:
                    message = "Username already exists"


                else:
                    accounts[username] = password
                    save_accounts(accounts)
                    message = "Registration successful"




            else:
                if accounts.get(username) == password:
                    current_user = username
                    game_state = "menu"
                    message = ""


                else:
                    message = "Incorrect username or password"




        elif switch_rect.collidepoint(event.pos):




            login_mode = (
                "register" if login_mode == "login"
                else "login"
            )




            message = ""




    elif event.type == pygame.KEYDOWN:




        if active_input == "username":




            if event.key == pygame.K_BACKSPACE:
                username = username[:-1]




            elif event.key != pygame.K_RETURN:
                username += event.unicode




        elif active_input == "password":




            if event.key == pygame.K_BACKSPACE:
                password = password[:-1]




            elif event.key != pygame.K_RETURN:
                password += event.unicode








def draw_account_screen():




    screen.blit(background_image, (0, 0))




    title = "Login" if login_mode == "login" else "Register"




    title_image = big_font.render(title, True, WHITE)
    screen.blit(title_image, title_image.get_rect(center=(480, 160)))




    pygame.draw.rect(screen, WHITE, username_rect)
    pygame.draw.rect(screen, WHITE, password_rect)




    draw_text(username, font, BLACK, 340, 258)
    draw_text("*" * len(password), font, BLACK, 340, 328)




    draw_text("Username", font, WHITE, 330, 220)
    draw_text("Password", font, WHITE, 330, 290)




    draw_button("Submit", submit_rect, BLUE)




    switch_text = (
        "Create an account"
        if login_mode == "login"
        else "Back to login"
    )




    draw_text(switch_text, font, WHITE, 370, 480)
    draw_text(message, font, RED, 330, 540)












def draw_text(text, text_font, color, x, y):
    image = text_font.render(str(text), True, color)
    screen.blit(image, (x, y))








def draw_button(text, rect, color):
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)


    text_image = font.render(text, True, WHITE)
    text_rect = text_image.get_rect(center=rect.center)


    screen.blit(text_image, text_rect)








new_game_rect = pygame.Rect(380, 280, 200, 60)
previous_game_rect = pygame.Rect(380, 370, 200, 60)








def draw_menu():
    screen.blit(background_image, (0, 0))


    title = big_font.render("Dungeon Adventure", True, WHITE)
    screen.blit(title, title.get_rect(center=(480, 170)))


    draw_button("New Game", new_game_rect, BLUE)


    if has_save():
        draw_button("Previous Game", previous_game_rect, GREEN)








def new_game():
    global coins, selected_character, game_state
    coins = 0
    selected_character = "Knight"
    game_state = "character_select"




character_buttons = []






def draw_character_select():
    screen.fill(DARK_GRAY)


    title = big_font.render("Choose Your Character", True, WHITE)
    screen.blit(title, title.get_rect(center=(480, 100)))


    character_buttons.clear()


    for i, name in enumerate(characters):


        rect = pygame.Rect(330, 180 + i * 75, 300, 55)
        character_buttons.append((name, rect))


        if characters[name].unlocked:
            draw_button(name, rect, GREEN)


        else:
            draw_button(name + " - Locked", rect, GRAY)
    draw_text("Coins: " + str(coins), font, WHITE, 30, 30)








def select_character(mouse_pos):
    global selected_character, game_state


    for name, rect in character_buttons:


        if rect.collidepoint(mouse_pos):


            if characters[name].unlocked:
                selected_character = name
                game_state = "lobby"


lobby_bounds = pygame.Rect(0, 0, 960, 640)




keys_pressed = set()




def draw_lobby():
    screen.fill((35, 35, 35))


    screen.blit(table_image, table_rect)


    character = characters[selected_character]
    screen.blit(character.image, character.rect)


    draw_text("Character: " + selected_character, font, WHITE, 20, 20)
    draw_text("Coins: " + str(coins), font, WHITE, 20, 55)
    draw_text("SPACE: Enter Battle", font, WHITE, 20, 550)
    draw_text("WASD / Arrow Keys: Move", font, WHITE, 20, 580)
    draw_text("ESC: Return to menu", font, WHITE, 20, 610)








wall_rects = []




battle_started = False




attack_rect = None
attacking = False




attack_start_time = 0
last_attack_time = 0




attack_duration = 150
attack_cooldown = 400








def load_walls():
    global wall_rects


    wall_rects = []
    wall_layer = tiled_map.get_layer_by_name("Object Layer 1")
    for obj in wall_layer:
            wall_rect = pygame.Rect(
                int(obj.x),
                int(obj.y),
                int(obj.width),
                int(obj.height)
            )
            wall_rects.append(wall_rect)




def enter_battle():
    global game_state, battle_started
    global attacking, last_attack_time
    draw_image_layers()
    load_walls()
    character = characters[selected_character]
    character.rect.center = (960 // 2,640 // 2)

    character.rect.clamp_ip(
        pygame.Rect(0, 0, 960, 640)
    )

    battle_started = True
    attacking = False
    last_attack_time = 0
    game_state = "combat"




def start_attack():




    global attacking, attack_rect
    global attack_start_time, last_attack_time




    current_time = pygame.time.get_ticks()




    if current_time - last_attack_time < attack_cooldown:
        return




    character = characters[selected_character]




    attack_rect = character.attack(pygame.mouse.get_pos())




    attacking = True
    attack_start_time = current_time
    last_attack_time = current_time








def use_character_skill():
    character = characters[selected_character]
    result = character.skill()
    if result:
        print(result)








def draw_attack():
    global attacking
    if not attacking:
        return
    current_time = pygame.time.get_ticks()
    if current_time - attack_start_time > attack_duration:
        attacking = False
        return
    if attack_rect:
        pygame.draw.rect(screen, (255, 220, 60), attack_rect)








def draw_combat():
    screen.blit(background, (0, 0))


    character = characters[selected_character]


    screen.blit(character.image, character.rect)


    draw_attack()


    draw_text("Character: " + selected_character,font,WHITE,15,15)




    draw_text("HP: " + str(character.hp),font,
        WHITE,
        15,
        45
    )




    draw_text(
        "Armor: " + str(character.armor),
        font,
        WHITE,
        15,
        75
    )




    draw_text(
        "Energy: " + str(character.energy),
        font,
        WHITE,
        15,
        105
    )




    draw_text(
        "Left Click: Attack | Q: Skill",
        font,
        WHITE,
        15,
        560
    )




    draw_text(
        "ESC: Save and return to menu",
        font,
        WHITE,
        15,
        590
    )




game_state = "account"
running = True




while running:




    clock.tick(60)




    for event in pygame.event.get():




        if event.type == pygame.QUIT:




            if battle_started:
                save_game()




            running = False




        elif game_state == "account":




            handle_account(event)




        elif game_state == "menu":




            if event.type == pygame.MOUSEBUTTONDOWN:




                if new_game_rect.collidepoint(event.pos):
                    new_game()




                elif (
                    previous_game_rect.collidepoint(event.pos)
                    and has_save()
                ):




                    if load_game():
                        game_state = "lobby"




        elif game_state == "character_select":




            if event.type == pygame.MOUSEBUTTONDOWN:
                select_character(event.pos)




        elif game_state == "lobby":




            if event.type == pygame.KEYDOWN:




                if event.key == pygame.K_SPACE:
                    enter_battle()




                elif event.key == pygame.K_ESCAPE:
                    keys_pressed.clear()
                    game_state = "menu"




                else:
                    keys_pressed.add(event.key)




            elif event.type == pygame.KEYUP:
                keys_pressed.discard(event.key)




        elif game_state == "combat":




            if event.type == pygame.KEYDOWN:




                if event.key == pygame.K_ESCAPE:




                    save_game()




                    battle_started = False
                    keys_pressed.clear()




                    game_state = "menu"




                elif event.key == pygame.K_q:
                    use_character_skill()




                else:
                    keys_pressed.add(event.key)




            elif event.type == pygame.KEYUP:
                keys_pressed.discard(event.key)




            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start_attack()






    if game_state == "lobby":




        character = characters[selected_character]




        character.move(
            keys_pressed,
            bounds=lobby_bounds
        )




    elif game_state == "combat":




        character = characters[selected_character]




        battle_bounds = pygame.Rect(
            0,
            0,
            960,
            640
        )




        character.move(
            keys_pressed,
            walls=wall_rects,
            bounds=battle_bounds
        )




    if game_state == "account":
        draw_account_screen()




    elif game_state == "menu":
        draw_menu()




    elif game_state == "character_select":
        draw_character_select()




    elif game_state == "lobby":
        draw_lobby()




    elif game_state == "combat":
        draw_combat()




    pygame.display.update()








pygame.quit()
