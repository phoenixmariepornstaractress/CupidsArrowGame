# Description 
Cupid's Arrow AR Game is an interactive augmented reality game built with OpenCV and MediaPipe, where players use real-time pose detection to simulate drawing and shooting a bow to hit animated heart targets. 

# Cupid's Arrow AR Game

Cupid's Arrow is an augmented reality (AR) game developed in Python using OpenCV and MediaPipe. In this game, players use their body movements to simulate drawing and shooting a bow to hit floating heart targets. The game leverages real-time pose detection to create an immersive and engaging interactive experience.

## Features

* Real-time pose tracking using MediaPipe
* Gesture-based archery mechanics
* Dynamic heart targets with movement and collision detection
* Animated welcome screen and interactive game visuals
* Score and timer tracking with game-over conditions

## Requirements

* Python 3.7+
* OpenCV (`opencv-python`)
* MediaPipe
* NumPy

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/cupids-arrow-ar-game.git
   cd cupids-arrow-ar-game
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Add a `heart.png` image (transparent background preferred) to the root directory. This will be used as the visual for the heart targets.

## How to Play

1. Launch the game:

   ```bash
   python cupids_arrow_game.py
   ```
2. Follow the instructions on the welcome screen.
3. Raise your right arm and pull back to draw the bow.
4. Release to shoot arrows at the heart targets.
5. Try to hit as many hearts as possible before time runs out!

## Contributing

We welcome contributions to improve this project! Whether it's fixing bugs, adding new features, or enhancing visuals, your input is appreciated.

To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Push to your fork
5. Open a pull request

Please ensure your code is clean, documented, and tested. For larger changes, consider opening an issue first to discuss the idea.

## License

This project is licensed under the MIT License.

---

**Let's build a better Cupid's Arrow together!**
 
