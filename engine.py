"""
@author : Léo Imbert
@created : 04/10/2025
@updated : 04/10/2025
"""

#? ---------- IMPORTATIONS ---------- ?#

import pygame
import math

#? ---------- CONSTANTS ---------- ?#

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#? ---------- BODIES ---------- ?#

class Body:
    
    def __init__(self, x, y, vx=0, vy=0, mass=1, color=WHITE):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.mass = mass
        self.color = color

    def apply_force(self, fx, fy):
        self.vx += fx / self.mass
        self.vy += fy / self.mass

    def update(self, dt=1):
        self.x += self.vx * dt
        self.y += self.vy * dt

class Rect(Body):

    def __init__(self, x, y, w, h, vx=0, vy=0, mass=1, color=WHITE, static=False, bounciness=0.8):
        super().__init__(x, y, vx, vy, mass, color)
        self.w, self.h = w, h
        self.static = static
        self.bounciness = bounciness

    def update(self, dt=1):
        if not self.static:
            super().update(dt)

    def draw(self, screen):
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(screen, self.color, rect)

#? ---------- FUNCTIONS ---------- ?#

def rects_collide(r1, r2):
    return (r1.x < r2.x + r2.w and r1.x + r1.w > r2.x and r1.y < r2.y + r2.h and r1.y + r1.h > r2.y)

def resolve_collision(r1, r2, restitution=1.0):
    dx = (r1.x + r1.w / 2) - (r2.x + r2.w / 2)
    dy = (r1.y + r1.h / 2) - (r2.y + r2.h / 2)
    overlap_x = (r1.w / 2 + r2.w / 2) - abs(dx)
    overlap_y = (r1.h / 2 + r2.h / 2) - abs(dy)

    if overlap_x < 0 or overlap_y < 0:
        return

    if overlap_x < overlap_y:
        if dx > 0:
            r1.x += overlap_x / 2
            r2.x -= overlap_x / 2 if not r2.static else 0
        else:
            r1.x -= overlap_x / 2
            r2.x += overlap_x / 2 if not r2.static else 0

        if not r1.static and not r2.static:
            r1.vx, r2.vx = r2.vx * restitution, r1.vx * restitution
        elif r1.static:
            r2.vx *= -restitution
        elif r2.static:
            r1.vx *= -restitution
    else:
        if dy > 0:
            r1.y += overlap_y / 2
            r2.y -= overlap_y / 2 if not r2.static else 0
        else:
            r1.y -= overlap_y / 2
            r2.y += overlap_y / 2 if not r2.static else 0

        if not r1.static and not r2.static:
            r1.vy, r2.vy = r2.vy * restitution, r1.vy * restitution
        elif r1.static:
            r2.vy *= -restitution
        elif r2.static:
            r1.vy *= -restitution

#? ---------- ENGINE ---------- ?#

class Engine:

    def __init__(self, x, y, w, h, gravity=0.5):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.bodies = []
        self.gravity = gravity

    def add_body(self, body):
        self.bodies.append(body)

    def update(self):
        for body in self.bodies:
            if isinstance(body, Rect) and not body.static:
                body.vy += self.gravity

            body.update()
            
            if isinstance(body, Rect):
                if body.x < self.x:
                    body.x = self.x
                    body.vx *= -body.bounciness
                elif body.x + body.w > self.x + self.w:
                    body.x = self.x + self.w - body.w
                    body.vx *= -body.bounciness

                if body.y < self.y:
                    body.y = self.y
                    body.vy *= -body.bounciness
                elif body.y + body.h > self.y + self.h:
                    body.y = self.y + self.h - body.h
                    body.vy *= -body.bounciness

        for i in range(len(self.bodies)):
            for j in range(i + 1, len(self.bodies)):
                b1, b2 = self.bodies[i], self.bodies[j]
                if isinstance(b1, Rect) and isinstance(b2, Rect):
                    if rects_collide(b1, b2):
                        resolve_collision(b1, b2, restitution=min(b1.bounciness, b2.bounciness))

    def draw(self, screen):
        for body in self.bodies:
            body.draw(screen)