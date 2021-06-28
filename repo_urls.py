import argparse
import gitutils


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--org', metavar='organization', help='organization')
    parser.add_argument('--hostname', metavar='hostname', help='hostname')
    args = parser.parse_args()

    if args.hostname:
        gh = gitutils.get_github(hostname=args.hostname)
    else:
        gh = gitutils.get_github()
    org = gh.get_organization(args.org)
    for repo in org.get_repos():
        print(repo.html_url)


if __name__ == '__main__':
    main()
