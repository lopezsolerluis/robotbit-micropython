# robotbit-micropython

A kind of API for controlling servos and stepper motors with [micro:bit board](https://microbit.org/) and the [robotbit expansion board](https://www.kittenbot.cc/products/robotbit-robotics-expansion-board-for-micro-bit).

## Usage Example

### Initialize
```python
pca = PCA9685()
```

### Servos

```python
pca.setServoDegree(1, 90) # First parameter is Servo (1..8). Second parameter is angle in degrees (0..180).
```

### Stepper Motors

```python
import time

delta = pca.setStepperDegree(1, 90) # First parameter is stepper motor (1..2). Second parameter is angle in degrees (-360..360).
time.sleep_ms(delta)
pca.stopMotor(1) # Parameter is the motor to stop (1..2)
```

The `setStepperDegree` method just gets the motor running in the desired direction.
To be able to stop it when the user desires, it returns the number of milliseconds after which that position is reached. Then you can feed it to
`time.sleep_ms`, or any other non-blocking solution.
