# T-Mobile Home Internet Integration for Home Assistant

## Action Response Examples

The `T-Mobile Home Internet Integration for Home Assistant` provides a number of actions that return responses.
Some actions simply return raw JSON data from the gateway, while others offer additional features of the integration.

The following sections show examples of the data returned by these actions.

### T-Mobile Home Internet: Get Access Point

```yaml
sensor.t_mobile_gateway:
  2.4ghz:
    airtimeFairness: true
    channel: Auto
    channelBandwidth: Auto
    isMUMIMOEnabled: true
    isRadioEnabled: true
    isWMMEnabled: true
    maxClients: 128
    mode: auto
    transmissionPower: 100%
  5.0ghz:
    airtimeFairness: true
    channel: Auto
    channelBandwidth: Auto
    isMUMIMOEnabled: true
    isRadioEnabled: true
    isWMMEnabled: true
    maxClients: 128
    mode: auto
    transmissionPower: 100%
  bandSteering:
    isEnabled: true
  ssids:
    - 2.4ghzSsid: true
      5.0ghzSsid: true
      encryptionMode: AES
      encryptionVersion: WPA2/WPA3
      guest: false
      isBroadcastEnabled: true
      ssidName: TMOBILE-xxxx
      wpaKey: xxxxxxxx
    - 2.4ghzSsid: true
      5.0ghzSsid: true
      encryptionMode: AES
      encryptionVersion: WPA2/WPA3
      guest: true
      isBroadcastEnabled: false
      ssidName: TMOBILE-xxxx
      wpaKey: xxxxxxxx
```

### T-Mobile Home Internet: Get Cell Status

```yaml
sensor.t_mobile_gateway:
  4g:
    bandwidth: 20M
    cqi: 7
    earfcn: "66786"
    ecgi: "310260xxxxxxxx"
    mcc: "310"
    mnc: "260"
    pci: "359"
    plmn: "310260"
    sector:
      antennaUsed: External
      bands:
        - b66
      bars: 4
      cid: 2
      eNBID: 17xxxx
      rsrp: -96
      rsrq: -9
      rssi: -86
      sinr: 7
    status: true
    supportedBands:
      - b2
      - b4
      - b5
      - b12
      - b25
      - b48
      - b66
      - b71
    tac: "10859"
  5g:
    bandwidth: 100M
    cqi: 10
    earfcn: "501390"
    ecgi: "310260xxxxxxxx"
    mcc: "310"
    mnc: "260"
    pci: "791"
    plmn: "310260"
    sector:
      antennaUsed: External
      bands:
        - n41
      bars: 3
      cid: 2
      gNBID: 17xxxx
      rsrp: -103
      rsrq: -11
      rssi: -90
      sinr: 4
    status: true
    supportedBands:
      - n25
      - n41
      - n48
      - n66
      - n71
      - n77
    tac: "10859"
  generic:
    apn: FBB.HOME
    hasIPv6: true
    registration: registered
    roaming: false
  gps:
    latitude: 43.xxxxxx
    longitude: -116.xxxx
```

### T-Mobile Home Internet: Get Client List

```yaml

sensor.t_mobile_gateway:
  clients:
    - connected: true
      ipv4: 192.168.12.xx
      ipv6: []
      mac: xx:xx:xx:xx:xx:xx
      name: xtouch
      signal: -45
      interface: 2.4GHz
    - connected: true
      ipv4: 192.168.12.xx
      ipv6:
        - xxxx::xxxx:xxxx:xxxx:xxxx
        - xxxx:xxxx:xxxx:xxx:xxxx:xxxx:xxxx:xxxx
      mac: xx:xx:xx:xx:xx:xx
      name: RokuPremiere
      signal: -57
      interface: 2.4GHz
    - connected: true
      ipv4: 192.168.12.xxx
      ipv6:
        - xxxx::xxxx:xxxx:xxxx:xxxx
        - xxxx:xxxx:xxxx:xxx:xxxx:xxxx:xxxx:xxxx
      mac: xx:xx:xx:xx:xx:xx
      name: Panel Theater
      signal: -78
      interface: 5.0GHz
    - connected: true
      ipv4: 192.168.12.xx
      ipv6:
        - xxxx::xxxx:xxxx:xxxx:xxxx
        - " "
      mac: xx:xx:xx:xx:xx:xx
      name: homeassistant
      interface: Wired
 ```

### T-Mobile Home Internet: Get Gateway

```yaml
sensor.t_mobile_gateway:
  device:
    friendlyName: 5G Gateway
    hardwareVersion: R02
    index: 1
    isEnabled: true
    isMeshSupported: true
    macId: xx:xx:xx:xx:xx:xx
    manufacturer: Sercomm
    manufacturerOUI: 00C002
    model: TMO-G4SE
    name: 5G Gateway
    role: gateway
    serial: 240xxxxxxxxxx
    softwareVersion: 1.03.20
    type: HSID
    updateState: latest
```

### T-Mobile Home Internet: Get Gateway Clients

```yaml
sensor.t_mobile_gateway:
  2.4ghz:
    - connected: true
      ipv4: 192.168.12.xx
      ipv6: []
      mac: xx:xx:xx:xx:xx:xx
      name: esp32-23802C
      signal: -45
    - connected: true
      ipv4: 192.168.12.xx
      ipv6:
        - xxxx::xxxx:xxxx:xxxx:xxxx
        - xxxx:xxxx:xxxx:xxx:xxxx:xxxx:xxxx:xxxx
      mac: xx:xx:xx:xx:xx:xx
      name: RokuPremiere
      signal: -53
  5.0ghz:
    - connected: true
      ipv4: 192.168.12.xxx
      ipv6:
        - xxxx::xxxx:xxxx:xxxx:xxxx
        - xxxx:xxxx:xxxx:xxx:xxxx:xxxx:xxxx:xxxx
      mac: xx:xx:xx:xx:xx:xx
      name: ""
      signal: -78
  ethernet:
    - connected: true
      ipv4: 192.168.12.xx
      ipv6:
        - xxxx::xxxx:xxxx:xxxx:xxxx
        - " "
      mac: xx:xx:xx:xx:xx:xx
      name: ""
```

### T-Mobile Home Internet: Get Gateway SIM Card

```yaml
sensor.t_mobile_gateway:
  sim:
    iccId: "8901xxxxxxxxxxxxxxx"
    imei: "3599xxxxxxxxxxx"
    imsi: "3102xxxxxxxxxxx"
    msisdn: "1986xxxxxxx"
    status: true
```

### T-Mobile Home Internet: List Client Hostnames

```yaml
sensor.t_mobile_gateway:
  - mac: xx:xx:xx:xx:xx:xx
    name: homeassistant
  - mac: xx:xx:xx:xx:xx:xx
    name: moode
  - mac: xx:xx:xx:xx:xx:xx
    name: Panel Living Room
```
