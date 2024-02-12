# Description
Short description of the software used.
## Sourcecode 
Our Sourcecode is written in MicroPython and contains everything needed to get Local Utilization device operational for reading and sending data.
### MQTT 
MQTT is a lightweight, open-source messaging protocol designed for efficient communication between devices with limited resources, such as IoT devices
#### Datacake
Datacake is an IoT-platform servsr where you can easily visualize data from IoT devices and we chose to save data when we send from MQTT.
##### Setup 
To setup Local Utilization device and be able to view its measured data, follow the steps below

### Prerequisites
- Thonny IDE
- Local Utilization 
- Micro-USB-cable, phone charger
- Datacake account
- MQTT account/Sevrver 
###### Device
# First time setup
1. Clone this repo
2. Copy `main.py`
  - Change the following in `main.py` file:
    - wifi_ssid = `Your WIFI Name` 
    - wifi_password = 'Wifi Password'
    - config['server'] = 'Host Server IP'
    - config['port'] = `Server port `
    - config['user'] = 'User name'
    - config['password'] = 'Server Passowrd'
    - config['ssid'] = wifi_ssid
    - config['wifi_pw'] = wifi_password  
3. Login to MQTT Server.
###### Datacake 
1. In your Datacake `Workspace` under `Devices`, add a API-device, 
2. Under `Configuration` on the device, scroll down to `MQTT Confiquration` then `Add New MQTT Server`
3. We gonna add 2 Uplink deoder
4. Both are going to subscribe to same topics `Room persons`
  - THE CODE FOR THE FIRST Uplink Decode
        function Decoder(topic, payload) {
        var count = parseInt(payload);

        // You can return totalOccupiedTime or do something else with it
        return [
            {
                device: "officeUtilization", // Serial Number or Device ID
                field: "PEOPLE_COUNTER",
                value: count,
            }
        ];
        }
    
  - 2en code for the uplink decord

        function Decoder(topic, payload) {
        // Anta att payload är en sträng som kan konverteras till ett nummer.
        // Om payload inte är i det formatet, behöver du modifiera denna del.
        var count = parseInt(payload);

        var value;
        if (count >= 1){
            value = true;  // Eller något annat värde baserat på din logik
        } else {
            value = false;  // Eller något annat värde baserat på din logik
        }
        PERSON_COUNTER = value;
        return [
            {
                device: "officeUtilization", // Serial Number or Device ID
                field: "IS_OFFICE_BUSY",
                value: value  // Använd det beräknade värdet här
            }
        ];
        }

5. Add the fields from the decoder in the `Fields`-section
6. Configure the `Dashboard` to your liking with the data from your `Fields`
7. create public link 
###### Deployment
1. Put the device in the box and connect to an electrical outlet
2. You can visualize the data or send it by joining the `Dashboard` from the public link you created previuosly
