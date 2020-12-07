This project is dedicated to the project VACTANILAD. 

The main idea is to move position-sensitive Schottky cavity doublet near the linear accelerator and check the difference in signal power.

The system consists of several parts:

- ISEL motor and driver to have the lateral movement
- SwissBOY 122M motor and modified driver to have vertical movement
- RaspberryPI 3B+ as a coordinator of all parts
- LimeSDR as a radiomodule to read the RF signal from Schottky
- Printed circuit with elements to read data from potentiometers, short relays, operate Lime and so on
- Megatron linear transducers which tell us current position of the cavities based on MCP3204 12-bit ADC

Files with names of the components contain simple class with primitive methods like "read data" or "go_up". They will be imported later into main script.

TO DO file has current tasks which have to be finished.

Further logic or updates will be written here

Swissboy: left connector in the black box is related to the left connector in SwissBOY driver box

Test command starts python3 test.py [vertical position] [horizontal position]
example: python3 test.py 70 40
answer: vertical steps and feedback from megatron and answer from ISEL also about carriage position
