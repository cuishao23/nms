<template>
  <div class="uctrl-terminal-edit">
    <div class="unctrl-terminal-back">
      <span class="back-btn" @click="$router.go(-1)"></span>
      <span class="base-info-title">编辑</span>
      <button class="normal-btn" @click="save()">保存</button>
    </div>
    <div class="edit">
      <nms-pair class="pair">
        <span slot="key">设备名称</span>
        <span slot="value">{{ deviceName }}</span>
      </nms-pair>
      <nms-pair class="pair">
        <span slot="key">设备IP</span>
        <span slot="value">{{ deviceIp }}</span>
      </nms-pair>
      <nms-pair class="pair">
        <span slot="key">设备类型</span>
        <el-select slot="value" v-model="deviceType">
          <el-option v-for="item in typeList" :key="item"
                      :label="item" :value="item"/>
        </el-select>
      </nms-pair>
      <nms-pair class="pair">
        <span slot="key">设备E164</span>
        <input type="text" v-model="deviceE164" slot="value"/>
      </nms-pair>
      <nms-pair class="pair">
        <span slot="key">版本号</span>
        <input type="text" v-model="version" slot="value"/>
      </nms-pair>
    </div>
  </div>
</template>

<script>
    import NmsPair from "../../common/nms-pair";
    import {getOldTerminalTypeList} from "../../../assets/js/platformdevice";
    import qs from 'qs';

    export default {
      components: {NmsPair},
      name: "unctrlterminaledit",
      inject: ['reload'],
      data() {
          return {
            deviceId: '',
            deviceName: '',
            deviceIp: '',
            deviceType: '',
            deviceE164: '',
            online: '',
            version: '',
            typeList: []
          }
      },
      activated: function () {
        this.deviceId = this.$route.params.id
        this.deviceIp = this.$route.params.ip
        this.deviceName = this.$route.params.name
        this.deviceType = this.$route.params.type
        this.deviceE164 = this.$route.params.e164
        this.online = this.$route.params.online
        this.version = this.$route.params.version
        this.typeList = getOldTerminalTypeList()
      },
      methods: {
        save: function () {
          this.axios.post("/nms/device/uncontroledterminal", qs.stringify(
            {
                      type: this.deviceType,
                      e164: this.deviceE164,
                      version: this.version,
                      id: this.deviceId
              }),
              {headers:{'Content-Type':'application/x-www-form-urlencoded'}}
            )
            //成功返回
            .then(response => {
                if(response.data.success == 1) {
                  this.$message({
                    duration: 2000,
                    center: true,
                    message: '保存成功',
                    offset: 400
                  })
                  this.$router.push('/terminaldeviceinfo/home')
                  this.reload()
                }
            })
            //失败返回
            .catch(error => {
                console.log("保存失败："+error);
            })
        }
      }
    }
</script>

<style scoped>
  .normal-btn {
    float: right;
  }

  .edit {
    clear: left;
    position: relative;
    top: 20px;
    display: block;
    text-align: left;
  }

  .pair {
    margin-bottom: 20px;
  }

  .pair span:first-child {
    color: #4e4e4e;
  }
</style>
