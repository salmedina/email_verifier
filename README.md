# Email Verifier

This tool verifies the email domains from an email list. Purges out the emails that do not have an existing email:

### Requirements
The pacakges used in this script are:

- `ping3`
- `tqdm`


### Installation
I prefer installing the software using conda to avoid any conflicts with any other installation. The steps would be the following:
```
conda create -n emailverify python=3.7
conda install tqdm
pip3 install ping3
```

### Usage

```
python3 check_domains.py --email_list=<input_file>
```

### Output
The script outputs by default the following files as described:

- `malformed_emails.txt`: email with domains that cannot be pinged
- `valid_domains.txt`: list of domains which were pinged
- `invalid_domains.txt`: list of domains which timedout the ping
- `valid_emails.txt`: list of emails with an existing domain