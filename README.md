<img align="right" width="200" src="images/big_brother.jpg" alt="mascot" />

Panopticon
==========
Panopticon is a web application for tracking time spent programming at work.

Why
---
What do you even do all day?

I was on an experimental SRE (site reliability engineering) team at a previous
job, and my manager suggested that we use something [like this][1] to track
time:

<img width="200" src="images/timeular.png" alt="octohedron" />

The idea was to measure how much SRE time was spent doing operational work,
and adjust prioritizes to make sure it's less than 50% (the other 50% to be
spent developing tooling and automation).

We didn't buy any octohedra, but I wrote a little user interface tool that
we could pin to the corner of one of our screens and use to indicate our
"activity status," e.g. "in a meeting," or "coding," or "responding to an
issue." Then the intervals of activity could be dumped to a spreadsheet for
analysis.

Panopticon is an web-based non-proprietary descendent of that tool.

What
----
Panopticon is a pair of HTML pages served by a Python web server, backed by a
SQLite database.

It implements a web application that allows you to indicate what kind of thing
you're currently doing, and then later analyze how much of each kind of thing
you were doing over a period of time (e.g. last week).

The status indicator looks like this:

<img src="images/demo.png" alt="UI screenshot" />

In this example, the "paperwork" status is selected.

How
---
Run the web server:
```console
david@carbon:~/src/panopticon$ python3 .
 /\     /\
{  `---'  }
{  O   O  }
~~>  V  <~~
 \  \|/  /
  `-----'____
  /     \    \_
 {       }\  )_\_   _
 |  \_/  |/ /  \_\_/ )
  \__/  /(_/     \__/
    (__/

http://127.0.0.1:4000/
```

Navigate to the printed URL:

<img src="images/main.png" width="500" alt="screenshot of URL webpage" />

Click "Save & Launch Popup" to launch the activity status indicator:

<img src="images/demo.png" alt="screenshot of activity status indicator" />

Then click the button that describes your current status. Click again to unset.

I like to set the window "always on top" in some out-of-the-way part of my
secondary monitor.

[1]: https://timeular.com/
