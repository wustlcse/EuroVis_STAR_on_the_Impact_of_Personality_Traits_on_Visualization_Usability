import pprint,collections,json
filepath = 'paper_table.txt'
paper_list=[]
categories = ['TRAITS','VIS','TASK','MEASURES']
current_category='none'
with open(filepath,'r') as paper_table, open('paper_list.json', 'w') as output_json:
    for line in paper_table:
        stripped_line = line.strip()
        if '~\cite' in stripped_line:
            current_paper = collections.defaultdict(dict) #for dynamically building dictionaries
            current_paper['reference']=stripped_line[:stripped_line.find('~')]
            paper_list.append(current_paper)
        next_category = next((category for category in categories if category in stripped_line),'none') # an elegant way to retrieve the category to be used
        if next_category != 'none':
            current_category = next_category # switch target sub-dictionary based on whether the last category we read
        else:
            if '& &' in stripped_line:
                value_index = max(stripped_line.find('no'),stripped_line.find('yes')) # get the index of either no or yes; use max() since only one exists and the other returns -1
                current_paper[current_category][stripped_line[stripped_line.find('%')+2:].strip()] = stripped_line[value_index:stripped_line.find('%')][:4].strip() #dynamically construct the nested dict
    json.dump(paper_list,output_json)






