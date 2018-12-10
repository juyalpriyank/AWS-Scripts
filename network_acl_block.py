import boto3
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--ip", required=True, help="IP to block")
parser.add_argument("--region_name", required=True, help="Region name of your EC2 instance")
parser.add_argument("--nacl_id", required=True, help="Network ACL id")

args = parser.parse_args()

class Block_ip(object):

    def __init__(self):
        self.region_name = args.region_name
        self.nacl_id = args.nacl_id
        self.ec2 = boto3.resource('ec2', region_name = str(self.region_name))
        self.network_acl = self.ec2.NetworkAcl(str(self.nacl_id))
        self.entries = self.network_acl.entries

    def block(self, ip):
        self.ip = str(ip) + '/32'
        rule_num = self.generate_rule_number()
        if self.already_blocked(self.ip):
            print('breaked')
            return
        self.network_acl.create_entry(CidrBlock=str(self.ip), Egress=False, Protocol='-1', RuleAction='deny', RuleNumber=rule_num)

    def already_blocked(self, ip):
        res = [True if rule['CidrBlock'] == ip else False for rule in self.entries]
        if True in res:
            return True
        else:
            return False

    def generate_rule_number(self):
        filtered = []
        [filtered.append(rule['RuleNumber']) for rule in self.entries if ((rule['RuleNumber'] < 100 or rule['RuleNumber'] > 100) and rule['RuleNumber'] != 32767)]
        try:
            rule_number = int(sorted(filtered)[len(filtered) - 1]) + 1
            if rule_number == 100:
                rule_number += 1
        except IndexError as e:
            rule_number = int(1)
        return rule_number


def main():
    block_ip = Block_ip()
    ip = args.ip
    block_ip.block(str(ip))

if __name__ == '__main__':
    main()
