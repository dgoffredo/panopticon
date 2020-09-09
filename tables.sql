-- PopupSettings is a historical record of the user's launch settings for the
-- activity popup window. If there are no rows, then use defaults. If there
-- are rows, then use the most recent (largest insertISO8601).
create table if not exists PopupSettings(
    insertISO8601 text not null primary key,  -- server time
    widthPixels integer,
    heightPixels integer,
    leftPixels integer,
    rightPixels integer,
    launchAutomatically boolean);

-- EventType enumerates the possible types of events.
create table if not exists EventType(
    name text not null primary key,
    description text not null);

insert or ignore into EventType(name, description) values
    ('launchPopup', 'the activity-selector browser popup was opened'),
    ('setActivity', 'the user pressed or depressed an activity on the browser popup'),
    ('closePopup', 'the browser popup''s "beforeunload" DOM event fired -- i.e. popup closed'),
    ('serverShutdown', 'the HTTP server behind the UI shut down cleanly');

-- Activity enumerates the possible activity statuses that the user can select
-- in the activity popup window.
create table if not exists Activity(
    name text not null primary key,
    description text not null);

insert or ignore into Activity(name, description) values
    ('none', 'no button is selected in the activity popup'),
    ('firefighting', 'something bad happened and you have to deal with it right now'),
    ('triaging', 'something might need immediate attention, but you''re not sure yet'),
    ('discussion', 'it''s not a meeting, but you''re discussing something, e.g. on Slack'),
    ('research', 'reading code, reading documentation, experimenting with tools, etc.'),
    ('coding', 'writing code, testing and debugging, and writing documentation'),
    ('break', 'not working'),
    ('review', 'reviewing someone else''s code, or responding to review feedback'),
    ('paperwork', 'project management tools (e.g. Jira), sysadmin requests, etc.'),
    ('meeting', 'in a scheduled meeting');

-- Event is a historical record of all happenings in the app that are relevant
-- for measuring time spent in different activity states.
-- By looking at all events during an interval of time, the total time spent in
-- each activity state can be calculated. The result of that calculation is not
-- stored in this database. Only the events are stored.
create table if not exists Event(
    insertISO8601 text not null primary key, -- server time
    type text not null references EventType(name),
    -- activityAfter is the activity status that the user is in now that the
    -- event has occurred.
    activityAfter text not null references Activity(name));
    
