<!--左边下拉导航栏-->
<template>
  <div id="left">
  <el-menu
      active-text-color="darkturquoise"
      text-color="#ffffff"
      :default-active="this.$route.path"
      class="el-menu-vertical-demo"
      :collapse="flag"
      :unique-opened="true"
      background-color="#124280"
      menu-trigger="click" router>
	  <el-menu-item class="el-menu-item" @click="handleTitle(0)" :index="'/'" >
	  		  <div :class="[elmenuitemischoose[0] ? 'selected-left-width' : 'left-width']">
	  		    <i class="iconfont" :class="'el-icon-s-home'"></i>
	  		    <span slot="title" class="title">首页</span>
	  		  </div>
	  </el-menu-item>
	  <el-menu-item class="el-menu-item" @click="handleTitle(1)" :index="'/EmbedWatermark'" >
		  <div :class="[elmenuitemischoose[1] ? 'selected-left-width' : 'left-width']">
		    <i class="iconfont" :class="'el-icon-circle-plus-outline'"></i>
		    <span slot="title" class="title">嵌入水印</span>
		  </div>
	  </el-menu-item>
	  <el-menu-item class="el-menu-item" @click="handleTitle(2)" :index="'/AreaDetection'" >
		  <div :class="[elmenuitemischoose[2] ? 'selected-left-width' : 'left-width']">
		    <i class="iconfont" :class="'el-icon-zoom-in'"></i>
		    <span slot="title" class="title">图像认证</span>
		  </div>
	  </el-menu-item>
	  <el-menu-item class="el-menu-item" @click="handleTitle(3)" :index="'/RestorePicture'" >
		  <div :class="[elmenuitemischoose[3] ? 'selected-left-width' : 'left-width']">
		    <i class="iconfont" :class="'el-icon-key'"></i>
		    <span slot="title" class="title">篡改恢复</span>
		  </div>
	  </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
import store from '@/vuex/store'
import {mapState} from 'vuex'
export default {
  name: "mainLeft",
  data() {
    return {
      elmenuitemischoose:[false,false,false,false],
      currentelmenuitem:null,
    }
  },
  computed: mapState(["flag","menu"]),
  created() {

  },
  methods: {
    //点击标题传递参数给navigator组件
    handleTitle(index) {
      if(this.currentelmenuitem!=null){
        this.elmenuitemischoose[this.currentelmenuitem]=false;
      }
      this.elmenuitemischoose[index]=true;
      this.currentelmenuitem=index;
      //设置全局参数，用于控制弹窗
      this.$cookies.set("addpictureflag", 0);
      console.log(this.$cookies.get("addpictureflag"))
    }
  },
  store
}
</script>

<style scoped>
.el-menu-vertical-demo .el-submenu__title {
  overflow: hidden;

}
.left-width .iconfont {
  font-size: 22px;
  color: #fff;
}
.left-width .title {
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  margin-left: 14px;
}
.left-width {
  width: 213px;
}
.selected-left-width{
  width: 213px;
}
.selected-left-width .iconfont {
  font-size: 22px;
  color: darkturquoise;
}
.selected-left-width .title {
  color: darkturquoise;
  font-size: 18px;
  font-weight: bold;
  margin-left: 14px;
}
.el-menu-vertical-demo:not(.el-menu--collapse) {
  min-height: 900px;
}
#left {
  height: 700px;
  background-color: #124280;
  z-index: 0;
}
.el-submenu {
  border-bottom: 1px solid #eeeeee0f !important;
}
.el-submenu__title:hover {
  background-color: #fff;
}
.el-submenu__title i {
    color: #fbfbfc !important;
}
.el-menu .el-menu--inline li{
  font-size: 16px;
  text-align: center;
}
</style>
