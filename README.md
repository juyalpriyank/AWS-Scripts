# AWS-Scripts
Various AWS automation scripts. Example - Taking snapshots of EBS

<b>Snapshots.py</b>
<br>#Parameters to be given - AWS EBS</br>
<br>"--volId", help="Volume Id of the volume to take backup of"</br>
<br>"--snap_name",  help="Set name of the snapshot"</br>
<br>"--snap_desc", help="Set description of the snapshot"</br>

<br>#Takes snapshot of the AWS EBS Volume</br>
<br>#Keeps 5 snapshots reserved and deletes the oldest one.</br>
