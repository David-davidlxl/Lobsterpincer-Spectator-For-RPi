# Lobsterpincer Spectator: Real-Time Chessboard Processor

## Overview

Lobsterpincer Spectator (named after the "Lobster Pincer mate") is a chessboard processor that gives players feedback in real time. This repository contains the Raspberry Pi's version of the Lobsterpincer Spectator, which features the following functionalities:

- alert the players (via Bluetooth speaker) at critical moments of the game
- inform the players (via LED lights) of the evaluation of the current position
- show the players (via LCD screen) the move played in the previous position

![](README%20attachments/High-level%20diagram%20for%20overview.png)

[![](https://markdown-videos.deta.dev/youtube/IExBi2OLkls)](https://youtu.be/IExBi2OLkls)

## Software Installation

The only dependencies of“ChessPieceModelTraining” are [`numpy`](https://pypi.org/project/numpy/) and [`Pillow`](https://pypi.org/project/Pillow/), which are automatically installed during the installation procedure for "LobsterpincerSpectatorForRPi" presented below.

The installation procedure (for "LobsterpincerSpectatorForRPi") below is tested to be fully functional for Raspberry Pi 4B.

First, flash a Bullseye operating system onto the Raspberry Pi’s micro SD card. You can do so by downloading, for example, “2023-02-21-raspios-bullseye-arm64.img.xz” from https://downloads.raspberrypi.org/raspios_arm64/images/raspios_arm64-2023-02-22/ and flashing it with the official Raspberry Pi Imager.


Next, run the following commands in the Raspberry Pi’s Terminal (you can copy, paste, and run all of them at once):

```
sudo apt-get update
sudo apt-get upgrade -y


sudo apt install code -y


sudo apt-get install git python3-pip


sudo -H pip3 install --upgrade protobuf==3.20.0


git clone https://github.com/Qengineering/Tensorflow-io.git
cd Tensorflow-io
sudo -H pip3 install tensorflow_io_gcs_filesystem-0.23.1-cp39-cp39-linux_aarch64.whl
cd ~


sudo -H pip3 install gdown
gdown https://drive.google.com/uc?id=1G2P-FaHAXJ-UuQAQn_0SYjNwBu0aShpd
sudo -H pip3 install tensorflow-2.10.0-cp39-cp39-linux_aarch64.whl


sudo -H pip3 install onnxruntime
sudo -H pip3 install matplotlib
sudo -H pip3 install pyclipper
sudo -H pip3 install scikit-learn


sudo -H pip3 install chess
sudo -H pip3 install RPLCD

sudo rpi-eeprom-update
sudo rpi-eeprom-update -a
```

Next, reboot the Raspberry Pi with the `sudo reboot` command.


Next, follow the "Memory swapping" section of [Install 64 bit OS on Raspberry Pi 4 + USB boot](https://qengineering.eu/install-raspberry-64-os.html) to perform memory swapping:

```
sudo /etc/init.d/dphys-swapfile stop
sudo apt-get remove --purge dphys-swapfile
sudo rm /var/swap
sudo wget -O /usr/bin/zram.sh https://raw.githubusercontent.com/novaspirit/rpi_zram/master/zram.sh
sudo nano /etc/rc.local
```

(add `/usr/bin/zram.sh &` before the line `exit 0` and then save with <Ctrl+X>, <Y> and <Enter>)

```
sudo chmod +x /usr/bin/zram.sh
sudo nano /usr/bin/zram.sh
```

(change `mem=$((  $totalmem * 1024 ))` to `mem=$((  $totalmem * 512 ))` and then save with <Ctrl+X>, <Y> and <Enter>)

```
sudo reboot
```

Then go to [Install OpenCV 4.5 on Raspberry 64 OS](https://qengineering.eu/install-opencv-4.5-on-raspberry-64-os.html), configure the GPU memory according to the "GPU memory" section, and run the installation script provided in the "installation script" section to install OpenCV:

```
wget https://github.com/Qengineering/Install-OpenCV-Raspberry-Pi-64-bits/raw/main/OpenCV-4-5-5.sh
sudo chmod 755 ./OpenCV-4-5-5.sh
./OpenCV-4-5-5.sh
```

Finally, download the "LobsterpincerSpectatorForRPi" folder onto Raspberry Pi's Desktop and then run the following code in the Raspberry Pi’s Terminal:

```
cd Desktop/LobsterpincerSpectatorForRPi/Stockfish/src/
chmod 777 stockfish
```

Here are some additional recommended steps for configuring the VS Code on the Raspberry Pi:


   1. Open VS Code, press “Ctrl + Shift + P,” type “Preferences: Configure Runtime Arguments,” and disable the hardware acceleration by uncommenting the line `"disable-hardware-acceleration": true,`.

   2. Install the Python extension in VS Code.

   3. Press “Ctrl + Shift + P,” type “Preferences: Open Keyboard Shortcuts,” and set your preferred keyboard shortcut for “Python: Run Python File.”

   4. (Optional) run `sudo -H pip3 install black` in the Raspberry Pi Terminal. Then:

      1. Go to Settings -> Python Formatting Provider -> choose “black.”

      2. Go to Settings -> Editor: Format On Save -> check the box.

   5. (Optional) install the Python style-check tool with `sudo -H pip3 install pydocstyle`.

   6. (Optional) install the PGN extension (by Jake Boone) in VS Code.

Another completely optional step, if you are planning to use the Chromium browser at all, is to open the Chromium browser and go to Settings -> System -> disable "Use hardware acceleration when available."

## Hardware Configuration

(Note: if you do not configure the hardware at all, the main program “lobsterpincer_spectator.py” can still run without error and without damaging the Raspberry Pi in any way (you just won’t see the screen and light outputs during the execution of the program). Also note that the information that the screen and lights convey is always shown in the “Current position” window on the computer screen.)

First, for configuring the LCD screen ([purchase link](https://www.piccircuit.com/shop/display/36-46-2x16-lcd-display-blue-backlight.html)), follow the “wiring the LCD in 4 bit mode” section of [Install OpenCV 4.5 on Raspberry 64 OS](https://www.circuitbasics.com/raspberry-pi-lcd-set-up-and-programming-in-python/) to connect the LCD to the Raspberry Pi through the breadboard. (Note that you’ll also need two potentiometers/resistors, as explained in the link.)


Now, before configuring the 8 LED lights ([purchase link](https://www.amazon.com/White-Individual-Single-Attached-Bright/dp/B078THB7BN)), it is important to understand how they will be used. These lights function as an evaluation bar. So the lights are arranged in a linear, ordered fashion. In the paragraph below, the leftmost light is referred to as the “first LED,” the second light from the left is referred to as the “second LED,” . . ., and the rightmost light is referred to as the “eighth LED.” The following figure illustrates the case where the first four lights are on and the last four lights are off:

![](README%20attachments/Illustration%20of%20LED%20arrangement.jpg)


For each of the 8 LED lights, connect the black wire to the ground strip of the breadboard and connect the red wire to their respective board pins on the Raspberry Pi. The first LED should be connected to the Raspberry Pi board pin 11, second LED to board pin 13, third LED to board pin 15, fourth LED to board pin 16, fifth LED to board pin 18, sixth LED to board pin 22, seventh LED to board pin 36, and eighth LED to board pin 38.


If you’re not familiar with wiring in general, you can see the example shown in the “Hardware setup - Make a circuit with your Raspberry Pi and the LED” section of [Control an LED with Raspberry Pi 4 and Python 3](https://roboticsbackend.com/raspberry-pi-control-led-python-3/#:~:text=Control%20an%20LED%20with%20Raspberry%20Pi%204%20and,Conclusion%20%E2%80%93%20Control%20LED%20from%20Raspberry%20Pi%20). In this example, the short leg of the LED is connected to the ground through the black wire and the long leg of the LED is connected to GPIO pin 17 (which corresponds to board pin 11) through the yellow wire. Note that this example uses the BCM numbering mode (`GPIO.BCM`) instead of the BOARD numbering mode (`GPIO.BOARD`) that the paragraph above assumes. For information on how these numbering modes differ, see [What is the difference between BOARD and BCM for GPIO pin numbering?](https://raspberrypi.stackexchange.com/questions/12966/what-is-the-difference-between-board-and-bcm-for-gpio-pin-numbering).

## Data Collection and Model Training

The "SqueezeNet1p1_all_last.onnx" chess-piece model (in "LobsterpincerSpectatorForRPi/livechess2fen
/selected_models") provided in this repository was trained based on [this specific chessboard](https://www.amazon.com/dp/B07YG7R27P?psc=1&ref=ppx_yo2ov_dt_b_product_details). If you have a different chessboard, you should follow the procedure below to collect your own data and obtain your own model.

First, collect labeled image data using "capture_and_label_img.py" (in "LobsterpincerSpectatorForRPi/lpspectator"):

1. You will need an app on your phone that turns your phone into an IP camera. For Android, you can use [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam&pli=1). Make sure your phone and the computer (that will run "capture_and_label_img.py") are in the same Wi-Fi network, open the app, and edit the `IMAGE_SOURCE` variable in "capture_and_label_img.py" accordingly.

2. Paste the PGN of the game to be played (during data collection) into "game_to_be_played.pgn" (in "LobsterpincerSpectatorForRPi").

3. Run "capture_and_label_img.py" from the "LobsterpincerSpectatorForRPi" directory (NOT from the "LobsterpincerSpectatorForRPi/lpspectator" directory) to collect image data.

4. Cut everything in the "Captured Images" folder (in "LobsterpincerSpectatorForRPi") and paste it into a subfolder in "ChessPieceModelTraining/BoardSlicer/images/chessboards" (NOT directly in "ChessPieceModelTraining/BoardSlicer/images/chessboards").

5. Repeat steps 2-4 until you have a sufficient number (e.g., hundreds) of labeled images.

Next, process the data and obtain the trained model as follows:

1. Run "board_slicer.py" and copy (or cut) all the output in the “ChessPieceModelTraining/BoardSlicer/images/tiles” directory into the “ChessPieceModelTraining/DataSplitter/data/full” directory.

2. Run “data_splitter.py” to randomize and split the data. The next two steps are optional (but somewhat recommended):

   1. Delete the “ChessPieceModelTraining/DataSplitter/data/full” directory (to reduce the size of the “ChessPieceModelTraining/DataSplitter/data” folder).
   
   2. Discard a significant amount of the empty-square data in "ChessPieceModelTraining/DataSplitter/data/train/\_" and "ChessPieceModelTraining/DataSplitter/data/validation/\_" (such that, for example, the amount of the remaining empty-square data is comparable to that of the white-pawn data or black-pawn data).

3. Compress the "ChessPieceModelTraining/DataSplitter/data" folder into a "data.zip" ZIP-file (in the “ChessPieceModelTraining/DataSplitter” directory).

4. Open "SqueezeNet1p1_model_training.ipynb" (in "ChessPieceModelTraining/ModelTrainer") with Google Colab, enable GPU on Google Colab, and upload the "data.zip" (in the "ChessPieceModelTraining/DataSplitter" directory) and "models.zip" file (in the "ChessPieceModelTraining/ModelTrainer" directory).

5. Run the entire "SqueezeNet1p1_model_training.ipynb" notebook to perform transfer learning (which should take at least a couple of hours, but exactly how long it takes depends on how much image data you collected in the first place).

6. Download the "SqueezeNet1p1_all_last.onnx" (and, optionally, "SqueezeNet1p1_all_last.h5") from Google Colab (in the "models" folder) to the "LobsterpincerSpectatorForRPi/livechess2fen/selected_models" directory.

The following video walks through the entire data-collection-and-model-training procedure (only 5 images are collected in this demo in order to keep the video brief; you want to collect hundreds of images in practice):

[![](https://markdown-videos.deta.dev/youtube/Yl_WZxMeNjk)](https://youtu.be/Yl_WZxMeNjk)

## Usage of Main Program

To use the main program, "lobsterpincer_spectator.py" (in "LobsterpincerSpectatorForRPi"):

1. Connect your Raspberry Pi to a Bluetooth speaker, open the app on your phone (that turns your phone into an IP camera), mount the phone on some kind of physical structure (such as a [phone stand](https://www.amazon.com/dp/B0B9N41MCS?ref=ppx_yo2ov_dt_b_product_details&th=1)), and edit the `IMAGE_SOURCE` variable in "capture_and_label_img.py" (see step 1 of the data-collection procedure above).

2. Edit the `FULL_FEN_OF_STARTING_POSITION`, `A1_POS`, and `BOARD_CORNERS` variables in "capture_and_label_img.py" (feel free to edit other variables as well, but these three are generally the most relevant to the user).

3. Run "lobsterpincer_spectator.py" from the "LobsterpincerSpectatorForRPi" directory and tune the slider values.

4. Play the game against your opponent. At any point during the game, feel free to press 'p' to pause the program, press 'r' to resume the program, or press 'q' to quit the program.

5. After the game, feel free to use "saved_game.pgn" for postgame analysis.

The video in the [Overview](#overview) section demos the case where `BOARD_CORNERS` is set to `[[0, 0], [1199, 0], [1199, 1199], [0, 1199]]`. In this case, manual (predetermined) chessboard detection is used, which accelerates the move-registration process (each move takes about 10 seconds to register). If `BOARD_CORNERS` is set to `None`, automatic (neural-network-based) chessboard detection is used, and each moves takes about 12 seconds to register.

## Technical Details

The figure below shows a high-level diagram for the signal-processing workflow:

![](README%20attachments/High-level%20diagram%20for%20technical%20details.png)

There are a few things to note:

1. The chess-piece model discussed in the [Data Collection and Model Training](#data-collection-and-model-training) section above is responsible for move detection.

2. After each move is registered (i.e., validated), a sound effect is played. There are sound effects for making "regular" moves, making captures, castling, promoting, checking, and checkmating. These are the same sound effects that you would hear in an online game on [chess.com](http://www.chess.com).

3. Engine evaluation is accomplished with [Stockfish](https://stockfishchess.org/) 15.1 at depth 17.

4. A critical moment is defined as one when one of the two conditions is satisfied:

   1. The best move forces a checkmate (against the opponent) whereas the second-best move does not.
   
   2. The best move is significantly better than the second-best move (a floating-point evaluation difference of 2 or more), and the position would not be completely winning (a floating-point evaluation of at least 2) for the player if they played the second-best move.

    The precise definition can be found in the `is_critical_moment()` function in "evaluate_position.py" (in "LobsterpincerSpectatorForRPi/lpspectator").

5. Besides the ability to detect critical moments, the program also detects Harry the h-pawn and the Lobster Pincer mate. When Harry the h-pawn is pushed into the opponent's territory (but not promoting) and the player pushing the h-pawn is not losing (a floating-point evaluation of at least -2), the "Look at Harry! Come on, Harry!" audio is played. When the Lobster Pincer mate happens, a special piece of audio is played as well.

## Acknowledgements

I give special thanks to David Mallasén Quintana. This project was made possible by Quintana's work: [LiveChess2FEN](https://github.com/davidmallasen/LiveChess2FEN). LiveChess2FEN provided me with the foundation for chess-piece identification. The "models.zip" file (in "ChessPieceModelTraining/ModelTrainer") came directly from the LiveChess2FEN repository, and the "SqueezeNet1p1_model_training.ipynb" notebook (in "ChessPieceModelTraining/ModelTrainer") was written largely based on the work in "cpmodels" folder in the repository as well.

I also thank Sergio Goodwin (serggood@umich.edu) and Aayush Mohanty (amohanty@umich.edu) for helping me with hardware configuration.

Finally, I thank [Simon Williams](https://www.youtube.com/@GingerGM) and [Daniel Naroditsky](https://www.youtube.com/@DanielNaroditskyGM) for creating the entertaining YouTube videos that I used to create the audio files. They also inspired and helped me to become a much stronger chess player than I would be without them.

## Contact

If you find this repository to be useful (but please use my work responsibly; use it in friendly practice games instead of tournament games!), or if you have any feedback, please do not hesitate to reach out to me via davidlxl@umich.edu.
