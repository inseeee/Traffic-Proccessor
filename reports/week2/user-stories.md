## US-01: Basic Packet Counting

**Requirement status:** Active
**MoSCoW priority:** Must Have

As a network administrator,
I want to see the total number of packets received and transmitted by the Traffic Processor in real time,
so that I can quickly verify that the TP is correctly seeing traffic on the network segment.

---

## US-02: Web Dashboard

**Requirement status:** Active
**MoSCoW priority:** Must Have

As a home user,
I want to view live packet counters and basic traffic graphs through a web‑based management UI,
so that I can intuitively understand and rate my metrics.

---

## US-03: Deploy TP as a Virtual Machine

**Requirement status:** Active
**MoSCoW priority:** Must Have

As a home user,
I want to have the possibility to run the Traffic Processor inside a VM,
so that I can test and validate the platform without dedicated hardware.

---

## US-04: Collect and Display Per‑Connection Statistics

**Requirement status:** Active
**MoSCoW priority:** Should Have

As a network administrator,
I want to see, for each source‑destination pair, the number of connections and the ports used,
so that I can detect unusual connection patterns.

---

## US-05: Block Traffic Based on a Blacklist

**Requirement status:** Active
**MoSCoW priority:** Should Have

As a network administrator,
I want to define a list of IP addresses or ports to block, and have the TP drop those packets,
so that I can prevent access to known malicious or undesirable destinations.

---

## US-06: Traffic Statistics History

**Requirement status:** Active
**MoSCoW priority:** Could Have

As a network administrator,
I want to view history of packet and connection data with timestamps,
so that I can produce audit reports or investigate past incidents.

---

## US-07: Tunnel Selected Traffic to a Remote Gateway Node

**Requirement status:** Active
**MoSCoW priority:** Could Have

As a network administrator,
I want to designate certain traffic to be encapsulated and forwarded to a Gateway Node instead of its original destination,
so that my traffic appears to originate from the gateway's location.

---

## US-08: Export Packet Captures for External Analysis

**Requirement status:** Active
**MoSCoW priority:** Could Have

As a network administrator,
I want to download a PCAP file of traffic that passed through the TP,
so that I can analyse suspicious traffic with tools like Wireshark.

---

## US-09: Monitor TP Health and Failure Behaviour

**Requirement status:** Active
**MoSCoW priority:** Should Have

As a network administrator,
I want to configure a fail‑open or fail‑close behaviour for the TP,
so that the network does not experience unexpected outages or security gaps.

---

## US-10: Plug‑and‑Run

**Requirement status:** Active
**MoSCoW priority:** Should Have

As a home user,
I want to physically connect the TP device between my router and the internet, power it on, and have it start working with default rules without any configuration,
so that I can run the software without deep network knowledge.