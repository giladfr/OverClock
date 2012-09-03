// include the library code:
#include <LiquidCrystal.h>

// General defines
#define PIN_BACKLIGHT 		10
#define CLK_LINE      		0  
#define LCD_NUM_LINES 		2
#define LCD_LINE_LENGTH		16


// general CMD op code
#define CMD_OP 				0xFF

// Low level op codes
#define CMD_CLEAR 			0x01
#define CMD_BACKLIGHT_OFF  	0x02
#define CMD_BACKLIGHT_ON  	0x03
#define CMD_SET_CURSOR  	0x04

// High level op codes
#define CMD_CLOCK_START		0x11
#define CMD_CLOCK_END		0x12
#define CMD_INFO_A_START	0x13
#define CMD_INFO_A_END		0x14

#define MAX_LINE_WIDTH 		80
#define INFO_LINE_A			1

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);
char lineA[MAX_LINE_WIDTH] = {0};

void update_line_A();
void write_line_A();


void setup()
{
	// set up the LCD's number of columns and rows: 
	lcd.begin(LCD_LINE_LENGTH, LCD_NUM_LINES);
	// initialize the serial communications:
	Serial.begin(9600);
	pinMode(PIN_BACKLIGHT,  OUTPUT);
	digitalWrite(PIN_BACKLIGHT, HIGH);
	// Write welcome messege
	lcd.print("Waiting...");
}


void loop()
{
	int in_byte;
	int cmd;
	int col;
	int row;
	
	// when characters arrive over the serial port...
	if (Serial.available()) 
	{
		// wait a bit for the entire message to arrive
		delay(100);
		// read all the available characters
		while (Serial.available() > 0) 
		{
			// display each character to the LCD
			in_byte = Serial.read();
			if (in_byte == CMD_OP) // Op Code
			{
				cmd = Serial.read();
				switch (cmd)
				{
				// ------ OP Codes
				case CMD_CLEAR:
					lcd.clear();
					break;
				case CMD_BACKLIGHT_OFF:
					digitalWrite(PIN_BACKLIGHT, LOW);
					break;
				case CMD_BACKLIGHT_ON:
					digitalWrite(PIN_BACKLIGHT, HIGH);
					break;
				case CMD_SET_CURSOR:
					col = Serial.read();
					row = Serial.read();
					lcd.setCursor(col,row);
					break;
					
				case CMD_INFO_A_START:
					update_line_A();
					write_line_A();
					break;
					
				}        
				
			}
			else // Regular Char, just print
			{
				lcd.write(in_byte);
			}
		}
	}
}

void update_line_A()
{
	int i = 0;
	int in_byte;
	while (Serial.available() > 0) 
	{
		in_byte = Serial.read();
		if (in_byte == CMD_INFO_A_END)
		{
			lineA[i] = 0;
			break;
		}
		if (i < MAX_LINE_WIDTH)
		{
			lineA[i] = (char)in_byte;
			i++;
		}
	}

}


void write_line_A()
{
	lcd.setCursor(0,INFO_LINE_A);
	// Clear line (TODO ANIMATION)
	lcd.print("                ");
	// Write line
	lcd.setCursor(0,INFO_LINE_A);
	lcd.print((char*)lineA);


}