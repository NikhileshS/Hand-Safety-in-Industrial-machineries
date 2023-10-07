# Hand Safety in industies with Deep Learning

### Objective of Project :
The objective of the Project is to create a Open-source application for detecting hand, thus providing safety while working under heavy machineries such as pistons, pressing machines, and thereby, reducing the risks of accidents while working with a help of deep learning Techniques.

---

### What have we done :
We have utilized the Deep learning techniques such as Canny edge detection, YOLO ( you only look once ) and many more algorithm and methods that are available to create a Hand safety detection, we further plan on improvising the code by establising a user friendly Interface and making the above code to be easily accessible to the users. The hand are detected when the hand passes through the fixed circular boundary, which can be calibrated easily by right clicking the mouse for calibration mode in which the position and the radius of the circular boundary can be changed by the user. This program uses your own computer webcam as its primary source for video capture. You can also set up a path for logging details, and thus, it provides you details of the hand breachment along with the time of breachment

---

### How did we manage to do it :
We made the hand detection possible by utilizing media-pipe and also at first we used YOLO algorithm for the Real time hand detection, But, The accuracy of it, detecting is lower than we expected it to be, Thereby we incorperated the canny edge detection along with it, thereby Inprovising its accuracy. we also have utilized the logging module to make logging of information along with time possible 

---

### How can we further Improvise the program :
We are quite aware of our Hold-back of what makes our program an fully fletched open source application, but We will try our best to further improvising the code

The things we are primarly focusing on improving are :
1. Adding a user friendly interface in which the users can directly interact with the program by the settings 
2. figuring out on how we can connect it to the server for better flexiblity and also making it easily accesible to the users.
3. Improvising the accuracy of the detection even under Low visibility condition.
4. Making the program an actual application for easier access
5. Improvising the fixed boundary in such a way that user can easily change the shape,size and position of the fixed boundary.
6. Better Logging system that saves the data in the databases for easier management

---
   
### Why we use Deep-learning techniques 
This is a question we frequently hear about, When we arrived at this problem statement, we quite fumbled with the possibility of solutions, There are quite a lot of sensors available that detects motion, quite particularly Proximity sensor, But the thing is that, Proximity sensor senses everything that is in motion, whether is it hand or object, It detects, and Utilizing sensors for the detection resulted in quite a complex setup that is not flexible and not easily accessible for the users and it is much higher cost for the operation it does, Thereby, We came up with a solution that utilizing the web-cam of the computer and also utilizing the Deep-Learning techniques meant that It is much highly flexible and accessible to the users compared to the sensor setup. 


---

 



