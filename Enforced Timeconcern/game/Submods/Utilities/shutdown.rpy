init 999 python:
    import win32security
    import win32api
    import os
    from ntsecuritycon import *

    def _adjustPrivilege(priv, enable=True):
        #Get process token
        flags = TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY
        htoken = win32security.OpenProcessToken(win32api.GetCurrentProcess(), flags)
        #Get the ID for the  privilege.
        idd = win32security.LookupPrivilegeValue(None, priv)
        #Get the privilege for this process and create a list of the privileges to be added
        if enable:
            newPrivileges = [(idd, SE_PRIVILEGE_ENABLED)]

        else:
            newPrivileges = [(idd, 0)]

        #Make the adjustment
        win32security.AdjustTokenPrivileges(htoken, 0, newPrivileges)

    def mas_shutdownHost(message="I'm doing this for your own good, [player].", timeout=30, _force=False, _reboot=False):
        _adjustPrivilege(SE_SHUTDOWN_NAME)
        try:
            win32api.InitiateSystemShutdown(
                os.environ["COMPUTERNAME"],
                renpy.substitute(message),
                timeout,
                _force,
                _reboot
            )

        finally:
            # Now we remove privilege
            _adjustPrivilege(SE_SHUTDOWN_NAME, 0)

    def mas_abortShutdown():
        _adjustPrivilege(SE_SHUTDOWN_NAME)
        try:
            win32api.AbortSystemShutdown(None)

        finally:
            _adjustPrivilege(SE_SHUTDOWN_NAME, 0)
