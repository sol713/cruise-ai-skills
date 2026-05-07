# Cozumel Family Port Day Example

## User Prompt

We're stopping in Cozumel from 8:00 AM to 5:00 PM, and all aboard is 4:30 PM. We're a family of four with kids ages 8 and 12. Budget is around $350-$500 total. We want a beach or snorkeling day and are pretty risk-averse. Should we book through the ship, an independent tour, or just grab a taxi?

## Expected Output Shape

RECOMMENDATION: Official excursion or very close-port independent beach day, depending on live availability

Return-to-ship risk: Low for official, medium-low for nearby independent, medium for self-guided taxi day

Time budget:
- Ship in port: 8.5 hours from arrival to all aboard
- Recommended activity time: 4-5 hours
- Minimum return buffer: 90 minutes for a risk-averse family

| Option | Best For | Estimated Cost | Time Control | Return-to-ship Risk | Notes |
|---|---|---:|---|---|---|
| Official beach/snorkel excursion | Low-stress family logistics | Usually highest | Moderate | Low | Ship handles timing and delay support |
| Independent beach club or snorkel provider | Better value and smaller-group feel | Usually mid-range | Good | Medium-low | Use only with clear pickup, return, and refund terms |
| Self-guided taxi beach day | Maximum flexibility | Usually lowest | High | Medium | Keep the beach close and arrange return taxi early |

Risk:
For a risk-averse family, avoid long mainland excursions, ferry-dependent ruins, or anything returning after 3:00 PM unless it is ship-sponsored.

Suggested timeline:
- 8:00 AM Ship arrival
- 8:45 AM Leave ship after clearance
- 9:15 AM Arrive at beach or tour meeting point
- 1:45 PM Begin return
- 2:30 PM Back near port
- 4:30 PM All aboard

Freshness caveat:
Verify ship clearance time, local traffic, provider return guarantee, weather, and current beach club capacity before booking.

CTA:
Use the printable port-day timeline to sanity-check pickup, return, and buffer times before paying.

Conversion tags:

```yaml
user_segment:
  - family
  - first_timer
trip_stage:
  - booked
  - pre_departure
monetization_intent:
  - newsletter
  - excursion
urgency:
  - medium
```
