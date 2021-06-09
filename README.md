# focus-detection  
This is the re-creation of the project that I worked on before graduated from college in 2019.  
The main goal of this project is detecting if the user is focusing on some kind of works, such as reading, watching videos, playing sudoku or whatever stimulus human nerve system.  
### GSR
To achieve this goal, I used the [GSR sensor by grove](https://wiki.seeedstudio.com/Grove-GSR_Sensor/) for measuring the stress level and put it on Raspberry pi.  
GSR stands for galvanic skin responce, which is a way of measuring the electrical conductance of the skin. Research shows that the value of GSR goes down when emotional arousal changes, on the other hand, it goes up when emotionally stable(relaxed). I decided to use this sensor since the price is cheap, however if there is an opportunity to use more advanced sensors such as EEG sensors, I would love to use them together to upgrade the system.  
### ML 
After measuring the data, the system start analysing the measured data by using machine learning model.
Since the data is time-series, I used LSTM as a main architecture of the ML.  
I used [hyperas](https://github.com/maxpumperla/hyperas) for auto-tuning.
## Required Python libraries 
```
hyperopt==0.2.5
tensorflow==2.4.0
Keras==2.4.3
pandas==1.2.0
hyperas==0.4.1
scipy==1.1.0
numpy==1.19.2
grove.py==0.6
grove==0.0.13
```
## How to use 
1. Run `main.py` in the `focus-detection` folder.
2. Input csv folder name
3. Start measuring GSR values
  * 1st session - calibration
  * 2nd session - focus (Training data)
  * 3rd session - relaxed (Training data)
  * 4th session - focus (Validation data)
  * 5th session - relaxed (Validation data)
4. Auto Tuning ML model using hyperas
5. Real time detection
