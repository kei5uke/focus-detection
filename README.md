# focus-detection  
This is re-creation of the project that I worked on before graduated from college in 2019.  
Main goal of this project is capturing features from the data measured by the sensors and detecting if the user is focusing on some kind of works, such as reading, watching videos, playing sudoku or whatever stimulus human nerve system.  
## Sensors
### GSR
<img src="https://user-images.githubusercontent.com/33390452/130960335-2aeb0d29-f083-4633-b283-fc15a75a20e0.jpg" width="500" height="250"></img>  
To achieve this goal, I used [GSR sensor from Grove](https://wiki.seeedstudio.com/Grove-GSR_Sensor/) for measuring the stress level and put it on Raspberry Pi.  
GSR stands for galvanic skin responce, which is a way of measuring the electrical conductance of the skin. Research shows that the value of GSR goes down when emotional arousal changes, on the other hand, it goes up when emotionally stable(relaxed).  
### [NEW] EEG     
<img src="https://user-images.githubusercontent.com/33390452/130960330-a60ab3f9-69c9-4209-8706-e8d922aa12df.jpg" width="500" height="250"></img>  
I added [EEG sensor from NeuroSky](https://store.neurosky.com/pages/mindwave). This tool can measure various brain waves such as alpha, beta, etc. It can be connected via bluetooth on any devices.   
Each brain wave has its own characteristics and will be able to capture changes in arousal, relaxation, and emotions.
## Neural Network 
After measuring the data, system start training neural network model.  
Since the data is time-series, I used LSTM as a main part of the architecture.  
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
thinkgear==0.2
```
## Usage
1. Connect the MindWave to `/dev/rfcomm0`
2. Run `main.py` in the `focus-detection` folder.
3. Input csv folder name
4. Start measuring GSR values
  * 1st session - calibration
  * 2nd session - focus (Training data)
  * 3rd session - relaxed (Training data)
  * 4th session - focus (Test data)
  * 5th session - relaxed (Test data)
5. Auto Tuning ML model using hyperas
6. Start Real time detection
## Things to improve
- It takes almost 2 minutes to train the model. (sort of slow)
- Uncertain if trained model can be used for others.
## Note
Thinkgear library is only available for Python2 so please replace the code with [this](https://github.com/groner/pythinkgear/pull/4/commits/2c13093b878dd8c7bb071ecc7f5e956de4e72d9d)
