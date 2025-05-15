import cv2
import mediapipe as mp
import numpy as np
import math
from datetime import datetime


class CupidsArrowGame:
    def __init__(self):
        self.pose = mp.solutions.pose.Pose()
        self.mp_draw = mp.solutions.drawing_utils
        self.score = 0
        self.hearts = []
        self.arrows = []
        self.is_drawing_bow = False
        self.last_shot_time = datetime.now()
        self.cooldown = 1.0
        self.heart_img = cv2.resize(cv2.imread('heart.png', cv2.IMREAD_UNCHANGED), (50, 50))
        self.start_time = datetime.now()
        self.high_score = 0
        self.screen_width, self.screen_height = 640, 480
        self.max_hearts = 5

    def spawn_heart(self):
        if len(self.hearts) < self.max_hearts:
            x = np.random.randint(100, self.screen_width - 100)
            y = np.random.randint(100, self.screen_height - 100)
            speed = np.random.uniform(1.5, 3.5)
            self.hearts.append({'x': x, 'y': y, 'speed': speed})

    def draw_bow(self, frame, elbow, wrist):
        if elbow and wrist:
            center = tuple(map(int, elbow))
            radius = 150
            cv2.ellipse(frame, center, (radius, radius), 0, -45, 45, (255, 0, 255), 12)
            cv2.ellipse(frame, center, (radius + 5, radius + 5), 0, -45, 45, (200, 0, 200), 8)
            cv2.line(frame, center, tuple(map(int, wrist)), (200, 200, 255), 12)
            cv2.line(frame, center, tuple(map(int, wrist)), (255, 255, 255), 6)
            return min(math.dist(elbow, wrist) / 100.0, 1.0)
        return 0

    def shoot_arrow(self, origin, direction):
        norm_dir = direction / np.linalg.norm(direction)
        self.arrows.append({
            'x': origin[0], 'y': origin[1],
            'dx': norm_dir[0] * 10,
            'dy': norm_dir[1] * 10
        })

    def update_game_objects(self):
        for heart in self.hearts[:]:
            heart['x'] += math.sin(datetime.now().timestamp()) * heart['speed']
            if heart['x'] < 0 or heart['x'] > self.screen_width:
                self.hearts.remove(heart)

        for arrow in self.arrows[:]:
            arrow['x'] += arrow['dx']
            arrow['y'] += arrow['dy']
            for heart in self.hearts[:]:
                if math.dist([arrow['x'], arrow['y']], [heart['x'], heart['y']]) < 25:
                    self.score += 10
                    self.hearts.remove(heart)
                    self.arrows.remove(arrow)
                    break
            else:
                if (arrow['x'] < 0 or arrow['x'] > self.screen_width or
                        arrow['y'] < 0 or arrow['y'] > self.screen_height):
                    self.arrows.remove(arrow)

    def show_welcome_screen(self):
        screen = np.zeros((self.screen_height, self.screen_width, 3), dtype=np.uint8)
        animation = 0
        while True:
            frame = screen.copy()
            animation = (animation + 5) % 255
            cv2.putText(frame, "CUPID'S ARROW", (120, 150), cv2.FONT_HERSHEY_TRIPLEX, 2, (animation, 0, 255), 3)
            cv2.putText(frame, "THE LOVE GAME", (170, 220), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, animation, animation), 2)

            instructions = [
                "HOW TO PLAY:",
                "1. RAISE YOUR RIGHT ARM",
                "2. DRAW BACK TO SHOOT",
                "3. HIT THE HEARTS",
                "",
                "PRESS ENTER TO START"
            ]
            for i, line in enumerate(instructions):
                intensity = int(abs(math.sin(animation / 50 + i / 2)) * 255)
                cv2.putText(frame, line, (180, 280 + i * 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (intensity, intensity, intensity), 2)

            for y in range(0, self.screen_height, 2):
                frame[y:y + 1] = frame[y:y + 1] * 0.5

            cv2.imshow("Cupid's Arrow AR Game", frame)
            if cv2.waitKey(50) == 13:
                break

        for i in range(255, 0, -5):
            fade = cv2.multiply(screen.copy(), np.array([i / 255.0]))
            cv2.imshow("Cupid's Arrow AR Game", fade)
            cv2.waitKey(1)

    def display_timer(self, frame):
        elapsed = int((datetime.now() - self.start_time).total_seconds())
        cv2.putText(frame, f"Time: {elapsed}s", (440, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    def check_game_over(self):
        return len(self.hearts) == 0 and len(self.arrows) == 0

    def run_game(self):
        self.show_welcome_screen()
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb)
            overlay = frame.copy()

            if results.pose_landmarks:
                lm = results.pose_landmarks.landmark
                get_point = lambda idx: (lm[idx].x * self.screen_width, lm[idx].y * self.screen_height)
                right_shoulder = get_point(mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER)
                right_elbow = get_point(mp.solutions.pose.PoseLandmark.RIGHT_ELBOW)
                right_wrist = get_point(mp.solutions.pose.PoseLandmark.RIGHT_WRIST)

                draw_percentage = self.draw_bow(frame, right_elbow, right_wrist)

                if draw_percentage > 0.8 and not self.is_drawing_bow and \
                        (datetime.now() - self.last_shot_time).total_seconds() > self.cooldown:
                    direction = np.array([right_wrist[0] - right_elbow[0], right_wrist[1] - right_elbow[1]])
                    self.shoot_arrow(right_shoulder, direction)
                    self.last_shot_time = datetime.now()

                self.is_drawing_bow = draw_percentage > 0.8

            if np.random.random() < 0.02:
                self.spawn_heart()

            self.update_game_objects()

            for heart in self.hearts:
                x, y = int(heart['x']), int(heart['y'])
                size = 40
                cv2.circle(overlay, (x - size // 4, y), size // 2, (0, 0, 255), -1)
                cv2.circle(overlay, (x + size // 4, y), size // 2, (0, 0, 255), -1)
                points = np.array([[x - size // 2, y + size // 4], [x, y + size], [x + size // 2, y + size // 4]])
                cv2.fillPoly(overlay, [points], (0, 0, 255))
                cv2.circle(overlay, (x, y), size + 10, (0, 0, 255), 4)

            for arrow in self.arrows:
                x, y = int(arrow['x']), int(arrow['y'])
                cv2.line(overlay,
                         (int(x - arrow['dx'] * 5), int(y - arrow['dy'] * 5)),
                         (x, y), (0, 255, 255), 8)
                cv2.circle(overlay, (x, y), 10, (0, 255, 0), -1)

            blended = cv2.addWeighted(overlay, 0.7, frame, 0.3, 0)
            cv2.rectangle(blended, (10, 10), (400, 100), (0, 0, 0), -1)
            cv2.putText(blended, f'Score: {self.score}', (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 4)

            self.display_timer(blended)
            cv2.imshow("Cupid's Arrow AR Game", blended)

            if self.check_game_over():
                self.high_score = max(self.high_score, self.score)
                print(f"Game Over! Final Score: {self.score}, High Score: {self.high_score}")
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    CupidsArrowGame().run_game()
