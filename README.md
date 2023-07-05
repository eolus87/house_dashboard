# house_dashboard repo
## Introduction
It is a dashboard based application that queries sensor data from a DB and display
it organised in different tabs:

- __Network__: This tab is about pinging different servers, from local ones to others online.
- __Energy__: Here energy/power sensors are queried and displayed.
- __Temperature__: TBD (probably based on ESP8266 Wi-Fi boards)
- Others: It is easily expandable by including new entries in the conf and 
creating new tabs.

So far just PostGreSQL is supported, but there is an abstract interface for the
link to any other system.

The code can be easily containerized using the Dockerfile in the repo (there is
a compose as well).

## Usage
The devices that the dashboard queries from the interface are specified in the 
`config.yaml` file. 

The recommended usage is by launching a container, see Dockerfile and docker 
compose.

## Future development
- Visual and features improvements -> Include more graphs and stats, better layout.
- Better querying per tab.
- Development and interface of the temperature sensors.


## Known bugs
No knowng bugs at the moment