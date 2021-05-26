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
            <nms-pager-table :data="PrivideoData" :fields="PrivideoFields" :pager='false'/>
            <span class="video">第一路辅视频</span>
            <nms-pager-table :data="AssvideoData" :fields="AssvideoFields" :pager='false'/>
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
            <nms-pager-table v-if="reset" :data="PrivideoData" :fields="PrivideoFields" :pager='false'/>
            <span class="video">第一路辅视频</span>
            <nms-pager-table v-if="reset" :data="AssvideoData" :fields="AssvideoFields" :pager='false'/>
            </el-tab-pane>
            <el-tab-pane label="数据协作" name="datacollaboration">
            <div class="coopMassage">
                <div class="notifyIteam">
                <span class="iteamKey">数据协作</span>
                <span class="iteamValue">{{ CoopOn }}</span>
                </div>
                <div class="notifyIteam">
                <span class="iteamKey">协作模式</span>
                <span class="iteamValue">{{ CoopType }}</span>
                </div>
            </div>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
    import api from '../../../axios'
    import NmsKeyValue from "../../common/nms-key-value";
    import {getmainVideoFields, getCollaborationFields, getCollaborativeModeFields} from "../../../assets/js/meetingtype";
    import NmsPagerTable from "../../common/nms-pager-table";

    export default {
        components: {
            NmsKeyValue,
            NmsPagerTable,
        },
        name: "realtimep2pmeeting",
        data() {
            return {
                p2ptabType: 'meetingcaller',
                reset: true,
                device_name: '',
                MeetingRoom: '',
                CalleeRoom: '',
                MultiType: '',
                MeetingDetailInfos: [],
                MeetingDetailInfoFields: [],
                CoopOn: '关闭',
                CoopType: '无',
                detail: null,
                deviceMeetingName: '',
                deviceName: '',
                deviceMoid: '',
                OperateList: ['未知', '中国电信', '中国联通', '中国移动', '有线通', '铁通', '海外', '本地', '其他'],
                // 会议各方面数据
                PrivideoData: [],
                PrivideoFields: [],
                AssvideoData: [],
                AssvideoFields: [],
                videoSource: '',
                p2pCollaborationsData: [],
                p2pCollaborationsField: [],
                // 点对点会议详细数据
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
                cage: 1,
                perPage: 10, // 表格每页显示数量
                p2pmeetingTotalPage: 1, // 点对点
                p2pcurPage: 1, // 点对点
            }
        },
        // 初始相关数据获取显示
        activated: function () {
            this.MeetingRoom = this.$route.params.meetingE164
            this.CalleeRoom = this.$route.params.calleeE164
            // 点对点会议详情界面
            this.AssvideoData = []
            this.PrivideoData = []
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
            this.reset = false
            this.$nextTick(() => {
                this.reset = true
            })
            this.p2ptabType = 'meetingcaller'
            api.getRealTimeTerminalDetail({params: {terminalE164: this.MeetingRoom}}).then(res => {
                console.log(res)
                if (res.success == 1) {
                    this.detail = res.data
                    this.deviceMeetingName = this.detail.name
                    this.deviceName = this.detail.name
                    this.deviceIP = this.detail.mt_ip
                    this.deviceE164 = this.detail.conf_e164
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
                    this.deviceVersion = this.detail.version
                    this.deviceTamper = this.detail.tamper
                    this.deviceMute = this.detail.mute
                    this.deviceDumbness = this.detail.dumbness
                    this.deviceNet = this.detail.nat_ip
                    if (this.detail.operator == '') {
                        this.deviceOperate = '无'
                    } else if (this.OperateList[parseInt(this.detail.operator)]) {
                        this.deviceOperate = this.OperateList[parseInt(this.detail.operator)]
                    } else {
                        this.deviceOperate = this.OperateList[0]
                    }
                    this.deviceMoid = this.detail.moid
                    console.log(this.deviceE164)
                    this.PrivideoFields = getmainVideoFields()
                    this.AssvideoFields = getmainVideoFields()
                    api.getRealTimeTerminalVideoDetail({params: {terminalE164: this.deviceE164}}).then(res => {
                        console.log(res)
                        if (res.success == 1) {
                            if (res.PrivideoData.length > 0) {
                            let priData = []
                            let priUpPower = ''
                            let priDownPower = ''
                            if ((res.PrivideoData[0]['send_video_res'] == '' && res.PrivideoData[0]['send_video_framerate'] == '' && res.PrivideoData[0]['send_video_bitrate'] == '') || (res.PrivideoData[0]['send_video_res'] == undefined && res.PrivideoData[0]['send_video_framerate'] == undefined && res.PrivideoData[0]['send_video_bitrate'] == undefined)) {
                            priUpPower = ''
                            } else {
                            priUpPower = (res.PrivideoData[0]['send_video_res'] + '@' + res.PrivideoData[0]['send_video_framerate'] + ' ' + res.PrivideoData[0]['send_video_bitrate'])
                            }
                            if ((res.PrivideoData[0]['recv_video_res'] == '' && res.PrivideoData[0]['recv_video_framerate'] == '' && res.PrivideoData[0]['recv_video_bitrate'] == '') || (res.PrivideoData[0]['recv_video_res'] == undefined && res.PrivideoData[0]['recv_video_framerate'] == undefined && res.PrivideoData[0]['recv_video_bitrate'] == undefined)) {
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
                            if (res.PrivideoData[0]['send_video_resource_exist'] == '1') {
                                this.videoSource = '有'
                            } else if (res.PrivideoData[0]['send_video_resource_exist'] == '0') {
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
                            if ((res.AssvideoData[0]['send_video_res'] == '' && res.AssvideoData[0]['send_framerate'] == '' && res.AssvideoData[0]['send_bitrate'] == '') || (res.AssvideoData[0]['send_video_res'] == undefined && res.AssvideoData[0]['send_framerate'] == undefined && res.AssvideoData[0]['send_bitrate'] == undefined)) {
                            assUpPower = ''
                            } else {
                            assUpPower = (res.AssvideoData[0]['send_video_res'] + '@' + res.AssvideoData[0]['send_framerate'] + ' ' + res.AssvideoData[0]['send_bitrate'])
                            }
                            if ((res.AssvideoData[0]['recv_video_res'] == '' && res.AssvideoData[0]['recv_framerate'] == '' && res.AssvideoData[0]['recv_bitrate'] == '') || (res.AssvideoData[0]['recv_video_res'] == undefined && res.AssvideoData[0]['recv_framerate'] == undefined && res.AssvideoData[0]['recv_bitrate'] == undefined)) {
                            assDownPower = ''
                            } else {
                            assDownPower = (res.AssvideoData[0]['recv_video_res'] + '@' + res.AssvideoData[0]['recv_framerate'] + ' ' + res.AssvideoData[0]['recv_bitrate'])
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
                api.getRealTimeDcsModeChangeInfo({params: {dcsMoid: data.dcs_moid}}).then(res => {
                    this.p2pCollaborationsField = getCollaborativeModeFields()
                    if (res.success == 1) {
                        this.p2pCollaborationsData = res.data
                        this.meetingTotalPage = Math.ceil(this.p2pCollaborationsData.length / this.perPage)
                    }
                })
                this.$refs.p2pCollaborationsDlg.open()
            }
        },
        watch: {
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
                    api.getRealTimeTerminalDetail({params: {terminalE164: this.MeetingRoom}}).then(res => {
                        console.log(res)
                        if (res.success == 1) {
                            this.detail = res.data
                            this.deviceMeetingName = this.detail.name
                            this.deviceName = this.detail.name
                            this.deviceIP = this.detail.mt_ip
                            this.deviceE164 = this.detail.conf_e164
                            this.deviceType = this.detail.mt_type_category
                            this.deviceBitrate = this.detail.conf_bitrate
                            this.deviceEncryption = this.detail.encryption
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
                            this.deviceVersion = this.detail.version
                            this.deviceTamper = this.detail.tamper
                            this.deviceMute = this.detail.mute
                            this.deviceDumbness = this.detail.dumbness
                            this.deviceNet = this.detail.nat_ip
                            if (this.detail.operator == '') {
                                this.deviceOperate = '无'
                            } else if (this.OperateList[parseInt(this.detail.operator)]) {
                                this.deviceOperate = this.OperateList[parseInt(this.detail.operator)]
                            } else {
                                this.deviceOperate = this.OperateList[0]
                            }
                            this.deviceMoid = this.detail.moid
                            console.log(this.deviceE164)
                            this.PrivideoFields = getmainVideoFields()
                            this.AssvideoFields = getmainVideoFields()
                            api.getRealTimeTerminalVideoDetail({params: {terminalE164: this.deviceE164}}).then(res => {
                                console.log(res)
                                if (res.success == 1) {
                                    if (res.PrivideoData.length > 0) {
                                        let priData = []
                                        let priUpPower = ''
                                        let priDownPower = ''
                                        if ((res.PrivideoData[0]['send_video_res'] == '' && res.PrivideoData[0]['send_video_framerate'] == '' && res.PrivideoData[0]['send_video_bitrate'] == '') || (res.PrivideoData[0]['send_video_res'] == undefined && res.PrivideoData[0]['send_video_framerate'] == undefined && res.PrivideoData[0]['send_video_bitrate'] == undefined)) {
                                        priUpPower = ''
                                        } else {
                                        priUpPower = (res.PrivideoData[0]['send_video_res'] + '@' + res.PrivideoData[0]['send_video_framerate'] + ' ' + res.PrivideoData[0]['send_video_bitrate'])
                                        }
                                        if ((res.PrivideoData[0]['recv_video_res'] == '' && res.PrivideoData[0]['recv_video_framerate'] == '' && res.PrivideoData[0]['recv_video_bitrate'] == '') || (res.PrivideoData[0]['recv_video_res'] == undefined && res.PrivideoData[0]['recv_video_framerate'] == undefined && res.PrivideoData[0]['recv_video_bitrate'] == undefined)) {
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
                                        if (res.PrivideoData[0]['send_video_resource_exist'] == '1') {
                                            this.videoSource = '有'
                                        } else if (res.PrivideoData[0]['send_video_resource_exist'] == '0') {
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
                                        if ((res.AssvideoData[0]['send_video_res'] == '' && res.AssvideoData[0]['send_framerate'] == '' && res.AssvideoData[0]['send_bitrate'] == '') || (res.AssvideoData[0]['send_video_res'] == undefined && res.AssvideoData[0]['send_framerate'] == undefined && res.AssvideoData[0]['send_bitrate'] == undefined)) {
                                        assUpPower = ''
                                        } else {
                                        assUpPower = (res.AssvideoData[0]['send_video_res'] + '@' + res.AssvideoData[0]['send_framerate'] + ' ' + res.AssvideoData[0]['send_bitrate'])
                                        }
                                        if ((res.AssvideoData[0]['recv_video_res'] == '' && res.AssvideoData[0]['recv_framerate'] == '' && res.AssvideoData[0]['recv_bitrate'] == '') || (res.AssvideoData[0]['recv_video_res'] == undefined && res.AssvideoData[0]['recv_framerate'] == undefined && res.AssvideoData[0]['recv_bitrate'] == undefined)) {
                                        assDownPower = ''
                                        } else {
                                        assDownPower = (res.AssvideoData[0]['recv_video_res'] + '@' + res.AssvideoData[0]['recv_framerate'] + ' ' + res.AssvideoData[0]['recv_bitrate'])
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
                    api.getRealTimeTerminalDetail({params: {terminalE164: this.CalleeRoom}}).then(res => {
                        console.log(res)
                        if (res.success == 1) {
                            this.detail = res.data
                            this.deviceMeetingName = this.detail.name
                            this.deviceName = this.detail.name
                            this.deviceIP = this.detail.mt_ip
                            this.deviceE164 = this.detail.conf_e164
                            this.deviceType = this.detail.mt_type_category
                            this.deviceBitrate = this.detail.conf_bitrate
                            this.deviceEncryption = this.detail.encryption
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
                            this.deviceVersion = this.detail.version
                            this.deviceTamper = this.detail.tamper
                            this.deviceMute = this.detail.mute
                            this.deviceDumbness = this.detail.dumbness
                            this.deviceNet = this.detail.nat_ip
                            if (this.detail.operator == '') {
                                this.deviceOperate = '无'
                            } else if (this.OperateList[parseInt(this.detail.operator)]) {
                                this.deviceOperate = this.OperateList[parseInt(this.detail.operator)]
                            } else {
                                this.deviceOperate = this.OperateList[0]
                            }
                            this.deviceMoid = this.detail.moid
                            console.log(this.deviceE164)
                            this.PrivideoFields = getmainVideoFields()
                            this.AssvideoFields = getmainVideoFields()
                            api.getRealTimeTerminalVideoDetail({params: {terminalE164: this.deviceE164}}).then(res => {
                                console.log(res)
                                if (res.success == 1) {
                                    if (res.PrivideoData.length > 0) {
                                        let priData = []
                                        let priUpPower = ''
                                        let priDownPower = ''
                                        if ((res.PrivideoData[0]['send_video_res'] == '' && res.PrivideoData[0]['send_video_framerate'] == '' && res.PrivideoData[0]['send_video_bitrate'] == '') || (res.PrivideoData[0]['send_video_res'] == undefined && res.PrivideoData[0]['send_video_framerate'] == undefined && res.PrivideoData[0]['send_video_bitrate'] == undefined)) {
                                        priUpPower = ''
                                        } else {
                                        priUpPower = (res.PrivideoData[0]['send_video_res'] + '@' + res.PrivideoData[0]['send_video_framerate'] + ' ' + res.PrivideoData[0]['send_video_bitrate'])
                                        }
                                        if ((res.PrivideoData[0]['recv_video_res'] == '' && res.PrivideoData[0]['recv_video_framerate'] == '' && res.PrivideoData[0]['recv_video_bitrate'] == '') || (res.PrivideoData[0]['recv_video_res'] == undefined && res.PrivideoData[0]['recv_video_framerate'] == undefined && res.PrivideoData[0]['recv_video_bitrate'] == undefined)) {
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
                                        if (res.PrivideoData[0]['send_video_resource_exist'] == '1') {
                                            this.videoSource = '有'
                                        } else if (res.PrivideoData[0]['send_video_resource_exist'] == '0') {
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
                                        if ((res.AssvideoData[0]['send_video_res'] == '' && res.AssvideoData[0]['send_framerate'] == '' && res.AssvideoData[0]['send_bitrate'] == '') || (res.AssvideoData[0]['send_video_res'] == undefined && res.AssvideoData[0]['send_framerate'] == undefined && res.AssvideoData[0]['send_bitrate'] == undefined)) {
                                        assUpPower = ''
                                        } else {
                                        assUpPower = (res.AssvideoData[0]['send_video_res'] + '@' + res.AssvideoData[0]['send_framerate'] + ' ' + res.AssvideoData[0]['send_bitrate'])
                                        }
                                        if ((res.AssvideoData[0]['recv_video_res'] == '' && res.AssvideoData[0]['recv_framerate'] == '' && res.AssvideoData[0]['recv_bitrate'] == '') || (res.AssvideoData[0]['recv_video_res'] == undefined && res.AssvideoData[0]['recv_framerate'] == undefined && res.AssvideoData[0]['recv_bitrate'] == undefined)) {
                                        assDownPower = ''
                                        } else {
                                        assDownPower = (res.AssvideoData[0]['recv_video_res'] + '@' + res.AssvideoData[0]['recv_framerate'] + ' ' + res.AssvideoData[0]['recv_bitrate'])
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
                }
                if (newTab === 'datacollaboration') {
                    // 获取数据协作
                    console.log(newTab)
                    this.CollaborationFields = getCollaborationFields(this.gotoP2PCollaboration)
                    api.getRealTimeDcsInfo({params: {meetingE164: this.MeetingRoom, page: 1, coopState: this.CoopState}}).then(res => {
                        console.log(res)
                        if (res.success == 1) {
                            if (res.data['dcsinfo'].length > 0) {
                                if (res.data['dcsinfo']['dcs_mode'] == '0') {
                                    this.CoopType = '自由模式'
                                } else if (res.data['dcsinfo']['dcs_mode'] == '1') {
                                    this.CoopType = '管理方模式'
                                } else {
                                    this.CoopType = '无'
                                }
                            } else {
                                this.CoopType = '无'
                            }
                            if (res.data['user'].length > 0) {
                                this.CoopOn = '开启'
                            } else {
                                this.CoopOn = '关闭'
                            }
                        }
                    })
                }
            }
        }
    }
</script>

<style scoped>
  .coopType{
    margin-top: 5px;
    font-size: 13px;
    margin-left: 30px;
  }
  .LiveType{
    font-size: 13px;
    width: 33%;
    text-align: left;
    float: left;
  }
  .overFlow{
    height: 240px;
    overflow:auto;
  }
  .MeetingDetail{
    margin-right: 10px;
  }
  .meetingDetailInfo{
    float: left;
    font-size: 15px;
    margin-bottom: 10px;
    text-align: left;
    width: 100%;
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
  .detail-search {
    margin-top: 15px;
    padding-right: 2px;
    flex-wrap: wrap;
    display: flex;
    text-align: left;
    margin-bottom: 13px;
  }
  .coopMassage {
    height: 62px;
    width: 100%;
    margin-top: 14px;
    margin-bottom: 42px;
    font-size: 14px;
    color: #8b8b8b;
  }
  .notifyIteam {
    margin-top: 17px;
    width: 341px;
    float: left;
  }
  .iteamKey {
    margin-left: 34px;
    width: 80px;
    float: left;
  }
  .iteamValue {
    float: left;
    color: #4e4e4e;
    width: 212px;
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
  .in_line{
    display: inline;
    float: left;
  }
</style>
