#include <SPI.h>
#include <MCP4251.h>
#include <CommandHandler.h>

#define pot0ResistanceRmax 10000.0 // These resistance values may vary
#define pot0ResistanceRmin 130.0
#define pot1ResistanceRmax 10000.0
#define pot1ResistanceRmin 130.0

#define CS_ADC_1 8 //PRESSURE REG OUTPUT READING
#define CS_ADC_2 9 //RESOVIOUR PRESSURE READING (After INA125P)
#define CS_DIGI_POT 10 //Digital Potentiometer
#define CLK 13
#define CIPO 12
#define PUMP_PIN 3

SerialComms comms; 

bool potNum = 0;

int i = 0;

MCP4251 digitalPot(CS_DIGI_POT, pot0ResistanceRmax, pot0ResistanceRmin, pot1ResistanceRmax, pot1ResistanceRmin);
SPISettings settings(80000, MSBFIRST, SPI_MODE0);

//Pressure rig variables
int pressure_control_state = 0;
double dpdt = 0.025; //The change in pressure per unit time allowed, less than this constitutes an error in the system
unsigned long pump_on_t0;
double pressure_at_t0;

//Timing Variables
unsigned long cur, prev;
unsigned long dt = 50000;
double dtf = dt / 1000000.0;

// serial comms vars
char command[200] = {0};
int command_index = 0;

void setup() {
  comms.begin();
  
  pinMode(PUMP_PIN, OUTPUT);
  digitalWrite(PUMP_PIN, LOW);
  pinMode(CS_ADC_1, OUTPUT);
  pinMode(CS_ADC_2, OUTPUT);
  pinMode(CS_DIGI_POT, OUTPUT);
  pinMode(CLK, OUTPUT);
  pinMode(CIPO, OUTPUT);
  digitalWrite(CS_ADC_1, HIGH);
  digitalWrite(CS_ADC_2, HIGH);
  digitalWrite(CS_DIGI_POT, HIGH);

  digitalPot.begin();

  //Get initial data readings before starting control and comms loop
  get_sensor_data(settings);

}

void loop() {
  //Update all sensor data
  get_sensor_data(settings); // , &data, &data2);
  
  comms.handle_command(); //checks serial buffer, process command if necessary
  comms.send_data(comms.data.p_regulator_voltage);

  
  //voltage to tank pressure is linear with an offset
  //voltage of 1.4 gives 26 psi in tank on gague (could be 2 psi high)
  control_tank_pressure(comms.data.p_tank_voltage, 2.15, 0.05); 

  //Send DIGI Pot
  digitalPot.DigitalPotSetWiperPosition(potNum, comms.data.p_reg_command);

}

//p_tank is reading, second value is voltage input, third is hysterisis
void control_tank_pressure(double p_actual, double p_desired, double hysteresis_amt)
{
  cur = micros(); //Update current time
  //Check if dt has passed
  if ((cur - prev) > dt)
  {
    switch (pressure_control_state)
    {
      case 0: //Tank at acceptable pressure (pump off)
        //turn off pump
        digitalWrite(PUMP_PIN, LOW);
        //If tank is below p_desired - hysteresis_amt, turn on pump (switch to state 1)
        if (p_actual < (p_desired - hysteresis_amt)) {
          pump_on_t0 = cur; //Get the current time that we started turning the pump on
          pressure_at_t0 = p_actual; //Get the pressure at this moment in time (for pressure rate check in state 1)
          pressure_control_state = 1;
        }
        break;

      case 1: //Tank pressure low, (pump on)\
        //Turn on Pump
        digitalWrite(PUMP_PIN, HIGH);

        //Check that the pump on time causes a reasonable change in pressure, if not, EMERGENCY STOP
        // Currently hardcoded delta time is 0.5 seconds (500_000 us)
        if ( (cur - pump_on_t0) > (0.5 * 1000000) ) //Check if delta time has passed
        {
          if ((p_actual - pressure_at_t0) < dpdt) //If the change in voltage of the mpx2200 is < dpdt, emergency stop
          {
            pressure_control_state = 2;
          }
          //If the rate is satisfactory, reset pump start time and start pressure for next safety check
          pump_on_t0 = cur;
          pressure_at_t0 = p_actual;
        }

        //If tank is above p_desired + hysteresis_amt, turn off pump (state 0)
        if (p_actual >= (p_desired + hysteresis_amt)) {
          pressure_control_state = 0;
        }

        break;

      case 2: //EMERGENCY
        digitalWrite(PUMP_PIN, LOW);
        break;
    }
    
    //Reset prev time
    prev = cur;
  }

}

void get_sensor_data(SPISettings setting)
{
  //Read Resivour Pressure
  digitalWrite(CS_ADC_2, LOW);
  delayMicroseconds(10);
  SPI.beginTransaction(setting);
  int16_t temp = convert_13bit_signed_to_16bit(SPI.transfer16(0b0000000000000000));
  digitalWrite(CS_ADC_2, HIGH);
  delayMicroseconds(10);
  SPI.endTransaction();
  //Do moving average on p_tank _voltage
  comms.data.p_tank_voltage = (temp * 5.0 / 4096.0); //Convert raw value into voltage value
  
  //Read Regulator Pressure
  digitalWrite(CS_ADC_1, LOW);
  delayMicroseconds(10);
  SPI.beginTransaction(setting);
  int16_t temp2 = convert_13bit_signed_to_16bit(SPI.transfer16(0b0000000000000000));
  digitalWrite(CS_ADC_1, HIGH);
  delayMicroseconds(10);
  SPI.endTransaction();
  comms.data.p_regulator_voltage = temp2 * 5.0 / 4096.0;
}


int16_t convert_13bit_signed_to_16bit(uint16_t b)
{
  //Starting bits with all 0s
  int16_t out = 0b0000000000000000;

  //Delete bits 15-13 (because we count from 0)
  b &= 0b0001111111111111;

  //if negative return -99 (to check negative, check bit #12
  if ((b & 0b0001000000000000) >> 12 == 1)
  {
    out = -99;
  }
  else {
    //Pull bits 11-0 from our input arg unsigned input to out
    out = 0b0000111111111111 & b;
  }

  return out;

}
