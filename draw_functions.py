import pygame
import cv2
import random


def draw_hand_points(frame, hand_keypoints):
    for point in hand_keypoints:
        x, y = int(point[0]), int(point[1])
        cv2.circle(frame, (x, y), 3, (0, 0, 255), 3)

    return frame


def draw_hand_points_pg(screen, hand_keypoints):
    """
    draw hand keypoints
    
    :param screen: pygame screen
    :param hand_keypoints: list of keybpoints
    """
    for point in hand_keypoints:
        pygame.draw.circle(surface=screen, color="red",
                           center=point, radius=2)


def draw_frame(screen, frame, top_left, size=None):
    """
    draws opencv frame on pygame screen

    :param screen: pygame screen
    :param frame: frame to draw (opencv brg matrix)
    :param top_left: top left corner formatted (x, y)
    :param size: (width, height) to draw it at
    """
    # get frame info
    frame_height, frame_width, num_channels = frame.shape
    
    # get size of target area to display on (default is entire screen)
    if size is None:
        target_width, target_height = screen.get_size()
    else:
        target_width, target_height = size

    # find scaled size depending which aspect is bigger compared to target
    scale_factor = min(target_width/frame_width, target_height/frame_height)
    new_frame_width, new_frame_height = frame_width * scale_factor, frame_height * scale_factor

    # resize if needed
    if new_frame_width != frame_width:
        frame = cv2.resize(frame, (new_frame_width, new_frame_height))

    # draw frame
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_surface = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))
    screen.blit(frame_surface, top_left)


def draw_points(screen, point_list, colour):
    """
    draw list of corners on given screen, with colour depending on whether they
    have been saved or not

    :param screen: pygame screen
    :param point_list: list of corner positions
    :param corners_saved: boolean
    """
    for corner in point_list:
        pygame.draw.circle(surface=screen,
                           color=colour,
                           center=corner,
                           radius=2)


def draw_keys(screen, key_tops, key_bases, overlap, outline_colour, outline_width):
    """
    draw polygons for white keys given coordinates
    the coordinates overlap

    :param screen: pygame screen
    :param key_tops: coordinates of key tops
    :param key_bases: coordinates of key bottoms
    :param overlap: boolean, true if 3 pairs of points for two keys, false if 4
    :param outline_colour: colour of key outline
    :param outline_colour: width of key outline
    """
    # don't draw anything if the lists of points are not the same length
    if len(key_tops) != len(key_bases):
        return None

    if overlap:
        step = 1
    else:
        step = 2

    for i in range(0, len(key_tops) - 1, step):
        # if no black key, don't draw
        if key_tops[i] is None:
            continue
        pygame.draw.polygon(surface=screen,
                            color=outline_colour,
                            points=(
                                key_tops[i],
                                key_tops[i+1],
                                key_bases[i+1],
                                key_bases[i]
                            ),
                            width=outline_width)


def draw_tabletop(screen, left, right, outline_colour, outline_width):
    """
    draw line for where table is being detected
    
    :param screen: pygame screen
    :param left: coordinate for left end
    :param right: coordinate for right end
    :param outline_colour: colour of key outline
    :param outline_colour: width of key outline
    """
    pygame.draw.line(surface=screen,
                     color=outline_colour,
                     start_pos=left,
                     end_pos=right,
                     width=outline_width)
    



class SmokeParticle:
    '''
    Docstring for SmokeParticle

    class to draw particles and make them fade away when we we press a specific key

    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(4, 8)
        self.life = 255  
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-3, -1)
        self.growth = 0.12 

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.radius += self.growth
        self.life -= 2  


    def draw(self, surface):
        if self.life > 0:
            s = pygame.Surface((int(self.radius*2), int(self.radius*2)), pygame.SRCALPHA)

            pygame.draw.circle(s, (150, 150, 150, self.life), (self.radius, self.radius), int(self.radius))
            
            surface.blit(s, (self.x - self.radius, self.y - self.radius))

