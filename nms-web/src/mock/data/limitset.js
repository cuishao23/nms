const limits = {
  "t_cpu": 80,
  "t_memory": 80,
  "s_pas": 5000,
  "s_callpair": 40,
  "s_nms": 10000,
  "s_upu": 10000,
  "s_media_resource": 80
};
const servers = {
  "p_servers_limit":
    [{
      "moid": "adebd206-34d2-11e9-a56a-a4bf01306860",
      "name": "172.16.185.180",
      "cpu": 3,
      "memory": 80,
      "disk": 80,
      "port": 60,
      "diskwritespeed": 2,
      "rateofflow": 500
    }],
  "total_count": 1
};

const services = [{
  "moid": "mooooooo-oooo-oooo-oooo-defaultserdo",
  "parent_moid": "mooooooo-oooo-oooo-oooo-topdoooomain",
  "name": "默认服务域",
  "type": "service"
}, {
  "moid": "mooooooo-oooo-oooo-oooo-topdoooomain",
  "parent_moid": -1,
  "name": "kedacom",
  "open": true,
  "type": "kernel"
}];

const machinerooms = [{
  "moid": "98d50ef0-34d2-11e9-ab08-a4bf01306860",
  "parent_moid": "mooooooo-oooo-oooo-oooo-topplatfoorm",
  "name": "核心域默认机房",
  "type": "machine_room"
}, {
  "moid": "mooooooo-oooo-oooo-oooo-defaultmachi",
  "parent_moid": "mooooooo-oooo-oooo-oooo-defaultplatf",
  "name": "默认机房",
  "type": "machine_room"
}];

const platforms = [{
  "moid": "mooooooo-oooo-oooo-oooo-topplatfoorm",
  "parent_moid": "mooooooo-oooo-oooo-oooo-topdoooomain",
  "name": "核心域平台",
  "type": "platform"
}, {
  "moid": "mooooooo-oooo-oooo-oooo-defaultplatf",
  "parent_moid": "mooooooo-oooo-oooo-oooo-defaultserdo",
  "name": "默认平台域",
  "type": "platform"
}];

const stopWarnings = [{
  "moid": "98d50ef0-34d2-11e9-ab08-a4bf01306860",
  "parent_moid": "mooooooo-oooo-oooo-oooo-topplatfoorm",
  "name": "核心域默认机房",
  "type": "machine_room",
  "is_stop_warning": false
}, {
  "moid": "mooooooo-oooo-oooo-oooo-topplatfoorm",
  "parent_moid": "mooooooo-oooo-oooo-oooo-topdoooomain",
  "name": "核心域平台",
  "type": "platform",
  "is_stop_warning": false
}, {
  "moid": "mooooooo-oooo-oooo-oooo-defaultmachi",
  "parent_moid": "mooooooo-oooo-oooo-oooo-defaultplatf",
  "name": "默认机房",
  "type": "machine_room",
  "is_stop_warning": true
}, {
  "moid": "mooooooo-oooo-oooo-oooo-defaultplatf",
  "parent_moid": "mooooooo-oooo-oooo-oooo-defaultserdo",
  "name": "默认平台域",
  "type": "platform",
  "is_stop_warning": false
}, {
  "moid": "44o9v2hl8rn27r41eix1cjat",
  "parent_moid": "mooooooo-oooo-oooo-oooo-defaultserdo",
  "name": "test1",
  "type": "user",
  "is_stop_warning": false
}, {
  "moid": "mooooooo-oooo-oooo-oooo-defaultserdo",
  "parent_moid": "mooooooo-oooo-oooo-oooo-topdoooomain",
  "name": "默认服务域",
  "type": "service",
  "is_stop_warning": false
}, {
  "moid": "mooooooo-oooo-oooo-oooo-topdoooomain",
  "parent_moid": -1,
  "name": "kedacom",
  "open": true,
  "type": "kernel",
  "is_stop_warning": false
}];

export {limits, servers, services, machinerooms, platforms, stopWarnings}
