/*
Event rows look like

     (inserted datetime, ..., activityAfter)

So, if you have two adjacent records

    timestamp, ..., snowboarding
    timestamp + delta, ..., fishing

then we can conclude that you were snowboarding for
`timetamp + delta - timestamp = delta` seconds.

This query returns rows

    (begin datetime, end datetime, activity, duration seconds)

calculated that way, from events within a given time period. The "after"
event is the one that's used when restricting the time period.
*/
select
    begin,
    end,
    activityDuring as activity,
    strftime('%s',end) - strftime('%s',begin) as seconds
from (
    select
        activityAfter as activity,
        inserted as end,
        lag(inserted) over (order by inserted) as begin,
        lag(activityAfter) over (order by inserted) as activityDuring
    from Event
    where inserted between ? and ?
    order by inserted
) adjacentEvents
where
    begin is not null
order by begin;
