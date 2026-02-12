import subprocess

def list_bounties():
    try:
        bounties = subprocess.check_output(['gh', 'issue', 'list', '--label=bounty'], stderr=subprocess.STDOUT).decode('utf-8')
        print("Current Bounties:\n", bounties)
    except Exception as e:
        print(f"Error listing bounties: {e}")

def claim_bounty(issue_number):
    try:
        subprocess.run(['gh', 'issue', 'comment', str(issue_number), '--body', 'I claim this bounty!'], check=True)
        print(f"Bounty claimed for issue #{issue_number}.")
    except Exception as e:
        print(f"Error claiming bounty: {e}")

if __name__ == '__main__':
    list_bounties()
    claim_bounty(789)
