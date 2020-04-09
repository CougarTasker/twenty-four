CS1822 Python Games Project - Group 24
    This is a simple game in which the goal is to catch fish to gain points within a certain timeframe while keeping your three lives safe from sharks below. 

To Run
    Run the program with python3 'start.py', computer must have simplegui installed.

Built With
    Python3 - The language used
    SimpleGUICS2Pygame - reimplemented SimpleGUI module of CodeSkulptor    

    
Graphics/Sounds
    The game graphics (sprite-sheets and images) are located inside ‘images’ folder and the sounds are placed inside the ’sounds’ folder. Images are self-created. Sound files are obtained from: http://soundbible.com.
    

Project Structure
    This section will describe the purpose of each file.
        start.py - Launches the game. Contains an object of the Interaction class.  
        
        inter.py - The main project file. Contains the Interaction class which has objects of all the other classes. 
        
        background.py - Background class. Draws the background images and sprite-sheets on the canvas using the SpriteSheet class from spritesheet.py. This includes waves, the sun, clouds, bubbles etc.
        
        fish.py - Contains School, Anim, Fsh, Shark and Bounds classes.
                    - School - Spawns a collection of fishes and sharks onto the canvas.
                    - Anim - Animates the fish/shark when it is caught by the player rod.
                    - Fsh - Implements the Boids Algorithm which steers the fishes to move as a
                            flock.
                    - Shark - Extends the Fsh class. Changes behaviour of fishes when a shark is nearby.
                    - Bounds - 
        
        rod.py - Rod class. Changes the length, position, the angle of the fishing line and the hook on key press. Also, checks if a fish has been caught.
        
        player.py - Player class. Draws the fishing boat and player on the canvas. Controls player movement.
        
        keyboard.py - Keyboard class. Recognises keyboard events and handles them.
        
        hearts.py - Hearts class. Draws hearts as player lives on the canvas. Replaces a full heart with an empty when a life is lost.
        
        timehandel.py - TimeHandeler class.
        
        overlay.py - Contains Overlay and Screen classes. 
                        - Overlay - Changes the state of the game from start, playing, paused or gameover to other states.
                        - Screen - Changes what is to be displayed on the screen depending on the game state.
        
        snd.py - Snd class. Adds sounds to various game events such as life lost, fish caught, hook deployed etc.
        
        spritesheet.py - SpriteSheet class. Animates sprite sheets on the canvas. Used within the background.py
        
        score.py - Score class. Real-time scoring mechanism.
        
        vect.py - Given Vector class with few modifications.

    

Developers
    Cougar Tasker
    Tiger-Lily Goldsmith
    Mihir Gosai 
    Xingrui Gu 
