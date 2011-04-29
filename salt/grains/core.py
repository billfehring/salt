'''
The static grains, these are the core, or built in grains.

When grains are loaded they are not loaded in the same way that modules are
loaded, grain functions are detected and executed, the functions MUST
return a dict which will be applied to the main grains dict. This module
will always be executed first, so that any grains loaded here in the core
module can be overwritten just by returning dict keys with the same value
as those returned here
'''
# Import python modules
import os
import subprocess

def _kernel():
    '''
    Return the kernel type
    '''
    grains = {}
    grains['kernel'] = subprocess.Popen(['uname', '-s'],
        stdout=subprocess.PIPE).communicate()[0].strip()
    if grains['kernel'] == 'aix':
        grains['kernelrelease'] = subprocess.Popen(['oslevel', '-s'],
            stdout=subprocess.PIPE).communicate()[0].strip()
    else:
        grains['kernelrelease'] = subprocess.Popen(['uname', '-r'],
            stdout=subprocess.PIPE).communicate()[0].strip()
    return grains

def _cpuarch():
    '''
    Return the cpu architecture
    '''
    return subprocess.Popen(['uname', '-m'],
        stdout=subprocess.PIPE).communicate()[0].strip()

def _virtual(os_data):
    '''
    Returns what type of virtual hardware is under the hood, kvm or physical
    '''
    # This is going to be a monster, if you are running a vm you can test this
    # grain with please submit patches!
    grains = {'virtual': 'physical'}
    if 'Linux FreeBSD OpenBSD SunOS HP-UX GNU/kFreeBSD'.count(os_data['kernel']):
        if os.path.isdir('/proc/vz'):
            if os.path.isfile('/proc/vz/version'):
                grains['virtual'] = 'openvzhn'
            else:
                grains['virtual'] = 'openvzve'
        if os.path.isdir('/.SUNWnative'):
            grains['virtual'] = 'zone'
        if os.path.isfile('/proc/cpuinfo'):
            if open('/proc/cpuinfo', 'r').read().count('QEMU Virtual CPU'):
                grains['virtual'] = 'kvm'
    return grains

def os_data():
    '''
    Return grins pertaining to the operating system
    '''
    grains = {}
    grains.update(_kernel())
    grains.update(_cpuarch())
    if grains['kernel'] == 'Linux':
        if os.path.isfile('/etc/arch-release'):
            grains['operatingsystem'] = 'Arch'
        elif os.path.isfile('/etc/debian_version'):
            grains['operatingsystem'] = 'Debian'
        elif os.path.isfile('/etc/gentoo-version'):
            grains['operatingsystem'] = 'Gentoo'
        elif os.path.isfile('/etc/fedora-version'):
            grains['operatingsystem'] = 'Fedora'
        elif os.path.isfile('/etc/mandriva-version'):
            grains['operatingsystem'] =  'Mandriva'
        elif os.path.isfile('/etc/mandrake-version'):
            grains['operatingsystem'] = 'Mandrake'
        elif os.path.isfile('/etc/meego-version'):
            grains['operatingsystem'] = 'MeeGo'
        elif os.path.isfile('/etc/vmware-version'):
            grains['operatingsystem'] = 'VMWareESX'
        elif os.path.isfile('/etc/bluewhite64-version'):
            grains['operatingsystem'] = 'Bluewhite64'
        elif os.path.isfile('/etc/slamd64-version'):
            grains['operatingsystem'] = 'Slamd64'
        elif os.path.isfile('/etc/slackware-version'):
            grains['operatingsystem'] = 'Slackware'
        elif os.path.isfile('/etc/enterprise-release'):
            if os.path.isfile('/etc/ovs-release'):
                grains['operatingsystem'] = 'OVS'
            else:
                grains['operatingsystem'] = 'OEL'
        elif os.path.isfile('/etc/redhat-release'):
            data = open('/etc/redhat-release', 'r').read()
            if data.count('centos'):
                grains['operatingsystem'] = 'CentOS'
            elif data.count('scientific'):
                grains['operatingsystem'] = 'Scientific'
            else:
                grains['operatingsystem'] = 'RedHat'
        elif os.path.isfile('/etc/SuSE-release'):
            data = open('/etc/SuSE-release', 'r').read()
            if data.count('SUSE LINUX Enterprise Server'):
                grains['operatingsystem'] = 'SLES'
            elif data.count('SUSE LINUX Enterprise Desktop'):
                grains['operatingsystem'] = 'SLED'
            elif data.count('openSUSE'):
                grains['operatingsystem'] = 'openSUSE'
            else:
                grains['operatingsystem'] = 'SUSE'
    elif grains['kernel'] == 'sunos':
        grains['operatingsystem'] = 'Solaris'
    elif grains['kernel'] == 'VMkernel':
        grains['operatingsystem'] = 'ESXi'
    else:
        grains['operatingsystem'] = kernel

    # Load the virtual machine info
    
    grains.update(_virtual(grains))
    return grains

def hostname():
    '''
    Return fqdn, hostname, domainname
    '''
    # This is going to need some work
    host = subprocess.Popen(['hostname'],
        stdout=subprocess.PIPE).communicate()[0].strip()
    domain = subprocess.Popen(['dnsdomainname'],
        stdout=subprocess.PIPE).communicate()[0].strip()
    return {'host': host,
            'domain': domain,
            'fqdn': host + '.' + domain}

def path():
    '''
    Return the path
    '''
    return {'path': os.environ['PATH'].strip()}


