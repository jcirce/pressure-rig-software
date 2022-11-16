#include "CommandHandler.h"
#include <string.h>

SerialComms::SerialComms(){
    //Initialize Serial buffer params
    cmd_index=0;
    data.p_reg_command = 255;
}

void SerialComms::begin(){
    Serial.begin(115200);
}

void SerialComms::process_command(char* cmd_string){
    int pos;
    int cmd;

    //Handshake command
    cmd = parse_number(cmd_string, 'H', -1);
    switch((int)(cmd)){
        case 0: // Handshake stuff to be implemented
            Serial.print("$OK%\n");
            break;
        default: break;
    }

    //Request command
    cmd = parse_number(cmd_string, 'R', -1);
    switch((int)(cmd)){
        case 0: //Flag to write data
            write_data = 1;
            break;

        //If no matches, break
        default: break;
    }

    //Set value/mode commands
    cmd = parse_number(cmd_string, 'S', -1);
    switch(int(cmd)){
        case 0: //set tank pressure as voltage
            break;
        case 1: //set tube pressure (0-255 to digital pot)
            //Cast return of parse_number to an int
            data.p_reg_command = (int)parse_number(cmd_string, 'A', -1);
            data.p_reg_command = constrain(data.p_reg_command, 0, 255);
            break;
        default: break;
    }
}

double SerialComms::parse_number(char* cmd_string, char key, int def){
    //Search cmd_string for key, return the number between key and delimiter
    // Serial.println(cmd_string);
    // Serial.println(key);

    int key_len=0; //Position of key in string
    int delim_len=0; //Position of next delimiter after key in string

    //Search string for first instance of key, increment key length each time key isn't found
    for(int i=0; i<100; i++) //TODO: Make this 100 value a HEADER_LENGTH #define
    {
        if(cmd_string[i] == '\0') { return def; } //If we can't find key, return default value
        if(cmd_string[i] == key){key_len = i; break;}
    }
    // Serial.print("key len: "); Serial.println(key_len);

    //Search string starting at character after key, looking for next delimiter the comma
    for(int i=key_len+1; i<100; i++){
        if(cmd_string[i] == ',' || cmd_string[i] == '\0')
        {
            break;
        }
        delim_len++;
    }
    // Serial.print("delim len: "); Serial.println(delim_len);

    //Create empty substring to use strncpy
    char substring[20] = {0};
    strncpy(substring, &cmd_string[key_len+1], delim_len);  //Copy subset of string to substring
    
    // Serial.print("test string: "); Serial.println(substring);
    return atof(substring); //return the substring in float format
}

void SerialComms::handle_command(){
// Arduino command handler
  if (Serial.available() != 0) {
    incoming_char = Serial.read();
    cmd[cmd_index] = incoming_char;
    if (incoming_char == '\0' || incoming_char == '%') {
      //      Serial.println("End of line, processing commands!");
      process_command(cmd);
      // Reset command buffer
      cmd_index = 0;
      memset(cmd, '\0', sizeof(cmd));
    }
    else {
      cmd_index ++;
    }
  }
}

void SerialComms::send_data(double reg_voltage) {
  // Check and if there is a request, send data
  if (write_data == 1) {
    Serial.print("$");
    Serial.print(reg_voltage, 5);
    Serial.print("%\n\r");

    write_data = 0; // Reset write data flag
  }
}