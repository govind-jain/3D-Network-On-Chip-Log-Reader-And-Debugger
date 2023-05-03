import collections

def read_switch_config(filepath):
  # [packet_id][clock_cycle][layer_id][node_id][dir_id][buffer_type][position_idx]
  node_log = []
  max_clock = 0
  layer_arr = []
  switch_arr = []
  
  with open(filepath) as fp:
    line = fp.readline().strip()
    cnt = 1
    while line:
        line_arr = line.split(' ')
        # Conversion to data structure
        packet_id = line_arr[6].split('=')[1]
        clock_cycle = line_arr[0].split('=')[1]
        layer_id = line_arr[1].split('=')[1]
        node_id = line_arr[2].split('=')[1]
        dir_id = line_arr[3].split('=')[1]
        buffer_type = line_arr[4].split('=')[1]
        position_idx = line_arr[5].split('=')[1]

        node_log.append({
            "packet_id" : packet_id,
            "clock_cycle" : clock_cycle,
            "layer_id" : layer_id,
            "node_id" : node_id,
            "dir_id" : dir_id,
            "buffer_type" : buffer_type,
            "position_idx" : position_idx
          })

        # Max clock cycle
        if(int(clock_cycle) > int(max_clock)):
          max_clock = int(clock_cycle)

        # Populate layer_arr
        if(layer_id not in layer_arr):
          layer_arr.append(layer_id)       

        # Populate switch_arr
        if(node_id not in switch_arr):
          switch_arr.append(node_id)

        line = fp.readline().strip() 
        cnt +=1

  layer_arr.sort()
  switch_arr.sort()

  # print(layer_arr)
  # print(switch_arr)
  # print(max_clock)
  # print(node_log)
  return node_log, max_clock, layer_arr, switch_arr
  
# read_switch_config('../input_files/switch_logger.txt')