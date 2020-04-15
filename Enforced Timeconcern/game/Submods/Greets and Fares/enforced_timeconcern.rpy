init -990 python in mas_submod_utils:
    Submod(
        author="multimokia",
        name="Enforced Timeconcern",
        description="This submod allows Monika to be more enforcing of your sleep schedule, by shutting your PC down.",
        version="1.0.0",
        settings_pane="enforced_timeconcern_settings"
    )

#Should we load in with Monika asleep?
default persistent._etc_sleep_load = False

#The time after which we are able to wake Monika up
default persistent._etc_can_wake_up = None

#The data storage for the times
default persistent._etc_weekday_map = {
    0: {"enabled": False, "start_time": 0, "end_time": 0}, #Monday
    1: {"enabled": False, "start_time": 0, "end_time": 0}, #Tuesday
    2: {"enabled": False, "start_time": 0, "end_time": 0}, #Wednesday
    3: {"enabled": False, "start_time": 0, "end_time": 0}, #Thursday
    4: {"enabled": False, "start_time": 0, "end_time": 0}, #Friday
    5: {"enabled": False, "start_time": 0, "end_time": 0}, #Saturday
    6: {"enabled": False, "start_time": 0, "end_time": 0}, #Sunday
}

#START: tooltips
init -1 python:
    etc_tt_start_time = (
        "Use this to let Monika know what time she should start to remind you to go to bed on {0}."
    )

    etc_tt_end_time = (
        "Use this to let Monika know what time she should no longer remind you to go to bed on {0}."
    )

    etc_tt_enable = (
        "Click this to let Monika know that she should remind you to go to bed on {0}."
    )

    etc_tt_day_map = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }

init 1 python in etc_warntimes:
    import store
    import datetime

    #Stuff for screen preprocessing
    NO_CHANGE = 0
    START_CHANGE = 1
    END_CHANGE = 2
    change_state = NO_CHANGE
    modifier = 5 # modifier for chunking the time

    start_prev = store.persistent._etc_weekday_map[0]["start_time"]
    end_prev = store.persistent._etc_weekday_map[0]["end_time"]

    weekday_edit = 0

    time_dict = {
        0: {
            "start_time": int(store.persistent._etc_weekday_map[0]["start_time"]/5),
            "end_time": int(store.persistent._etc_weekday_map[0]["end_time"]/5)
        },
        1: {
            "start_time": int(store.persistent._etc_weekday_map[1]["start_time"]/5),
            "end_time": int(store.persistent._etc_weekday_map[1]["end_time"]/5)
        },
        2: {
            "start_time": int(store.persistent._etc_weekday_map[2]["start_time"]/5),
            "end_time": int(store.persistent._etc_weekday_map[2]["end_time"]/5)
        },
        3: {
            "start_time": int(store.persistent._etc_weekday_map[3]["start_time"]/5),
            "end_time": int(store.persistent._etc_weekday_map[3]["end_time"]/5)
        },
        4: {
            "start_time": int(store.persistent._etc_weekday_map[4]["start_time"]/5),
            "end_time": int(store.persistent._etc_weekday_map[4]["end_time"]/5)
        },
        5: {
            "start_time": int(store.persistent._etc_weekday_map[5]["start_time"]/5),
            "end_time": int(store.persistent._etc_weekday_map[5]["end_time"]/5)
        },
        6: {
            "start_time": int(store.persistent._etc_weekday_map[6]["start_time"]/5),
            "end_time": int(store.persistent._etc_weekday_map[6]["end_time"]/5)
        }
    }

    def startChangeAdjust():
        """
        Runs changes for changing the start time
        """
        global time_dict
        global weekday_edit
        global end_prev
        global NO_CHANGE
        global change_state

        weekday_offset = (weekday_edit + 1) % 7

        start_times = time_dict[weekday_edit]
        end_times = time_dict[weekday_offset]

        if end_times["end_time"] > start_times["start_time"]:
            # ensure sunset remains >= than sunrise
            start_times["start_time"] = end_times["end_time"]

        if end_prev == end_times["end_time"]:
            # if no change since previous, then switch state
            change_state = NO_CHANGE

        end_prev = end_times["end_time"]

    def endChangeAdjust():
        """
        Runs changes for changing the end time
        """
        global time_dict
        global weekday_edit
        global start_prev
        global NO_CHANGE
        global change_state

        weekday_offset = (weekday_edit + 1) % 7

        start_times = time_dict[weekday_edit]
        end_times = time_dict[weekday_offset]

        if start_times["start_time"] < end_times["end_time"]:
            # ensure end_time remains <= than start_time
            end_times["end_time"] = start_times["start_time"]

        if start_prev == start_times["start_time"]:
            # if no change since previous, then switch state
            change_state = NO_CHANGE

        start_prev = start_times["start_time"]

    def setChanging():
        """
        Sets vars for what's changing
        """
        global change_state
        global start_prev, end_prev
        global START_CHANGE, END_CHANGE
        global time_dict, weekday_edit

        weekday_offset = (weekday_edit + 1) % 7

        start_times = time_dict[weekday_edit]
        end_times = time_dict[weekday_offset]

        if start_prev != start_times["start_time"]:
            change_state = START_CHANGE

        elif end_prev != end_times["end_time"]:
            change_state = END_CHANGE

        # set previous values
        start_prev = start_times["start_time"]
        end_prev = end_times["end_time"]

    def setTimes():
        """
        Sets the times into the persistent

        OUT:
            tuple:
                [0] - display start_time
                [1] - display end_time
        """
        global time_dict, weekday_edit

        offset_weekday = (weekday_edit + 1) % 7

        start_times = time_dict[weekday_edit]
        end_times = time_dict[offset_weekday]

        store.persistent._etc_weekday_map[weekday_edit]["start_time"] = start_times["start_time"] * 5
        store.persistent._etc_weekday_map[offset_weekday]["end_time"] = end_times["end_time"] * 5

        st_display = store.mas_cvToDHM(store.persistent._etc_weekday_map[weekday_edit]["start_time"])
        et_display = store.mas_cvToDHM(store.persistent._etc_weekday_map[offset_weekday]["end_time"])

        return (st_display, et_display)

    def HMtoDTT(HM):
        """
        Converts an (hour, minute) tuple to datetime.time

        IN:
            HM - tuple:
                [0] - hour
                [1] - minute

            OUT - datetime.time corresponding to the hour-minute tuple given
        """
        return datetime.time(
            HM[0],
            HM[1]
        )

    def getDictPointer(weekday, _offset=0):
        """
        Returns the pointer to the persistent
        """
        global time_dict

        weekday = (weekday + _offset) % 7

        return time_dict[weekday]

    def getStartDT(weekday=None, _offset=0):
        """
        Gets the start date (in datetime.datetime) for the period we should enforce sleep

        IN:
            weekday - weekday we should get the start date for. If none, current weekday is assumed (Default: None)
            _offset - amount by which we want to offset the weekday. (Default: 0)

        OUT:
            datetime.datetime representing the start date for the enforcing period

        NOTE: Accounts for weekdays not fitting in the dict (will wrap)
        """
        #If we have no weekday, we'll just get that now
        if weekday is None:
            weekday = datetime.date.today().weekday()

        if _offset:
            #Add the offset and sanitize the weekday
            weekday = (weekday + _offset) % 7

        #Now combine new datetime.datetime
        return datetime.datetime.combine(
            datetime.date.today() + datetime.timedelta(days=_offset),
            HMtoDTT(
                store.mas_cvToHM(
                    store.persistent._etc_weekday_map[weekday]["start_time"]
                )
            )
        )

    def getEndDT(weekday=None, _offset=0):
        """
        Gets the end date (in datetime.datetime) for the period we should enforce sleep

        IN:
            weekday - weekday we should get the end date for. If none, current weekday is assumed (Default: None)
            _offset - amount by which we want to offset the weekday. (Default: 0)

        OUT:
            datetime.datetime representing the end date for the enforcing period

        NOTE: Accounts for weekdays not fitting in the dict (will wrap)
        """
        #If we have no weekday, we'll just get that now
        if weekday is None:
            weekday = datetime.date.today().weekday()

        if _offset:
            #Add the offset and sanitize the weekday
            weekday = (weekday + _offset) % 7

        #Now combine new datetime.datetime
        return datetime.datetime.combine(
            datetime.date.today() + datetime.timedelta(days=_offset),
            HMtoDTT(
                store.mas_cvToHM(
                    store.persistent._etc_weekday_map[weekday]["end_time"]
                )
            )
        )

    def shouldEnforceToday(weekday=None, _offset=0):
        """
        Checks if we should enforce timeconcern today

        IN:
            weekday - Weekday to check if we should enforce on

        OUT:
            boolean - True if we should enforce today, False otherwise
        """
        if weekday is None:
            weekday = datetime.date.today().weekday()

        #Sanitize weekday and factor offset
        weekday = (weekday + _offset) % 7

        return store.persistent._etc_weekday_map[weekday]["enabled"]

    def enforcedAlready(weekday=None, _offset=0):
        """
        Checks if we've enforced timeconcern already

        IN:
            weekday - Weekday to get data for

        OUT:
            boolean - True if we've already enforced for the period, False otherwise
        """
        if weekday is None:
            weekday = datetime.date.today().weekday()

        #Sanitize weekday and account for offset
        weekday = (weekday + _offset) % 7

        #Try to get last seen
        try:
            etc_ev = store.mas_getEV("etc_monika_enforced_timeconcern")

        #Since we queue, this doesn't actually matter. But we can't do anything further without the ev
        except:
            return False

        last_seen = etc_ev.last_seen

        #No last seen? We didn't enforce
        if not last_seen:
            return False

        #Now we need to do some work.
        #First, let's verify that we're not past our end time
        start_time = getStartDT(weekday)
        end_time = getEndDT(weekday, _offset=1)

        return start_time <= last_seen <= end_time

#START: settings pane
screen enforced_timeconcern_settings():
    #Preprocessing
    python:
        submods_screen = store.renpy.get_screen("submods", "screens")

        if submods_screen:
            _tooltip = submods_screen.scope.get("tooltip", None)
        else:
            _tooltip = None

    #Setup our weekday stuff
    hbox:
        vbox:
            box_wrap False

            style_prefix mas_ui.cbx_style_prefix

            textbutton _("Monday"):
                action SetField(etc_warntimes, "weekday_edit", 0)
                selected etc_warntimes.weekday_edit == 0

            textbutton _("Tuesday"):
                action SetField(etc_warntimes, "weekday_edit", 1)
                selected etc_warntimes.weekday_edit == 1

            textbutton _("Wednesday"):
                action SetField(etc_warntimes, "weekday_edit", 2)
                selected etc_warntimes.weekday_edit == 2

            textbutton _("Thursday"):
                action SetField(etc_warntimes, "weekday_edit", 3)
                selected etc_warntimes.weekday_edit == 3

            textbutton _("Friday"):
                action SetField(etc_warntimes, "weekday_edit", 4)
                selected etc_warntimes.weekday_edit == 4

            textbutton _("Saturday"):
                action SetField(etc_warntimes, "weekday_edit", 5)
                selected etc_warntimes.weekday_edit == 5

            textbutton _("Sunday"):
                action SetField(etc_warntimes, "weekday_edit", 6)
                selected etc_warntimes.weekday_edit == 6

        vbox:
            xfill True
            box_wrap False

            python:
                ### start_time / end_time preprocessing
                # figure out which value is changing (if any)
                if etc_warntimes.change_state == etc_warntimes.START_CHANGE:
                    # we are modifying start time
                    etc_warntimes.startChangeAdjust()

                elif etc_warntimes.change_state == etc_warntimes.END_CHANGE:
                    # we are modifying end time
                    etc_warntimes.endChangeAdjust()

                else:
                    # decide if we are modifying start time or end time
                    etc_warntimes.setChanging()

                ## preprocess display time
                st_display, et_display = etc_warntimes.setTimes()

            if _tooltip:
                textbutton _("Enabled"):
                    action ToggleDict(persistent._etc_weekday_map[etc_warntimes.weekday_edit], "enabled")
                    selected etc_warntimes.shouldEnforceToday(etc_warntimes.weekday_edit)
                    hovered SetField(_tooltip, "value", etc_tt_enable.format(etc_tt_day_map[etc_warntimes.weekday_edit]))
                    unhovered SetField(_tooltip, "value", _tooltip.default)

                hbox:
                    box_wrap True
                    style_prefix mas_ui.sld_style_prefix
                    label "Start time   "

                    # display time
                    label "[[ " + st_display + " ]"

                bar:
                    value DictValue(etc_warntimes.getDictPointer(etc_warntimes.weekday_edit), "start_time", range=mas_max_suntime, style="slider")
                    hovered SetField(_tooltip, "value", etc_tt_start_time.format(etc_tt_day_map[etc_warntimes.weekday_edit]))
                    unhovered SetField(_tooltip, "value", _tooltip.default)

                hbox:
                    box_wrap True
                    style_prefix mas_ui.sld_style_prefix
                    label "End time   "

                    # display time
                    label "[[ " + et_display + " ]"

                bar:
                    value DictValue(etc_warntimes.getDictPointer(etc_warntimes.weekday_edit, 1), "end_time", range=mas_max_suntime, style="slider")
                    hovered SetField(_tooltip, "value", etc_tt_end_time.format(etc_tt_day_map[(etc_warntimes.weekday_edit + 1) % 7]))
                    unhovered SetField(_tooltip, "value", _tooltip.default)

            else:
                textbutton _("Enabled"):
                    action ToggleDict(persistent._etc_weekday_map[etc_warntimes.weekday_edit], "enabled")
                    selected etc_warntimes.shouldEnforceToday(etc_warntimes.weekday_edit)

                hbox:
                    box_wrap True
                    style_prefix mas_ui.sld_style_prefix
                    label "Start time   "

                    # display time
                    label "[[ " + st_display + " ]"

                bar:
                    value DictValue(etc_warntimes.getDictPointer(etc_warntimes.weekday_edit), "start_time", range=mas_max_suntime, style="slider")

                hbox:
                    box_wrap True
                    style_prefix mas_ui.sld_style_prefix
                    label "End time   "

                    # display time
                    label "[[ " + et_display + " ]"

                bar:
                    value DictValue(etc_warntimes.getDictPointer(etc_warntimes.weekday_edit, 1), "end_time", range=mas_max_suntime, style="slider")


#START: helpers
init 10 python in etc_utils:
    import store
    import datetime

    def lastSeenToday(ev_label):
        """
        Checks if the ev for the inputted ev_label was last seen today
        """
        ev = store.mas_getEV(ev_label)

        return ev and ev.last_seen.date() == datetime.date.today()

    @store.mas_submod_utils.functionplugin("ch30_day")
    def resetTC_EV():
        """
        Resets the TC EV
        """
        #Get the ev
        ev = store.mas_getEV("etc_monika_enforced_timeconcern")

        #Re-conditional/action
        ev.conditional = (
            "not store.etc_warntimes.enforcedAlready() "
            "and store.etc_warntimes.shouldEnforceToday() "
            "and (store.etc_warntimes.getEndDT() >= datetime.datetime.now() or store.etc_warntimes.getStartDT() <= datetime.datetime.now())"
        )
        ev.action = store.EV_ACT_QUEUE

    @store.mas_submod_utils.functionplugin(
        "mas_ch30_post_retmoni_check",
        auto_error_handling=False,
        priority=store.mas_submod_utils.JUMP_CALL_PRIORITY
    )
    def checkSleepLoad():
        """
        Checks if we should load in asleep
        """
        current_time = datetime.datetime.today()

        #Now we need to get the end time (for yesterday, which is stored in today's key) and the start time for today
        start_time = store.etc_warntimes.getStartDT()
        end_time = store.etc_warntimes.getEndDT()

        if (
            current_time <= end_time
            or current_time >= start_time
        ):
            renpy.jump("etc_sleep_checktime")

    #Reset the ev
    resetTC_EV()


#START: new TC topic
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="etc_monika_enforced_timeconcern",
            conditional=(
            "not store.etc_warntimes.enforcedAlready() "
            "and store.etc_warntimes.shouldEnforceToday() "
            "and (store.etc_warntimes.getEndDT() >= datetime.datetime.now() or store.etc_warntimes.getStartDT() <= datetime.datetime.now())"
            ),
            action=EV_ACT_QUEUE,
            unlocked=False,
            rules={"no unlock": 0, "skip alert": 0},
            show_in_idle=True
        )
    )


label etc_monika_enforced_timeconcern:
    #NOTE: We do not re-conditional/re-action here because we don't want this to requeue instantly
    #Skipping checks because this is pretty much one time anyway, and we should probably force show the notif
    $ display_notif(m_name, ["Honey, it's getting late..."], skip_checks=True)

    $ persistent._etc_sleep_load = True

    m 1eka "Hey [player]..."
    m 3eka "It's getting a little late and I just want to make sure you're getting your rest, alright?"

    m 3eka "Is it alright if I turn your computer off so you can get some rest?{nw}"
    $ _history_list.pop()
    menu:
        m "Is it alright if I turn your computer off so you can get some rest?{fast}"

        "Yes.":
            m 3eua "Alright [player]. I'm going to shut down your computer in half an hour."
            m 1eka "Your health is really important to me, so I just want to make sure you're not neglecting your sleep."
            m 3eua "Anyway, I'm feeling a little tired so I'm going to go to bed."
            m 3eka "'Sleep tight, and don't let the bedbugs bite,' ehehe."
            m 1ekbfu "I love you~"

            scene black with dissolve

            #Set PC to shut down
            $ mas_shutdownHost(message="I'll see you tomorrow, [player].\nI love you~", timeout=1800)

            # We should be allowed to wake Monika up only after the timeout is up + 5 minutes for safety
            $ persistent._etc_can_wake_up = datetime.datetime.now() + datetime.timedelta(seconds=2100)

            return "no_unlock|quit"

        "Can we spend a little more time together, [m_name]?":
            m 1eka "Alright, [player]."
            m 1hua "I don't mind spending a little more time with you tonight."
            m 1ekbsa "I'll stay up with you for a little longer. Just promise me that we'll go to bed soon, alright?"

        "No.":
            m 2euc "Oh, are you doing something important right now?{nw}"
            $ _history_list.pop()
            menu:
                m "Oh, are you doing something important right now?{fast}"

                "Yes.":
                    m 2eka "Oh, alright then."
                    m 3eka "If you could finish up soon, it'd make me really happy."
                    m 3eud "I just want to make sure you're getting your rest, alright?"
                    m 3eka "I'll stay up with you until you're done, [player]."

                "No.":
                    m "Alright, [player]."
                    m 1esc "Just make sure you go to bed soon though...{w=0.2}{nw}"
                    extend 1rksdlb "I don't want you to be tired when we spend time together tomorrow after all."
                    m "I'll stay up with you until you're ready to go to bed, alright?"

    return "no_unlock"

#START: Sleep loop flow
label etc_sleep_checktime:
    python:
        #Get current time
        current_time = datetime.datetime.now()

        #Now we need to get the end time (for yesterday, which is stored in today's key) and the start time for today
        start_time = store.etc_warntimes.getStartDT()
        end_time = store.etc_warntimes.getEndDT()

    #Is it slep time?
    if current_time <= end_time or current_time >= start_time:
        #Few things:
        #Monika doesn't know you're here as she's asleep, so we disable the quit warn
        $ mas_enable_quit()

        #Buttons should be hidden
        $ HKBHideButtons()

        #Hotkeys should be disabled
        $ store.mas_hotkeys.music_enabled = False

        #Start loop
        call etc_sleep_start
        jump etc_sleep_main

    else:
        #Buttons should be hidden
        $ HKBHideButtons()

        $ woke_moni = False

        jump etc_sleep_cleanup

label etc_sleep_start:
    hide screen mas_background_timed_jump

    scene black

    $ renpy.music.play(store.songs.FP_MONIKA_LULLABY, loop=True, fadein=1.0, if_changed=True)

    show screen mas_background_timed_jump(60, "etc_sleep_start")

    window hide
    $ ui.add(PauseDisplayable())
    $ ui.interact()
    window auto

    hide screen mas_background_timed_jump

    return

label etc_sleep_main:
    hide screen mas_background_timed_jump

    scene black

    show screen mas_background_timed_jump(60, "etc_sleep_main")
    menu:
        "Wake Monika up." if (not persistent._etc_can_wake_up or (persistent._etc_can_wake_up and persistent._etc_can_wake_up < datetime.datetime.now())):
            $ woke_moni = True
            hide screen mas_background_timed_jump
            jump etc_sleep_cleanup

        "Let her sleep.":
            hide screen mas_background_timed_jump
            pass

    jump etc_sleep_checktime

label etc_sleep_cleanup:

    # Set up weather here
    if not mas_weather.force_weather and not skip_setting_weather:
        $ set_to_weather = mas_shouldRain()
        if set_to_weather is not None:
            $ mas_changeWeather(set_to_weather)
        $ skip_setting_weather = True

    #Also Monika's up so we disable quit
    $ mas_disable_quit()
    #Reset the ev (just to be sure it'll have the right dates on it)
    $ etc_utils.resetTC_EV()

    # Reset our vars so that we won't load back to sleep flow
    $ persistent._etc_sleep_load = False
    $ persistent._etc_can_wake_up = None

    #Stop the music
    stop music fadeout 1.0

    #Transition
    pause 5.0
    call spaceroom(hide_monika=True, dissolve_all=True, scene_change=True)
    pause 2.0
    call mas_transition_from_emptydesk
    #show monika 1eua at ls32 zorder MAS_MONIKA_Z
    call monikaroom_greeting_cleanup

    $ day = "day" if mas_globals.time_of_day_4state in ["morning", "afternoon"] else "night"

    m 1hub "Good [mas_globals.time_of_day_3state], [player]!"
    m 3eub "Let's have another wonderful [day] together."
    jump ch30_post_exp_check
