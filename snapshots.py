#!/usr/bin/env python2.7

import boto3
import sys
from operator import itemgetter


ec2 = boto3.client('ec2', region_name = 'ap-south-1')
waiter = ec2.get_waiter('snapshot_completed')


class Backup(object):


	def CreateSnap(self, VolId):

		try:
			old_snapshot = ec2.describe_snapshots(Filters=[
					{
						'Name': 'volume-id',
						'Values': [VolId,
						]
					},
				])
			snapshots = old_snapshot['Snapshots']
			sortedsnap = sorted(snapshots, key = itemgetter('StartTime'), reverse = True)
			old_snapid = sortedsnap[1]['SnapshotId']
			print 'Old Snapshot Id', old_snapid

		except Exception as e:
			pass


		snapshot = ec2.create_snapshot(VolumeId = VolId,  TagSpecifications=[
             		{
		                 'ResourceType': 'snapshot',
		                 'Tags': [
                		     {
		                         'Key': 'name',
		                         'Value': 'flask1'
                		     },
		                 ]
		             }
		         ], Description="Flaskr snap")

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
			print 'Snapshot created with ID', SnapshotId
			print 'No old Snapshot Found !!'

	def DeleteSnap(self, SnapshotId, old_snapid):
			ec2.delete_snapshot(SnapshotId = str(old_snapid))
			print 'New Snapshot created with ID', SnapshotId
			print 'Old Snapshot with ID', old_snapid, 'is deleted'



if __name__ == '__main__':
	Create_Backup = Backup()
	Create_Backup.CreateSnap(sys.argv[1])
