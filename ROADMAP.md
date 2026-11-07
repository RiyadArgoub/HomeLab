# Roadmap

This prototype has working software-side components, but substantial hardware, security, reliability, and usability work remains. The estimates below are rough engineering estimates and should be updated as the implementation evolves.

## Planned work

| Workstream | Planned work | Estimate |
| --- | --- | ---: |
| Hardware validation | Bench-test ESP32, ST7789V, microSD, I²C LCD, joystick, buttons, and piezo together; document measured voltages and pin behavior | 4–5 h |
| BLE security | Replace unauthenticated demo BLE commands with authenticated/encrypted pairing and reject untrusted clients | 5–6 h |
| Remote-control safety | Add per-device permissions, clearer action scopes, stronger confirmation flow, and an auditable action log | 4–5 h |
| Status model | Separate network reachability from power state and add configurable health checks per machine | 3–4 h |
| 128-PC usability | Improve filtering/search, bulk editing, validation, and navigation for large registries | 3–4 h |
| Enclosure validation | Measure real modules, print a fit-check enclosure, revise tolerances, cable relief, battery access, and mounting points | 4–6 h |
| Test coverage | Add protocol edge cases, 128-record boundary tests, malformed SD input tests, and GUI-independent regression tests | 3–4 h |
| Documentation | Record a complete first-build procedure, hardware test results, troubleshooting observations, and deployment limitations | 2–3 h |

**Estimated remaining work: 28–37 hours.**

## Suggested issue breakdown

- [ ] Bench-test complete ESP32 hardware stack
- [ ] Add authenticated BLE pairing
- [ ] Add per-device remote-action permissions and audit log
- [ ] Improve power-state and health detection
- [ ] Improve 128-PC search and bulk editing
- [ ] Print and validate enclosure fit
- [ ] Expand boundary and protocol test coverage
- [ ] Document first complete hardware build

## Current limitations

- Physical ESP32/BLE/display integration has not yet been validated as one complete assembled system.
- The demo PIN and BLE protocol are intentionally prototype-grade and must not protect production infrastructure.
- TCP reachability is not equivalent to verified computer power state.
- Wake-on-LAN and SSH shutdown depend on host configuration outside this project.
- The enclosure is based on nominal module dimensions until real-hardware fit testing is completed.
