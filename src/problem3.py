from bs4 import BeautifulSoup
import json
import logging
import requests
import re

from config import config

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='logs/app.log',
                    filemode='w')

class FetchCaltransOffices():

    def __init__(self):
        self.web_page_name = config.page_name
        self.base_url = config.base_url
        self.url = "".join([self.base_url, self.web_page_name])
        self.offices_info = []
    
    def call_url(self):
        '''
            Call the page url.
        '''
        self.r = requests.get(self.url)
        self.soup = BeautifulSoup(self.r.content, features="lxml")
    
    def process_html_page(self):
        '''
            Finding table element in html page.

            Returns
            ----------
            False: In case web site structure change and generates appropriate
                   warning.
        '''
        self.table_elem = self.soup.find('table')

        if self.table_elem == None:
            logging.warning("No table elem found. check the base url {self.url} whether it's still valid or not?")
            return False

        self.rows = self.table_elem.findChildren('tr')

    def get_records(self):
        '''
            Retriving records from all the elements.
        '''
        self.records = [[x for x in row('td')] for row in self.rows[1:-1]]
    
    def set_office_info(self):
        '''
            Set the office info in the list.
        '''
        for record in self.records:
            office_info = {}
    
            # office name
            name_elem = record[0]

            if name_elem != None:
                logging.info('setting office name info..')
                raw_office_name = name_elem.text
                office_info['office_name'] = raw_office_name
            else:
                logging.warning('setting office name to None..')
                office_info['office_name'] = None
            
            #office_link
            raw_office_elem = name_elem.find('a', href=True)
            if raw_office_elem != None:
                logging.info('setting office link info..')
                office_info['office_link'] = "".join([self.base_url, raw_office_elem['href']])  
            else:
                logging.warning('setting office link to None..')
                office_info['office_link'] = None
            
            #office_address, city, state and zip
            raw_office_address_elem = record[1]
            if raw_office_address_elem != None:
                logging.info('setting office address info..')
                raw_office_address = re.sub('\n', ',', raw_office_address_elem.text.strip(' \t\n\r'))
                office_address = raw_office_address.split(',')
                office_city = office_address[1].strip(" ")
                office_info['office_address'] = ",".join([office_address[0],
                                                        office_city,
                                                        office_address[2]])
                office_info['office_city'] = office_city

                state_zipcode = office_address[2].lstrip(" ").split(" ")
                state, zipcode = state_zipcode[0], state_zipcode[1]
                office_info['office_state'] = state
                office_info['office_zip'] = zipcode
            else:
                logging.warning('setting office address to None..')
                office_info['office_address'] = None
                office_info['office_city'] = None
                office_info['office_state'] = None
                office_info['office_zip'] = None
            
            #office_phone
            general_information_elem = record[3]
            if general_information_elem != None:
                logging.info('setting office general info..')
                raw_general_information = general_information_elem
                office_phone = " ".join([str(x).strip(' \t\n\r<br/>\s+') for x in raw_general_information.contents])
                office_info['office_phone'] = office_phone
            else:
                logging.warning('setting office general info to None..')
                office_info['office_phone'] = None

            #mail_address
            mail_address_elem = record[2]
            if mail_address_elem != None:
                logging.info('setting mail address info..')
                raw_mail_address = re.sub('\n', ',', mail_address_elem.text.strip(' \t\n\r'))
                mail_address = raw_mail_address.split(',')
                office_info['mail_address'] = ",".join([mail_address[0],mail_address[1].strip(" "),mail_address[2]])
                
                #mail_city
                office_info['mail_city'] =  mail_address[1].lstrip()

                #mail_state
                start_zipcpde = mail_address[2].lstrip().split(' ')
                office_info['mail_state'] =  start_zipcpde[0]

                #mail_zip
                office_info['mail_zip'] =  start_zipcpde[1]
                
                '''
                mail_phone 
                TODO: There is no element found for mail phone in website.
                      add in future if website updated with this info.  
                '''
                office_info['mail_phone'] =  None

            else:
                logging.warning('setting office mail address to None..')
                office_info['mail_address'] = None
                office_info['mail_city'] = None
                office_info['mail_address'] = None
                office_info['mail_zip'] = None
            
            #mail_pobox
            match = re.search("P.O. Box",mail_address[0])
            if match != None:
                logging.info('setting mail pobox info..')
                office_info['mail_pobox'] =  re.sub("P.O. Box", '', mail_address[0]).lstrip()
            else:
                logging.warning('setting mail pobox info to None..')
                office_info['mail_pobox'] = None

            #mail_to
            mail_to_elem = record[4].find('a', href=True)

            if mail_to_elem != None:
                logging.info('setting mail-to info..')
                office_info['mail_to'] = mail_to_elem['href']
            else:
                logging.warning('setting mail-to to None..')
                office_info['mail_to'] = None
            
            self.offices_info.append(office_info)
        
    def retun_office_info_json_format(self):
        '''
            Convert the office info in json formate.

            Returns:
            -----------
            json formatted office info.
        '''
        return json.dumps(self.offices_info, indent=4, sort_keys=True)

if __name__ == '__main__':
    ws_obj = FetchCaltransOffices()
    ws_obj.call_url()
    ws_obj.process_html_page()
    ws_obj.get_records()
    ws_obj.set_office_info()

    with open('output/problem3_output.json', 'w') as file_obj:
        file_obj.write(ws_obj.retun_office_info_json_format())