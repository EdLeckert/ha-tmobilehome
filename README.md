# T-Mobile Home Internet Integration for Home Assistant

The `ha-tmobilehome` implementation allows you to integrate your T-Mobile Home Internet gateway data into Home Assistant.

## Features

- Provides detailed gateway device data.
- Provides frequent cell tower and received signal data.
- Provides detailed list of all connected clients.
- Provides detailed access point (wireless) settings.
- Provides sim card information.
- Allows changes to access point settings.
- Allows rebooting of the gateway.
- Allows manual editing of missing or obscure hostnames in the integration.

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

### Simple Sensor Entities
Simple entities can be used directly on dashboards in cards such as the `Entities` card.

All entities begin with `T-Mobile`, which will be omitted from the "Friendly Name" here for brevity.

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


### Aggregate Sensor Entities
Aggregate entities contain a group of related values as attributes. They can be viewed using the 
`Developer tools` `STATES` tab. To use values from these entities in cards on a dashboard, they must first be extracted into 
a `Template Entity`. See `Examples` below.

Identical values are available via Actions of a similar name. Actions have the advantage of not filling history unneccesarily. See `Actions` below.

All entities begin with `T-Mobile`, which will be omitted from the "Friendly Name" here for brevity.

| Friendly Name      | Example State | State Source | Description
| -------------      | ------------- | ------------ | -----------
| `Gateway`          | 5G Gateway    | Gateway Name | Detailed gateway device data
| `Gateway Clients`  | 29            | Client Count | Detailed list of all connected clients. Disabled by default.
| `Gateway Sim Card` | 5G Gateway    | Gateway Name | SIM card information
| `Access Point`     | TMOBILE-xxxx  | SSID Name    | Detailed access point (wireless, or Wi-Fi) settings. Disabled by default.
| `Cell Status`      | Bands: b2 n41 | Bands in Use | Detailed cell tower and received signal data (disabled by default). Disabled by default.

The `T-Mobile Cell Status` entity is particularly likely to bloat history, as it is somewhat large and changes very frequently.


### Select Entities
Select Entities allow you to make changes to the gateway's settings by selecting from a list of choices.

All entities begin with `T-Mobile`, which will be omitted from the "Friendly Name" here for brevity.

| Friendly Name            | Example Choices         | Description
| -------------            | ---------------         | -----------
| `Wi-Fi 2.4GHz Channel`   | Auto, 1, 2, 3           | Sets the channel used for 2.4GHz Wi-Fi
| `Wi-Fi 5.0GHz Channel`   | Auto, 36,40,44,48...165 | Sets the channel used for 5.0GHz Wi-Fi
| `Wi-Fi 2.4GHz Bandwidth` | Auto, 20MHz,40MHz       | Sets the bandwidth used for 2.4GHz Wi-Fi
| `Wi-Fi 5.0GHz Bandwidth` | Auto, 20MHz,40HMz,80MHz | Sets the bandwidth used for 5.0GHz Wi-Fi

**Note: After changing any of these settings, the gateway will need some time to reconfigure to the new settings.
It is best to allow the gateway to settle before changing another setting. The gateway has settled when the `state`
of the select control matches the new value.**

A [custom:mushroom-select-card](https://github.com/piitaya/lovelace-mushroom/blob/main/docs/cards/select.md) 
is an example of a card that can show both the current state and the desired new state at the same time.


### Switch Entities
Switch Entities allow you to make changes to the gateway's settings by turning a feature on or off.

All entities begin with `T-Mobile`, which will be omitted from the "Friendly Name" here for brevity.

| Friendly Name    | Description
| -------------    | -----------
| `Wi-Fi 2.4GHz`   | Turn off the radio for 2.4GHz Wi-Fi. Disabled by default.
| `Wi-Fi 5.0GHz`   | Turn off the radio for 5.0GHz Wi-Fi. Disabled by default.

**Note: Turning off either radio disables Wi-Fi on that frequency. Do not turn off the Wi-Fi on the frequency you are currently using.
Only turn all Wi-Fi off if you have a wired connection to your gateway.**


### Actions

Actions are available to control the gateway and to display gateway information.

All actions begin with `T-Mobile Home Internet`, which will be omitted from the "Action Name" here for brevity.

| Action Name                           | Description
| -------------                         | -----------
| `Reboot Gateway`                      | Reboot T-Mobile Home Internet Gateway
| `Set 2.4GHz Wi-Fi Transmission Power` | Set 2.4GHz Wi-Fi transmission power level on T-Mobile Home Internet Gateway
| `Set 5.0GHz Wi-Fi Transmission Power` | Set 5.0GHz Wi-Fi transmission power level on T-Mobile Home Internet Gateway
| `Enable/disable 2.4GHz Wi-Fi`         | Enable/disable 2.4GHz Wi-Fi on T-Mobile Home Internet Gateway
| `Enable/disable 5.0GHz Wi-Fi`         | Enable/disable 5.0GHz Wi-Fi on T-Mobile Home Internet Gateway
| `Get Client List`                     | Returns a list of all clients known to the T-Mobile Home Internet Gateway
| `Set Client Hostname`                 | Sets the hostname for a client locally in the integration
| `Clear Client Hostname`               | Clears a previously set hostname for a client
| `List Client Hostnames`               | Lists all manually set hostnames
| `Get Gateway`                         | Gets gateway device details
| `Get Gateway Clients`                 | Gets gateway wired and wireless clients
| `Get Gateway SIM Card`                | Gets SIM card details
| `Get Access Point`                    | Get access point (wireless) settings
| `Get Cell Status`                     | Get cell connection status

`Get Client List` can be used to return the entire list of wired and wireless clients in a single list for easy display
(the gateway splits clients into 2.4GHz, 5.0GHz, and Wired groups, as returned by `Get Gateway Clients`).

Often the gateway will be unable to obtain a useful hostname from a client. `Set Client Hostname` can be used to manually
save preferred hostnames to make viewing the client list more useful. `Get Client List` will automatically substitute the 
alternate hostname.

Note that these hostnames are only stored in the integration, and will not be passed back to the gateway or client device.

`List Client Hostnames` can be used to show which clients have had an alternate hostname provided.

`Clear Client Hostname` can be used to remove one or all alternate hostnames.

`Get Gateway`, `Get Gateway Clients`, `Get Gateway SIM Card`, `Get Access Point`, and `Get Cell Status` return data that
is identical to that provided by the aggregate sensor entities above, but without filling history.

Actions are useful for populating a table (see table example below), while aggregate sensor entities are useful for creating template
sensors (see template example below).

## Examples

### Create a Template Entity to monitor the gateway's software version

To extract the `softwareVersion` value from the `device` attribute in the `sensor.t_mobile_gateway` entity, 
create a Template Sensor Helper or add this to `configuration.yaml`:

```yaml
template:
  - sensor:
      - name: "T-Mobile Software Version"
        unique_id: t_mobile_home_internet_softwareVersion
        state: '{{ state_attr("sensor.t_mobile_gateway","device")["softwareVersion"] }}'
```

### Display a list of clients known to the gateway in a table

The gateway's client list can be conveniently displayed by using a [custom:flex-table-card](https://github.com/custom-cards/flex-table-card).

This sample configuration uses the `Get Client List` action mentioned above to populate a table with client details:

```yaml
type: custom:flex-table-card
title: T-Mobile Home Internet Clients
action: tmobile_home_internet.get_client_list
entities:
  include: sensor.t_mobile_gateway
sort_by: IP Address
columns:
  - name: Name
    data: clients.name
  - name: IP Address
    data: clients.ipv4
  - name: MAC Address
    data: clients.mac
  - name: Interface
    data: clients.interface
  - name: Connected
    data: clients.connected
    modify: "x ? 'Yes' : 'No'"
  - name: Signal
    data: clients.signal
    modify: x || 'N/A'
```

## Contribute
Feel free to contribute by opening a PR or issue on this project.
