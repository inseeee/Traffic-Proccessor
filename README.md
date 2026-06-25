# Traffic Processor (TP)

## Project Information

**Project Name:** Traffic Processor (TP)  
**Short Description:** A network visibility and control tool that captures live packet counters, per-connection statistics, traffic history, and supports blocking, tunneling, and failover behaviours.  
**Root LICENSE:** [LICENSE](/LICENSE)

---

To run via docker:

Run in src folder
```docker compose up --build```

Then in a new cmd tab
```docker exec tproc cat /data/data.txt | head -3```
