# robotbit-micropython

A kind of API for controlling servos and stepper motors with [micro:bit board](https://microbit.org/) and the [robotbit expansion board](https://www.kittenbot.cc/products/robotbit-robotics-expansion-board-for-micro-bit).

## Usage Example

### Initialize
```python
pca = PCA9685()
```

### Servos

```python
pca.setServoDegrees(1, 90) 
```
First parameter is Servo (1..8). Second parameter is angle in degrees (0..180).

### Stepper Motors

```python
pca.startStepper(1, True) 
```
Puts a stepper motor in motion. First parameter is stepper motor (1..2). Second parameter is direction of rotation: `True` (clockwise) or `False` (anti-clockwise) [Defaults to `True`].

```python
pca.stopStepper(1) 
```
Stops stepper motor motion. Parameter is stepper motor (1..2).

```python
pca.moveStepperDegreesBlocking(1, 180) 
```
Moves a Stepper motor across a given angle, positive (clockwise) or negative (anti-clockwise). 
First parameter is stepper motor (1..2). Second parameter is angle in degrees.
*Warning*: it's a blocking method.

```python
import time

delta = pca.moveStepperDegrees(1, 90)
time.sleep_ms(delta)
pca.stopMotor(1) 
```

The `moveStepperDegrees` method just gets the motor running in the desired direction.
To be able to stop it when the user desires, it returns the number of milliseconds after which that position is reached. Then you can feed it to
`time.sleep_ms`, or use with any other non-blocking solution.
 First parameter is stepper motor (1..2). Second parameter is angle in degrees, positive (clockwise) or negative (anti-clockwise). 
