# earnings_events
Grab various earning events from faunadb and marketview and make latex reports that get sent to discord.

So for the weekly reports just use pylatex to make a tex document as for the annual report use a tex template and just generate stuff in there.


Rather than run meaningless cron jobs, attempt to scrap cnbc headlines afterwards from the rss feed.

## TODO
- discord sending convert table to html somehow, would like a preview of today's table
- try installing the discord library instead of making my own wrapper