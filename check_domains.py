import argparse
import pyping

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--email_lst', type=str,
                        help='Path to the file with the email list')
    parser.add_argument('--domain_lst', type=str, 
                        help='Path to the output file with the domain list')
    parser.add_argument('--output_path', type=str,
                        help='Path to the output file with the verified domains')
    args = parser.parse_args()
    return args


def main(args):
    email_list = [l.strip() for l in open(args.email_lst, 'r').read_lines()]
    print(f'Total emails in file:   {len(email_list)}')
    
    email_list = [e for e in email_list if e.find('@') != -1]
    print(f'Total emails with @:    {len(email_list)}')

    domain_set = set([e[e.find('@')+1:] for e in email_list])
    print(f'Total domains found:    {len(domain_set)}')

    existing_domain_list = list()
    for domain in domain_set:
        r = pyping.ping(domain)
        if r.ret_code == 0:
            existing_domain_list.append(domain)
    print(f'Total existing domains: {len(existing_domain_list)}')

    with open(args.domain_lst, 'w') as domains_file:
        domains_file.write('\n'.join(existing_domain_list))

    existing_domain_email_list = list()
    for email in email_list:
        if email[email.find('@')+1:] in existing_domain_list:
            existing_domain_email_list.append(email)
    
    with open(args.output_path, 'w') as emails_file:
        emails_file.write('\n'.join(existing_domain_email_list))
    
    print(f'Finished processing emails.')
    

if __name__ == '__main__':
    args = parse_args()
    main(args)