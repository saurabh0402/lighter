import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import random

DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()

def make_token(prefix):
    return f"{prefix}{random.randint(100000, 999999)}"

def get_screencast_node_id():
    portal = bus.get_object('org.freedesktop.portal.Desktop', '/org/freedesktop/portal/desktop')
    screencast = dbus.Interface(portal, 'org.freedesktop.portal.ScreenCast')
    sender = bus.get_unique_name()[1:].replace('.', '_')

    loop = GLib.MainLoop()
    result = {}

    def request_path(token):
        return f"/org/freedesktop/portal/desktop/request/{sender}/{token}"

    def listen_once(token, callback):
        """Register a listener for exactly this request's Response, then forget it."""
        path = request_path(token)
        def handler(response, results):
            bus.remove_signal_receiver(handler, signal_name='Response',
                                        dbus_interface='org.freedesktop.portal.Request', path=path)
            if response == 0:
                callback(results)
            else:
                print("Cancelled or failed")
                loop.quit()
        bus.add_signal_receiver(handler, signal_name='Response',
                                 dbus_interface='org.freedesktop.portal.Request', path=path)

    # --- Step 3: Start finished → we have our fd + node_id, we're done ---
    def on_started(session_handle, results):
        node_id = results['streams'][0][0]
        fd_obj = screencast.OpenPipeWireRemote(session_handle, {}, byte_arrays=True)
        result['fd'] = fd_obj.take()
        result['node_id'] = node_id
        loop.quit()

    # --- Step 2: SelectSources finished → call Start ---
    def on_sources_selected(session_handle, _results):
        start_token = make_token("start")
        listen_once(start_token, lambda r: on_started(session_handle, r))
        screencast.Start(session_handle, '', {'handle_token': start_token})

    # --- Step 1: CreateSession finished → call SelectSources ---
    def on_session_created(results):
        session_handle = results['session_handle']
        select_token = make_token("select")
        listen_once(select_token, lambda r: on_sources_selected(session_handle, r))
        screencast.SelectSources(session_handle, {
            'types': dbus.UInt32(1),
            'cursor_mode': dbus.UInt32(2),
            'handle_token': select_token,
        })

    # --- Kick off the chain ---
    create_token = make_token("create")
    listen_once(create_token, on_session_created)
    screencast.CreateSession({
        'session_handle_token': make_token("session"),
        'handle_token': create_token,
    })

    loop.run()  # blocks here for the *entire* chain, quits only once fd+node_id are set
    return result['fd'], result['node_id']
