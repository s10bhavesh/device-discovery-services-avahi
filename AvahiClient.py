# http://avahi.org/wiki/PythonBrowseExample
import dbus,avahi
from gi.repository import GObject as gobject
from dbus import DBusException
from dbus.mainloop.glib import DBusGMainLoop


TYPE = "_http._tcp"

def service_resolved(*args):
    print('service resolved')
    print('name:', args[2])
    print('address:', args[7])
    print('port:', args[8])
    print("\n\n")

def print_error(*args):
    print('error_handler')
    print(args[0])

def myhandler(interface, protocol, name, stype, domain, flags):
    print("Found service '%s' type '%s' domain '%s' " % (name, stype, domain))
    print(f"\n flags {flags} \n looku result {avahi.LOOKUP_RESULT_LOCAL}")

    if flags & avahi.LOOKUP_RESULT_LOCAL:
            # local service, skip
            pass

    server.ResolveService(interface, protocol, name, stype, 
        domain, avahi.PROTO_UNSPEC, dbus.UInt32(0), 
        reply_handler=service_resolved, error_handler=print_error)

loop = DBusGMainLoop()

bus = dbus.SystemBus(mainloop=loop)

server = dbus.Interface( bus.get_object(avahi.DBUS_NAME, '/'),
        'org.freedesktop.Avahi.Server')
# self.server = dbus.Interface(
#                 self._bus.get_object(avahi.DBUS_NAME, avahi.DBUS_PATH_SERVER), 
#                 avahi.DBUS_INTERFACE_SERVER)

sbrowser = dbus.Interface(bus.get_object(avahi.DBUS_NAME,
        server.ServiceBrowserNew(avahi.IF_UNSPEC,
            avahi.PROTO_UNSPEC, TYPE, 'local', dbus.UInt32(0))),
        avahi.DBUS_INTERFACE_SERVICE_BROWSER)

sbrowser.connect_to_signal("ItemNew", myhandler)

gobject.MainLoop().run()
# GLib.MainLoop.main()