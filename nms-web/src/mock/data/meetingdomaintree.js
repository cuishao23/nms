const meetingDomainTree = [{
  moid: 'mooooooo-oooo-oooo-oooo-topdoooomain',
  name: 'kedacom',
  type: 'kernel',
  children: [
    {
      moid: 'mooooooo-oooo-oooo-oooo-defaultserdo',
      name: '默认服务域',
      type: 'service',
      children: [{
        moid: '44o9v2hl8rn27r41eix1cjat',
        name: 'test1',
        type: 'user',
        parent_moid: 'mooooooo-oooo-oooo-oooo-defaultserdo'
      }]
    }]
}]

export { meetingDomainTree }
