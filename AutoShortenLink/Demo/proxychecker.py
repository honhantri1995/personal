from proxy_checker import ProxyChecker

checker = ProxyChecker()
# print(checker.check_proxy('203.204.200.107:80'))      # success
# print(checker.check_proxy('124.158.12.3:3128'))       # fail

proxy_list = [
    # '46.41.134.79:5836',
    # '88.199.21.76:80',              # success
    # '91.234.127.222:53281',                                        # success lan 2
    # '36.67.24.109:31255',
    # '162.223.89.220:8080',
    # '91.219.164.110:3128',
    '51.222.12.136:8080',
    '131.108.62.103:41380',
    '89.218.170.54:35704'
]

for proxy in proxy_list:
    print(proxy + ' is ' + str(checker.check_proxy(proxy)))