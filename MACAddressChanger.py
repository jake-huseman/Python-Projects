import subprocess as sub
import argparse
import re

# This class operates on MAC Addresses
# This class gives the functionality to get_args(), change_mac(), and to get_current_mac()

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_arguments('-i', '--interface', dest = 'interface', help = 'Interface name whose MAC is to be changed')
    parser.add_arguments('-m', '--mac', dest = 'new_mac', help = 'New MAC Address')
    options = parser.parse_args()

    # Error checking
    if not options.interface:
        parser.error('~ Please specify an interface using arguements, --help for info')

    elif not options.new_mac:
        parser.error('~ Please specify a new MAC Adress, --help for info')

    return options


def change_mac(interface, new_mac):
    # Checking for correct MAC Address length [17]
    if len(new_mac) != 17:
        print('~ Please enter a MAC Address with a length of 17')
        quit()

    print('\n~ Changing MAC Address ~')
    sub.call(['sudo', 'ifcongif', interface, 'down'])
    sub.call(['sudo', 'ifconfig', interface, 'hw', 'ether', new_mac])
    sub.call(['sudo', 'ifconfig', interface, 'up'])
    print('\n~ MAC Address changed to', new_mac)


def get_current_mac(interface):
    output = sub.check_output(['ifconfig', interface], universal_newlines = True)
    search_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", output)
    if search_mac:
        return search_mac.group(0)
    else:
        print('~ Could not read the MAC Address')


command_args = get_args()

prev_mac = get_current_mac(command_args.interface)
print('~ Old MAC Address --> {}'.format(prev_mac))

change_mac(command_args.interface, command_args.new_mac)

changed_mac = get_current_mac(command_args.interface)
print('~ New MAC Address --> {}'.format(changed_mac))

# Checking if new MAC == given MAC
if changed_mac == command_args.new_mac:
    print('~ Successfully changed the MAC Address from {} to {}'.format(prev_mac, changed_mac))
else:
    print('~ Could not change the MAC Address')