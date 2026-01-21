# Aeronautica ATC Discord Bot
The **Aeronautica ATC Discord Bot** is a specialized discord application designed for the Aeronautica ATC server. It currently offers one core function, creating an airport ATIS, with additional features under active development.
## Current Functionality
### ATIS Generation
The bot's primary function is creating an ATIS *(Automatic Terminal Information Service)* for any in-game airport.
* **Generating:** Simply provide the bot with basic weather data, active runways, and other pertinent details to generate a formatted ATIS.
* **Editing:** The original ATIS creator can both edit their ATIS and tranfer ATIS ownership to a different user for easy controller changes.
* **Deleting:** Any user can delete an ATIS that they ow. Additionally, staff can delete every open ATIS for easy cleanup, especially following large events.
For an in-depth guide on the ATIS tools, see the [User Guide](about:blank)
### Miscellanous commands
* **Squawk Codes:** Generate a random, 4 digit, base-8 squawk code for you
* **UTC Time:** Gives the current time in UTC for easy time conversion and synchronization
* **Staff Broadcast:** High-ranking staff can instruct the bot to send messages for announcements or community engagment.
## Planned functionality
### Leave of Absence (LOA)
A work-in-progress feature for staff to track temporary periods of inactivity.
* **Auto-Notification:** If enabled, the bot will gently notify users who ping a staff member on LOA that they may be slow to respond.
* **Logging:** All LOA requests will be posted in the `#loa-notice` channel with precise start and end timestamps.
## User Guide
Detailed information on all commands, use cases, and technical specifications can be found in the [User Guide](about:blank).

**Contributors:** If you are looking to help with development, the User Guide is a great starting point for understanding the bot's logic, as in-code documentation may be brief.