
<template>
  <div class="device-all">
    <div class="deciceitem">
      <span class="back-btn" @click="back_page()"></span>
      <span class="base-info-title">{{ deviceName }}设备详情</span>
    </div>
    <div>
        <!-- <nms-pages-table :data="physicals" :fields="devicenameFields" :total-page="physicalTotalPage" v-model="curPagePhysical" /> -->
        <nms-pages-table v-if="deviceReset" :data="physicals" :fields="devicenameFields" :total-page="physicalTotalPage" v-model="curPagePhysical" />
    </div>

  </div>
</template>

<script>
import ResInfo from "../../common/res-info";
import api from "../../../axios";
import {getTimePeriod} from "assets/js/common";
import NmsPagesTable from "../../common/nms-pages-table";
import {getPhysicalDeviceListFields} from "../../../assets/js/platformdevice";
import NmsBigDialog from "../../../components/common/nms-big-dialog";
import NmsTransfer from "../../../components/common/nms-transfer";
import { getDeviceNameDetail } from '../../../axios/api';


export default {
      components: {
        NmsPagesTable,
        ResInfo,
        NmsBigDialog,
        NmsTransfer
    },
    name: "device-detail",
    data() {
        return {
            deviceReset: true,
            physicals: [],
            physicalFields: [],
            deviceName: '',
            deviceFrame: '',
            deviceMoid: '',
            // tab标签类型
            tabType: "",
            // 表格每页显示数量
            perPage: 10,
            // 物理服务器
            physicalTotalPage: 1, // 总页数
            devicenameFields: [], // 物理服务器表格字段列表

            sMachineRoomMoid: '',
            top_main: "",
            slistFlash: false,
            curPagePhysical: 1,
            filest: []
        };
    },
    async activated() {
        this.deviceFrame = this.$route.params.frame
        this.deviceMoid = this.$route.params.moid
        this.deviceName = this.$route.params.name
        this.devicenameFields = []
        this.physicals = []
        this.deviceReset = false
        this.$nextTick(() => {
          this.deviceReset = true
        })
        api.getDeviceNameDetail({params: {parentMoid: this.$route.params.moid, frameMoid: this.$route.params.frame}}).then((res) => {
          console.log(res)
          this.physicals = res.data

        })
        this.devicenameFields = getPhysicalDeviceListFields(this.gotoPhysicalDetail)
    },
    methods: {
      back_page: function() {
        this.$router.push({ name: 'platformdeviceinfohome', params: {tabTypeProp:'meetingservice'}})
      },
      gotoPhysicalDetail: function(data) {
            console.log("data112 "+JSON.stringify(data))
            console.log("name: " + data.name + " moid: " + data.moid + " type: " + data.type);
            this.$router.push({
                name: "physicaldetail",
                params: {moid: data.moid, page:'device'}
            });
        },
    }

}
</script>>

<style scoped>
.device-all {
  width: 100%;
  height: 100%;
}
.deciceitem {
    margin-bottom: 20px;
    float: left;
}
.no-info-tip {
    text-align: left;
}

.device-search {
    display: flex;
    padding-bottom: 10px;
}

.device-search ul {
    display: flex;
}
.device-search li {
    padding-right: 15px;
}
.device-search ul .device-info-button {
    padding-left: 0px;
}
.device-search li .search {
  margin-left: 10px;
}

#frameToolbar {
    height: 45px;
}

#btnDelFrame {
    float: right;
    margin-top: 20px;
    margin-right: 5px;
}

input.timeInputdisable[type="button"],
button.timeInputdisable {
    color: #fff;
    cursor: default;
    background-color: #e5e5e5;
    border-width: 0px;
    padding: 6px 22px 5px 22px;
    background-image: none;
}

#btnUpdateFrame {
    float: right;
    margin-top: 20px;
    margin-right: 5px;
}

#btnAddFrame {
    float: right;
    margin-top: 20px;
    margin-right: 5px;
}
.res-chart {
  width: 750px;
  height: 650px;
}
.filter-text {
  margin-left: 14px;
}
/* .log-content {
  float: left;
} */
</style>


