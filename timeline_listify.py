import math
f = open("timeline.txt", "r")
q = open("formatted.txt", "w")
b = open("prediction_country_to_newcases_v1.txt", "r")
line = f.readline()
output = []

codeToCountry  = {'af': 'Afghanistan', 'al': 'Albania', 'dz': 'Algeria', 'ao': 'Angola', 'ar': 'Argentina', 'am': 'Armenia', 'au': 'Australia', 'at': 'Austria', 'az': 'Azerbaijan', 'bs': 'Bahamas', 'bd': 'Bangladesh', 'by': 'Belarus', 'be': 'Belgium', 'bz': 'Belize', 'bj': 'Benin', 'bt': 'Bhutan', 'bo': 'Bolivia', 'ba': 'Bosnia and Herzegovina', 'bw': 'Botswana', 'br': 'Brazil', 'bn': 'Brunei Darussalam', 'bg': 'Bulgaria', 'bf': 'Burkina Faso', 'bi': 'Burundi', 'kh': 'Cambodia', 'cm': 'Cameroon', 'ca': 'Canada', 'ci': 'Ivory Coast', 'cf': 'Central African Republic', 'td': 'Chad', 'cl': 'Chile', 'cn': 'China', 'co': 'Colombia', 'cg': 'Congo', 'cd': 'DR Congo', 'cr': 'Costa Rica', 'hr': 'Croatia', 'cu': 'Cuba', 'cy': 'Cyprus', 'cz': 'Czechia', 'dk': 'Denmark', 'oa': ' Diamond Princess', 'dj': 'Djibouti', 'do': 'Dominican Republic', 'ec': 'Ecuador', 'eg': 'Egypt', 'sv': 'El Salvador', 'gq': 'Equatorial Guinea', 'er': 'Eritrea', 'ee': 'Estonia', 'et': 'Ethiopia', 'fk': 'Falkland Islands', 'fj': 'Fiji', 'fi': 'Finland', 'fr': 'France', 'gf': 'French Guiana', 'tf': 'French Southern Territories', 'ga': 'Gabon', 'gm': 'Gambia', 'ge': 'Georgia', 'de': 'Germany', 'gh': 'Ghana', 'gr': 'Greece', 'gl': 'Greenland', 'gt': 'Guatemala', 'gn': 'Guinea', 'gw': 'Guinea-Bissau', 'gy': 'Guyana', 'ht': 'Haiti', 'hn': 'Honduras', 'hk': 'Hong Kong', 'hu': 'Hungary', 'is': 'Iceland', 'in': 'India', 'id': 'Indonesia', 'ir': 'Iran', 'iq': 'Iraq', 'ie': 'Ireland', 'il': 'Israel', 'it': 'Italy', 'jm': 'Jamaica', 'jp': 'Japan', 'jo': 'Jordan', 'kz': 'Kazakhstan', 'ke': 'Kenya', 'kp': 'North Korea', 'xk': 'Republic of Kosovo', 'kw': 'Kuwait', 'kg': 'Kyrgyzstan', 'la': 'Lao', 'lv': 'Latvia', 'lb': 'Lebanon', 'ls': 'Lesotho', 'lr': 'Liberia', 'ly': 'Libya', 'lt': 'Lithuania', 'lu': 'Luxembourg', 'mk': 'Macedonia', 'mg': 'Madagascar', 'mw': 'Malawi', 'my': 'Malaysia', 'ml': 'Mali', 'mr': 'Mauritania', 'mx': 'Mexico', 'md': 'Moldova', 'mn': 'Mongolia', 'me': 'Montenegro', 'ma': 'Morocco', 'mz': 'Mozambique', 'mm': 'Myanmar', 'na': 'Namibia', 'np': 'Nepal', 'nl': 'Netherlands', 'nc': 'New Caledonia', 'nz': 'New Zealand', 'ni': 'Nicaragua', 'ne': 'Niger', 'ng': 'Nigeria', 'no': 'Norway', 'om': 'Oman', 'pk': 'Pakistan', 'ps': 'Palestine', 'pa': 'Panama', 'pg': 'Papua New Guinea', 'py': 'Paraguay', 'pe': 'Peru', 'ph': 'Philippines', 'pl': 'Poland', 'pt': 'Portugal', 'pr': 'Puerto Rico', 'qa': 'Qatar', 'ro': 'Romania', 'ru': 'Russia', 'rw': 'Rwanda', 'sa': 'Saudi Arabia', 'sn': 'Senegal', 'rs': 'Serbia', 'sl': 'Sierra Leone', 'sg': 'Singapore', 'sk': 'Slovakia', 'si': 'Slovenia', 'sb': 'Solomon Islands', 'so': 'Somalia', 'za': 'South Africa', 'kr': 'South Korea', 'ss': 'South Sudan', 'es': 'Spain', 'lk': 'Sri Lanka', 'sd': 'Sudan', 'sr': 'Suriname', 'sj': 'Svalbard and Jan Mayen', 'sz': 'Swaziland', 'se': 'Sweden', 'ch': 'Switzerland', 'sy': 'Syrian Arab Republic', 'tw': 'Taiwan', 'tj': 'Tajikistan', 'tz': 'Tanzania', 'th': 'Thailand', 'tl': 'Timor-Leste', 'tg': 'Togo', 'tt': 'Trinidad and Tobago', 'tn': 'Tunisia', 'tr': 'Turkey', 'tm': 'Turkmenistan', 'ae': 'UAE', 'ug': 'Uganda', 'gb': 'United Kingdom', 'ua': 'Ukraine', 'us': 'USA', 'uy': 'Uruguay', 'uz': 'Uzbekistan', 'vu': 'Vanuatu', 've': 'Venezuela', 'vn': 'Vietnam', 'eh': 'Western Sahara', 'ye': 'Yemen', 'zm': 'Zambia', 'zw': 'Zimbabwe', '': ''}

line2 = b.readline()
predict = {}
while line2 != "":
    loc = line2.index(",")
    predict[line2[:loc]] = line2[loc + 1:].replace("\n", "")
    line2 = b.readline()


while line != "":
    if "Country" in line:
        f.readline()
        f.readline()
        f.readline()
        temp = f.readline()
        value = int(temp[9:])
        if value == 0:
            output.append([line[9:11], {"v": 0, "f": "0"}, "Cases: 0, Predicted: N/A"])
        else:
            name = codeToCountry[line[9:11].lower()]
            if not name in predict.keys():
                output.append([{"v": line[9:11], "f": codeToCountry[line[9:11].lower()]}, {"v": math.log(int(temp[9:]), 10), "f":temp[9:len(temp) - 2]}, "Cases: " + str(temp[9:len(temp)-2]) + ", Predicted: N/A"])
            else:
                output.append([{"v": line[9:11], "f": codeToCountry[line[9:11].lower()]}, {"v": math.log(int(temp[9:]), 10), "f":temp[9:len(temp) - 2]}, "Cases: " + str(temp[9:len(temp)-2]) + ", Predicted: " + str(predict[name])])
        line = f.readline()

print(output)
q.write(str(output).replace("'v'", "v").replace("'f'", "f").replace("], [", "],\n["))
