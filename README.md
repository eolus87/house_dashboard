# network_tools repo
## Introduction
Network tools is a dashboard based application that queries different sensors and display the 
temporal signal in charts. The dashboard is composed of 4 tabs:

- Network: This tab is about pinging different servers, from local ones to others online.
- Energy: Here energy/power sensors are queried and displayed.
- Temperature: TBD (probably based on ESP8266 Wi-Fi boards)
- Control: TBD (same devices as in the energy one using public APIs)

So far, just Kasa smart devices are supported. 

The code can be easily containararised using the Dockerfile and compose in the repo.

## Usage
The devices the dashboard queries are specified in the config.yaml file. 

The recommended usage is by launching a container, see Dockerfile and docker compose.

## Future development
- Development and interface of the temperature sensors.
- Probably splitting this repo into different layers, leaving the dashboard just as a frontend, not driving
the query system as well.

## Known bugs
- Kasa plugs sometimes restart, cutting its power randomly when they are queried from the Kasa API.