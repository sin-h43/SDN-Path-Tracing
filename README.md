# SDN Path Tracing Tool (POX + Mininet)

## Overview
This project implements a Software Defined Networking (SDN) based path tracing tool using POX controller and Mininet.

## Features
- Captures packets using PacketIn
- Tracks forwarding path
- Displays route between hosts
- Validates connectivity using pingall

## Setup
1. Clone POX
2. Run controller:
   ./pox.py misc.path_trace

3. Run Mininet:
   sudo mn --topo single,3 --controller remote

## Output
- Displays path logs in controller terminal
- Verifies using pingall

## Author
Sinchana-PES1UG24AM405
