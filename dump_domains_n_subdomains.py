import subprocess
import json
import os

def get_route53_hosted_zones():
    cmd = "aws route53 list-hosted-zones"
    output = subprocess.check_output(cmd.split()).decode("utf-8")
    data = json.loads(output)

    hosted_zones = data["HostedZones"]

    return hosted_zones

def extract_subdomains(domain_name, record_sets):
    subdomains = []
    for record_set in record_sets:
        name = record_set["Name"]
        if name.endswith(domain_name):
            subdomain = name[: -len(domain_name)].rstrip(".")
            if subdomain:
                subdomains.append(subdomain)

    return subdomains

def main():
    hosted_zones = get_route53_hosted_zones()

    domains = []
    for hosted_zone in hosted_zones:
        domain_name = hosted_zone["Name"]
        record_sets_cmd = f"aws route53 list-resource-record-sets --hosted-zone-id {hosted_zone['Id']}"
        record_sets_output = subprocess.check_output(record_sets_cmd.split()).decode("utf-8")
        record_sets_data = json.loads(record_sets_output)
        record_sets = record_sets_data["ResourceRecordSets"]
        subdomains = extract_subdomains(domain_name, record_sets)
        domains.append(domain_name)
        domains.extend([subdomain + "." + domain_name for subdomain in subdomains])

    with open("domains_with_dot.txt", "w") as file:
        for domain in domains:
            file.write(domain + "\n")

    print("Domains and subdomains saved to domains_with_dot.txt")

if __name__ == "__main__":
    main()
    os.system("sed 's/\.$//' domains_with_dot.txt > temp.txt")
    os.system("cat temp.txt | sort -u | tee all_domains.txt")
    os.system("rm temp.txt")
