import argparse
from graphviz import Digraph


def viz_simple(pc,format):
    g=Digraph('net',format=format)
    g.node('input_data')

    for i,layer in enumerate(pc[1:]):
        ltype=layer['type']
        if ltype=='convolutional':
            label="{}{size}x{size}\\n{num}".format(ltype,size=layer.get('size'),num=layer.get('filters'))
        else:
            label=ltype
        g.node("{}".format(i),label=label,color='red')
        if i==0:
            g.edge('input_data',str(i))
        if ltype=='shortcut':
            g.edge(str(int(layer['from'])+i),str(i))
            g.edge(str(i-1),str(i))
        elif ltype=='route':
            bottoms=layer['layers'].split(',')
            for bottom in bottoms:
                bottom=bottom.strip()
                g.edge(str(i+int(bottom)) if '-' in bottom else bottom,str(i))
        else:
            g.edge(str(i-1),str(i))
    return g


def read_option(l,current):
    if '=' in l:
        l=l.split('=')
        current[l[0].strip()]=l[1].strip()
   

def read_cfg(filename):
    file=open(filename,'r')
    options=[]
    current={}
    for i in file.readlines():
        #print(i)
        if(i[0]=='['):
            options.append(current.copy())
            current.clear()
            current['type']=i.split(']')[0][1:]
            pass
        elif(i[0] in ['\0','#',';']):
            pass
        else:
            read_option(i,current)
    file.close()
    return options[1:]


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cfg', help='config file path')
    parser.add_argument('--format', help='graph format. Default: png',default='png')
    parser.add_argument('--show', action='store_true', help='show the graph')
    args = parser.parse_args()
    cfg = read_cfg(args.cfg)
    g = viz_simple(cfg, args.format)
    if not args.show:
        g.render()
    else:
        try:
            g.view()
        except RuntimeError:
            print("Sorry, current platform does not support this option.")
            g.render()










