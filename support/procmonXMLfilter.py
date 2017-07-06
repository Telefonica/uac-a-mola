# This file is part of uac-a-mola
# Copyright (C) Santiago Hernandez Ramos <shramos@protonmail.com>
#
# DESCRIPTION
# This file is aimed for simplify the search of some Registry values
# that resides in a Procmon XML generated file.


def remove(events, to_remove):
    for k in to_remove.keys():
        for e in to_remove[k]:
            events[k].remove(e)
    return events


def by_operation(events, operation):
    for k in events.keys():
        if operation.lower() != k.lower():
            del events[k]
    return events


def by_result(events, result):
    to_remove = {}
    for k in events.keys():
        to_remove[k] = []
        for e in events[k]:
            if e.find("Result").text.lower() != result.lower():
                to_remove[k].append(e)

    return remove(events, to_remove)


def by_process(events, proc_name):
    to_remove = {}
    for k in events.keys():
        to_remove[k] = []
        for e in events[k]:
            if e.find("Process_Name").text.lower() != proc_name.lower():
                to_remove[k].append(e)
    return remove(events, to_remove)


def by_path(events, path):
    to_remove = {}
    for k in events.keys():
        to_remove[k] = []
        for e in events[k]:
            if e.find("Path").text.lower() != path.lower():
                to_remove[k].append(e)
    return remove(events, to_remove)


def by_pid(events, pid):
    to_remove = {}
    for k in events.keys():
        to_remove[k] = []
        for e in events[k]:
            if e.find("PID").text.lower() != str(pid).lower():
                to_remove[k].append(e)
    return remove(events, to_remove)


def by_pattern(events, pattern):
    if not isinstance(pattern, list):
        pattern = list(pattern)
    to_remove = {}
    for k in events.keys():
        to_remove[k] = []
        for e in events[k]:
            for p in pattern:
                if p.lower() not in e.find("Path").text.lower():
                    to_remove[k].append(e)
                    break
    return remove(events, to_remove)


def parse_events(events):
    new_events = {}
    for k in events.keys():
        new_events[k] = []
        for e in events[k]:
            new_events[k].append(fill_event(e))
    return new_events


def fill_event(e):
    event = {}
    event["Process_Name"] = e.find("Process_Name").text
    event["PID"] = e.find("PID").text
    event["Operation"] = e.find("Operation").text
    event["Path"] = e.find("Path").text
    event["Result"] = e.find("Result").text
    event["Detail"] = e.find("Detail").text
    return event
