const platformDomainTree = [{
  moid: 'mooooooo-oooo-oooo-oooo-topdoooomain',
  name: 'kedacom',
  type: 'kernel',
  children: [
    {
      moid: 'mooooooo-oooo-oooo-oooo-topplatfoorm',
      name: '核心平台域',
      type: 'platform',
      children: [{
        moid: 'mooooooo-oooo-oooo-oooo-toppmachi',
        name: '核心域机房',
        type: 'machine_room',
        parent_moid: 'mooooooo-oooo-oooo-oooo-topplatfoorm'
      }]
    },
    {
      moid: 'mooooooo-oooo-oooo-oooo-defaultser',
      name: '默认服务域',
      type: 'service',
      children: [{
        moid: 'mooooooo-oooo-oooo-oooo-defaultplat',
        name: '默认平台域',
        type: 'platform',
        children: [
          {
            moid: 'mooooooo-oooo-oooo-oooo-defaultmachi',
            name: '默认机房',
            type: 'machine_room',
          },
          {
            moid: 'mooooooo-oooo-oooo-oooo-gameroom',
            name: 'GameRoooooooooooom',
            type: 'machine_room',
          }
        ]
      }]
    }]
}]

export { platformDomainTree }
