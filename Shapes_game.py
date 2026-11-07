import cv2
import numpy as np
import time
import random

width = 700
height = 600
gametime = 30
score = 0
lives = 3
shapes = ["Circle", "Square", "Triangle", "Pentagon"]
target = random.choice(shapes)
start = time.time()
game = True
mousex = 0
mousey = 0
clicked = False
quit_game = False


def create_screen():
    img = np.ones((height, width, 3), dtype=np.uint8) * 255

    for i in range(15):
        shape = random.choice(shapes)
        x = random.randint(100, width - 50)
        y = random.randint(100, height - 50)

        if shape == "Circle":
            cv2.circle(img, (x, y), 30, (255, 0, 255), -1)

        elif shape == "Square":
            cv2.rectangle(img, (x, y), (x + 50, y + 50),
                          (255, 0, 255), -1)

        elif shape == "Pentagon":
            points = np.array([
                [x, y - 45],
                [x + 43, y - 14],
                [x + 27, y + 36],
                [x - 27, y + 36],
                [x - 43, y - 14]
            ])
            cv2.fillPoly(img, [points], (255, 0, 255))

        else:
            points = np.array([
                (x, y),
                (x - 40, y + 30),
                (x + 40, y + 30)
            ], dtype=np.int32)
            cv2.fillPoly(img, [points], (255, 0, 255))

    return img


def detect_shapes(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(
        gray, 150, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(
        threshold,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)

    detected = []

    for contour in contours:
        area = cv2.contourArea(contour)

        if area < 500:
            continue

        perimeter = cv2.arcLength(contour, True)

        corners = cv2.approxPolyDP(
            contour,
            0.04 * perimeter,
            True)

        if len(corners) == 3:
            name = "Triangle"
        elif len(corners) == 4:
            name = "Square"
        elif len(corners) == 5:
            name = "Pentagon"
        else:
            name = "Circle"

        detected.append({
            "name": name,
            "contour": contour
        })

    return detected


def mouse_click(event, x, y, flags, param):
    global mousex, mousey, clicked

    if event == cv2.EVENT_LBUTTONDOWN:
        mousex = x
        mousey = y
        clicked = True


screen = create_screen()

cv2.namedWindow("Shape Hunter")
cv2.setMouseCallback("Shape Hunter", mouse_click)


while game:
    elapsed = time.time() - start

    if elapsed > gametime:
        game = False

    if clicked:
        detected_shapes = detect_shapes(screen)
        found_shape = None

        for shape in detected_shapes:
            contour = shape["contour"]
            inside = cv2.pointPolygonTest(
                contour, (mousex, mousey), False)

            if inside >= 0:
                found_shape = shape["name"]
                break

        if found_shape is not None:
            print("Clicked:", found_shape, "| Target:", target)

            if target == found_shape:
                score += 1
            else:
                lives -= 1
                print(lives)

        target = random.choice(shapes)
        screen = create_screen()
        clicked = False

        if lives <= 0:
            game = False

    cv2.rectangle(
        screen, (0, 0), (700, 50), (255, 255, 255), -1)

    cv2.putText(
        screen, f"Time: {int(elapsed)}", (550, 30),
        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)

    cv2.putText(
        screen, f"Score: {score}", (400, 30),
        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)

    cv2.putText(
        screen, f"Lives: {lives}", (280, 30),
        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)

    cv2.putText(
        screen, f"Target: {target}", (40, 30),
        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)

    cv2.imshow("Shape Hunter", screen)

    key = cv2.waitKey(30)

    if key == ord("q"):
        quit_game = True
        game = False


# GAME OVER SCREEN
if not quit_game:
    game_over_screen = np.ones(
        (height, width, 3), dtype=np.uint8) * 255

    cv2.putText(
        game_over_screen, "GAME OVER", (190, 200),
        cv2.FONT_HERSHEY_SIMPLEX, 2,
        (0, 0, 255), 3)

    cv2.putText(
        game_over_screen, f"Final Score: {score}", (220, 270),
        cv2.FONT_HERSHEY_SIMPLEX, 1,
        (0, 0, 0), 2)

    cv2.putText(
        game_over_screen, "Press Q to exit", (230, 330),
        cv2.FONT_HERSHEY_SIMPLEX, 0.8,
        (0, 0, 0), 2)

    while True:
        cv2.imshow("Shape Hunter", game_over_screen)

        key = cv2.waitKey(30)

        if key == ord("q"):
            break


cv2.destroyAllWindows()
