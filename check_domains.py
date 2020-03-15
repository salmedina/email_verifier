import argparse
import ping3
from joblib import Parallel, delayed
import multiprocessing
from tqdm import tqdm

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--email_lst', type=str,
                        help='Path to the file with the email list')
    parser.add_argument('--num_ping_threads', type=int, default=8,
                        help='Number of threads that ping the domains')
    parser.add_argument('--malformed_lst', type=str, default='malformed_emails.txt',
                        help='Path to the output file with the malformed emails')
    parser.add_argument('--valid_domain_lst', type=str, default='valid_domains.txt',
                        help='Path to the output file with the domain list')
    parser.add_argument('--invalid_domain_lst', type=str, default='invalid_domains.txt',
                        help='Path to the output fiel with the invalid domain list')
    parser.add_argument('--output_path', type=str, default='valid_emails.txt',
                        help='Path to the output file with the verified domains')
    args = parser.parse_args()
    return args

def get_domain(email):
    return email[email.find('@')+1:]

def tag_domain_exists(domain):
    tag = True
    if ping3.ping(domain) == False:
        tag = False
    return (domain, tag)

def main(args):
    email_list = [l.strip() for l in open(args.email_lst, 'r').readlines()]
    print(f'Total emails in file:        {len(email_list)}')

    wellformed_emails = list()
    malformed_emails = list()
    for email in tqdm(email_list):
        if len(email) < 1 or \
            email.find('@') == -1 or \
            email[email.find('@')+1:][0] == ' ' or \
            email[email.find('@')+1:][0] == '.' or \
            email[email.find('@')+1:].find('..') != -1:
            malformed_emails.append(email)
        else:
            wellformed_emails.append(email)

    with open(args.malformed_lst, 'w') as malformed_file:
        malformed_file.write('\n'.join(malformed_emails))
        print(f'Wrote malformed emails to {args.malformed_lst}')

    print(f'Total well-formed emails:    {len(wellformed_emails)}')

    domain_set = set(map(get_domain, wellformed_emails))
    print(f'Total domains found:         {len(domain_set)}')

    
    domain_inputs = tqdm(domain_set)
    tagged_domains = Parallel(n_jobs=args.num_ping_threads)(delayed(tag_domain_exists)(d) for d in domain_inputs)

    existing_domain_list = [d for d, t in tagged_domains if t==True]
    nonexisting_domain_list = [d for d, t in tagged_domains if t==False]
    print(f'Total valid domains:          {len(existing_domain_list)}')
    print(f'Total invalid domains:        {len(nonexisting_domain_list)}')

    with open(args.valid_domain_lst, 'w') as domains_file:
        domains_file.write('\n'.join(existing_domain_list))
        print(f'Wrote valid domains to {args.valid_domain_lst}')

    with open(args.invalid_domain_lst, 'w') as domains_file:
        domains_file.write('\n'.join(nonexisting_domain_list))
        print(f'Wrote valid domains to {args.invalid_domain_lst}')

    print(f'Filtering emails with valid domains')
    existing_domain_email_list = list()
    pbar = tqdm(email_list)
    for email in pbar:
        pbar.set_description(f'{email}')
        if email[email.find('@')+1:] in existing_domain_list:
            existing_domain_email_list.append(email)
    
    with open(args.output_path, 'w') as emails_file:
        emails_file.write('\n'.join(existing_domain_email_list))
        print(f'Wrote valid domain emails to {args.output_path}')
    
    print(f'Finished processing emails.')
    

if __name__ == '__main__':
    args = parse_args()
    main(args)