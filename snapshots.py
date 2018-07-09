#!/usr/bin/env python2.7

import boto3
import sys
from operator import itemgetter
import argparse
from time import gmtime, strftime

ec2 = boto3.client('ec2', region_name = 'ap-south-1')
waiter = ec2.get_waiter('snapshot_completed')

parser = argparse.ArgumentParser()

parser.add_argument("--volId", required=True, help="Volume Id of the volume to take backup of")
parser.add_argument("--snap_name", required=True, help="Set name of the snapshot")
parser.add_argument("--snap_desc", required=True, help="Set description of the snapshot")

args = parser.parse_args()

class Backup(object):

    def __init__(self):
        self.volId = args.volId
        self.snap_name = args.snap_name
        self.snap_desc = args.snap_desc

    def CreateSnap(self):
        try:
            old_snapshot = ec2.describe_snapshots(Filters=[
                                        {
					    'Name': 'volume-id',
					    'Values': [self.volId,
					    ]
					},
				])
            snapshots = old_snapshot['Snapshots']
            sortedsnap = sorted(snapshots, key = itemgetter('StartTime'), reverse = True)
            old_snapid = sortedsnap[1]['SnapshotId']
            print ('Old Snapshot Id'), old_snapid
        
        except Exception as e:
            pass


        snapshot = ec2.create_snapshot(VolumeId = self.volId,  TagSpecifications=[
             		{
                            'ResourceType': 'snapshot',
                            'Tags': [
                		     {
		                         'Key': 'name',
		                         'Value': self.snap_name
                		     },
		                 ]
		             }
		         ], Description=self.snap_desc)
        
        waiter.wait(
                SnapshotIds=[
                    snapshot.get('SnapshotId'),
                    ],
                WaiterConfig={
                		  'Delay': 10,
		                  'MaxAttempts': 15
                            }
		)
        try:
            self.DeleteSnap(snapshot.get('SnapshotId'), old_snapid)
        except:
            print ('Snapshot created with ID'), snapshot.get('SnapshotId'), 'at', strftime("%Y-%m-%d %H:%M:%S", gmtime())
            print ('No old Snapshot Found or not deleting Snapshot for Best Practices!!')
            
    def DeleteSnap(self, SnapshotId, old_snapid):
        ec2.delete_snapshot(SnapshotId = str(old_snapid))
        print ('New Snapshot created with ID'), SnapshotId, 'at', strftime("%Y-%m-%d %H:%M:%S", gmtime()), ', 2 Snapshots now exists for the volume!!'
        print ('Old Snapshot with ID'), old_snapid, 'is deleted'



if __name__ == '__main__':
    Create_Backup = Backup()
    Create_Backup.CreateSnap()

