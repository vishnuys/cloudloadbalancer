import os
import json
import requests
from uhashring import HashRing
from traceback import format_exc
from mmh3 import hash as mmh
from clouder.settings import NODE_LIST, NODE_ADDRESS, REPLICATION_FACTOR, BASE_DIR


def status_check():
    result = {}
    for i in NODE_LIST:
        try:
            addr = os.path.join(NODE_ADDRESS[i], 'status/')
            r = requests.get(addr)
            if r.ok:
                result[i] = 'Live'
            else:
                result[i] = 'Down'

        except requests.exceptions.RequestException:
            print(i, 'is down')
        except Exception:
            print(format_exc())
            result[i] = 'Down'
    return result

def status_checker():
    status = {}
    with open(BASE_DIR + '/node_status.json','r') as f:
        status = json.load(f)
    return status
        

def reconcile_gossip(recieved_list):
    with open(BASE_DIR + '/gossip_list.json','r') as f:
        GOSSIP_LIST = json.load(f)
        for s in GOSSIP_LIST:
            for r in recieved_list:
                if s['name'] == r['name']:
                    s['HB'] = max(s['HB'], r['HB'])
                    s['last_modified'] = max(s['last_modified'], r['last_modified'])
                    break
    with open(BASE_DIR + '/gossip_list.json','w+') as f:
        json.dump(GOSSIP_LIST,f)



def node_to_contact(name):
    node_status = status_check()
    alive_nodes = [x for x in NODE_LIST if node_status[x] == 'Live']
    hr = HashRing(nodes=alive_nodes, hash_fn=mmh)
    node = hr.get_node(name)
    print(node)
    return node


def handle_result(req, node):
    print("HTTP STATUS CODE = %d" % req.status_code)
    response = ''
    if req.ok:
        res = req.json()
        replication_count = res['count']
        node_result = res['result']
        print('result=%s count=%d' % (node_result, replication_count))
        if replication_count >= REPLICATION_FACTOR:
            result = {
                'status': 'success',
                'node': node,
            }
            if 'vector_clocks' in res and len(res['vector_clocks'].keys()) > 0:
                result['vector_clocks'] = res['vector_clocks']
            response = "SUCCESS"
            return result, response
        elif replication_count == 0:
            response = "BAD_REQUEST"
            return node_result, response
        elif replication_count < REPLICATION_FACTOR:
            result = {
                'status': 'Failed to write in majority nodes',
                'node': node,
            }
            response = "SUCCESS"
            return result, response
    else:
        result = "Something went wrong"
        response = "SERVER_ERROR"
        return result, response
