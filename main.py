import pygame 
import time 
import math 


def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)




Track = pygame.image.load("racetrack1.png")
Track = pygame.transform.scale(Track, (1000, 1000))



Track_Border = (62,171,83)

Path = PATH = [(109, 544), (423, 831), (492, 609), (577, 558), (662, 596), (695, 794), (764, 829), (760, 848), (823, 452), (495, 422), (477, 370), (529, 329), (815, 313), (836, 212), (809, 131), (367, 136), (338, 435), (288, 485), (205, 132)]






Blue_Car = pygame.image.load("pixel_racecar_blue.png")

Orange_car = pygame.image.load("pixel_racecar_orange.png")

WIDTH, HEIGHT = Track.get_width(), Track.get_height()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))



pygame.display.set_caption('Racing Game')

FPS = 1000

class Car: 
    def __init__(self, max_vel, rotation_vel):
        self.img = Blue_Car 
        self.rect = self.img.get_rect()
        self.max_vel = max_vel 
        self.vel = 0 
        self.rotation_vel = rotation_vel
        self.angle = 0 
        self.x, self.y = self.START_POS 

        self.rect.x, self.rect.y = self.START_POS
        self.acceleration = .1 
        

    
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

        

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)


    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()


    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()
    
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel 
        horizontal = math.sin(radians) * self.vel 

        self.rect.x -= horizontal
        self.rect.y -= vertical

        self.y -= vertical 
        self.x -= horizontal 

    def hit(self, win):
       # print(self.x, self.y)
        x = self.x
        x = x 
        x = round(x)
        y = self.y 
        y = round(y)

        if win.get_at((x, y)) ==  (79,176,95):
           player_car.bounce()
         #  print('collided')


        



    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0
    
    def bounce(self):
        self.vel -= self.vel 
        self.move()

    def reduce_speed(self):
        self.vel -= self.vel
        self.move()



class PlayerCar(Car):
  
    IMG = Blue_Car
    START_POS = (185, 134)





class ComputerCar(Car):
    Img = Orange_car
    START_POS = (185, 134)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path 
        self.current_point = 0 
        self.vel = max_vel 

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)
    
    def draw(self, win):
        super().draw(win)
    
    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(
            self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return

        if self.path == self.path[-1]:
            self.path == self.path[0]
        self.calculate_angle()
        self.update_path_point()
        super().move()
    
    def reverse_move(self):
        if self.current_point <= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        super().move()
        



def move_player(player_car): 
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()

    if not moved:
        player_car.reduce_speed()



def draw(win, images, player_car, computer_car, computer_car2):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    computer_car.draw(win)
    computer_car2.draw(win)

    player_car.hit(win)
    pygame.display.update()


run = True
clock = pygame.time.Clock()
images = [(Track, (0, 0))]
player_car = PlayerCar(4, 4)
computer_car = ComputerCar(3, 3, Path)
computer_car2 = ComputerCar(7, 7, Path)

#computer_car2 = ComputerCar(4, 4, Path_Reverse)
while run:
    clock.tick(FPS)


    draw(WINDOW, images, player_car, computer_car, computer_car2)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
    keys = pygame.key.get_pressed()

    move_player(player_car)


    computer_car.move()

    if computer_car.x != 185:
        computer_car2.move()


pygame.quit()
