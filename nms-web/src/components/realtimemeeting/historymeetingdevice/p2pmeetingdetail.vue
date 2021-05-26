<template>
  <div class="tradition-meeting-detail">
    <div class="tradition-meeting-back">
        <span class="back-btn" @click="$router.go(-1)"></span>
        <span class="base-info-title">{{ deviceMeetingName }}的会议室</span>
    </div>
    <el-tabs v-model="p2ptabType">
        <el-tab-pane label="主叫终端" name="meetingcaller">
            <div class="tradition-meeting-fields">
                <nms-key-value label="设备名称" :value="deviceMeetingName"/>
                <nms-key-value label="设备IP" :value="deviceIP"/>
                <nms-key-value label="E164号码" :value="deviceE164"/>
                <nms-key-value label="设备类型" :value="deviceType"/>
                <nms-key-value label="呼叫码率" :value="deviceBitrate"/>
                <nms-key-value label="加密类型" :value="deviceEncryption"/>
                <nms-key-value label="设备型号" :value="deviceTypecode"/>
                <nms-key-value label="软件版本" :value="deviceVersion"/>
                <nms-key-value label="码流篡改" :value="deviceTamper"/>
                <nms-key-value label="静音状态" :value="deviceMute"/>
                <nms-key-value label="哑音状态" :value="deviceDumbness"/>
                <nms-key-value label="NAT地址" :value="deviceNet"/>
                <nms-key-value label="运营商" :value="deviceOperate"/>
            </div>
            <span class="video">第一路主视频</span>
            <span class="videoif">有无视频源 <span class="sourse">{{ videoSource }}</span></span>
            <nms-pager-table v-if="reset" :data="PrivideoData" :fields="PrivideoFields" :pager='false'/>
            <span class="video">第一路辅视频</span>
            <nms-pager-table v-if="reset" :data="AssvideoData" :fields="AssvideoFields" :pager='false'/>
        </el-tab-pane>
        <el-tab-pane label="被叫终端" name="meetingcallee">
            <div class="tradition-meeting-fields">
                <nms-key-value label="设备名称" :value="deviceName"/>
                <nms-key-value label="设备IP" :value="deviceIP"/>
                <nms-key-value label="E164号码" :value="deviceE164"/>
                <nms-key-value label="设备类型" :value="deviceType"/>
                <nms-key-value label="呼叫码率" :value="deviceBitrate"/>
                <nms-key-value label="加密类型" :value="deviceEncryption"/>
                <nms-key-value label="设备型号" :value="deviceTypecode"/>
                <nms-key-value label="软件版本" :value="deviceVersion"/>
                <nms-key-value label="码流篡改" :value="deviceTamper"/>
                <nms-key-value label="静音状态" :value="deviceMute"/>
                <nms-key-value label="哑音状态" :value="deviceDumbness"/>
                <nms-key-value label="NAT地址" :value="deviceNet"/>
                <nms-key-value label="运营商" :value="deviceOperate"/>
            </div>
            <span class="video">第一路主视频</span>
            <span class="videoif">有无视频源 <span class="sourse">{{ videoSource }}</span></span>
            <nms-pager-table v-if="reset"  :data="PrivideoData" :fields="PrivideoFields" :pager='false'/>
            <span class="video">第一路辅视频</span>
            <nms-pager-table v-if="reset" :data="AssvideoData" :fields="AssvideoFields" :pager='false'/>
        </el-tab-pane>
        <el-tab-pane label="数据协作" name="datacollaboration">
            <nms-pager-table :data="CollaborationData" :fields="CollaborationFields" :total-page="p2pmeetingTotalPage" :biao-zhi="cage" v-model="p2pcurPage"/>
            <nms-dialog title="数据协作详情" ref="p2pCollaborationsDlg" >
            <div slot="content" class="overFlow">
                <nms-pager-table :data="p2pCollaborationsData" :fields="p2pCollaborationsField" :pager='false'/>
            </div>
            </nms-dialog>
        </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
    import api from '../../../axios'
    import NmsKeyValue from "../../common/nms-key-value";
    import {getmainVideoFields, getCollaborationFields, getCollaborativeModeFields} from "../../../assets/js/meetingtype";
    import NmsPagerTable from "../../common/nms-pager-table";
    import NmsDialog from "../../common/nms-dialog";
    export default {
        components: {
            NmsKeyValue,
            NmsPagerTable,
            NmsDialog
        },
        name: "p2ptmeetingdetail",
        data() {
            return {
                reset: true,
                p2ptabType: 'meetingcaller',
                deviceMeetingName: '',
                deviceName: '',
                deviceMoid: '',
                PrivideoData: [],
                PrivideoFields: [],
                AssvideoData: [],
                AssvideoFields: [],
                videoSource: '',
                CollaborationData: [],
                CollaborationFields: [],
                p2pCollaborationsData: [],
                p2pCollaborationsField: [],
                detail: '',
                deviceIP: '',
                deviceE164: '',
                deviceType: '',
                deviceBitrate: '',
                deviceEncryption: '',
                deviceTypecode: '',
                deviceVersion: '',
                deviceTamper: '',
                deviceMute: '',
                deviceDumbness: '',
                deviceNet: '',
                deviceOperate: '',
                dcs_moid: '',
                OperateList: ['未知', '中国电信', '中国联通', '中国移动', '有线通', '铁通', '海外', '本地', '其他'],
                cage: 1,
                perPage: 10, // 表格每页显示数量
                p2pmeetingTotalPage: 1, // 点对点
                p2pcurPage: 1, // 点对点
            }
        },
        activated: function () {
            this.MeetingRoom = this.$route.params.meetingRoom
            console.log(this.MeetingRoom)
            // 点对点会议详情界面
            this.PrivideoData = []
            this.AssvideoData = []
            this.PrivideoFields = []
            this.AssvideoFields = []
            this.reset = false
            this.$nextTick(() => {
                this.reset = true
            })
            this.videoSource = '无'
            this.deviceName = ''
            this.deviceIP = ''
            this.deviceE164 = ''
            this.deviceType = ''
            this.deviceEncryption = ''
            this.deviceVersion = ''
            this.deviceTamper = ''
            this.deviceMute = ''
            this.deviceDumbness = ''
            this.deviceNet = ''
            this.deviceOperate = ''
            this.deviceMoid = ''
            this.p2ptabType = 'meetingcaller'
            api.getHistoryP2pMeetingDetail({params: {meetingMoid: this.MeetingRoom}}).then(res => {
                console.log(res)
                if (res.success === 1 && JSON.stringify(res.data) !== '{}') {
                    this.detail = res.data
                    this.deviceMeetingName = this.detail.name
                    this.deviceName = this.detail.name
                    this.deviceIP = this.detail.mt_ip
                    this.deviceE164 = this.detail.e164
                    this.deviceType = this.detail.mt_type_category
                    this.deviceBitrate = this.detail.conf_bitrate
                    if (this.detail.encryption === 'aes') {
                        this.deviceEncryption = 'AES加密'
                    } else if (this.detail.encryption === 'des') {
                        this.deviceEncryption = 'DES加密'
                    } else if (this.detail.encryption === 'sm1') {
                        this.deviceEncryption = 'SM1加密'
                    } else if (this.detail.encryption === 'sm4') {
                        this.deviceEncryption = 'SM4加密'
                    } else if (this.detail.encryption === 'none' || this.detail.encryption === 'NONE') {
                        this.deviceEncryption = '无'
                    }
                    this.deviceTypecode = this.detail.mt_type
                    this.deviceVersion = this.detail.softversion
                    this.deviceTamper = this.detail.tamper
                    this.deviceMute = this.detail.mute
                    this.deviceDumbness = this.detail.dumbness
                    this.deviceNet = this.detail.nat_ip
                    if (this.detail.operate === '') {
                        this.deviceOperate = '无'
                    } else if (this.OperateList[parseInt(this.detail.operate)]) {
                        this.deviceOperate = this.OperateList[parseInt(this.detail.operate)]
                    } else {
                        this.deviceOperate = this.OperateList[0]
                    }
                    // 主辅视频数据
                    this.deviceMoid = this.detail.moid
                    console.log(this.deviceMoid)
                    this.reset = false
                    this.$nextTick(() => {
                        this.reset = true
                    })
                    this.PrivideoFields = getmainVideoFields()
                    this.AssvideoFields = getmainVideoFields()
                    api.getHistoryP2pMeetingVideo({params: {terminalMoid: this.deviceMoid, meetingMoid: this.MeetingRoom}}).then(res => {
                        console.log(res)
                        if (res.success === 1) {
                            if (res.PrivideoData.length > 0) {
                                let priData = []
                                let priUpPower = ''
                                let priDownPower = ''
                                if (res.PrivideoData[0]['send_video_res'] == '' && res.PrivideoData[0]['send_video_framerate'] == '' && res.PrivideoData[0]['send_video_bitrate'] == '') {
                                priUpPower = ''
                                } else {
                                priUpPower = (res.PrivideoData[0]['send_video_res'] + '@' + res.PrivideoData[0]['send_video_framerate'] + ' ' + res.PrivideoData[0]['send_video_bitrate'])
                                }
                                if (res.PrivideoData[0]['recv_video_res'] == '' && res.PrivideoData[0]['recv_video_framerate'] == '' && res.PrivideoData[0]['recv_video_bitrate'] == '') {
                                priDownPower = ''
                                } else {
                                priDownPower = (res.PrivideoData[0]['recv_video_res'] + '@' + res.PrivideoData[0]['recv_video_framerate'] + ' ' + res.PrivideoData[0]['recv_video_bitrate'])
                                }
                                priData.push({'updown': '上行',
                                'video_format': res.PrivideoData[0]['send_video_format'],
                                'video_power': priUpPower,
                                'video_lostrate': res.PrivideoData[0]['send_video_pkts_loserate'],
                                'audio_format': res.PrivideoData[0]['send_audio_format'],
                                'audio_lostrate': res.PrivideoData[0]['send_audio_pkts_loserate'],
                                })
                                priData.push({'updown': '下行',
                                'video_format': res.PrivideoData[0]['recv_video_format'],
                                'video_power': priDownPower,
                                'video_lostrate': res.PrivideoData[0]['recv_video_pkts_loserate'],
                                'audio_format': res.PrivideoData[0]['recv_audio_format'],
                                'audio_lostrate': res.PrivideoData[0]['recv_audio_pkts_loserate'],
                                })
                                this.PrivideoData = priData
                                if (res.PrivideoData[0].send_video_resource_exist === '1') {
                                this.videoSource = '有'
                                } else if (res.PrivideoData[0].send_video_resource_exist === '0') {
                                this.videoSource = '无'
                                } else {
                                this.videoSource = '未知'
                                }
                            } else {
                                this.PrivideoData = []
                                this.videoSource = '无'
                                this.reset = false
                                this.$nextTick(() => {
                                    this.reset = true
                                })
                            }
                            if (res.AssvideoData.length > 0) {
                                let assData = []
                                let assUpPower = ''
                                let assDownPower = ''
                                if (res.AssvideoData[0]['send_video_res'] == '' && res.AssvideoData[0]['send_framerate'] == '' && res.AssvideoData[0]['send_up_bitrate'] == '') {
                                assUpPower = ''
                                } else {
                                assUpPower = (res.AssvideoData[0]['send_video_res'] + '@' + res.AssvideoData[0]['send_framerate'] + ' ' + res.AssvideoData[0]['send_up_bitrate'])
                                }
                                if (res.AssvideoData[0]['recv_video_res'] == '' && res.AssvideoData[0]['recv_framerate'] == '' && res.AssvideoData[0]['recv_down_bitrate'] == '') {
                                assDownPower = ''
                                } else {
                                assDownPower = (res.AssvideoData[0]['recv_video_res'] + '@' + res.AssvideoData[0]['recv_framerate'] + ' ' + res.AssvideoData[0]['recv_down_bitrate'])
                                }
                                assData.push({'updown': '上行',
                                'video_format': res.AssvideoData[0]['send_format'],
                                'video_power': assUpPower,
                                'video_lostrate': res.AssvideoData[0]['send_pkts_loserate'],
                                })
                                assData.push({'updown': '下行',
                                'video_format': res.AssvideoData[0]['recv_format'],
                                'video_power': assDownPower,
                                'video_lostrate': res.AssvideoData[0]['recv_pkts_loserate'],
                                })
                                this.AssvideoData = assData
                            } else {
                                this.AssvideoData = []
                                this.reset = false
                                this.$nextTick(() => {
                                    this.reset = true
                                })
                            }
                        }
                    })
                }
            })
        },
        methods: {
            // 点对点会议数据协作详情
            gotoP2PCollaboration: function(data) {
                console.log('gotoP2PCollaboration')
                console.log(data.dcs_moid)
                this.p2pCollaborationsData = []
                this.dcs_moid = data.dcs_moid
                api.getHistoryDcsModeChangeInfo({params: {dcsMoid: data.dcs_moid}}).then(res => {
                this.p2pCollaborationsField = getCollaborativeModeFields()
                if (res.success === 1) {
                    this.p2pCollaborationsData = res.data
                }
                })
                this.$refs.p2pCollaborationsDlg.open()
            }
        },
        watch: {
            p2pcurPage: function (newpage, oldpage) {
                this.cage = 1
                if (newpage > 0 && newpage <= this.p2pmeetingTotalPage) {
                this.CollaborationFields = getCollaborationFields(this.gotoP2PCollaboration)
                api.getHistoryMeetingDcsInfo({params: {meetingMoid: this.MeetingRoom, page: newpage}}).then(res => {
                    if (res.success === 1) {
                        this.CollaborationData = res.data
                        this.p2pmeetingTotalPage = Math.ceil(res.total_num / this.perPage)
                        this.cage = 2
                    }
                })
                }
            },
            // 监听点对点会议详情
            p2ptabType: function (newTab, oldTab) {
                if (newTab === '' || this.MeetingRoom === '') {
                    return;
                }
                if (newTab === 'meetingcaller') {
                    // 获取主叫终端
                    this.AssvideoData = []
                    this.deviceName = ''
                    this.deviceIP = ''
                    this.deviceE164 = ''
                    this.deviceType = ''
                    this.deviceEncryption = ''
                    this.deviceVersion = ''
                    this.deviceTamper = ''
                    this.deviceMute = ''
                    this.deviceDumbness = ''
                    this.deviceNet = ''
                    this.deviceOperate = ''
                    this.deviceMoid = ''
                    this.PrivideoFields = []
                    this.AssvideoFields = []
                    api.getHistoryP2pMeetingDetail({params: {meetingMoid: this.MeetingRoom}}).then(res => {
                        console.log(res)
                        if (res.success === 1) {
                            this.detail = res.data
                            this.deviceMeetingName = this.detail.name
                            this.deviceName = this.detail.name
                            this.deviceIP = this.detail.mt_ip
                            this.deviceE164 = this.detail.e164
                            this.deviceType = this.detail.mt_type_category
                            this.deviceBitrate = this.detail.conf_bitrate
                            if (this.detail.encryption === 'aes') {
                                this.deviceEncryption = 'AES加密'
                            } else if (this.detail.encryption === 'des') {
                                this.deviceEncryption = 'DES加密'
                            } else if (this.detail.encryption === 'sm1') {
                                this.deviceEncryption = 'SM1加密'
                            } else if (this.detail.encryption === 'sm4') {
                                this.deviceEncryption = 'SM4加密'
                            } else if (this.detail.encryption === 'none' || this.detail.encryption === 'NONE') {
                                this.deviceEncryption = '无'
                            }
                            this.deviceTypecode = this.detail.mt_type
                            this.deviceVersion = this.detail.softversion
                            this.deviceTamper = this.detail.tamper
                            this.deviceMute = this.detail.mute
                            this.deviceDumbness = this.detail.dumbness
                            this.deviceNet = this.detail.nat_ip
                            if (this.detail.operate === '') {
                                this.deviceOperate = '无'
                            } else if (this.OperateList[parseInt(this.detail.operate)]) {
                                this.deviceOperate = this.OperateList[parseInt(this.detail.operate)]
                            } else {
                                this.deviceOperate = this.OperateList[0]
                            }
                            // 主辅视频数据
                            this.deviceMoid = this.detail.moid
                            console.log(this.deviceMoid)
                            this.PrivideoFields = getmainVideoFields()
                            this.AssvideoFields = getmainVideoFields()
                            api.getHistoryP2pMeetingVideo({params: {terminalMoid: this.deviceMoid, meetingMoid: this.MeetingRoom}}).then(res => {
                                console.log(res)
                                if (res.success === 1) {
                                    if (res.PrivideoData.length > 0) {
                                        let priData = []
                                        let priUpPower = ''
                                        let priDownPower = ''
                                        if (res.PrivideoData[0]['send_video_res'] == '' && res.PrivideoData[0]['send_video_framerate'] == '' && res.PrivideoData[0]['send_video_bitrate'] == '') {
                                        priUpPower = ''
                                        } else {
                                        priUpPower = (res.PrivideoData[0]['send_video_res'] + '@' + res.PrivideoData[0]['send_video_framerate'] + ' ' + res.PrivideoData[0]['send_video_bitrate'])
                                        }
                                        if (res.PrivideoData[0]['recv_video_res'] == '' && res.PrivideoData[0]['recv_video_framerate'] == '' && res.PrivideoData[0]['recv_video_bitrate'] == '') {
                                        priDownPower = ''
                                        } else {
                                        priDownPower = (res.PrivideoData[0]['recv_video_res'] + '@' + res.PrivideoData[0]['recv_video_framerate'] + ' ' + res.PrivideoData[0]['recv_video_bitrate'])
                                        }
                                        priData.push({'updown': '上行',
                                        'video_format': res.PrivideoData[0]['send_video_format'],
                                        'video_power': priUpPower,
                                        'video_lostrate': res.PrivideoData[0]['send_video_pkts_loserate'],
                                        'audio_format': res.PrivideoData[0]['send_audio_format'],
                                        'audio_lostrate': res.PrivideoData[0]['send_audio_pkts_loserate'],
                                        })
                                        priData.push({'updown': '下行',
                                        'video_format': res.PrivideoData[0]['recv_video_format'],
                                        'video_power': priDownPower,
                                        'video_lostrate': res.PrivideoData[0]['recv_video_pkts_loserate'],
                                        'audio_format': res.PrivideoData[0]['recv_audio_format'],
                                        'audio_lostrate': res.PrivideoData[0]['recv_audio_pkts_loserate'],
                                        })
                                        this.PrivideoData = priData
                                        if (res.PrivideoData[0].send_video_resource_exist === '1') {
                                        this.videoSource = '有'
                                        } else if (res.PrivideoData[0].send_video_resource_exist === '0') {
                                        this.videoSource = '无'
                                        } else {
                                        this.videoSource = '未知'
                                        }
                                    } else {
                                        this.PrivideoData = []
                                        this.videoSource = '无'
                                    }
                                    if (res.AssvideoData.length > 0) {
                                        let assData = []
                                        let assUpPower = ''
                                        let assDownPower = ''
                                        if (res.AssvideoData[0]['send_video_res'] == '' && res.AssvideoData[0]['send_framerate'] == '' && res.AssvideoData[0]['send_up_bitrate'] == '') {
                                        assUpPower = ''
                                        } else {
                                        assUpPower = (res.AssvideoData[0]['send_video_res'] + '@' + res.AssvideoData[0]['send_framerate'] + ' ' + res.AssvideoData[0]['send_up_bitrate'])
                                        }
                                        if (res.AssvideoData[0]['recv_video_res'] == '' && res.AssvideoData[0]['recv_framerate'] == '' && res.AssvideoData[0]['recv_down_bitrate'] == '') {
                                        assDownPower = ''
                                        } else {
                                        assDownPower = (res.AssvideoData[0]['recv_video_res'] + '@' + res.AssvideoData[0]['recv_framerate'] + ' ' + res.AssvideoData[0]['recv_down_bitrate'])
                                        }
                                        assData.push({'updown': '上行',
                                        'video_format': res.AssvideoData[0]['send_format'],
                                        'video_power': assUpPower,
                                        'video_lostrate': res.AssvideoData[0]['send_pkts_loserate'],
                                        })
                                        assData.push({'updown': '下行',
                                        'video_format': res.AssvideoData[0]['recv_format'],
                                        'video_power': assDownPower,
                                        'video_lostrate': res.AssvideoData[0]['recv_pkts_loserate'],
                                        })
                                        this.AssvideoData = assData
                                    } else {
                                        this.AssvideoData = []
                                    }
                                }
                            })
                        }
                    })
                }
                if (newTab === 'meetingcallee') {
                    // 获取被叫终端
                    this.AssvideoData = []
                    this.deviceName = ''
                    this.deviceIP = ''
                    this.deviceE164 = ''
                    this.deviceType = ''
                    this.deviceEncryption = ''
                    this.deviceVersion = ''
                    this.deviceTamper = ''
                    this.deviceMute = ''
                    this.deviceDumbness = ''
                    this.deviceNet = ''
                    this.deviceOperate = ''
                    this.deviceMoid = ''
                    this.PrivideoFields = []
                    this.AssvideoFields = []
                    api.getHistoryP2pMeetingCallee({params: {meetingMoid: this.MeetingRoom}}).then(res => {
                        console.log(res)
                        if (res.success === 1) {
                            this.detail = res.data
                            this.deviceName = this.detail.name
                            this.deviceIP = this.detail.mt_ip
                            this.deviceE164 = this.detail.e164
                            this.deviceType = this.detail.mt_type_category
                            this.deviceBitrate = this.detail.conf_bitrate
                            if (this.detail.encryption === 'aes') {
                                this.deviceEncryption = 'AES加密'
                            } else if (this.detail.encryption === 'des') {
                                this.deviceEncryption = 'DES加密'
                            } else if (this.detail.encryption === 'sm1') {
                                this.deviceEncryption = 'SM1加密'
                            } else if (this.detail.encryption === 'sm4') {
                                this.deviceEncryption = 'SM4加密'
                            } else if (this.detail.encryption === 'none' || this.detail.encryption === 'NONE') {
                                this.deviceEncryption = '无'
                            }
                            this.deviceTypecode = this.detail.mt_type
                            this.deviceVersion = this.detail.softversion
                            this.deviceTamper = this.detail.tamper
                            this.deviceMute = this.detail.mute
                            this.deviceDumbness = this.detail.dumbness
                            this.deviceNet = this.detail.nat_ip
                            if (this.detail.operate === '') {
                                this.deviceOperate = '无'
                            } else if (this.OperateList[parseInt(this.detail.operate)]) {
                                this.deviceOperate = this.OperateList[parseInt(this.detail.operate)]
                            } else {
                                this.deviceOperate = this.OperateList[0]
                            }
                            this.deviceMoid = this.detail.moid
                            console.log(this.deviceMoid)
                            this.PrivideoFields = getmainVideoFields()
                            this.AssvideoFields = getmainVideoFields()
                            api.getHistoryP2pMeetingVideo({params: {terminalMoid: this.deviceMoid, meetingMoid: this.MeetingRoom}}).then(res => {
                                console.log(res)
                                if (res.success === 1) {
                                    if (res.PrivideoData.length > 0) {
                                        let priData = []
                                        let priUpPower = ''
                                        let priDownPower = ''
                                        if (res.PrivideoData[0]['send_video_res'] == '' && res.PrivideoData[0]['send_video_framerate'] == '' && res.PrivideoData[0]['send_video_bitrate'] == '') {
                                        priUpPower = ''
                                        } else {
                                        priUpPower = (res.PrivideoData[0]['send_video_res'] + '@' + res.PrivideoData[0]['send_video_framerate'] + ' ' + res.PrivideoData[0]['send_video_bitrate'])
                                        }
                                        if (res.PrivideoData[0]['recv_video_res'] == '' && res.PrivideoData[0]['recv_video_framerate'] == '' && res.PrivideoData[0]['recv_video_bitrate'] == '') {
                                        priDownPower = ''
                                        } else {
                                        priDownPower = (res.PrivideoData[0]['recv_video_res'] + '@' + res.PrivideoData[0]['recv_video_framerate'] + ' ' + res.PrivideoData[0]['recv_video_bitrate'])
                                        }
                                        priData.push({'updown': '上行',
                                        'video_format': res.PrivideoData[0]['send_video_format'],
                                        'video_power': priUpPower,
                                        'video_lostrate': res.PrivideoData[0]['send_video_pkts_loserate'],
                                        'audio_format': res.PrivideoData[0]['send_audio_format'],
                                        'audio_lostrate': res.PrivideoData[0]['send_audio_pkts_loserate'],
                                        })
                                        priData.push({'updown': '下行',
                                        'video_format': res.PrivideoData[0]['recv_video_format'],
                                        'video_power': priDownPower,
                                        'video_lostrate': res.PrivideoData[0]['recv_video_pkts_loserate'],
                                        'audio_format': res.PrivideoData[0]['recv_audio_format'],
                                        'audio_lostrate': res.PrivideoData[0]['recv_audio_pkts_loserate'],
                                        })
                                        this.PrivideoData = priData
                                        if (res.PrivideoData[0].send_video_resource_exist === '1') {
                                        this.videoSource = '有'
                                        } else if (res.PrivideoData[0].send_video_resource_exist === '0') {
                                        this.videoSource = '无'
                                        } else {
                                        this.videoSource = '未知'
                                        }
                                    } else {
                                        this.PrivideoData = []
                                        this.videoSource = '无'
                                    }
                                    if (res.AssvideoData.length > 0) {
                                        let assData = []
                                        let assUpPower = ''
                                        let assDownPower = ''
                                        if (res.AssvideoData[0]['send_video_res'] == '' && res.AssvideoData[0]['send_framerate'] == '' && res.AssvideoData[0]['send_up_bitrate'] == '') {
                                        assUpPower = ''
                                        } else {
                                        assUpPower = (res.AssvideoData[0]['send_video_res'] + '@' + res.AssvideoData[0]['send_framerate'] + ' ' + res.AssvideoData[0]['send_up_bitrate'])
                                        }
                                        if (res.AssvideoData[0]['recv_video_res'] == '' && res.AssvideoData[0]['recv_framerate'] == '' && res.AssvideoData[0]['recv_down_bitrate'] == '') {
                                        assDownPower = ''
                                        } else {
                                        assDownPower = (res.AssvideoData[0]['recv_video_res'] + '@' + res.AssvideoData[0]['recv_framerate'] + ' ' + res.AssvideoData[0]['recv_down_bitrate'])
                                        }
                                        assData.push({'updown': '上行',
                                        'video_format': res.AssvideoData[0]['send_format'],
                                        'video_power': assUpPower,
                                        'video_lostrate': res.AssvideoData[0]['send_pkts_loserate'],
                                        })
                                        assData.push({'updown': '下行',
                                        'video_format': res.AssvideoData[0]['recv_format'],
                                        'video_power': assDownPower,
                                        'video_lostrate': res.AssvideoData[0]['recv_pkts_loserate'],
                                        })
                                        this.AssvideoData = assData
                                    } else {
                                        this.AssvideoData = []
                                    }
                                }
                            })
                        }
                    })
                }
                if (newTab === 'datacollaboration') {
                    // 获取数据协作
                    console.log(newTab)
                    this.CollaborationFields = getCollaborationFields(this.gotoP2PCollaboration)
                    api.getHistoryMeetingDcsInfo({params: {meetingMoid: this.MeetingRoom, page: 1}}).then(res => {
                        console.log(res)
                        if (res.success === 1) {
                        this.CollaborationData = res.data
                        this.p2pmeetingTotalPage = Math.ceil(res.total_num / this.perPage)
                        this.cage = 2
                        }
                    })
                }
            },
        },
    }
</script>

<style scoped>
  .overFlow{
    height: 240px;
    overflow:auto;
  }
  .meetingDetailInfo{
    float: left;
  }
  .tradition-meeting-detail {
    display: block;
  }
  .tradition-meeting-back {
    padding-bottom: 45px;
  }
  .normal-btn {
    float: right;
  }
  .meetingtext{
    margin-left: 6px;
  }
  .detail-search {
    margin-top: 15px;
    padding-right: 2px;
    flex-wrap: wrap;
    display: flex;
    text-align: left;
    margin-bottom: 13px;
  }

  .tradition-meeting-fields {
    margin-top: 24px;
    clear: both;
    display: flex;
    flex-wrap: wrap;
    border-bottom: 1px dotted #c0c0c0;
  }

  .tradition-meeting-fields > div {
    width: 25%;
    padding-bottom: 25px;
  }

  .warning, .time-range {
    text-align: left;
  }

  .meetingContent {
    text-align: left;
  }
  .livestreaming{
    text-align: left;
  }

  .tmeeting-search {
    padding-bottom:7px;
  }

  /*搜索图标*/
.search-met {
    width: 30px;
    height: 30px;
    background: url("../../../assets/image/search1.png") 0 0;
    cursor: pointer;
    margin-left: 21px;
    vertical-align: bottom;
    position: relative;
    /*bottom: -2px;*/
 }
 .video{
   float: left;
   font-size: 13px;
   padding-bottom:7px;
   padding-top:20px;
 }
 .videoif{
   float: left;
   font-size: 11px;
   color: #8b8b8b;
   padding-bottom:7px;
   padding-top:20px;
   padding-left:200px;
 }
  .livevalue{
   float: left;
   color: #8b8b8b;
   font-size: 13px;
   padding-bottom:10px;
   padding-top:10px;
 }
  .livetime{
   float: left;
   font-size: 13px;
   color: #8b8b8b;
   padding-bottom:10px;
   padding-top:10px;
   padding-left:100px;
 }
 .sourse{
   padding-left:15px;
   color: #4e4e4e;
 }
 .peripheral{
   float: left;
 }
 .cascading{
   float: left;
 }
  .lineDiv {
    margin-top: 28px;
  }

 .setName {
    font-size: 12px;
    color: #4e4e4e;
    display: inline-block;
    text-align: left;
    width: 110px;
  }

  .setValue {
    font-size: 12px;
    color: #4e4e4e;
    display: inline-block;
    text-align: left;
    width: 110px;
  }

  .setValue input{
    width: 59px;
  }
</style>
