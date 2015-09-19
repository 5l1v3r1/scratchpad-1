#!/bin/bash

tld="ca"
domains=$(cat /usr/share/dict/words | \
          grep -vP "('s$|[^a-z])" | \
          xargs printf "%s.$tld\n")

check_domain() {
    # check this way using whois, but CIRA whois ratelimits
    #if grep -Pq 'Domain status:\s*available' <(whois $1 2>&1); then
    if ! dig $1 SOA +noall +answer | grep -q '^[^;].*SOA'; then
        echo $1
    fi
}

export -f check_domain
parallel check_domain ::: $domains
