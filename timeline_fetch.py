import requests

countries = ['AE', 'AF', 'AL', 'AM', 'AO', 'AR', 'AT', 'AU', 'AZ', 'BA', 'BD', 'BE', 'BF', 'BG', 'BI', 'BJ', 'BN', 'BO', 'BR',\
         'BS', 'BT', 'BW', 'BY', 'BZ', 'CA', 'CD', 'CF', 'CG', 'CH', 'CI', 'CL', 'CM', 'CN', 'CO', 'CR', 'CU', 'CY', 'CZ', 'DE',\
         'DJ', 'DK','DO', 'DZ', 'EC', 'EE', 'EG', 'EH', 'ER', 'ES', 'ET', 'FK', 'FI', 'FJ', 'FR', 'GA', 'GB', 'GE', 'GF', 'GH',\
         'GL', 'GM', 'GN', 'GQ', 'GR', 'GT', 'GW', 'GY', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IN', 'IQ', 'IR', 'IS', 'IT',\
         'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KP', 'KR', 'XK', 'KW', 'KZ', 'LA', 'LB', 'LK', 'LR', 'LS', 'LT', 'LU', 'LV', 'LY',\
         'MA', 'MD', 'ME', 'MG', 'MK', 'ML', 'MM', 'MN', 'MR', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NC', 'NE', 'NG', 'NI', 'NL', 'NO',\
         'NP', 'NZ', 'OM', 'PA', 'PE', 'PG', 'PH', 'PL', 'PK', 'PR', 'PS', 'PT', 'PY', 'QA', 'RO', 'RS', 'RU', 'RW', 'SA', 'SB',\
         'SD', 'SE', 'SI', 'SJ', 'SK', 'SL', 'SN', 'SO', 'SR', 'SS', 'SV', 'SY', 'SZ', 'TD', 'TF', 'TG', 'TH', 'TJ', 'TL', 'TM',\
         'TN', 'TR', 'TT', 'TW', 'TZ', 'UA', 'UG', 'US', 'UY', 'UZ', 'VE', 'VN', 'VU', 'YE', 'ZA', 'ZM', 'ZW']


f = open("timeline.txt", "w")
dates = {}
for i in countries:
    req = requests.get(url = "https://api.thevirustracker.com/free-api?countryTimeline=" + i)
    data = req.json()
    relevent = data["timelineitems"][0]
    for j in relevent.keys():
        if j in dates.keys():
            dates[j] = dates[j] + 1
        else:
            dates[j] = 0

print(dates)

def do(s, relevent):
    if s in relevent.keys():
        return s + ": " + str(relevent[s]["total_cases"]) + "\n"
    else:
        return s + ": " + "0" + "\n"


for i in countries:
    req = requests.get(url = "https://api.thevirustracker.com/free-api?countryTimeline=" + i)
    data = req.json()
    relevent = data["timelineitems"][0]
    f.write("Country: " + i + "\n")
    output = ""
    output += do("2/01/20", relevent)
    output += do("3/01/20", relevent)
    output += do("4/01/20", relevent)
    output += do("4/28/20", relevent)
    f.write(output)

    """for j in relevent.keys():
        output = ""
        temp = 0
        if relevent[j] != "ok":
            temp = relevent[j]["total_cases"]

        output += j + ": " + str(temp) + "\n"
        f.write(output)"""

f.close()
