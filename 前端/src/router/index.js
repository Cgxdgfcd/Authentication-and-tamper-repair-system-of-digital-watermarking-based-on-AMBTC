import Vue from 'vue'
import Router from 'vue-router'
Vue.use(Router)

export default new Router({
  mode:'history',//去掉url后面的#
  routes: [
    {
      path: '/', //主菜单界面
      component: () => import('@/components/page/mainControl'),
      children: [
        {
          path: '/', //首页
          component: () => import('@/components/page/hello')
        },
		{
		  path: '/RestorePicture', //图片修复
		  component: () => import('@/components/page/RestorePicture')
		},
		{
		  path: '/AreaDetection', //区域检测
		  component: () => import('@/components/page/AreaDetection')
		},
		{
		  path: '/EmbedWatermark', //嵌入水印
		  component: () => import('@/components/page/EmbedWatermark')
		}
      ]
    }
  ]
})
