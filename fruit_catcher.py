import cv2
import mediapipe as mp
import pygame
import random
import time
import os
import mediapipe as mp
# --------------------------
# Initialize Pygame
# --------------------------
pygame.init()

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Head Controlled Fruit Catcher")

font = pygame.font.SysFont("Arial", 35)
big_font = pygame.font.SysFont("Arial", 60)

# --------------------------
# Colors
# --------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# --------------------------
# Load Images
# --------------------------

# --------------------------
# Load Images From PC Location
# --------------------------

background = pygame.image.load(
    r"D:\USER FILES DONT DELETE\Downloads\background.png"
)
background = pygame.transform.scale(
    background,
    (WIDTH, HEIGHT)
)

basket_img = pygame.image.load(
    r"D:\USER FILES DONT DELETE\Downloads\basketnew.png"
)
basket_img = pygame.transform.scale(
    basket_img,
    (150, 100)
)

apple_img = pygame.image.load(
    r"D:\USER FILES DONT DELETE\Downloads\applenew.png"
)
apple_img = pygame.transform.scale(
    apple_img,
    (60, 60)
)

banana_img = pygame.image.load(
    r"D:\USER FILES DONT DELETE\Downloads\banananew.png"
)
banana_img = pygame.transform.scale(
    banana_img,
    (60, 60)
)

orange_img = pygame.image.load(
    r"D:\USER FILES DONT DELETE\Downloads\orangenew.png"
)
orange_img = pygame.transform.scale(
    orange_img,
    (60, 60)
)

# --------------------------
# Fruit Data
# --------------------------

fruit_data = [
    (apple_img, 1),
    (banana_img, 2),
    (orange_img, 3)
]

current_fruit, fruit_points = random.choice(
    fruit_data
)

fruit_width = 60
fruit_height = 60

fruit_x = random.randint(
    50,
    WIDTH - fruit_width
)

fruit_y = 0
fruit_speed = 7

# --------------------------
# Basket
# --------------------------

basket_width = 150
basket_height = 100

basket_x = WIDTH // 2

# --------------------------
# Score
# --------------------------

score = 0
lives = 3

# --------------------------
# Timer
# --------------------------

GAME_TIME = 60
start_time = time.time()

# --------------------------
# Webcam Setup
# --------------------------

cap = cv2.VideoCapture(0)
mp_face = mp.solutions.face_detection
face_detection_model = mp_face.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.5
)

# --------------------------
# Game Loop
# --------------------------

running = True

while running:

    # ----------------------
    # Background
    # ----------------------

    screen.blit(background, (0, 0))

    # ----------------------
    # Webcam Input
    # ----------------------

    ret, frame = cap.read()

    if ret:

        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = face_detection_model.process(rgb)

        if results.detections:

            for detection in results.detections:

                bbox = detection.location_data.relative_bounding_box

                h, w, _ = frame.shape

                face_x = int(
                    bbox.xmin * w
                )

                basket_x = int(
                    (face_x / w) * WIDTH
                )

                basket_x = max(
                    0,
                    min(
                        WIDTH - basket_width,
                        basket_x
                    )
                )

        cv2.imshow(
            "Head Tracking Camera",
            frame
        )

    # ----------------------
    # Move Fruit
    # ----------------------

    fruit_y += fruit_speed

    # ----------------------
    # Draw Fruit
    # ----------------------

    screen.blit(
        current_fruit,
        (fruit_x, fruit_y)
    )

    # ----------------------
    # Draw Basket
    # ----------------------

    screen.blit(
        basket_img,
        (
            basket_x,
            HEIGHT - 110
        )
    )

    # ----------------------
    # Collision
    # ----------------------

    fruit_rect = pygame.Rect(
        fruit_x,
        fruit_y,
        fruit_width,
        fruit_height
    )

    basket_rect = pygame.Rect(
        basket_x,
        HEIGHT - 110,
        basket_width,
        basket_height
    )

    if fruit_rect.colliderect(
        basket_rect
    ):

        score += fruit_points

        fruit_x = random.randint(
            50,
            WIDTH - fruit_width
        )

        fruit_y = 0

        current_fruit, fruit_points = random.choice(
            fruit_data
        )

    # ----------------------
    # Missed Fruit
    # ----------------------

    if fruit_y > HEIGHT:

        lives -= 1

        fruit_x = random.randint(
            50,
            WIDTH - fruit_width
        )

        fruit_y = 0

        current_fruit, fruit_points = random.choice(
            fruit_data
        )

    # ----------------------
    # Timer
    # ----------------------

    elapsed = int(
        time.time() - start_time
    )

    remaining = GAME_TIME - elapsed

    # ----------------------
    # Score Panel
    # ----------------------

    panel = pygame.Surface(
        (250, 140)
    )

    panel.set_alpha(180)
    panel.fill((255, 255, 255))

    screen.blit(panel, (10, 10))

    score_text = font.render(
        f"Score: {score}",
        True,
        BLACK
    )

    lives_text = font.render(
        f"Lives: {lives}",
        True,
        BLACK
    )

    timer_text = font.render(
        f"Time: {remaining}",
        True,
        BLACK
    )

    screen.blit(score_text, (25, 25))
    screen.blit(lives_text, (25, 65))
    screen.blit(timer_text, (25, 105))

    # ----------------------
    # Game Over
    # ----------------------

    if lives <= 0 or remaining <= 0:

        screen.blit(
            background,
            (0, 0)
        )

        over_text = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        final_score = font.render(
            f"Final Score : {score}",
            True,
            BLACK
        )

        screen.blit(
            over_text,
            (
                WIDTH // 2 - 180,
                HEIGHT // 2 - 80
            )
        )

        screen.blit(
            final_score,
            (
                WIDTH // 2 - 100,
                HEIGHT // 2 + 10
            )
        )

        pygame.display.update()

        pygame.time.delay(5000)

        running = False

    # ----------------------
    # Events
    # ----------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

    pygame.display.update()

    if cv2.waitKey(1) & 0xFF == 27:
        running = False

# --------------------------
# Cleanup
# --------------------------

cap.release()
cv2.destroyAllWindows()
pygame.quit()