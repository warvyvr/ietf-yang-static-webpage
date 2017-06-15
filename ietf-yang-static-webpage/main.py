import os
import sys
import jinja2
import json
import re


def render(template_path, context):
    path, filename = os.path.split(template_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)


def dashboard(data):
    d = {}
    for area in data:
        if area == 'meta':
            continue
        for wg in data[area]:
            num_in_wg = 0
            for artifact in data[area][wg]:
                num_in_wg += len(artifact['models'])
            #num_in_area += num_in_wg
            if (d.has_key(area)):
                d[area][wg] = num_in_wg
            else:
                d[area] = {wg:num_in_wg}

        #d[area]['num'] = num_in_area

    return d

def name_of_area(data):
    names = {}
    for area in data:
        if area == 'meta':
            continue
        names[area] = re.search('\((.*)\)',area).group(1)
    return names

def utc_time_from(local_time):
    print local_time
    import time
    from datetime import datetime
    d = datetime.strptime(local_time,"%Y-%m-%d %H:%M:%S.%f")
    t = time.mktime(d.timetuple())
    utc_time_st = datetime.utcfromtimestamp(t)
    #utc_time_str = utc_time_st.strftime("%Y-%m-%d %H:%M:%S %z")
    utc_time_str = utc_time_st.isoformat()

    return utc_time_str


def run(json_file, path):
    output_files = []
    with open(json_file) as data_file:
        data = json.load(data_file)

        s = name_of_area(data)

        dashboard_data = dashboard(data)
        utc_time = utc_time_from(data['meta']['finish_time'])

        bad_requests = []
        for item in ['wg','area','artifact']:
            bad_requests += data['meta']['bad_requests'][item]

        data.pop('meta',None)

        context = { "dashboard":dashboard_data,
                    "data":data,
                    "short_name":s,
                    "t":utc_time,
                    "bad_requests":bad_requests 
                }

        d = render("./template/index.html.template",context)
        index_file = os.path.join(path,'index.html')
        html_file = open(index_file,'w')
        html_file.write(d)
        output_files.append(index_file)

        for area in data:
            filename = os.path.join(path, '%s.html' %(s[area]))
            d = render("./template/area.html.template",{"area_name":area, "data":data, "short_name":s, "t":utc_time})
            html_file = open(filename,'w')
            html_file.write(d)
            output_files.append(filename)
            print "write file to %s" %(filename)

    return output_files

def generate_search_info(input_files, folder):
    from operator import itemgetter
    l = []
    for file in input_files:
        if file.find("index.html") != -1:
            from bs4 import BeautifulSoup
            bs = BeautifulSoup(open(file),"html.parser")
            for item in bs.find_all("td","wg"):
                l.append({"location":"/index.html#{}".format(item.string),"text":item.string,"title":"{}".format(item.string)})
        else:
            from bs4 import BeautifulSoup
            bs = BeautifulSoup(open(file), "html.parser")
            for item in bs.find_all("tr","doc"):
                location = "/%s#%s" %(os.path.split(file)[1], item.find("td","doc_name").string)
                content = " ".join([i.string for i in item.find_all("td")[1:-1]])
                content += " " + item.find("td","doc_name").a['href']
                title = item.find("td","doc_name").string

                l.append({'location':location, 'text':content, 'title':title})

    with open(os.path.join(folder,"search_index.json"),"w") as s_file:
        import json
        s_file.write(json.dumps({"docs":l},indent=4))
        



if __name__ == '__main__':
    output_files = None
    output_folder = "./"

    if (len(sys.argv) > 2):
        output_folder = sys.argv[2]

    output_files = run(sys.argv[1], output_folder)

    generate_search_info(output_files, output_folder)

