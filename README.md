# AWS-Scripts
Various AWS automation scripts. Example - Taking snapshots of EBS

<b>Snapshots.py</b>
<br>Takes snapshot of the AWS EBS Volume.Keeps 5 snapshots reserved and deletes the oldest one.</br>
<br>#Parameters to be given --</br>
<br>"--volId", help="Volume Id of the volume to take backup of"</br>
<br>"--snap_name",  help="Set name of the snapshot"</br>
<br>"--snap_desc", help="Set description of the snapshot"</br>

<b>Network_acl_block.py</b>
<br>Blocks the IP address provided as the argument, from VPC's Network-acl Inbound Rules.It also takes care of the rule number protocols to be followed.</br>
<br>#Parameters to be given --</br>
<br>"--ip", help="IP to block"</br>
<br>"--region_name", help="Region name of your EC2 instance"</br>
<br>"--nacl_id", help="Network ACL id"</br>


