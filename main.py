from manila_standard_online import sections_mst, scraper_mst
from philstar import sections_ps, scraper_ps

def options():
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
    print('0 - Exit')
    
    my_option = input('Please select Online Site to collect links ===>>> ')

    return my_option

def main(my_option):

    if my_option == '1':
        print('Development Phase')

    elif my_option == '2':
        # sections = sections_ps()
        sections = {}
        scraper_ps(sections)
        
    elif my_option == '7':
        sections = sections_mst()
        scraper_mst(sections)

    return

my_option = options()
main(my_option)



