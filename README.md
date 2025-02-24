# T-Mobile Home Internet Integration for Home Assistant

The `ha-tmobilehome` implementation allows you to integrate your T-Mobile Home Internet gateway data into Home Assistant.

## Features

- Provides detailed gateway device data.
- Provides frequent cell tower and received signal data.
- Provides detailed list of all connected clients.
- Provides detailed access point (wireless) settings.
- Provides sim card information.
- Allows changes to access point settings.
- Allows rebooting of gateway.

## Disclaimer
This is an unofficial integration of T-Mobile Home Internet for Home Assistant. The developer and the contributors are not in any way 
affiliated with T‑Mobile USA, Inc. or Deutsche Telekom AG.

## Requirements
- T-Mobile Home Internet account
- T-Mobile Home Internet gateway (only the TMO-G4SE has been tested, but other models may work)

## Installation
1. Install manually by copying the `custom_components/tmobile_home_internet` folder into `<config_dir>/custom_components`.
2. Restart Home Assistant.
3. In the Home Assistant UI, navigate to `Settings` then `Devices & services`. In the `Integrations` tab, click on the `ADD INTEGRATION` button at the bottom right and select `T-Mobile Home Internet`. Fill out the options and save.
   - Admin Username - Listed as "Username" on the back of your gateway--"admin" unless you have changed it.
   - Admin Password - Listed as "Admin password" on the back of your gateway, unless you have changed it.

## Usage

### Sensor Entities
Two types of sensor entities are provided:
1. Simple entities provide a single piece of data.
2. Aggregate entities provide one or more dict objects as attributes.

Simple entities provide an easy way to display data that is most commonly viewed. 

Aggregate entities provide the complete set of data available from the gateway.

### Simple Entities
Simple entities can be used directly on dashboards in cards such as the `Entities` card.

All entities begin with `T-Mobile Home Internet`, which will be omitted from the "Friendly Name" here for brevity:

| Friendly Name       | Example State  | Description
| -------------       | -------------  | -----------
| `4G Antenna Used`   | Internal_omni  | Antenna currently in use for 4G
| `4G Bands`          | b2             | Band(s) currently in use for 4G
| `4G Bandwidth`      | 15M            | The Bandwidth of the band(s) in use for 4G
| `4G Cell Global ID` | 310260xxxxxxxx | The (E)CGI identifier of the cell in use for 4G
| `4G RSRP`           | -95            | The Reference Signal Received Power of the 4G signal
| `4G RSRQ`           | -12            | The Reference Signal Received Quality of the 4G signal
| `4G SINR`           | 2              | The Signal to Interference & Noise Ratio of the 4G signal
| `5G Antenna Used`   | Internal_omni  | Antenna currently in use for 5G
| `5G Bands`          | n41            | Band(s) currently in use for 5G
| `5G Bandwidth`      | 90M            | The Bandwidth of the band(s) in use for 5G
| `5G Cell Global ID` | 310260xxxxxxxx | The (E)CGI identifier of the cell in use for 5G
| `5G RSRP`           | -97            | The Reference Signal Received Power of the 5G signal
| `5G RSRQ`           | -11            | The Reference Signal Received Quality of the 5G signal
| `5G SINR`           | 7              | The Signal to Interference & Noise Ratio of the 5G signal
| `Gateway Uptime`    | 29.2           | The number of hours since the gateway was started


### Aggregate Entities
Aggregate entities contain a group of related values as attributes. They can be viewed using the 
`Developer tools` `STATES` tab. To use some of these values in cards on a dashboard, they must first be extracted into 
a `Template Entity`. See below for examples.

All entities begin with `T-Mobile Home Internet`, which will be omitted from the "Friendly Name" here for brevity:

| Friendly Name      | Example State | State Source | Description
| -------------      | ------------- | ------------ | -----------
| `Gateway`          | 5G Gateway    | Gateway Name | Detailed gateway device data
| `Gateway Clients`  | 29            | Client Count | Detailed list of all connected clients
| `Gateway Sim Card` | 5G Gateway    | Gateway Name | SIM card information
| `Access Point`     | TMOBILE-xxxx  | SSID Name    | Detailed access point (wireless, or WiFi) settings
| `Cell Status`      | Bands: b2 n41 | Bands in Use | Detailed cell tower and received signal data (diabled by default)

The `T-Mobile Home Internet Cell Status` entity is disabled by default to prevent bloat of history, 
as it is somewhat large and changes very frequently.

### Actions

Actions are available to control the gateway. They are:

| Action Name                           | Description
| -------------                         | -----------
| `Reboot Gateway`                      | Reboot T-Mobile Home Internet Gateway
| `Set 2.4GHz Wi-Fi Transmission Power` | Set 2.4GHz Wi-Fi transmission power level on T-Mobile Home Internet Gateway
| `Set 5.0GHz Wi-Fi Transmission Power` | Set 5.0GHz Wi-Fi transmission power level on T-Mobile Home Internet Gateway
| `Enable/disable 2.4GHz Wi-Fi`         | Enable/disable 2.4GHz Wi-Fi on T-Mobile Home Internet Gateway
| `Enable/disable 5.0GHz Wi-Fi`         | Enable/disable 5.0GHz Wi-Fi on T-Mobile Home Internet Gateway

## Examples

### Create a Template Entity to monitor the gateway's software version

To extract the `softwareVersion` value from the `device` attribute in the `sensor.t_mobile_home_internet_gateway` entity, 
create a Template Sensor Helper or add this to `configuration.yaml`:

```yaml
template:
  - sensor:
      - name: "T-Mobile Home Internet Software Version"
        unique_id: t_mobile_home_internet_softwareVersion
        state: '{{ state_attr("sensor.t_mobile_home_internet_gateway","device")["softwareVersion"] }}'
```


## Contribute
Feel free to contribute by opening a PR or issue on this project.
