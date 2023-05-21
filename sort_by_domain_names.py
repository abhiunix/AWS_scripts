with open('updated_domains.txt', 'r') as file:
    domains = file.read().splitlines()

sorted_domains = sorted(domains, key=lambda domain: domain.split('.')[-2:])

with open('sorted_domains.txt', 'w') as file:
    file.write('\n'.join(sorted_domains))
