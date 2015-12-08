// This is a more robust sophisticated temperture sensor 1-wire device. Measures up to 8 devices (can be changed as needed) 
//on a bus. Can have multiple buses running. Pin numbers can change as necessary.

#include "Temp_Sensor.h"


OneWire* busses[ONEWIRE_BUS_COUNT];
DallasTemperature* temps[ONEWIRE_BUS_COUNT];

SoftwareSerial* debug;
Stream* data;

device_data upload;
device_info start_delim;
device_info end_delim;

//uint8_t retry_count = 0;

void setup()
{
  uint8_t *buf = (uint8_t *)&start_delim;
  uint8_t *buf2 = (uint8_t *)&end_delim;
  for(uint16_t i = 0; i < sizeof(device_info); i++)
  {
    buf[i] = i;
    buf2[sizeof(device_info) - i - 1] = i;
  }
  Serial.begin(9600);
  data = &Serial;
//  debug = new SoftwareSerial(DEBUG_RX_PIN, DEBUG_TX_PIN);
//  debug->begin(9600);
  Serial.println("Starting...");
  busses[0] = new OneWire(ONE_WIRE_BUS_ONE_PIN);
  busses[1] = new OneWire(ONE_WIRE_BUS_TWO_PIN);
  temps[0] = new DallasTemperature(busses[0]);
  temps[1] = new DallasTemperature(busses[1]);
//  Serial.setTimeout(5000);

}

void loop()
{
  clear_input();

  if(!repeat(&temp_display, 5, 100))
  {
 //   Serial.println("Failed to send data.");
  }
}

void clear_input()
{
  while(data->available())
  {
    data->read();
  }
}

bool temp_display(int repeat_count)
{
  data->write((uint8_t*)&start_delim, sizeof(device_info));
  upload.temperature_count = 0;
//  delay(3500); // Measures bus 1 waits 750ms for conversion measure bus 2 wait 750ms for conversion then delay 3500ms to make delay total of 5seconds MUST CHANGE DELAY TO 4250ms IF ONLY RUNNING ONE BUS
  for(int i = 0; i < ONEWIRE_BUS_COUNT; i++)
  {
    temps[i]->begin();
    temps[i]->requestTemperatures();
  }
  for(int i = 0; i < ONEWIRE_BUS_COUNT; i++)
  {
//    delay(4250); // measure bus 1 wait 750ms for conversion delay 4250ms for 5 second delay and then measure bus 2 following same schedule
    Serial.print("Displaying Bus: ");
    Serial.println(i);
    display_bus(i);
  }

  Serial.print("Temperature Count: ");
  Serial.println(upload.temperature_count);
  Serial.println();

  data->write((uint8_t*)&end_delim, sizeof(device_info));
}

void display_bus(uint8_t bus)
{
  busses[bus]->reset_search();
  uint8_t address[8];

  while(busses[bus]->search(address))
  {
    if (OneWire::crc8(address, 7) == address[7]) {

      switch(address[0])
      {
        case 0x28:
        case 0x10:
          display_temperature(bus, address);
          break;
        case 0x30:
        default:
          break;
      }
    }else
    {
      Serial.println("Error");
    }
  }
}

void display_temperature(uint8_t bus, uint8_t *address)
{

  device_info record;
  record.value = temps[bus]->getTempC(address);
  memcpy(&record.address, address, 8); //This changed the output garbage
  if(temps[bus]->getResolution(address) != 12)
  {
    temps[bus]->setResolution(address, 12);
  }

  data->write((uint8_t*)&record, sizeof(device_info));

  Serial.print(' ');
  display_address(debug, address);
  Serial.print(' ');
  Serial.println(record.value);
  upload.temperature_count++;
}

void display_address(Stream* stream, uint8_t *address)
{
  for(int i = 0; i < 8; i++)
  {
    if(address[i] < 0x10)
    {
      Serial.print(0, HEX);
    }
    Serial.print(address[i], HEX);
  }
}

bool repeat(bool (*func)(int repeat_count), uint32_t count, uint32_t delayms)
{
  for(uint32_t i = 0; i < count; i++)
  {
    if(func(i))
    {
      return true;
    }
    delay(delayms);
  }
  return false;
}


