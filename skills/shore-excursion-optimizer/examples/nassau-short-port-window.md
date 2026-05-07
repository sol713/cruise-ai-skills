# Nassau Short Port Window Example

## User Prompt

We're in Nassau from 12:00 PM to 6:00 PM, all aboard at 5:30 PM. Two adults and one grandparent with limited walking. Budget is around $250-$400. We want beach time or a short food/culture experience. We are low-risk because this is our first cruise. Should we do a ship excursion, independent tour, or self-guided?

## Expected Output Shape

RECOMMENDATION: Official short excursion or close self-guided port-area plan

Return-to-ship risk: Medium for independent beach/taxi plans, medium-low for close self-guided, low for official

Why this fits:
- The usable port window is short once clearance and return buffer are removed.
- A grandparent with limited walking makes long transfers and uncertain return transport less attractive.
- A low-risk first-time group should avoid plans that return inside a 90-120 minute buffer.

Time budget:
- Ship in port: 5.5 hours from arrival to all aboard
- Practical activity window: about 2.5-3 hours after clearance and return buffer
- Minimum return buffer: 90-120 minutes

Risk drivers:
- Short midday port window
- Limited walking
- First-time, low-risk group
- Taxi return uncertainty if going farther from port

| Option | Best For | Estimated Cost | Time Control | Return-to-Ship Risk | Notes |
|---|---|---:|---|---|---|
| Official short beach or city excursion | Lowest-stress timing | Usually highest | Moderate | Low | Best if mobility needs are clearly supported |
| Independent nearby food/culture tour | Better local feel | Mid-range | Good if timing is explicit | Medium-low to medium | Use only if pickup, drop-off, walking distance, and return time are clear |
| Self-guided port-area food/culture walk | Flexible and easy to abort | Lowest to mid-range | High | Medium-low | Keep it near the pier and plan a seated stop |

Suggested timeline:
- 12:00 PM Ship arrival
- 12:45 PM Leave ship after clearance
- 1:00 PM Start close activity
- 3:30 PM Begin return toward port area
- 4:00 PM Back near the pier
- 5:30 PM All aboard

Caveats:
- I do not have live inventory, local operating conditions, or current provider schedules here, so treat this as a planning estimate and verify before booking or leaving the port area.
- Confirm walking distance, accessible transport, restroom access, and cancellation terms before paying.

CTA:
Build a port-day timeline with the exact tour pickup and return times before booking.

Conversion tags:

```yaml
user_segment:
  - first_timer
  - family
trip_stage:
  - booked
  - pre_departure
monetization_intent:
  - newsletter
  - excursion
urgency:
  - medium
```
