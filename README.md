# Traffic Processor (TP)

## Project Information

**Project Name:** Traffic Processor (TP)  
**Short Description:** A network visibility and control tool that captures live packet counters, per-connection statistics, traffic history, and supports blocking, tunneling, and failover behaviours.  
**LICENSE:** [LICENSE](/LICENSE)

---

To run via [docker](https://www.docker.com/):

Run in src folder to start the cnss, remote server that recieves and shows data collected

```docker compose up --build```

Run in src folder (in the other cmd tab, or on the other device) to start the tp, program that scans your network activity and send data to cnss

```docker exec tproc cat /data/data.txt | head -3```
