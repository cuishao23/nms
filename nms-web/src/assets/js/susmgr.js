/**
 * 获取设备表格属性
 * @param detailCallback
 * @returns {*[]}
 */
export function getDevicesTableFields(detailCallback) {
  return [
    {
      prop: 'device_type',
      label: '设备型号'
    },
    {
      prop: 'soft_ver',
      label: '版本号'
    },
    {
      prop: 'file_name',
      label: '升级文件'
    },
    {
      prop: 'oem_mark',
      label: 'oem标志'
    },
    {
      prop: 'release_attribute',
      label: '版本属性',
      flag: 'release_attribute_tip'
    },
    {
      prop: 'release_notes',
      label: '版本描述'
    },
    {
      prop: 'operate',
      label: '操作',
      opts: [
        {
          text: '详情',
          click: detailCallback
        }
      ]
    }
  ]
}

export function getTerminalTableFields() {
  return [
    {
      prop: 'soft_ver',
      label: '版本号'
    },
    {
      prop: 'oem_mark',
      label: 'oem标志'
    },
    {
      prop: 'release_attribute',
      label: '版本属性',
      flag: 'release_attribute_tip'
    },
    {
      prop: 'ver_level',
      label: '版本级别',
      flag: 'version_level_tip'
    },
    {
      prop: 'release_notes',
      label: '版本描述'
    }
  ]
}

export const vAttributes = [
  {
    text: '普通版本',
    value: '1'
  },
  {
    text: '推荐版本',
    value: '2'
  },
  {
    text: '灰度版本',
    value: '4'
  }
]

export const vLevels = [
  {
    text: '建议',
    value: '1'
  },
  {
    text: '强制',
    value: '0'
  },
  {
    text: '普通',
    value: '2'
  }
]
