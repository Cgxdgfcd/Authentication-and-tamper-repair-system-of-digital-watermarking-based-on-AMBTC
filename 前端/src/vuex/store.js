import VUE from 'vue'
import VUEX from 'vuex'

VUE.use(VUEX)

const state = {
  isPractice: false,
  flag: true, //菜单栏左右滑动标志
  userInfo: null,
  menu: [
	{
	  index: '1',
	  title: '图片管理',
	  no: "嵌入水印",
	  icon: 'el-icon-s-data',
	  content:[
				{item1:'嵌入水印',path:'/EmbedWatermark',icon: 'el-icon-circle-plus-outline'},
				{item2:'区域检测',path:'/AreaDetection',icon: 'el-icon-zoom-in'},
				{item3:'恢复图片',path:'/RestorePicture',icon: 'el-icon-key'},
		],
	},
  ],
}
const mutations = {
  practice(state,status) {
    state.isPractice = status
  },
  toggle(state) {
    state.flag = !state.flag
  },
  changeUserInfo(state,info) {
    state.userInfo = info
  }
}
const getters = {

}
const actions = {
  getUserInfo(context,info) {
    context.commit('changeUserInfo',info)
  },
  getPractice(context,status) {
    context.commit('practice',status)
  }
}
export default new VUEX.Store({
  state,
  mutations,
  getters,
  actions
})
