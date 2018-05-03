from compute import *

from base import ARMTemplate
from network import VirtualNetwork, AddressSpace, Subnet

template = ARMTemplate()

vnet = VirtualNetwork("myvnet",
                      addressSpace=AddressSpace(addressPrefixes=['10.0.0.0/24']),
                      subnets=[Subnet('subnet1', addressPrefix='10.0.0.0/24')])

linux_conf = LinuxConfiguration(disablePasswordAuthentication=False)

ip_conf = VirtualMachineScaleSetIPConfiguration('my_ip_config',
                                                subnet=SubResource(id=vnet.SubnetRef('subnet1')))
nic_conf = VirtualMachineScaleSetNetworkConfiguration('my_nic',
                                                      primary=True,
                                                      ipConfigurations=[ip_conf])

ss_vm_prof = VirtualMachineScaleSetVMProfile(
    osProfile=VirtualMachineScaleSetOSProfile(computerNamePrefix='testVm',
                                              adminUsername='adminuser',
                                              adminPassword='Welcome1234567+',
                                              linuxConfiguration=linux_conf),
    storageProfile=VirtualMachineScaleSetStorageProfile(imageReference=ImageReference(publisher='Canonical',
                                                                                      offer='UbuntuServer',
                                                                                      sku='16.04-LTS'),
                                                        osDisk=VirtualMachineScaleSetOSDisk(createOption='FromImage')),
    networkProfile=VirtualMachineScaleSetNetworkProfile(networkInterfaceConfigurations=[nic_conf])
)

vm_scale_set = VirtualMachineScaleSets('my_scale_set',
                                       # plan=Plan(),
                                       sku=Sku(name='Standard_A1', tier='Standard', capacity=3),
                                       overprovision=True,
                                       upgradePolicy=UpgradePolicy(mode='Manual'),
                                       virtualMachineProfile=ss_vm_prof).with_depends_on(vnet)

template.add_resource([vm_scale_set, vnet])

print(template.to_json())
