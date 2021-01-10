# ScheduleBot

## Version-1.0

### Added

* Added a loop which checks every certain amount of seconds if there is a new last message in the guild. If no message was sent for 24 hours it will send a certain message to encourge meetups(#1, TheMisterMA).
* Added the BotsDataHandler to handle the meetings and implement by that meeting commands(#5, TheMisterMA).

### Changed

* Until now all the `Bot`'s logic was implemented inside a derived class from discord.Client, from now it would be implemented inside `discord.ext.commands.Cog` like it was intended to be in the original API(#7, TheMisterMA).
* Fixed the bug which sent to everyone in the group the callout message, each time the Bot restarts(#10, TheMisterMA).
