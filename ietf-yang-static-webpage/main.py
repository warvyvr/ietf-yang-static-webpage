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
    with open(json_file) as data_file:
        data = json.load(data_file)

        s = name_of_area(data)

        dashboard_data = dashboard(data)
        utc_time = utc_time_from(data['meta']['finish_time'])

        data.pop('meta',None)

        d = render("./template/index.html.template",{"dashboard":dashboard_data, "data":data, "short_name":s, "t":utc_time })
        html_file = open(os.path.join(path,'index.html'),'w')
        html_file.write(d)

        for area in data:
            filename = os.path.join(path, '%s.html' %(s[area]))
            d = render("./template/area.html.template",{"area_name":area, "data":data, "short_name":s, "t":utc_time})
            html_file = open(filename,'w')
            html_file.write(d)
            print "write file to %s" %(filename)


if __name__ == '__main__':
    if (len(sys.argv) > 2):
        run(sys.argv[1], sys.argv[2])
    else:
        run(sys.argv[1],"./")
