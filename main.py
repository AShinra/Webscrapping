from manila_standard_online import sections_mst, scraper_mst

print('Options')
print('1 - Philippine Daily Inquirer')
print('2 - Philippine Star')
print('3 - Manila Bulletin')
print('4 - Business World')
print('5 - Business Mirror')
print('6 - Manila Times')
print('7 - Manila Standard')
print('8 - Malaya Business Insight')
print('9 - Daily Tribune')

my_option = input('Please select Online Site to collect links ===>>> ')

if my_option == 7:
    print('7')
    sections = sections_mst()
    scraper_mst(sections)