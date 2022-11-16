#include <Arduino.h>

struct pressure_data {
    double p_regulator_voltage; //output
    double p_tank_voltage; //from pressure sensor MPX2200, connected to tank
    int p_reg_command; //0-255 digital pot wiper position, connected to regulator

};

class SerialComms{
public:
    //Process a command received from serial buffer
    void process_command(char*);
    //Search cmd for letter, return number immideately after letter
    double parse_number(char*, char, int);
    // SerialComms(int*, double*, pwmAngle, pwmVelocity, time);
    SerialComms();
    
    void begin();
    void handle_command();
    void send_data(double);

    //-------
    //Serial communication buffer params
    char cmd [200]; //Input command from serial
    int cmd_index; //Current index in cmd[] 
    char incoming_char; //Serial incoming character for "parallel processing" of serial data
    int write_data=0;

    //--------------------------
    //relevant data for pressure rig
    struct pressure_data data;


};


/*
Serial command protocol
H0 - Handshake
R0 - Request data dependent on lab type
S0,P#,I#,D# - Set PID gains on arduino
S1,Z# - Set the setpoint of the controller
S2,Y# - Lab type 0-angle, 1-ang_velocity, 2-openloop
S3,M# - Turn controller on/off
S4,T# - Set sample time
S5,L#,U# - Set lower and upper controller output limits
S6,O# - Open loop PWM
S7,F# - Feedforward gain in volts
S8, T#(seconds to run)  - Start Open Loop Charactization Analysis

Data to python protocol
T# - time in micros
S# - setpoint
A# - value, angle or ang_speed dependent on labtype
Q# - PMW
D#(index),T#(us),P#,V#,I#$D1, etc... \0
*/

// S0,P0.1,I0,D0,%
// S1,Z100,%
// S2,Y0,%
// S3,M1,%
// S4,T0.005,%
// S5,L-12,U12,%




/*
H0 - Handshake
R0 - Request data
S0,P# - set tank pressure as voltage (1.4 until we get new valve)
S1,A# - set tube pressure (0-255 to digital pot)

$ - start of line character
% - end of line character


data gives back:
- voltage reading from regulator (pressure in tube)




*/