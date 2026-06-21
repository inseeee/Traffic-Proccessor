# Week 3 Reflection

## Learning points
The team migrated user stories to GitHub Issues, estimated them in Story Points, and split tem into tasks. We successfully connected Frontend, Backend, Communication Node, and Traffic Processor inside a working VM. We also practiced strict Git workflow rules with mandatory peer reviews and comments.

## Validated assumptions
We confirmed that our VM environment is working and stable for deployment. We validated that network telemetry transfers correctly between all software components without data loss. We also proved that a web interface is effective for showing real-time metrics.

## Friction and gaps
The current UI displays only two simple numbers and does not clearly split traffic. The client wants one-way packet counts as a large font and the combined round-trip total separately. Additionally, the monitored network protocols are not yet categorized into inbound and outbound groups.

## Planned response
In the next Sprint, we will update the UI layout to show one-way counts as the main metric and total counts separately. We will also update our database and frontend logic to divide all tracked protocols into inbound and outbound categories. New backlog issues will track these updates.
