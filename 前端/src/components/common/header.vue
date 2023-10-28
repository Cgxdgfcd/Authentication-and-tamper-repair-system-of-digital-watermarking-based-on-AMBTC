<!-- 顶部信息栏 -->
<template>
  <div id="top_head">
    <header id="topbar">
      <el-row>
        <el-col :span="8" class="topbar-left">
          <i class="el-icon-s-promotion"></i>
<!--          <img
            src="../../assets/img/watermark1.png"
            class="image"
          /> -->
          <span class="title" @click="index()">基于AMBTC的数字水印的图像认证与修复系统</span>
        </el-col>
        <el-col :span="16" class="topbar-right">
          <i :class="[flag ? 'el-icon-s-unfold' : 'el-icon-s-fold']" @click="toggle()"></i>
        </el-col>
      </el-row>
    </header>
  </div>

</template>

<script>
import store from '@/vuex/store'
import {mapState,mapMutations} from 'vuex'
export default {
  data() {
    return {
		  login_flag: false,
		  user: { //用户信息
			userName: null,
			userId: null
		  }
    }
  },
  created() {
    this.getUserInfo()
  },
  computed: mapState(["flag","menu"]),
  methods: {
    //显示、隐藏退出按钮
    showSetting() {
      this.login_flag = !this.login_flag
    },
    //左侧栏放大缩小
    ...mapMutations(["toggle"]),
    getUserInfo() { //获取用户信息
      // let userName = this.$cookies.get("cname")
      // let userId = this.$cookies.get("cid")
      this.user.userName = "202016"
      this.user.userId = 123456
    },
    index() {

    },
    exit() {
      let role = this.$cookies.get("role")
      this.$router.push({path:"/"}) //跳转到登录页面
      this.$cookies.remove("cname") //清除cookie
      if(role == 0) {
        this.menu.pop()
      }
    }
  },
  store
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to{
  opacity: 0;
}
#topbar {
  position: relative;
  z-index: 10;
  background-color: #124280;
  height: 80px;
  line-height: 80px;
  color: #fff;
  box-shadow: 5px 0px 10px rgba(0, 0, 0, 0.5);
}
#topbar .topbar-left {
  height: 80px;
  display: flex;
  justify-content: center;
  background: rgba(0, 0, 0, 0.05);
  overflow: hidden;
}
.topbar-left .el-icon-office-building {
  font-size: 40px;
  padding-top: 20px;
  margin-right: 10px;
}
.topbar-left .el-icon-s-promotion {
  font-size: 40px;
  padding-top: 20px;
  margin-right: 10px;
}

.topbar-left .title {
  font-size: 20px;
  cursor: pointer;
}
.topbar-right {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.topbar-right .user-img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}
.topbar-right .el-icon-caret-left {
  font-size: 30px;
  margin-left: 20px;
}
.topbar-right .el-icon-caret-right {
  font-size: 30px;
  margin-left: 20px;
}
.topbar-right .el-icon-s-unfold {
  font-size: 30px;
      margin-left: 20px;
      margin-top: 25px;
}
.topbar-right .el-icon-s-fold {
  font-size: 30px;
      margin-left: 20px;
      margin-top: 25px;
}
.topbar-right .user {
  position: relative;
  margin-right: 40px;
  display: flex;
}
.topbar-right .user .user-img {
  margin-top: 15px;
  margin-left: 10px;
  cursor: pointer;
}
.user .out {
  font-size: 14px;
  position: absolute;
  top: 80px;
  right: 0px;
  background-color: #fff;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  padding: 12px;
}
.user .out ul {
  list-style: none;
}
.user .out ul > li {
  height: 26px;
  line-height: 26px;
}
.out a {
  text-decoration: none;
  color: #000;
}
.out .exit {
  margin-top: 4px;
  padding-top: 4px;
  border-top: 1px solid #ccc;
}
</style>
