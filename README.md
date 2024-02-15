# MLX90640 IR Array Thermal Imaging Camera Controlled by a FeatherS2
Capture IR-filtered images with the MLX90640 thermal camera module connected to a FeatherS2. This project aims to capture and convert those bits into a readable image that can be further translated into histograms with external software.

### Contents
- Adafruit FeatherWing Adalogger, supporting a (PCF8523) RTC chip with 32KHz crystal and battery backup, and a microSD socket that connects to the SPI port pins 
- Adafruit SH1107 128x64 OLED FeatherWing
- ESP32-S2 Feather S2 by Unexpected Maker
- Simple Slide-Switch
- Li-Ion 2000mAh battery

## Setup
The board is stored inside an ABS plastic enclosure. The box is provided with its proprietary screws to seal the contents inside. Inside the box, a triple stacked FeatherWing setup, using an Adafruit FeatherWing Adalogger, an SH1107 128x64 OLED display FeatherWing and an Unexpected Maker Feather S2. A hole has been drilled to accommodate the size of the MLX90640 camera lens. Use the screws provided to make the enclosure is sealed tight.

## Operation
The board is mainly controlled through the Feather S2. The FeatherWing Adalogger has an RTC clock that updates the board's internal clock. The SD card slot is used for storing the captured images instead of writing to the board's filesystem. The SH1107 OLED display is the main board for user interaction and interfacing with the device.

## Interaction
The board has a slide switch connected to the EN (enable and GND (ground) pins to turn on the microcontroller. Slide the switch up to turn on the device. Once switched on, a purple LED will light up to indicate that the device has booted. The screen will light up and the board will go through a series of checks to ensure that the camera is connected, the RTC is running correctly and that the SD card has been mounted. Please make sure that you insert the SD card into its dedicated slot before you turn on the device. Once done, a main menu should display 'IR Thermal Camera Main Menu'.

The OLED display comes with four buttons: RST, A, B and C. Each button has been configured to interact with the board. 

### RESET Button
The main use for this button is to power cycle the device to make sure that files are written onto the SD card. A secondary is mainly to help the device restart if a bug happens, although it has been thoroughly tested and should not happen.

### Button A - Date/Time Page and Start Recording Action
From the main menu, by pressing this button, you will see the date and time displayed and constantly updating. To exit this page, hold down button A again until the time no longer refreshes. You will have access to buttons B and C from this point.

### Button B - Recording Page
By pressing this button, you will be directed to the Recording Page. A title called 'Ready to Record' and two button options should appear. Button A will start the recording and Button C will exit back to the main menu. Please make sure that the SD card is slotted in before you attempt to record, otherwise, the board will fail to save any captured images. 

Once the Record button is pressed, you will be able to stop the recording again by holding down button A (it may take a few seconds to respond) until a 'Stopped' message appears, to which you will have to press button A again, to get a 'Stopped Recording' message. Press Button A once again to enter the Recording Page again. You should then press Button C to exit to the main menu. The files will have been captured, but to ensure that they have been saved, please make sure to hit the RESET button after you have reached the Recording Page again.

### Button C - Check Files Page and Exit to Main Menu Action
By pressing this button, you will be able to see a timestamp of the most recent file recorded and the total number of files recorded. All images are stored inside a dedicated 'Images' folder on the SD card. To access the files directly, make sure to power off the board, by switching it off with its switch. You may then remove the SD card.

## File Format & Recommended Software for Accessing
All images are stored in a `.pgm` format. Each file will have a dedicated timestamp and a count number before the `.pgm` extension to be able to distinguish each one.
If you are using Windows or Linux, the software recommended to access and edit a file is a Metadata display software package, `vipsdisp`, available at: https://github.com/jcupitt/vipsdisp/releases
`.pgm` files are accessible from MacOS directly. 

Any questions or concerns, please raise an issue and I will get in touch.
