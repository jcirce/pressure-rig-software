#include <SPI.h>
#include <MCP4251.h>

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

bool potNum = 0;

int i = 0;

MCP4251 digitalPot(CS_DIGI_POT, pot0ResistanceRmax, pot0ResistanceRmin, pot1ResistanceRmax, pot1ResistanceRmin);
SPISettings settings(80000, MSBFIRST, SPI_MODE0);

uint16_t p_reg, p_tank;
int pressure_control_state = 0;
double pressure_integral=0;
double dpdt = 0.05; //The change in pressure per unit time allowed, less than this constitutes an error in the system
unsigned long pump_on_t0;
double pressure_at_t0;

unsigned long cur, prev;
unsigned long dt = 50000;
double dtf = dt/1000000.0;
  
void setup() {
  Serial.begin(9600);
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
}

void loop() {
  
  get_sensor_data(settings); // , &data, &data2);

  control_tank_pressure(convert_13bit_signed(p_tank)*5./4096., 1.1, 0.1);
  
  //Send DIGI Pot
  digitalPot.DigitalPotSetWiperPosition(potNum, 255);

//  Serial.print(pressure_control_state);
//  Serial.print(" | ");
//  Serial.println(convert_13bit_signed(p_tank)*5./4096.,7);
}

void control_tank_pressure(double p_actual, double p_desired, double hysteresis_amt)
{
  cur = micros();
  if((cur-prev)>dt)
  {
    switch(pressure_control_state)
    {
      case 0: //Tank at acceptable pressure (pump off)
        //turn off pump
        digitalWrite(PUMP_PIN, LOW);
        //If tank is below p_desired - hysteresis_amt, turn on pump
        if(p_actual < (p_desired - hysteresis_amt)) { 
          pump_on_t0 = cur;
          pressure_at_t0 = p_actual;
          pressure_control_state = 1; 
          }
        
        break;
        
      case 1: //Tank pressure low, (pump on)
        digitalWrite(PUMP_PIN, HIGH);
  
        //Check that the pump on time causes a reasonable change in pressure, if not, EMERGENCY STOP
        if( (cur - pump_on_t0) > (0.5 * 1000000) )
        {
          if((p_actual - pressure_at_t0) < 0.05)
          {
            pressure_control_state = 2;
          }
          pump_on_t0 = cur;
          pressure_at_t0 = p_actual;
        }
        
        //If tank is above p_desired + hysteresis_amt, turn off pump (state 0)
        if(p_actual >= (p_desired + hysteresis_amt)) { pressure_control_state = 0; }
        
        break;
        
      case 2: //EMERGENCY
        digitalWrite(PUMP_PIN, LOW);
        break;
    }
    //Reset prev time
    prev=cur;

    //ds
    Serial.print(p_actual);
    Serial.print(" | ");
    Serial.print(pressure_control_state);
    Serial.print(" | ");
    Serial.println();
  }
  
}

void get_sensor_data(SPISettings setting) //, uint16_t* pressure_actuator, uint16_t* pressure_reservoir)
{
   //Read Resivour Pressure
  digitalWrite(CS_ADC_2, LOW);
  delayMicroseconds(10);
  SPI.beginTransaction(setting);
  p_tank = SPI.transfer16(0b0000000000000000);
  digitalWrite(CS_ADC_2, HIGH);
  delayMicroseconds(10);
  SPI.endTransaction();

  //Read Regulator Pressure
  digitalWrite(CS_ADC_1, LOW);
  delayMicroseconds(10);
  SPI.beginTransaction(setting);
  p_reg = SPI.transfer16(0b0000000000000000);
  digitalWrite(CS_ADC_1, HIGH);
  delayMicroseconds(10);
  SPI.endTransaction();
}


int16_t convert_13bit_signed(uint16_t b)
{
  int16_t out = 0b0000000000000000;

  //Delete bits 16-14
  b &= 0b0001111111111111;

  //if negative return -99
  if ((b & 0b0001000000000000) >> 12 == 1)
  {

    out = -99;
  }
  else {
    out = 0b0000111111111111 & b;
  }

  return out;

}
