select 
  sum(milliseconds) / 1000.0 / 60.0 / 60.0 as totalHours,
  activity
from (
  -- This is copied from durations.sql
  select
      begin,
      end,
      activityDuring as activity,
      -- These gnarly calculations convert a datetime to the number of
      -- milliseconds since the UNIX epoch, via the "Julian day."
      -- See https://stackoverflow.com/a/32789171
      -- The Julian day is necessary to preserve better-than-seconds precision.
      ((julianday(end) - 2440587.5) * 86400000) - 
          ((julianday(begin) - 2440587.5) * 86400000)
          as milliseconds
  from (
      select
          activityAfter as activity,
          inserted as end,
          lag(inserted) over (order by inserted) as begin,
          lag(activityAfter) over (order by inserted) as activityDuring
      from Event
      -- The two bound parameters are the start datetime (ISO date string, no TZ)
      -- and the end datetime. Either can be null, which means "no constraint,"
      -- so this "where" clause is a little ugly.
      where
        (case
          when ?1 is null then true
          else inserted >= ?1
         end)
        and
        (case
          when ?2 is null then true
          else inserted <= ?2
         end)
      order by inserted
  ) adjacentEvents
  where
      begin is not null
  order by begin) durations
where activity != 'none' -- exclude unaccounted time
group by activity
order by activity;
