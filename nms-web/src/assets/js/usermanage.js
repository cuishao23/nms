/**
 * 获取用户管理表格属性
 * @param settingCallback
 * @returns {*[]}
 */
export function getUsermanageTableFields(settingCallback) {
  return [
    {
      prop: 'name',
      label: '用户名'
    },
    {
      prop: 'email',
      label: '邮箱'
    },
    {
      prop: 'phone',
      label: '手机'
    },
    {
      prop: 'officeLocation',
      label: '联系地址'
    },
    {
      prop: 'role',
      label: '角色'
    },
    {
      prop: 'moid',
      label: '权限设置',
      opts: [
        {
          text: '设置',
          click: settingCallback
        }
      ]
    }
  ]
}
